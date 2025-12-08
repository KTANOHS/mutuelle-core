# correction_assureurs.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Agent
from assureur.models import Assureur

def corriger_agents_sans_assureur():
    """Associe les agents sans assureur au premier assureur disponible"""
    print("🔧 CORRECTION DES AGENTS SANS ASSUREUR")
    print("=" * 50)
    
    # Trouver un assureur par défaut
    assureur_par_defaut = Assureur.objects.first()
    
    if not assureur_par_defaut:
        print("❌ Aucun assureur trouvé dans la base de données")
        return
    
    print(f"✅ Assureur par défaut: {assureur_par_defaut}")
    
    # Trouver les agents sans assureur
    agents_sans_assureur = Agent.objects.filter(assureur__isnull=True)
    print(f"🔍 Agents sans assureur: {agents_sans_assureur.count()}")
    
    if agents_sans_assureur.count() == 0:
        print("✅ Tous les agents ont déjà un assureur associé")
        return
    
    # Associer chaque agent à l'assureur par défaut
    for agent in agents_sans_assureur:
        agent.assureur = assureur_par_defaut
        agent.save()
        agent_nom = agent.user.get_full_name() if agent.user else f"Agent {agent.id}"
        print(f"✅ {agent_nom} (ID: {agent.id}) associé à l'assureur")

def verifier_correction():
    """Vérifie que la correction a fonctionné"""
    print("\n🔍 VÉRIFICATION DE LA CORRECTION")
    print("=" * 50)
    
    agents_sans_assureur = Agent.objects.filter(assureur__isnull=True)
    print(f"Agents sans assureur après correction: {agents_sans_assureur.count()}")
    
    if agents_sans_assureur.count() == 0:
        print("🎯 CORRECTION RÉUSSIE: Tous les agents ont un assureur")
    else:
        print("⚠️  Il reste des agents sans assureur")

if __name__ == "__main__":
    corriger_agents_sans_assureur()
    verifier_correction()