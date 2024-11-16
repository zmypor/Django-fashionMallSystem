#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.apps import AppConfig


class ArticleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fashionMall.apps.article'
    verbose_name = '内容'
