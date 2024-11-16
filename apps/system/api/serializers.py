#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from fashionMall.apps.system.models import fashionMallComment
from fashionMall.apps.shop.models import fashionMallOrderSKU


class fashionMallOrderCommentSerializer(serializers.Serializer):
    """ 序列化 """
    app_label = serializers.CharField(max_length=80)
    model = serializers.CharField(max_length=80)
    object_id = serializers.IntegerField(min_value=1)
    content = serializers.CharField(max_length=200)
    score = serializers.IntegerField(min_value=1, max_value=5, default=5)
    tag = serializers.CharField(max_length=200, required=False, default="")

    def create(self, validated_data):
        instance = fashionMallComment.objects.create(
            owner=self.context['request'].user,
            content_type=validated_data['content_type'],
            object_id=validated_data['object_id'],
            content=validated_data['content'],
            score=validated_data['score'],
            tag=validated_data['tag']
        )
        # 如果是对订单商品评价，则需要执行以下操作
        if isinstance(instance.content_object, fashionMallOrderSKU):
            ordersku = instance.content_object
            order = ordersku.order
            ordersku.is_commented = True
            ordersku.save()
            is_commented_list = order.fashionMallordersku_set.values_list('is_commented', flat=True)
            if is_commented_list and all(is_commented_list):
                order.status = 5
                order.save()
        return instance
    
    def validate(self, attrs):
        try:
            content_type = ContentType.objects.get(
                app_label=attrs['app_label'],
                model = attrs['model']
            )
            attrs['content_type'] = content_type
        except ContentType.DoesNotExist:
            raise serializers.ValidationError('模型不存在！')
        return attrs