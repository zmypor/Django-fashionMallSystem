#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from fashionMall.common.permission import IsOwnerAuthenticated
from fashionMall.apps.shop.models import fashionMallCart, fashionMallAddress
from .serializers import (
    fashionMallCartSerializer, fashionMallCartNumSerializer,
    fashionMallCreateOrderSerializer, fashionMallAddressSerializer,
    fashionMallOrderCashSerializer, ConfirmReceiptSerializer
)


class fashionMallCartCreateAPIView(CreateAPIView):
    """ 商品添加购物车 """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = fashionMallCartSerializer

    def get_queryset(self):
        return fashionMallCart.objects.filter(owner=self.request.user)
    

class fashionMallCartUpdateNumAPIView(APIView):
    """ 修改购物车商品数量 """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        serializer.is_valid(raise_exception=True)
        fashionMallCart.objects.filter(
            id=serializer.validated_data['cartid'],
            owner=request.user
        ).update(num=serializer.validated_data['num'])
        return Response({"code": "ok"})

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        serializer.is_valid(raise_exception=True)
        fashionMallCart.objects.filter(
            id=serializer.validated_data['cartid'],
            owner=request.user,
        ).delete()
        return Response({"code": "ok"})

    def get_serializer(self):
        serializer = fashionMallCartNumSerializer(
            data=self.request.data, 
            context={"request": self.request}
        )
        return serializer
    

class fashionMallOrderCreateAPIView(CreateAPIView):
    """ 创建订单 """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = fashionMallCreateOrderSerializer


class fashionMallOrderCashAPIView(APIView):
    """ 立即支付 """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = fashionMallOrderCashSerializer(
            data=request.data, 
            context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        instance=serializer.get_instance(serializer.validated_data['orderid'])
        serializer.update(instance, serializer.validated_data)
        return Response(serializer.data)


class fashionMallAddressViewSet(viewsets.ModelViewSet):
    """ 地址增删改查 """
    serializer_class = fashionMallAddressSerializer
    permission_classes = [IsAuthenticated, IsOwnerAuthenticated]

    def get_queryset(self):
        return fashionMallAddress.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        self.save_only_default(serializer)
        return super().perform_create(serializer)
    
    def perform_update(self, serializer):
        self.save_only_default(serializer)
        return super().perform_update(serializer)
    
    def save_only_default(self, serializer):
        # 处理默认收货地址只能有一个
        if serializer.validated_data['is_default']:
            self.get_queryset().filter(is_default=True).update(is_default=False)


class ConfirmReceiptAPIView(APIView):
    """ 确认收货接口 """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ConfirmReceiptSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.get_order(serializer.validated_data['orderid'])
        order.update(status=4)
        messages.success(request, '确认收货成功！')
        return Response({'code':'ok'})