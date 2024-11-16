#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
# Create your models here.
from fashionMall.common.models import BaseModelMixin, ContentTypeAbstract


class fashionMallADPosition(BaseModelMixin):
    """Model definition for fashionMallADPosition."""
    name = models.CharField(_("名称"), max_length=50)
    slug = models.SlugField(_("slug"), unique=True)
    desc = models.CharField(_("说明"), max_length=150, blank=True, default="")
    # TODO: Define fields here

    class Meta:
        """Meta definition for fashionMallADPosition."""
        ordering = ['-add_date']
        verbose_name = _("广告位")
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of fashionMallADPosition."""
        return self.desc or self.name
    
    @classmethod
    def get_position_spaces(cls, slug):
        spaces = []
        try:
            position = cls.objects.get(slug=slug)
            spaces = position.fashionMalladspace_set.exclude(status=False)
        except cls.DoesNotExist:
            pass
        return spaces


class fashionMallADSpace(BaseModelMixin):
    """Model definition for fashionMallADSpace."""

    class ADSpaceChoices(models.TextChoices):
        TEXT = "text", _("文字广告")
        IMG = "img", _("图片广告")
        HTML = "html", _("自定义广告")

    name = models.CharField(_("名称"), max_length=50)
    slug = models.SlugField(_("slug"), max_length=50, unique=True)
    space = models.CharField(
        choices=ADSpaceChoices.choices, 
        max_length=10, 
        default="img",
        verbose_name=_("类型")
    )
    position = models.ForeignKey(
        fashionMallADPosition, 
        on_delete=models.CASCADE, 
        verbose_name=_("广告位"),
        blank=True,
        null=True
    )
    remark = models.CharField(_("备注"), max_length=150, blank=True, default="")
    img = models.ImageField(_("图片广告"), upload_to="common/ad", blank=True, null=True)
    text = models.CharField(_("文字广告"), max_length=150, blank=True, default="")
    html = models.TextField(_("自定义广告"), blank=True, default="")
    target = models.URLField(_("跳转地址"), max_length=200, blank=True, default="")
    sort = models.PositiveSmallIntegerField(_("排序"), default=1)
    status = models.BooleanField(_("状态"), default=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for fashionMallADSpace."""
        ordering = ['sort']
        verbose_name = _("广告内容")
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of fashionMallADSpace."""
        return self.name
    
    @classmethod
    def get_space(cls, slug):
        obj = None
        try:
            obj = cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            pass
        return obj
    

class fashionMallComment(ContentTypeAbstract):
    """Model definition for fashionMallComment."""

    class ScoreChoices(models.IntegerChoices):
        BAD = 1, _("差评")
        MIDDL = 3, _("中评")
        GOOD = 5, _("好评")

    owner = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        verbose_name=_("用户")
    )
    content = models.CharField(_("评论"), max_length=200)
    score = models.PositiveSmallIntegerField(
        choices=ScoreChoices.choices, 
        default=5,
        verbose_name=_("评价")
    )
    reply = models.CharField(_("回复内容"), max_length=200, blank=True, default="")
    # TODO: Define fields here

    class Meta:
        """Meta definition for fashionMallComment."""
        ordering = ['-add_date']
        verbose_name = _("评论")
        verbose_name_plural = verbose_name
        permissions = [
            ("reply_to_comments", "Reply to comments"),
        ]

    def __str__(self):
        """Unicode representation of fashionMallComment."""
        return self.content
    

class fashionMallSiteMenus(BaseModelMixin):
    """ 后台管理菜单自定义 """
    name = models.CharField(_("名称"), max_length=50, unique=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    icon = models.CharField(_("图标"), max_length=50, blank=True, default="")
    permission = models.OneToOneField(
        Permission, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        verbose_name=_("权限")
    )

    # TODO: Define fields here

    class Meta:
        ordering = ['-add_date']
        verbose_name = 'SiteMenus'
        verbose_name_plural = 'SiteMenus'

    def __str__(self):
        return self.name