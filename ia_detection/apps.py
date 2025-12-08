from django.apps import AppConfig

class IaDetectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ia_detection'
    verbose_name = 'Détection IA'
    
    def ready(self):
        # Importer les signaux
        try:
            import ia_detection.signals
        except ImportError:
            pass
