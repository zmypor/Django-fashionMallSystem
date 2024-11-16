from django.conf import settings

settings.DEBUG = True

settings.INSTALLED_APPS += [
    'fashionMall.common.AdminConfig',
    'fashionMall.apps.user',
    'fashionMall.apps.article',
    'fashionMall.apps.system',
    'fashionMall.apps.shop',
    'rest_framework',
    'captcha',
    'tinymce',
]

STATIC_ROOT = settings.BASE_DIR / "static"

MEDIA_URL = 'media/'
MEDIA_ROOT = settings.BASE_DIR / 'media'

TINYMCE_CONFIG = {
    'menubar': True,
    'relative_urls': False,
    'toolbar_sticky': False,
    'plugins_exclude': 'upgrade'  # 禁用升级插件
}

SECURE_CROSS_ORIGIN_OPENER_POLICY = None