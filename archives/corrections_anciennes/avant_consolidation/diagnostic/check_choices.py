# check_choices.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Cotisation

print("=== CHOIX DU MODÈLE COTISATION ===")
print(f"\n1. Type de cotisation:")
field = Cotisation._meta.get_field('type_cotisation')
if hasattr(field, 'choices') and field.choices:
    for value, label in field.choices:
        print(f"   - '{value}': {label}")
else:
    print("   Pas de choix définis")

print(f"\n2. Statut:")
field = Cotisation._meta.get_field('statut')
if hasattr(field, 'choices') and field.choices:
    for value, label in field.choices:
        print(f"   - '{value}': {label}")
else:
    print("   Pas de choix définis")

print(f"\n3. Champs obligatoires (non null):")
for field in Cotisation._meta.fields:
    if not field.null and not field.blank and field.name != 'id':
        print(f"   - {field.name}")