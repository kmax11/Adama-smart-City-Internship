from django.apps import AppConfig


class MpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mp'
    def ready(self):
        import mp.signals
