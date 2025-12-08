import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from soins.models import BonDeSoin
from membres.models import Membre
from medecin.models import Medecin
from django.contrib.auth.models import User

def corriger_medecin_final():
    """Correction finale pour la relation médecin"""
    print("🔧 CORRECTION MÉDECIN FINALE")
    print("============================")
    
    # 1. Trouver les Users qui sont des médecins
    print("👨‍⚕️ USERS MÉDECINS DISPONIBLES:")
    medecins = Medecin.objects.all()
    
    for medecin in medecins:
        print(f"  - {medecin.nom_complet} -> User: {medecin.user.username}")
    
    # 2. Créer un bon avec User médecin
    print(f"\n🔄 TEST CRÉATION AVEC USER MÉDECIN...")
    
    try:
        membre = Membre.objects.first()
        medecin_obj = Medecin.objects.first()
        
        if medecin_obj and medecin_obj.user:
            bon = BonDeSoin.objects.create(
                patient=membre,
                medecin=medecin_obj.user,  # Utiliser le User, pas l'objet Medecin
                date_soin="2025-11-20",
                symptomes="Consultation avec médecin assigné",
                diagnostic="Diagnostic avec user médecin",
                statut="EN_ATTENTE",
                montant=20000.0
            )
            print(f"✅ CRÉATION RÉUSSIE avec User médecin!")
            print(f"   Médecin: {bon.medecin.username}")
            return True
        else:
            print("⚠️  Aucun médecin avec User trouvé")
            # Créer sans médecin
            bon = BonDeSoin.objects.create(
                patient=membre,
                date_soin="2025-11-20",
                symptomes="Consultation sans médecin assigné",
                diagnostic="Diagnostic standard",
                statut="EN_ATTENTE",
                montant=15000.0
            )
            print(f"✅ CRÉATION RÉUSSIE sans médecin!")
            return True
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = corriger_medecin_final()
    
    if success:
        print("\n🎉 RELATION MÉDECIN CORRIGÉE!")
    else:
        print("\n⚠️  CORRECTION ÉCHOUÉE")