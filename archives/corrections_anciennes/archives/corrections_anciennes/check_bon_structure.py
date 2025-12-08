# check_bon_structure.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps

def check_bon_structure():
    print("🔍 STRUCTURE DU MODÈLE BON_DE_SOIN")
    print("=" * 50)
    
    # Chercher le modèle BonDeSoin ou Bon
    for model in apps.get_models():
        if 'bon' in model.__name__.lower():
            print(f"📦 Modèle: {model._meta.app_label}.{model.__name__}")
            fields = [f.name for f in model._meta.get_fields()]
            print(f"   Champs: {fields}")
            print()

if __name__ == "__main__":
    check_bon_structure()