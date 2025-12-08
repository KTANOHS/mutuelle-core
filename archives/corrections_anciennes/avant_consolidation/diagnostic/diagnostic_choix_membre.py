import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre

print("🔍 DIAGNOSTIC DES CHOIX DU MODÈLE MEMBRE")
print("==========================================")

# Analyser tous les champs avec choix
for field in Membre._meta.get_fields():
    if hasattr(field, 'choices') and field.choices:
        print(f"\n📋 Champ: {field.name}")
        print(f"   Type: {field.__class__.__name__}")
        print(f"   Choix disponibles:")
        for choice_value, choice_label in field.choices:
            print(f"     - '{choice_value}' : {choice_label}")
    
    # Afficher aussi les champs CharField pour voir les valeurs par défaut
    elif field.__class__.__name__ == 'CharField':
        print(f"\n📋 Champ: {field.name}")
        print(f"   Type: CharField")
        if field.default != django.db.models.NOT_PROVIDED:
            print(f"   Valeur par défaut: {field.default}")