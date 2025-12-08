# apps.py
from django.apps import AppConfig

class AssureurConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assureur'
    
    def ready(self):
        # Évitez les requêtes à la base de données ici
        # Si vous avez besoin d'initialisation, faites-la dans une vue ou un management command
        try:
            import assureur.signals  # Si vous avez des signaux
        except ImportError:
            pass