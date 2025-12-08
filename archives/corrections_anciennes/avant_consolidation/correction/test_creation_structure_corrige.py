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
from agents.models import Agent
from medecin.models import Medecin

def test_creation_structure_correcte():
    """Test de création avec la structure réelle du modèle"""
    print("🧪 TEST CRÉATION - STRUCTURE CORRECTE")
    print("====================================")
    
    try:
        # Récupérer les objets nécessaires
        membre = Membre.objects.first()
        agent = Agent.objects.first()
        
        print(f"👤 Membre: {membre.nom} {membre.prenom}")
        print(f"👨‍💼 Agent: {agent.matricule}")
        
        # Essayer de récupérer un médecin (peut être nécessaire)
        try:
            medecin = Medecin.objects.first()
            print(f"👨‍⚕️ Médecin: {medecin}")
        except:
            medecin = None
            print("⚠️  Aucun médecin trouvé")
        
        # Créer le bon avec les champs disponibles
        print(f"\n🔄 CRÉATION AVEC CHAMPS DISPONIBLES...")
        
        bon_data = {
            'patient': membre,  # Champ 'patient' au lieu de 'membre'
            'date_soin': datetime.now().date(),
            'symptomes': 'Test de symptômes',
            'diagnostic': 'Diagnostic test',
            'statut': 'EN_ATTENTE',
            'montant': 15000.0,
        }
        
        # Ajouter medecin seulement s'il existe
        if medecin:
            bon_data['medecin'] = medecin
        
        bon = BonDeSoin.objects.create(**bon_data)
        
        print(f"✅ BON DE SOIN CRÉÉ AVEC SUCCÈS!")
        print(f"   ID: {bon.id}")
        print(f"   Patient: {bon.patient.nom_complet}")
        print(f"   Date soin: {bon.date_soin}")
        print(f"   Statut: {bon.statut}")
        print(f"   Montant: {bon.montant}")
        
        # Vérification finale
        print(f"\n📊 VÉRIFICATION FINALE:")
        print(f"   Total bons de soin: {BonDeSoin.objects.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_creation_structure_correcte()
    
    if success:
        print("\n🎉 CRÉATION RÉUSSIE!")
    else:
        print("\n⚠️  CRÉATION ÉCHOUÉE")