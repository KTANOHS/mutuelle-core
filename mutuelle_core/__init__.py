# votre_app/__init__.py
from django.apps import AppConfig
import os

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'votre_app'
    
    def ready(self):
        if os.environ.get('RUN_MAIN'):
            # Code qui nécessite la DB ici
            from . import signals  # si vous avez des signaux