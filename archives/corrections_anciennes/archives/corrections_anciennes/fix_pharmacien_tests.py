# fix_pharmacien_tests.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def fix_pharmacien_tests():
    """Corriger les tests pharmacien pour utiliser les bons champs"""
    print("🔧 CORRECTION DES TESTS PHARMACIEN...")
    
    test_file_path = 'pharmacien/tests.py'
    
    try:
        with open(test_file_path, 'r') as f:
            content = f.read()
        
        # Remplacer les champs incorrects
        content = content.replace(
            "medicament='Paracétamol'", 
            "medicament_delivre='Paracétamol'"
        )
        content = content.replace(
            "posologie='1 comprimé 3 fois par jour'", 
            "posologie_appliquee='1 comprimé 3 fois par jour'"
        )
        content = content.replace(
            "duree=7", 
            "duree_traitement=7"
        )
        content = content.replace(
            "medicament='Paracétamol'", 
            "nom_medicament='Paracétamol'"
        )
        content = content.replace(
            "quantite_en_stock=100", 
            "quantite_stock=100"
        )
        
        with open(test_file_path, 'w') as f:
            f.write(content)
        
        print("✅ Tests pharmacien corrigés avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")

if __name__ == "__main__":
    fix_pharmacien_tests()