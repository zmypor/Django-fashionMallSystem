#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.core import management
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = "导入初始数据"
    
    def handle(self, *args, **options):
        fashionMalladposition = settings.BASE_DIR / 'fashionMall/conf/fashionMalladposition.json'
        fashionMalladspace = settings.BASE_DIR / 'fashionMall/conf/fashionMalladspace.json'
        fashionMallcategory = settings.BASE_DIR / 'fashionMall/conf/fashionMallcategory.json'
        management.call_command('loaddata', fashionMalladposition, verbosity=0)
        management.call_command('loaddata', fashionMalladspace, verbosity=0)
        management.call_command('loaddata', fashionMallcategory, verbosity=0)
        self.stdout.write(self.style.SUCCESS("数据导入成功！"))