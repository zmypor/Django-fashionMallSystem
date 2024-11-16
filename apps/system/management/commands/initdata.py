#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand

from fashionMall.apps.system.models import fashionMallADSpace, fashionMallADPosition
from fashionMall.conf import fashionMall_settings

class Command(BaseCommand):
    help = "初始化数据"
    
    def handle(self, *args, **options):
        instance, iscreated = fashionMallADPosition.objects.update_or_create(
            slug="systemConf",
            defaults={
                "name": "系统配置",
                "slug": "systemConf",
                "desc": "系统相关配置"
            }
        )
        fashionMallADSpace.objects.update_or_create(
            slug="alipay_APPID",
            space="text",
            defaults={
                "name": "支付宝APPID",
                "slug": "alipay_APPID",
                "space": "text",
                "text": fashionMall_settings.ALIPAY['APPID'],
                "position": instance
            }
        )
        fashionMallADSpace.objects.update_or_create(
            slug="alipay_PUBLIC_KEY",
            space="html",
            defaults={
                "name": "支付宝PUBLIC_KEY",
                "slug": "alipay_PUBLIC_KEY",
                "space": "html",
                "text": "",
                "html": fashionMall_settings.ALIPAY['PUBLIC_KEY'],
                "position": instance
            }
        )
        fashionMallADSpace.objects.update_or_create(
            slug="alipay_PRIVATE_KEY",
            space="html",
            defaults={
                "name": "支付宝PRIVATE_KEY",
                "slug": "alipay_PRIVATE_KEY",
                "space": "html",
                "text":"",
                "html": fashionMall_settings.ALIPAY['PRIVATE_KEY'],
                "position": instance
            }
        )

        for key, value in fashionMall_settings.EMAIL_BACKEND_CONF.items():
            fashionMallADSpace.objects.update_or_create(
                slug=key,
                space="text",
                defaults={
                    "name": key,
                    "slug": key,
                    "text": value,
                    "position": instance
                }
            )
        self.stdout.write(self.style.SUCCESS(f"初始化必要数据成功！"))