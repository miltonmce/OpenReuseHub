from django.apps import AppConfig


class ClientsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.clients'

    def ready(self):
        # Importa los modelos para que Django los detecte
        from .infrastructure import models