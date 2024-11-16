from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fashionMall.apps.user'

    def ready(self) -> None:
        from . import signals
