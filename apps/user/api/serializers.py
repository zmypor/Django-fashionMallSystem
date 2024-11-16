#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import serializers

from fashionMall.conf import fashionMall_settings
from fashionMall.common.utils import code_random, push_main
from fashionMall.apps.user.models import fashionMallUser

class fashionMallUserUpdateAvatarSerializer(serializers.ModelSerializer):
    """ 修改用户头像 """
    class Meta:
        model = fashionMallUser
        fields = ('avatar', )

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            fashionMalluser = user.fashionMalluser
        except fashionMallUser.DoesNotExist:
            fashionMalluser = fashionMallUser.objects.create(owner=user, name=user.username)
        self.update(fashionMalluser, validated_data)
        return fashionMalluser
    
    def update(self, instance, validated_data):
        instance.avatar = validated_data['avatar']
        instance.save()
        return instance
    

class fashionMallUserUpdateAboutSerializer(fashionMallUserUpdateAvatarSerializer):
    """ 修改个人简介 """
    class Meta:
        model = fashionMallUser
        fields = ('about', )

    def update(self, instance, validated_data):
        instance.about = validated_data['about']
        instance.save()
        return instance
    

class SendEmailSerializer(serializers.Serializer):
    """ 发送邮件 """
    email = serializers.EmailField(max_length=80)
    
    def push_mail(self, validated_data):
        code = code_random()
        cache_code = cache.get_or_set(validated_data['email'], code, 300)
        push_main(cache_code, validated_data['email'])
        return True


class VerifyEmailSerializer(serializers.Serializer):
    """ 验证邮箱 """
    email = serializers.EmailField(max_length=80)
    code = serializers.CharField(
        max_length=fashionMall_settings.CODE_LENGTH,
        min_length=fashionMall_settings.CODE_LENGTH,
        write_only=True
    )

    def validate_email(self, email):
        user = get_user_model().objects.filter(email=email)
        if email == self.context['request'].user.email:
            raise serializers.ValidationError("邮箱地址似乎未改变哦？")
        if user.exists():
            raise serializers.ValidationError("该邮箱已被占用，请更换邮箱！")
        return email
    
    def validate(self, attrs):
        cache_code = cache.get(attrs['email'])
        if cache_code != attrs['code']:
            raise serializers.ValidationError("验证码有误！")
        return super().validate(attrs)
    

class fashionMallUserBalancePushSerializer(serializers.Serializer):
    """ 余额充值序列化 """
    add_balance = serializers.DecimalField(max_digits=10, decimal_places=2)