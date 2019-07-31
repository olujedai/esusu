from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'api'

    def ready(self):
        from .signals import user_joined_society
        from .handlers import user_joined_society_handler
        user_joined_society.connect(user_joined_society_handler)
