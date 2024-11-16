from django.core import management
from django.core.management.base import BaseCommand, CommandError

from django.conf import settings


class Command(BaseCommand):
    help = "导出初始数据"
    
    def handle(self, *args, **options):
        fashionMalladposition = settings.BASE_DIR / 'fashionMall/conf/fashionMalladposition.json'
        fashionMalladspace = settings.BASE_DIR / 'fashionMall/conf/fashionMalladspace.json'
        fashionMallcategory = settings.BASE_DIR / 'fashionMall/conf/fashionMallcategory.json'
        management.call_command('dumpdata', 'system.fashionMalladposition', output=fashionMalladposition, indent=2, format='json')
        management.call_command('dumpdata', 'system.fashionMalladspace', output=fashionMalladspace, indent=2, format='json')
        management.call_command('dumpdata', 'shop.fashionMallcategory', output=fashionMallcategory, indent=2, format='json')
        self.stdout.write(self.style.SUCCESS(f"数据导出成功，导出数据路径在{settings.BASE_DIR / 'fashionMall/conf'}文件夹下"))