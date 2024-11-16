#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.urls import path

from . import views

app_name = "userapi"

urlpatterns = [
    path(
        'update-user-avatar/', 
         views.fashionMallUserUpdateAvatarAPIView.as_view(), 
         name='update-user-avatar'
    ),
    path(
        'update-user-about/', 
         views.fashionMallUserUpdateAboutAPIView.as_view(), 
         name='update-user-about'
    ),
    path(
        'send-email/', 
         views.SendEmailAPIView.as_view(), 
         name='send-email'
    ),
    path(
        'update-user-email/', 
         views.UserUpdateEmailAPIView.as_view(), 
         name='update-user-email'
    ),
    path(
        'push-balance/', 
         views.fashionMallUserBanlancePushAPIView.as_view(), 
         name='push-balance'
    )
]

