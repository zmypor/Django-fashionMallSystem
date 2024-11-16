#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.utils.functional import cached_property
from django.urls import reverse
from rest_framework.renderers import TemplateHTMLRenderer
# Create your views here.
from fashionMall.common.mixins import LoginRequiredMixin
from fashionMall.common.renderers import TemplateHTMLRenderer
from fashionMall.apps.shop.api.views import fashionMallAddressViewSet
from fashionMall.apps.user.models import fashionMallUserBalanceLog
from fashionMall.apps.system.models import (
    fashionMallADPosition, fashionMallComment, fashionMallADSpace
) 
from fashionMall.apps.shop.models import (
    fashionMallCategory, fashionMallSPU, fashionMallSKU, fashionMallCart,
    fashionMallOrder
)


    
class SPUAliasAnnotateMixin:
    
    def alias_annotate_queryset(self, queryset):
        return queryset.alias(
            price=models.Min('fashionMallsku__price'),
            sales=models.Sum('fashionMallsku__sales')
        ).annotate(
            price=models.F('price'),
            sales=models.F('sales')
        )


class HomeTemplateView(TemplateView, SPUAliasAnnotateMixin):
    """ 首页 """
    template_name = "shop/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'fashionMall开源商城系统'
        context['banners'] = self.banners
        context['floors'] = self.get_floors
        return context
    
    @cached_property
    def get_floors(self):
        cates = fashionMallCategory.objects.filter(is_nav=True, parent__isnull=True)
        for cate in cates:
            subcates = cate.fashionMallcategory_set.filter(is_nav=True)
            cate.spus = self.alias_annotate_queryset(
                fashionMallSPU.objects.filter(category__in=subcates).distinct()
            )[:10]
        return cates
    
    @cached_property
    def banners(self):
        instance, iscreated = fashionMallADPosition.objects.get_or_create(
            name="商城首页轮播图广告位",
            slug="shophomebanner",
            desc="商城首页轮播图广告位【多图】"
        )
        if iscreated:
            fashionMallADSpace.objects.create(
                name="轮播图1",
                slug="shopbanner",
                space="img",
                position=instance,
                img="common/ad/banner.jpg"
            )
        return fashionMallADPosition.get_position_spaces(slug="shophomebanner")
    

class fashionMallSPUListView(ListView, SPUAliasAnnotateMixin):
    """ 全部商品 """

    model = fashionMallSPU
    template_name = "shop/list.html"
    paginate_by = 20
    paginate_orphans = 4
    ordering = "add_date"

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset().filter(status=True)
        return self.alias_annotate_queryset(queryset)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['parent_cates'] = self.get_fashionMallcategory
        context['sub_cates'] = self.get_fashionMallcategory_set
        context['title'] = "全部商品"
        context['sort_params'] = self.get_sort_params
        return context
    
    @cached_property
    def get_fashionMallcategory(self):
        parent_cates = fashionMallCategory.objects.filter(
            status=True, parent__isnull=True
        )
        return parent_cates
    
    @cached_property
    def get_fashionMallcategory_set(self):
        queryset = fashionMallCategory.objects.none()
        if self.get_fashionMallcategory.exists():
            queryset = self.get_fashionMallcategory.first() \
                .fashionMallcategory_set.filter(status=True)
        return queryset
    
    def alias_annotate_queryset(self, queryset):
        # 对注解过的queryset进行排序
        return super().alias_annotate_queryset(queryset).order_by(self.get_sort_params)
    
    @cached_property
    def get_sort_params(self):
        # 排序字段
        return self.request.GET.get('ordering', self.ordering)
        
    def get_absolute_url(self):
        return reverse('shop:goods')


class fashionMallCategoryDetailView(SingleObjectMixin, fashionMallSPUListView):
    """ 商品分类详情列表 """

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            queryset=fashionMallCategory.objects.filter(status=True)
        )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_cates'] = self.get_fashionMallcategory_set
        context['title'] = self.object.name
        return context

    def get_queryset(self) -> QuerySet[Any]:
        queryset = self.object.fashionMallspu_set.filter(status=True)
        if self.object.parent is None:
            queryset = fashionMallSPU.objects.filter(
                status=True, 
                category__in=self.object.fashionMallcategory_set.filter(status=True)
            )
        return self.alias_annotate_queryset(queryset)
    
    @cached_property
    def get_fashionMallcategory_set(self):
        queryset = self.object.fashionMallcategory_set.filter(status=True)
        if self.object.parent:
            queryset = self.object.parent.fashionMallcategory_set.filter(status=True)
        return queryset
    
    def get_absolute_url(self):
        return reverse('shop:cate-detail', kwargs={'pk': self.pk})


