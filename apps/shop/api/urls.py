#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = "shopapi"

router = DefaultRouter()

router.register('address', views.fashionMallAddressViewSet, basename='address')

urlpatterns = [
    path(
        'create-cart/', 
        views.fashionMallCartCreateAPIView.as_view(), 
        name='create-cart'
    ),
    path(
        'update-cart-num/', 
        views.fashionMallCartUpdateNumAPIView.as_view(), 
        name='update-cart-num'
    ),
    path(
        'del-cart/', 
        views.fashionMallCartUpdateNumAPIView.as_view(), 
        name='del-cart'
    ),
    path(
        'create-order/', 
        views.fashionMallOrderCreateAPIView.as_view(), 
        name='create-order'
    ),
    path(
        'cash-order/', 
        views.fashionMallOrderCashAPIView.as_view(), 
        name='cash-order'
    ),
    path(
        'confirm-receipt/', 
        views.ConfirmReceiptAPIView.as_view(), 
        name='confirm-receipt'
    ),
    *router.urls
]