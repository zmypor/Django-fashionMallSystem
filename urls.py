#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from django.urls import path, include
from tinymce.views import TinyMCEImageUpload

urlpatterns = [
    path('', include('fashionMall.apps.shop.urls')),
    path('article/', include('fashionMall.apps.article.urls')),
    path('system/', include('fashionMall.apps.system.urls')),
    path('user/', include('fashionMall.apps.user.urls')),
    path('captcha/', include('captcha.urls')),
    path("tinymce/upload-image/", TinyMCEImageUpload.as_view(), name="tinymce-upload-image"),

    # 接口url
    path('api-auth/', include('rest_framework.urls'))
]