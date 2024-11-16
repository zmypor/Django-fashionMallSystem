#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.urls import path

from . import views

app_name = "systemapi"

urlpatterns = [
    path(
        'order-comment/', 
         views.fashionMallOrderCommentAPIView.as_view(), 
         name='order-comment'
    ),
]

