from django.apps import AppConfig


class AiopsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aiops'

    def ready(self):
        from nacos_service import Command
        # Command().handle()