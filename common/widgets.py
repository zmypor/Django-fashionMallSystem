#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.forms import widgets
from captcha.fields import CaptchaTextInput as BaseCaptchaTextInput


class TextInput(widgets.TextInput):
    input_type = "text"
    template_name = "system/widgets/text.html"


class PasswordInput(widgets.PasswordInput):
    input_type = "password"
    template_name = "system/widgets/text.html"


class CaptchaTextInput(BaseCaptchaTextInput):
    template_name = "system/widgets/captcha.html"

