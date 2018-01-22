from django.apps import AppConfig


class RestCoreConfig(AppConfig):
    name = 'rest_core'

    def ready(self):
        from .signals import create_user_profile, save_user_profile