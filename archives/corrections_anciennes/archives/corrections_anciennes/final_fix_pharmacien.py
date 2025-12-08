# final_fix_pharmacien.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def final_fix_pharmacien():
    """Correction finale complète des tests pharmacien"""
    print("🔧 CORRECTION FINALE DES TESTS PHARMACIEN...")
    
    test_file_path = 'pharmacien/tests.py'
    
    try:
        with open(test_file_path, 'r') as f:
            content = f.read()
        
        # CORRECTION COMPLÈTE - Tous les champs problématiques
        corrections = {
            # OrdonnancePharmacien
            "medicament='Paracétamol'": "medicament_delivre='Paracétamol'",
            "posologie='1 comprimé 3 fois par jour'": "posologie_appliquee='1 comprimé 3 fois par jour'", 
            "duree=7": "duree_traitement=7",
            
            # StockPharmacie
            "medicament='Paracétamol'": "nom_medicament='Paracétamol'",
            "quantite_en_stock=100": "quantite_stock=100",
            
            # Champs manquants supplémentaires
            "pharmacien=self.pharmacien": "pharmacien_validateur=self.pharmacien",
        }
        
        for old, new in corrections.items():
            content = content.replace(old, new)
        
        with open(test_file_path, 'w') as f:
            f.write(content)
        
        print("✅ Correction pharmacien appliquée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    final_fix_pharmacien()