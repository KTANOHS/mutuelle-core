import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from soins.models import BonDeSoin

def inspect_bondesoin():
    """Inspecter la structure réelle du modèle BonDeSoin"""
    print("🔍 INSPECTION MODÈLE BONDESOIN")
    print("===============================")
    
    # Vérifier s'il existe des instances
    count = BonDeSoin.objects.count()
    print(f"📊 Nombre de bons de soin: {count}")
    
    if count > 0:
        bon = BonDeSoin.objects.first()
        print(f"\n📄 EXEMPLE EXISTANT:")
        for field in bon._meta.fields:
            value = getattr(bon, field.name)
            print(f"  - {field.name}: {value}")
    
    print(f"\n📋 TOUS LES CHAMPS DISPONIBLES:")
    for field in BonDeSoin._meta.fields:
        print(f"  - {field.name} ({field.get_internal_type()})")
    
    print(f"\n🔗 RELATIONS DISPONIBLES:")
    for field in BonDeSoin._meta.related_objects:
        print(f"  - {field.name} -> {field.related_model}")

if __name__ == "__main__":
    inspect_bondesoin()