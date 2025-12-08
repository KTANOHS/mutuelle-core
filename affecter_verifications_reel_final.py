# affecter_verifications_reel_final.py
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from agents.models import Agent, VerificationCotisation

def creer_agents_si_manquants():
    """Crée des agents s'il n'y en a pas"""
    if Agent.objects.count() == 0:
        print("🆕 CRÉATION D'AGENTS PAR DÉFAUT...")
        
        # Créer quelques agents
        agents_data = [
            {"nom": "Agent_Validation_1", "email": "agent1@system.com", "statut": "actif"},
            {"nom": "Agent_Validation_2", "email": "agent2@system.com", "statut": "actif"},
            {"nom": "Agent_Validation_3", "email": "agent3@system.com", "statut": "actif"},
        ]
        
        for data in agents_data:
            agent = Agent.objects.create(
                nom=data["nom"],
                email=data["email"],
                statut=data["statut"],
                capacite_validation=10  # Nombre max de vérifications
            )
            print(f"✅ Agent créé: {agent.nom}")
        
        return True
    return False

def affecter_verifications_reelles():
    print("🔄 AFFECTATION RÉELLE DES VÉRIFICATIONS...")
    
    # 1. Vérifier/Créer des agents
    agents_crees = creer_agents_si_manquants()
    
    # 2. Récupérer les agents disponibles
    agents = list(Agent.objects.filter(statut="actif"))
    print(f"👨‍💼 Agents disponibles: {len(agents)}")
    
    if not agents:
        print("❌ Aucun agent disponible même après création")
        return
    
    # 3. Trouver les membres sans vérification
    membres_sans_verification = []
    for membre in Membre.objects.all():
        if not VerificationCotisation.objects.filter(membre=membre).exists():
            membres_sans_verification.append(membre)
    
    print(f"📊 {len(membres_sans_verification)} membres sans vérification")
    
    if not membres_sans_verification:
        print("✅ Tous les membres ont déjà une vérification!")
        return
    
    # 4. Affecter les vérifications
    verifications_creees = 0
    for membre in membres_sans_verification:
        agent = random.choice(agents)
        
        try:
            # Créer la vérification
            verification = VerificationCotisation.objects.create(
                membre=membre,
                agent=agent,
                statut='en_attente',
                date_assignation=django.utils.timezone.now()
            )
            verifications_creees += 1
            print(f"✅ Vérification {verifications_creees}: Membre {membre.id} → Agent {agent.nom}")
            
        except Exception as e:
            print(f"❌ Erreur pour membre {membre.id}: {e}")
    
    print(f"\n🎯 RÉSULTAT: {verifications_creees} vérifications créées!")
    print(f"👥 Membres restants sans vérification: {len(membres_sans_verification) - verifications_creees}")

if __name__ == "__main__":
    affecter_verifications_reelles()