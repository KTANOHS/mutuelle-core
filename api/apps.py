# api/apps.py
from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    def ready(self):
        """Code à exécuter lorsque l'application est prête"""
        try:
            # Import pour s'assurer que Django est bien configuré
            from django.conf import settings
            from django.core.checks import register, Tags
            
            @register(Tags.compatibility)
            def check_settings(app_configs, **kwargs):
                """Vérifier la configuration de l'API"""
                errors = []
                
                # Vérifier que DRF est installé
                if 'rest_framework' not in settings.INSTALLED_APPS:
                    errors.append(
                        {
                            'id': 'api.E001',
                            'msg': 'rest_framework doit être dans INSTALLED_APPS',
                            'hint': "Ajoutez 'rest_framework' à INSTALLED_APPS",
                            'obj': self,
                        }
                    )
                
                return errors
            
            print("✅ API configurée avec succès")
            
        except Exception as e:
            print(f"⚠️  Erreur lors de la configuration de l'API: {e}")