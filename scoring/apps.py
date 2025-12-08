from django.apps import AppConfig

class ScoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scoring'
    verbose_name = 'Scoring Membres'
    
    def ready(self):
        # Importer les signaux
        try:
            import scoring.signals
        except ImportError:
            pass
