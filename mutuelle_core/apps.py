from django.apps import AppConfig

class MutuelleCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mutuelle_core'
    verbose_name = 'Core Mutuelle'
    
    def ready(self):
        # Import des modèles pour s'assurer qu'ils sont chargés
        try:
            from . import models  # noqa
        except ImportError:
            pass
