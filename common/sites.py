#!/usr/bin/env python
# -*- encoding: utf-8 -*-



from django.contrib import admin
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from fashionMall.conf import fashionMall_settings

from .forms import AdminLoginForm


class AdminSite(admin.AdminSite):
    """ 自定义AdminSite """
    site_header = gettext_lazy(fashionMall_settings.SITE_HEADER)
    site_title = gettext_lazy(fashionMall_settings.SITE_TITLE)
    index_title = gettext_lazy(fashionMall_settings.INDEX_TITLE)

    login_form = AdminLoginForm
    login_template = "system/login.html"
    index_template = "system/index.html"
    
    
    def get_app_list(self, request, app_label=None):
        if fashionMall_settings.CUSTOM_MENU:
            from fashionMall.common.menus import MenusMixins
            menu = MenusMixins()
            return menu.get_menus(request)
        return super().get_app_list(request)
