#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.urls import path, include
from fashionMall.pay.alipay.views import AliPayCallBackView, fashionMallUserBalanceCallBackView
from . import views


app_name = "shop"

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('goods/', views.fashionMallSPUListView.as_view(), name='goods'),
    path('search/', views.fashionMallSPUSearchView.as_view(), name='search'),
    path('cate/<int:pk>/', views.fashionMallCategoryDetailView.as_view(), name='cate-detail'),
    path('spu/<int:pk>/', views.fashionMallSPUDetailView.as_view(), name='spu-detail'),
    path('carts/', views.fashionMallCartListView.as_view(), name='carts'),
    path('order-cash/<int:pk>/', views.fashionMallOrderCashDetailView.as_view(), name='order-cash'),
    path('member/', views.fashionMallUserMemberView.as_view(), name='member'),
    path('address/', views.fashionMallAddressView.as_view({'get': 'list'}), name='address'),
    path('orders/', views.fashionMallOrderListView.as_view(), name='orders-list'),
    path('orders-detail/<int:pk>/', views.fashionMallOrderDetailView.as_view(), name='orders-detail'),
    path('balance-log/', views.fashionMallUserBalanceLogTemplateView.as_view(), name='balance-log'),
    path('alipay/', AliPayCallBackView.as_view(), name='alipay'),
    path('balance/', fashionMallUserBalanceCallBackView.as_view(), name='balance'),
    path('orders/comment/<int:pk>/', views.fashionMallOrderCommentView.as_view(), name='comment'),

    path('api/', include('fashionMall.apps.shop.api.urls')),
]