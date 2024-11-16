#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.db.models import F
from django.db.utils import IntegrityError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.utils import timezone

from rest_framework import serializers

from fashionMall.common.validators import validate_phone
from fashionMall.apps.shop.models import (
    fashionMallCart, fashionMallOrder, fashionMallOrderSKU,
    fashionMallAddress
)
from fashionMall.apps.user.models import fashionMallUserBalanceLog
from fashionMall.pay.alipay.client import client
from fashionMall.pay.alipay.trade_page_pay import trade_page_pay


class fashionMallCartSerializer(serializers.ModelSerializer):
    """ 购物车序列化 """
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = fashionMallCart
        fields = "__all__"
    
    def create(self, validated_data):
        try:
            instance = super().create(validated_data)
        except IntegrityError:
            carts = fashionMallCart.objects.filter(
                owner=self.context['request'].user, 
                sku=validated_data.get('sku')
            )
            if carts.exists():
                carts.update(num=F("num")+validated_data["num"])
                instance = carts.first()
        return instance


class fashionMallCartNumSerializer(serializers.Serializer):
    """ 购物车商品数量修改接口 """
    cartid = serializers.IntegerField(min_value=1)
    num = serializers.IntegerField(min_value=1, required=False, default=1)

    def validate_cartid(self, cartid):
        try:
            self.get_instance()
        except fashionMallCart.DoesNotExist:
            raise serializers.ValidationError("该购物车商品不存在，请检查！")
        return cartid
    
    def validate_num(self, num):
        instance = self.get_instance()
        if instance.sku.stock < self.initial_data['num']:
            raise serializers.ValidationError("数量不能大于库存！")
        return num

    def get_instance(self):
        initial_data = self.initial_data
        return fashionMallCart.objects.get(
            id=initial_data['cartid'], 
            owner=self.context['request'].user
        )
    

class fashionMallOrderSKUSerializer(serializers.ModelSerializer):
    """ 订单商品 """
    class Meta:
        model = fashionMallOrderSKU
        exclude = ('order',)

class fashionMallCreateOrderSerializer(serializers.ModelSerializer):
    """ 订单 """
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    fashionMallordersku_set = fashionMallOrderSKUSerializer(many=True)

    class Meta:
        model = fashionMallOrder
        fields = "__all__"

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs['total_price'] = self.get_total_price(attrs)
        return attrs

    def create(self, validated_data):
        fashionMallordersku_set = validated_data.pop('fashionMallordersku_set')
        instance = super().create(validated_data)
        for ordersku in fashionMallordersku_set:
            ordersku['order'] = instance
            fashionMallOrderSKU.objects.create(**ordersku)
        return instance
    
    def get_total_price(self, attrs):
        fashionMallordersku_set = attrs['fashionMallordersku_set']
        shipping_price = fashionMallordersku_set[0]['sku'].spu.shipping_price
        total_price = sum([(ordersku['count'] * ordersku['sku'].price) 
             for ordersku in fashionMallordersku_set]) + shipping_price
        return total_price
    
    @property
    def data(self):
        data = super().data
        data['cashurl'] = reverse("shop:order-cash", args=[data['id']])
        return data
    

class fashionMallOrderCashSerializer(serializers.Serializer):
    """ 订单结算 """
    orderid = serializers.IntegerField(min_value=1)
    paymethod = serializers.IntegerField(
        min_value=1, 
        max_value=3, 
        default=1, 
        error_messages={
            'min_value': _('不支持该支付方式.'),
            'max_value': _('不支持该支付方式.')
        }
    )
    name = serializers.CharField(min_length=1, max_length=50)
    phone = serializers.CharField(validators=[validate_phone], min_length=11, max_length=11)
    email = serializers.EmailField(required=False, min_length=3, max_length=60)
    address = serializers.CharField(min_length=10, max_length=150)
    mark = serializers.CharField(max_length=150, required=False, allow_blank=True)

    def validate_orderid(self, orderid):
        try:
            self.get_instance(orderid)
        except fashionMallOrder.DoesNotExist:
            raise serializers.ValidationError("订单不存在或已支付，请检查！")
        return orderid

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.paymethod = validated_data['paymethod']
        instance.phone = validated_data['phone']
        instance.address = validated_data['address']
        instance.mark = validated_data['mark']
        instance.status = 1 
        instance.save()
        return instance
    
    def get_instance(self, orderid):
        return fashionMallOrder.objects.get(
            id=orderid, owner=self.context['request'].user, status=1
        )
    
    @property
    def data(self):
        data = super().data
        instance = self.get_instance(data['orderid'])
        data['payurl'] = self.get_payurl(instance)
        return data
    
    def get_payurl(self, instance):
        request = self.context['request']
        if instance.paymethod == 1:
            return_url = f"{request.scheme}://{request.get_host()}{reverse('shop:alipay')}"
            notify_url = f"{request.scheme}://{request.get_host()}{reverse('shop:alipay')}"
            response = trade_page_pay(
                out_trade_no=instance.order_sn, total_amount=instance.total_price.to_eng_string(),
                subject=instance.order_sn, body=f"alipay{instance.order_sn}", 
                return_url=return_url, notify_url=notify_url
            )
            payurl = response
            return payurl
        elif instance.paymethod == 2:
            pass
        elif instance.paymethod == 3:
            fashionMalluser = request.user.fashionMalluser
            balance = fashionMalluser.balance
            # 判断余额是否足够
            if balance < instance.total_price:
                raise serializers.ValidationError('余额不足')
            # 减掉用户余额
            fashionMalluser.balance -= instance.total_price
            fashionMalluser.save()
            # 修改订单状态
            instance.status = 2
            instance.paymethod = 3
            instance.paytime = timezone.now()
            instance.save()
            # 创建余额变动记录
            fashionMallUserBalanceLog.objects.create(
                owner=request.user, 
                amount=instance.total_price, 
                change_status=2,
                change_way=3
            )
            messages.success(request, '支付成功，请耐心等待发货!')
            return reverse('shop:orders-detail', args=[instance.id])


class fashionMallAddressSerializer(serializers.ModelSerializer):
    """ 地址序列化 """
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = fashionMallAddress
        fields = "__all__"


class ConfirmReceiptSerializer(serializers.Serializer):
    """ 确认收货 """
    orderid = serializers.IntegerField(min_value=1)

    def validate_orderid(self, orderid):
        order = self.get_order(orderid)
        if not order.exists():
            raise serializers.ValidationError("该订单不存在！")
        return orderid
    
    def get_order(self, orderid):
        order = fashionMallOrder.objects.filter(
            id=orderid, status=3, owner=self.context['request'].user
        )
        return order