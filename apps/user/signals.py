#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import fashionMallUser


@receiver(post_save, sender=get_user_model())
def save_user_handler(sender, instance, created, **kwargs):
    # 同步创建一个用户的拓展字段
    if created:
        try:
            instance.fashionMalluser
        except fashionMallUser.DoesNotExist:
            user = fashionMallUser(
                owner=instance, 
                name=instance.username
            )
            user.save()

    