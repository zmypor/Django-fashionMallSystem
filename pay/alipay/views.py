#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from datetime import datetime
from decimal import Decimal

from django.utils import timezone
from django.views.generic import View
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

from fashionMall.common.mixins import LoginRequiredMixin
from fashionMall.apps.shop.models import fashionMallOrder
from fashionMall.apps.user.models import fashionMallUserBalanceLog
from . import mixins


class AliPayCallBackView(View, mixins.AlipayCallBackVerifySignMixin):
    """ PC支付宝支付成功回调 """
    
    def get(self, request, *args, **kwargs):
        # 验签通过处理逻辑
        data = request.GET.dict()
        order_queryset = fashionMallOrder.objects.filter(order_sn=data['out_trade_no'])
        instance = order_queryset.first()
        if self.has_verify_sign(data):
            paytime = datetime.strptime(data['timestamp'], "%Y-%m-%d %H:%M:%S")
            order_queryset.update(pay_time=timezone.make_aware(paytime), 
                                  total_price=data['total_amount'], 
                                  paymethod=1, status=2)
            return render(request, 'shop/payok.html', {'order': instance})
    
    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        if self.has_verify_sign(data):
            order_queryset = fashionMallOrder.objects.filter(order_sn=data['out_trade_no'])
            instance = order_queryset.first()
            if not instance.pay_time:
                paytime = datetime.strptime(data['timestamp'], "%Y-%m-%d %H:%M:%S")
                order_queryset.update(pay_time=timezone.make_aware(paytime), 
                                      total_price=data['total_amount'], paymethod=1, status=2)
            return HttpResponse("success")
        

class fashionMallUserBalanceCallBackView(LoginRequiredMixin, AliPayCallBackView):
    """ 余额充值回调 """
    def get(self, request, *args, **kwargs):
        # 验签通过处理逻辑
        data = request.GET.dict()
        fashionMalluser = request.user.fashionMalluser
        if self.has_verify_sign(data):
            fashionMalluser.balance += Decimal(data['total_amount'])
            fashionMalluser.save()
            fashionMallUserBalanceLog.objects.create(
                owner=request.user, 
                amount=Decimal(data['total_amount']),
                change_status=1,
                change_way=1
            )
            messages.success(request, '充值成功！')
        return redirect('shop:member')
    
    def post(self, request, *args, **kwargs):
        # 验签通过处理逻辑
        data = request.POST.dict()
        fashionMalluser = request.user.fashionMalluser
        if self.has_verify_sign(data):
            fashionMalluser.balance += Decimal(data['total_amount'])
            fashionMalluser.save()
            fashionMallUserBalanceLog.objects.create(
                owner=request.user, 
                amount=Decimal(data['total_amount']),
                change_status=1,
                change_way=1
            )
        return HttpResponse('success')