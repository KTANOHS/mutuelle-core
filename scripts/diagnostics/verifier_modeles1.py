# verifier_modeles.py
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps

print("🔍 LISTE DES MODÈLES DISPONIBLES DANS LE PROJET")
print("=" * 50)

for app_config in apps.get_app_configs():
    print(f"\n📦 APPLICATION: {app_config.verbose_name} ({app_config.name})")
    print("-" * 40)
    
    for model in app_config.get_models():
        print(f"   🎯 {model.__name__}")
        # Afficher les champs importants
        fields = [f.name for f in model._meta.fields[:5]]  # 5 premiers champs
        print(f"      Champs: {', '.join(fields)}...")

print(f"\n🎯 TOTAL: {len([m for app in apps.get_app_configs() for m in app.get_models()])} modèles trouvés")