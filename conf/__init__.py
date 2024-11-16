#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from django.conf import settings
from . import default


class Settings:
    
    def __init__(self, conf=None) -> None:
        self._conf = conf or default.DEFAULTS_CONF
        
    def __getattribute__(self, __name: str) -> str:
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            return getattr(settings, __name.upper(), self.get_attr(__name)) 
            
    def get_attr(self, name):
        try:
            return self._conf[name.upper()]
        except KeyError:
            raise ValueError("该配置项未设置...")
    
fashionMall_settings = Settings()