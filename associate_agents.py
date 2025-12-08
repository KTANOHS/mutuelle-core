# associate_agents.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Agent
from assureur.models import Assureur

def associate_agents_with_assureurs():
    """Associe les agents existants à des assureurs"""
    print("🔗 ASSOCIATION AGENTS-ASSUREURS")
    print("=" * 50)
    
    # Vérifier que le champ assureur existe
    if not hasattr(Agent, 'assureur'):
        print("❌ Le champ 'assureur' n'existe pas encore")
        print("💡 Exécutez d'abord les migrations:")
        print("   python manage.py makemigrations agents")
        print("   python manage.py migrate")
        return
    
    # Obtenir les assureurs
    assureurs = Assureur.objects.all()
    if not assureurs.exists():
        print("❌ Aucun assureur trouvé")
        return
    
    print(f"✅ {assureurs.count()} assureur(s) trouvé(s)")
    
    # Associer les agents
    agents = Agent.objects.all()
    assureur_par_defaut = assureurs.first()
    compteur = 0
    
    for agent in agents:
        if agent.assureur is None:
            agent.assureur = assureur_par_defaut
            agent.save()
            compteur += 1
            print(f"   ✅ {agent.nom_complet} -> {assureur_par_defaut}")
    
    print(f"\n🎯 {compteur} agent(s) associé(s)")

if __name__ == "__main__":
    associate_agents_with_assureurs()