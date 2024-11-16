#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.urls import path
from . import views

app_name = "fashionMallarticle"

urlpatterns = [
    path('', views.fashionMallArticleContentListView.as_view(), name='article-list'),
    path('category/<int:pk>/', views.fashionMallArticleCategoryDetailView.as_view(), name='category-detail'),
    path('content/<int:pk>/', views.fashionMallArticleContentDetailView.as_view(), name='content-detail'),
    path('archive/<int:year>/<int:month>/', views.fashionMallArticleContentMonthArchiveView.as_view(), name='archive-list'),
    path('tags/<int:pk>/', views.fashionMallArticleTagsToArticleListView.as_view(), name='tags-list'),
]