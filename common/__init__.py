#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.contrib.admin import apps

class AdminConfig(apps.AdminConfig):
    default_site = "fashionMall.common.sites.AdminSite"