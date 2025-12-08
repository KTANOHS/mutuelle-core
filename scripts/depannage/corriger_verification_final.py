# corriger_verification_final.py
import os
import sys
import django
from pathlib import Path
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from agents.models import VerificationCotisation

print("🔧 CORRECTION URGENTE - CHAMP PROCHAINE_ECHEANCE")
print("=" * 50)

def corriger_urgence_prochaine_echeance():
    """Correction urgente du champ prochaine_echeance manquant"""
    
    # Compter les vérifications à corriger
    verifications_sans_echeance = VerificationCotisation.objects.filter(
        prochaine_echeance__isnull=True
    )
    
    print(f"🔍 {verifications_sans_echeance.count()} vérifications sans prochaine échéance")
    
    if verifications_sans_echeance.count() == 0:
        print("✅ Aucune correction nécessaire")
        return
    
    # Appliquer les corrections
    corrections = 0
    for verification in verifications_sans_echeance:
        try:
            # Calculer une échéance par défaut (30 jours après la vérification)
            if verification.date_verification:
                date_base = verification.date_verification.date()
            else:
                date_base = datetime.now().date()
            
            verification.prochaine_echeance = date_base + timedelta(days=30)
            verification.save()
            corrections += 1
            
            if corrections <= 5:  # Afficher les 5 premières
                print(f"✅ Vérification {verification.id}: échéance fixée au {verification.prochaine_echeance}")
                
        except Exception as e:
            print(f"❌ Erreur sur vérification {verification.id}: {e}")
    
    print(f"🎯 {corrections} vérifications corrigées avec succès")

if __name__ == "__main__":
    corriger_urgence_prochaine_echeance()