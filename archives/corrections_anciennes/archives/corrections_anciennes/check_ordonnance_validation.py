# check_ordonnance_validation.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def check_ordonnance_validation():
    """Vérifier pourquoi l'ordonnance n'est pas valide"""
    print("📋 VÉRIFICATION DE LA VALIDATION DES ORDONNANCES...")
    
    from soins.models import Ordonnance
    
    try:
        ordonnance = Ordonnance.objects.first()
        if ordonnance:
            print(f"📄 Ordonnance #{ordonnance.id}:")
            print(f"   - Diagnostic: {getattr(ordonnance, 'diagnostic', 'Non défini')}")
            print(f"   - Médecin: {getattr(ordonnance, 'medecin', 'Non défini')}")
            print(f"   - Statut: {getattr(ordonnance, 'statut', 'Non défini')}")
            print(f"   - Est valide: {getattr(ordonnance, 'est_valide', 'Propriété non trouvée')}")
            
            # Vérifier la propriété est_valide
            if hasattr(ordonnance, 'est_valide'):
                print(f"   - est_valide (propriété): {ordonnance.est_valide}")
        else:
            print("❌ Aucune ordonnance trouvée dans la base de données")
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    check_ordonnance_validation()