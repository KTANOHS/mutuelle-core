# find_problematic_model.py
import os
import django
from django.apps import apps

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def find_model_with_fields():
    print("🔍 RECHERCHE DU MODÈLE AVEC CES CHAMPS...")
    print("=" * 50)
    
    target_fields = ['bon_de_soin', 'duree', 'instructions', 'medicament', 'posologie']
    models_found = []
    
    for model in apps.get_models():
        field_names = [f.name for f in model._meta.get_fields()]
        
        # Vérifie si tous les champs cibles sont présents
        if all(field in field_names for field in target_fields):
            models_found.append(model)
            print(f"📦 Modèle trouvé: {model._meta.app_label}.{model.__name__}")
            print(f"   Champs: {field_names}")
            
            # Vérifie si date_creation est manquant
            if 'date_creation' not in field_names:
                print("   ❌ CHAMP MANQUANT: date_creation")
            else:
                print("   ✅ date_creation est présent")
            print()
    
    if not models_found:
        print("❌ Aucun modèle trouvé avec tous ces champs")
        print("🔍 Recherche de modèles avec certains de ces champs...")
        
        for model in apps.get_models():
            field_names = [f.name for f in model._meta.get_fields()]
            matching_fields = [f for f in target_fields if f in field_names]
            if matching_fields:
                print(f"📦 {model._meta.app_label}.{model.__name__}")
                print(f"   Champs correspondants: {matching_fields}")
                print(f"   Tous les champs: {field_names}")
                print()

if __name__ == "__main__":
    find_model_with_fields()