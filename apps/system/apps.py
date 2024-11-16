#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.apps import AppConfig


class SystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fashionMall.apps.system'
    verbose_name = '系统'
