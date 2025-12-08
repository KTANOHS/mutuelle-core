# fix_ordonnance_validation.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def fix_ordonnance_validation():
    """Forcer la validation des ordonnances pour les tests"""
    print("📋 CORRECTION VALIDATION ORDONNANCES...")
    
    try:
        # Vérifier le modèle Ordonnance
        from soins.models import Ordonnance
        
        # Vérifier si la propriété est_valide existe
        ordonnance = Ordonnance.objects.first()
        if ordonnance and hasattr(ordonnance, 'est_valide'):
            print(f"📄 Ordonnance #{ordonnance.id}: est_valide = {ordonnance.est_valide}")
            
            # Si False, forcer temporairement pour les tests
            if not ordonnance.est_valide:
                print("⚠️  Ordonnance non valide - vérifier la logique de validation")
        else:
            print("ℹ️  Aucune ordonnance trouvée ou propriété manquante")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    fix_ordonnance_validation()