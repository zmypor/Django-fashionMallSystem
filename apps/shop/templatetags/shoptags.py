from django.template import Library
from django.db.models import Sum, Avg

from fashionMall.apps.system.models import fashionMallComment
from fashionMall.apps.shop.models import fashionMallCart

register = Library()


def spudata(spu):
    skus = spu.fashionMallsku_set.all()
    return {
        "img": skus.first().img.url,
        "spu": spu,
    }


@register.inclusion_tag("shop/spubox.html")
def spubox(spu):
    return spudata(spu)


@register.inclusion_tag("shop/specs.html")
def spuspecs(spu):
    skus = spu.fashionMallsku_set.all()
    return {
        "skus": list(skus.values())
    }


@register.inclusion_tag("shop/spubanners.html")
def spubanners(spu):
    return {
        "images": list(spu.fashionMallspuatlas_set.filter(status=True).values("id", "img"))
    }


@register.simple_tag
def cartscount(request):
    # 购物车商品数量
    return (
        fashionMallCart.get_cart_count(request.user) 
        if request.user.is_authenticated else 0
    )


def ordersku_func(ordersku_queryset):
    from decimal import Decimal
    count__sum = ordersku_queryset.aggregate(Sum("count"))
    freight = ordersku_queryset.first().sku.spu.shipping_price
    total = sum([Decimal(ordersku.sku_json['price']) * ordersku.count for ordersku in ordersku_queryset])
    total_price = total + freight
    return {
        **count__sum,
        'freight': freight,
        'total': total_price,
        'total_price': ordersku_queryset.first().order.total_price
    }


@register.simple_tag
def ordersku(ordersku_queryset):
    return ordersku_func(ordersku_queryset)


@register.inclusion_tag('shop/member/action.html')
def order_action(order):
    ordersku_queryset = order.fashionMallordersku_set.all()
    context = ordersku_func(ordersku_queryset)
    context['order'] = order
    return context


@register.simple_tag
def comments_score(spu):
    comments = fashionMallComment.objects.filter(tag=str(spu.id))
    gte_3 = comments.filter(score__gte=3).count()
    rate = gte_3 / comments.count() if comments.count() else 0.98
    score_avg = comments.aggregate(Avg('score')).get('score__avg') or 4.8
    return {
        'rate': rate * 100,
        'score_avg': score_avg
    }