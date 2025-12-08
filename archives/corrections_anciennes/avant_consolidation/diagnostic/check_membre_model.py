# check_membre_model.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Membre

print("="*70)
print("🔍 VÉRIFICATION DU MODÈLE MEMBRE")
print("="*70)

print("\n📋 TOUS LES CHAMPS DE MEMBRE:")
for field in Membre._meta.fields:
    field_type = field.get_internal_type()
    is_relation = field.is_relation
    print(f"  • {field.name}: {field_type} (relation: {is_relation})")

print("\n🔍 CHAMPS DE RELATION (pour select_related):")
related_fields = []
for field in Membre._meta.fields:
    if field.is_relation:
        related_fields.append(field.name)
        print(f"  • {field.name} → {field.related_model.__name__}")

print(f"\n✅ Choix valides pour select_related: {related_fields}")

print("\n" + "="*70)