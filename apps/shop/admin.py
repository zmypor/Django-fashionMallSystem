#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

# Register your models here.
from fashionMall.common.options import ModelAdmin, TabularInline, StackedInline
from .models import (
    fashionMallCategory, fashionMallBrand, fashionMallSPU,
    fashionMallSKU, fashionMallSpec, fashionMallSpecValue,
    fashionMallSPUAtlas, fashionMallOrder, fashionMallOrderSKU
)
from .forms import fashionMallSKUForm


class fashionMallSKUInline(StackedInline):
    '''Tabular Inline View for fashionMallSKU'''
    model = fashionMallSKU
    min_num = 1
    max_num = 20
    extra = 0
    form = fashionMallSKUForm


class fashionMallSpecValueInline(TabularInline):
    '''Tabular Inline View for fashionMallSpecValue'''

    model = fashionMallSpecValue
    min_num = 1
    max_num = 20
    extra = 1

class fashionMallSPUAtlasInline(TabularInline):
    '''Stacked Inline View for fashionMallSPUAtlas'''

    model = fashionMallSPUAtlas
    min_num = 1
    max_num = 10
    extra = 1
    

class fashionMallCategoryInline(TabularInline):
    '''Stacked Inline View for fashionMallCategory'''

    model = fashionMallCategory
    min_num = 1
    max_num = 100
    extra = 1
    exclude = ('figure', 'desc')


@admin.register(fashionMallCategory)
class fashionMallCategoryAdmin(ModelAdmin):
    '''Admin View for fashionMallCategory'''

    list_display = ('id', 'name', 'parent', 'sort', 'status', 'add_date')
    list_display_links = ('id', 'name')
    inlines = [fashionMallCategoryInline]
    exclude = ('parent', )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).exclude(parent__isnull=False)


@admin.register(fashionMallBrand)
class fashionMallBrandAdmin(ModelAdmin):
    '''Admin View for fashionMallBrand'''

    list_display = ('id', 'name', 'add_date')


@admin.register(fashionMallSPU)
class fashionMallSPUAdmin(ModelAdmin):
    '''Admin View for fashionMallSPU'''

    list_display = ('id', 'title', 'brand', 'add_date')
    # filter_horizontal = ("category", )
    list_display_links = ('id', 'title')
    inlines = [fashionMallSKUInline, fashionMallSPUAtlasInline]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = fashionMallCategory.objects.exclude(parent__isnull=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    def save_formset(self, request: Any, form: Any, formset: Any, change: Any) -> None:
        if issubclass(formset.form, fashionMallSKUForm):
            specs = [ str(data['specs'].keys()) for data in formset.cleaned_data if data['specs']]   
            if len(set(specs)) < len(specs):
                self.message_user(request, "规格重复,不能存在两个同样规格的sku!", level="ERROR")      
        super().save_formset(request, form, formset, change)

    
@admin.register(fashionMallSpec)
class fashionMallSpecAdmin(ModelAdmin):
    '''Admin View for fashionMallSpec'''

    list_display = ('id', 'name', 'add_date')
    inlines = [fashionMallSpecValueInline,]


@admin.register(fashionMallOrder)
class fashionMallOrderAdmin(ModelAdmin):
    '''Admin View for fashionMallOrder'''

    list_display = (
        'id', 'owner', 'order_sn', 'orderskus', 'status', 
        'paymethod', 'total_price', 'pay_time', 'orderaction'
    )
    list_filter = ('paymethod', 'status')
    list_display_links = ('id', 'owner', 'order_sn')
    readonly_fields = ('owner', 'order_sn', 'paymethod', 'status', 'orderskus', )

    @admin.display(description="订单商品")
    def orderskus(self, obj):
        orderskus = obj.fashionMallordersku_set.all()
        return render_to_string(
            "shop/admin/orderskus.html", 
            context={'orderskus': orderskus}
        )
    
    @admin.display(description="操作")
    def orderaction(self, obj):
        return render_to_string("shop/admin/orderaction.html", context={'obj':obj})

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        my_urls = [path("sendGoods/<int:pk>/", self.admin_site.admin_view(self.send_goods), name='send_goods')]
        return my_urls + urls

    @method_decorator(staff_member_required)
    @method_decorator(permission_required("shop.send_out_goods", raise_exception=True))
    def send_goods(self, request, pk):
        # 订单发货操作
        obj = get_object_or_404(fashionMallOrder, pk=pk)
        context = dict(
            self.admin_site.each_context(request),
            title=f"订单{obj.order_sn}发货操作",
            order=obj
        )
        if request.method == 'POST':
            obj.status = 3
            obj.save()
            return redirect('admin:shop_fashionMallorder_changelist')
        return TemplateResponse(request, "shop/admin/send_goods.html", context)
    
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        if obj and obj.status == 1:
            return True
        return False
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False


# @admin.register(fashionMallOrderSKU)
# class fashionMallOrderSKUAdmin(ModelAdmin):
#     '''Admin View for fashionMallOrderSKU'''

#     list_display = ('id', 'order', 'sku', 'count')
   
   