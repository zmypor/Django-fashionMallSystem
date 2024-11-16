from django.template import Library
from fashionMall.apps.shop.models import fashionMallCategory
from fashionMall.common.utils import get_cache_space

register = Library()

@register.inclusion_tag("system/pagination.html")
def pagination(page_obj):
    return {
        "count": page_obj.paginator.count,
        "current": page_obj.number,
        "per_page":page_obj.paginator.per_page
    }

@register.simple_tag
def shopcates():
    return fashionMallCategory.objects.filter(parent__isnull=True, is_nav=True)

@register.filter
def multiply(value, arg):
    # 相乘计算
    from decimal import Decimal
    return Decimal(value) * int(arg)

@register.simple_tag
def space(slug):
    return get_cache_space(slug)

