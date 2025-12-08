import os
import django
import sys
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from soins.models import BonDeSoin
from membres.models import Membre

def creation_directe():
    """Création directe d'un bon de soin sans formulaire"""
    print("🛠️ CRÉATION DIRECTE BON DE SOIN")
    print("===============================")
    
    try:
        membre = Membre.objects.first()
        print(f"👤 Utilisation du membre: {membre.nom} {membre.prenom}")
        
        # Création la plus simple possible
        bon = BonDeSoin(
            patient=membre,
            date_soin=datetime.now().date(),
            symptomes="Création directe - symptômes test",
            diagnostic="Création directe - diagnostic test", 
            statut="EN_ATTENTE",
            montant=10000.0
        )
        
        bon.save()
        
        print(f"✅ BON CRÉÉ DIRECTEMENT!")
        print(f"   ID: {bon.id}")
        print(f"   Patient: {bon.patient.nom_complet}")
        print(f"   Date: {bon.date_soin}")
        print(f"   Statut: {bon.statut}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création directe: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = creation_directe()
    
    if success:
        print("\n🎉 CRÉATION DIRECTE RÉUSSIE!")
    else:
        print("\n⚠️  CRÉATION DIRECTE ÉCHOUÉE")