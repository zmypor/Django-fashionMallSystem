#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.urls import path, include
from . import views

app_name = 'system'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('api/', include('fashionMall.apps.system.api.urls'))
]