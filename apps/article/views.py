#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from typing import Any, Dict
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.dates import MonthArchiveView
# Create your views here.
from .models import fashionMallArticleContent, fashionMallArticleCategory, fashionMallArticleTags


class fashionMallArticleContentListView(ListView):
    """列表页
    """
    queryset = fashionMallArticleContent.objects.exclude(status=0)
    template_name = "article/list.html"
    paginate_by = 20
    paginate_orphans = 2
    extra_context = {"title": "全部文章"}


class fashionMallArticleCategoryDetailView(SingleObjectMixin, fashionMallArticleContentListView):
    """分类列表页
    """
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=fashionMallArticleCategory.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

    def get_queryset(self):
        return self.object.fashionMallarticlecontent_set.filter(status=1)
    

class fashionMallArticleContentDetailView(DetailView):
    """文章详情页
    """
    model = fashionMallArticleContent
    template_name = "article/detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['article_next'] = self.get_object().next_article
        context['article_previous'] = self.get_object().previous_article
        context['title'] = self.get_object().title
        return context


class fashionMallArticleContentMonthArchiveView(MonthArchiveView, fashionMallArticleContentListView):
    """ 文章归档 """
    date_field = "add_date"
    allow_future = True
    month_format = "%m"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = context.get('month')
        return context
    

class fashionMallArticleTagsToArticleListView(SingleObjectMixin, fashionMallArticleContentListView):
    # 文章标签列表页
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(fashionMallArticleTags.objects.all())
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return self.object.fashionMallarticlecontent_set.all()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

