#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from fashionMall.conf import fashionMall_settings


def validate_phone(value):
    # 中国区手机号验证
    reg = re.compile(fashionMall_settings.REGEX_PHONE)
    if not reg.search(value):
        raise ValidationError(
            _("%(value)s 格式有误"),
            params={"value": value},
        )
 

def validate_count(value):
    # 验证列表的长度不超过10个
    if isinstance(value, list):
        if len(value) > 10:
            raise ValidationError(
                _("%(value)s is max length 10"),
                params={"value": value},
            )