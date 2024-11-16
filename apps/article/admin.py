#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from typing import Any
from django.contrib import admin
from django.contrib import messages
from django.http.request import HttpRequest
from django.utils.translation import ngettext
# Register your models here.
from fashionMall.common.options import ModelAdmin, TabularInline
from .models import (
    fashionMallArticleCategory, fashionMallArticleContent, fashionMallArticleTags
)

class fashionMallArticleCategoryInline(TabularInline):
    '''Stacked Inline View for fashionMallArticleCategory'''

    model = fashionMallArticleCategory
    min_num = 1
    max_num = 100
    extra = 1
    exclude = ('desc', 'keywords')


@admin.register(fashionMallArticleCategory)
class fashionMallArticleCategoryAdmin(ModelAdmin):
    '''Admin View for fashionMallArticleCategory'''

    list_display = ('id', 'name', 'parent', 'sort', 'status', 'add_date')
    list_display_links = ('id', 'name')
    list_editable = ('sort', )
    search_fields = ('name',)
    exclude = ('parent',)
    inlines = [fashionMallArticleCategoryInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
       if db_field.name == 'parent':
           kwargs['queryset'] = fashionMallArticleCategory.objects.filter(parent__isnull=True)
       return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_change_permission(self, request, obj=None):
        if obj and obj.parent:
            return False
        return super().has_change_permission(request, obj)
    
    def get_exclude(self, request, obj=None):
        if obj and obj.parent:
            self.exclude = None
        return super().get_exclude(request, obj)


@admin.register(fashionMallArticleContent)
class fashionMallArticleContentAdmin(ModelAdmin):
    '''Admin View for fashionMallArticleContent'''

    list_display = ('id', 'title', 'category', 'status', 'add_date', 'pub_date')
    list_display_links = ('id', 'title')
    list_filter = ('category',)
    search_fields = ('title',)
    filter_horizontal = ('tags',)
    date_hierarchy = 'add_date'
    actions = ['make_draft']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
       if db_field.name == 'category':
           kwargs['queryset'] = fashionMallArticleCategory.objects.exclude(parent__isnull=True)
       return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    @admin.action(description="所选内容批量设为草稿", permissions=["change"])
    def make_draft(self, request, queryset):
        updated = queryset.update(status=0)
        self.message_user(
            request,
            ngettext(
                "%d story was successfully marked as draft.",
                "%d stories were successfully marked as draft.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    
@admin.register(fashionMallArticleTags)
class fashionMallArticleTagsAdmin(ModelAdmin):
    '''Admin View for fashionMallArticleTags'''

    list_display = ('id', 'name', 'add_date')
    list_display_links = ('id', 'name')