class fashionMallSPUSearchView(fashionMallSPUListView):
    """ 搜索视图 """

    def get_queryset(self) -> QuerySet[Any]:
        words = self.request.GET.get('words', '')
        return super().get_queryset().filter(
            models.Q(title__icontains=words)|
            models.Q(subtitle__icontains=words)|
            models.Q(content__icontains=words)
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.GET.get('words')
        return context


class fashionMallSPUDetailView(DetailView):
    """ 商品详情页 """
    model = fashionMallSPU
    context_object_name = "spu"
    template_name = "shop/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_object().title
        context['spuhots'] = fashionMallSPU.get_hots()
        context['comments'] = self.get_page_comments()
        return context

    def get_absolute_url(self):
        return reverse('shop:spu-detail', kwargs={'pk': self.pk})
    
    def get_comments(self):
        # 商品评价
        comments = fashionMallComment.objects.filter(tag=str(self.get_object().id))
        return comments
    
    def get_page_comments(self):
        # 评价分页
        comments = self.get_comments()
        from django.core.paginator import Paginator
        paginator = Paginator(comments, 20)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj
    

class fashionMallCartListView(LoginRequiredMixin, ListView):
    """ 购物车列表 """
    model = fashionMallCart
    template_name = "shop/carts.html"
    context_object_name = "carts"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = '购物车'
        context['carts_values'] = self.get_queryset_values
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(owner=self.request.user)
    
    @cached_property
    def get_queryset_values(self):
        cart_queryset = self.get_queryset().values('id', 'sku', 'num', 'add_date')
        for cart in cart_queryset:
            sku = fashionMallSKU.objects.get(id=cart['sku'])
            cart['sku'] = {
                "id": sku.id,
                "title": sku.spu.title,
                "price": sku.price,
                "img": sku.img.url,
                "cost_price": sku.cost_price,
                "discount_price": sku.discount_price,
                "stock": sku.stock,
                "sales": sku.sales,
                "code": sku.code,
                "specs": { key: value for key, value in sku.specs.items() if not key.isdigit() }
            }
        return list(cart_queryset)
    

class fashionMallOrderCashDetailView(LoginRequiredMixin, DetailView):
    """ 订单收银台 """
    model = fashionMallOrder
    template_name = "shop/ordercash.html"
    context_object_name = "order"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(owner=self.request.user)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = "收银台"
        return context
    

class fashionMallUserMemberView(LoginRequiredMixin, TemplateView):
    """ 个人中心 """
    template_name = "shop/member/member.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = "个人中心"
        return context
    

class fashionMallAddressView(fashionMallAddressViewSet):
    """ 用户地址 """
    renderer_classes = [TemplateHTMLRenderer, ]
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.template_name = "shop/member/address.html"
        return response
    

class fashionMallOrderListView(LoginRequiredMixin, ListView):
    """ 我的订单 """
    model = fashionMallOrder
    template_name = "shop/member/orders.html"
    paginate_by = 5

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = '我的订单'
        return context

    def get_queryset(self) -> QuerySet[Any]:
        status = self.request.GET.get('status')
        queryset = super().get_queryset().filter(owner=self.request.user)
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class fashionMallOrderDetailView(LoginRequiredMixin, DetailView):
    """ 订单详情 """
    model = fashionMallOrder
    template_name = "shop/member/orders-detail.html"
    context_object_name = "order"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = "订单详情"
        return context


class fashionMallUserBalanceLogTemplateView(LoginRequiredMixin, TemplateView):
    """ 余额变动记录日志 """

    template_name = "shop/member/balance.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['add_sum_amount'] = fashionMallUserBalanceLog.add_sum_amount(self.request.user)
        context['minus_sum_amount'] = fashionMallUserBalanceLog.minus_sum_amount(self.request.user)
        context['balance_list'] = self.get_queryset()
        context['title'] = '我的余额'
        return context
    
    def get_queryset(self):
        return fashionMallUserBalanceLog.objects.filter(owner=self.request.user)
    

class fashionMallOrderCommentView(LoginRequiredMixin, SingleObjectMixin, ListView):
    """ 订单评价 """

    template_name = "shop/member/comment.html"
    paginate_by = 1000

    def get(self, request, *args, **kwargs):    
        self.object = self.get_object(
            queryset=fashionMallOrder.objects.filter(status=4, owner=request.user)
        )
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self) -> QuerySet[Any]:
        return self.object.fashionMallordersku_set.filter(is_commented=False)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = "订单评价"
        return context