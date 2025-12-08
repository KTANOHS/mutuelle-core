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

def corriger_relation_medecin():
    """Corriger la relation médecin qui attend un User"""
    print("🔧 CORRECTION RELATION MÉDECIN")
    print("==============================")
    
    # 1. Vérifier les médecins existants
    medecins = Medecin.objects.all()
    print(f"👨‍⚕️ Médecins trouvés: {medecins.count()}")
    
    for medecin in medecins:
        print(f"  - {medecin.nom_complet} -> User: {medecin.user}")
    
    # 2. Vérifier les Users avec des médecins
    users_medecins = User.objects.filter(medecin__isnull=False)
    print(f"👤 Users avec médecin: {users_medecins.count()}")
    
    for user in users_medecins:
        print(f"  - {user.username} -> {user.medecin}")
    
    # 3. Tester la création avec User médecin
    if users_medecins.exists():
        user_medecin = users_medecins.first()
        membre = Membre.objects.first()
        
        print(f"\n🔄 TEST CRÉATION AVEC USER MÉDECIN...")
        
        try:
            bon = BonDeSoin.objects.create(
                patient=membre,
                medecin=user_medecin,  # User au lieu de Medecin
                date_soin="2025-11-20",
                symptomes="Test avec user médecin",
                diagnostic="Diagnostic test user",
                statut="EN_ATTENTE",
                montant=18000.0
            )
            print(f"✅ CRÉATION RÉUSSIE avec User médecin!")
            print(f"   Médecin: {bon.medecin.username}")
            return True
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    return False

if __name__ == "__main__":
    success = corriger_relation_medecin()
    
    if success:
        print("\n🎉 RELATION MÉDECIN CORRIGÉE!")
    else:
        print("\n⚠️  CORRECTION ÉCHOUÉE - Vérifier les données")