import os
import django
import sys
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from members.models import Membre
from bons_soins.models import BonDeSoin
from agents.models import Agent
from django.contrib.auth.models import User

def test_creation_bon_manuel():
    """Test manuel de création d'un bon de soin"""
    print("🧪 TEST MANUEL CRÉATION BON DE SOIN")
    print("===================================")
    
    # 1. Récupérer un membre
    try:
        membre = Membre.objects.first()
        print(f"👤 Membre sélectionné: {membre.nom} {membre.prenom}")
    except:
        print("❌ Aucun membre trouvé")
        return False
    
    # 2. Récupérer un agent
    try:
        agent = Agent.objects.first()
        print(f"👨‍💼 Agent sélectionné: {agent.nom_complet}")
    except:
        print("❌ Aucun agent trouvé")
        return False
    
    # 3. Créer un bon de soin directement
    try:
        bon = BonDeSoin.objects.create(
            membre=membre,
            agent_createur=agent,
            type_soin="Consultation générale",
            montant_total=15000.0,
            montant_remboursable=12000.0,
            date_soin=datetime.now().date(),
            statut="EN_ATTENTE",
            description="Consultation de routine"
        )
        print(f"✅ BON DE SOIN CRÉÉ AVEC SUCCÈS!")
        print(f"   Numéro: {bon.numero_bon}")
        print(f"   Membre: {bon.membre.nom_complet}")
        print(f"   Montant: {bon.montant_total} FCFA")
        print(f"   Statut: {bon.statut}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return False

if __name__ == "__main__":
    success = test_creation_bon_manuel()
    
    # Vérification finale
    print("\n📊 VÉRIFICATION FINALE:")
    print(f"   Bons de soin en base: {BonDeSoin.objects.count()}")
    print(f"   Membres en base: {Membre.objects.count()}")
    print(f"   Agents en base: {Agent.objects.count()}")
    
    if success:
        print("🎉 TEST RÉUSSI!")
    else:
        print("⚠️  TEST ÉCHOUÉ - Vérifiez les problèmes ci-dessus")