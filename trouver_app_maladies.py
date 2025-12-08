import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps

print("🔍 RECHERCHE DES APPLICATIONS ET MODÈLES")
print("==========================================")

# Lister toutes les applications installées
for app_config in apps.get_app_configs():
    print(f"\n📦 Application: {app_config.name}")
    print(f"   📁 Chemin: {app_config.path}")
    
    # Lister tous les modèles de cette application
    for model in app_config.get_models():
        print(f"   🎯 Modèle: {model.__name__}")
        
        # Afficher les champs si c'est un modèle de maladie
        if 'maladie' in model.__name__.lower() or 'chronique' in model.__name__.lower():
            print(f"      🩺 CHAMPS DISPONIBLES:")
            for field in model._meta.get_fields():
                print(f"        - {field.name} ({field.__class__.__name__})")