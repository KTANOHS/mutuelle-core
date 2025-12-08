# associer_agents.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Agent
from assureur.models import Assureur

def associer_agents_automatiquement():
    print("🔗 ASSOCIATION AUTOMATIQUE AGENTS-ASSUREURS")
    print("=" * 60)
    
    # Vérifier que le champ assureur existe
    if not hasattr(Agent, 'assureur'):
        print("❌ Le champ 'assureur' n'existe pas encore dans le modèle Agent")
        print("💡 Exécutez d'abord les migrations:")
        print("   python manage.py makemigrations agents")
        print("   python manage.py migrate")
        return
    
    # Obtenir les assureurs disponibles
    assureurs = Assureur.objects.all()
    if assureurs.count() == 0:
        print("❌ Aucun assureur trouvé dans la base de données")
        return
    
    print(f"✅ {assureurs.count()} assureur(s) trouvé(s)")
    
    # Associer chaque agent au premier assureur disponible
    assureur_par_defaut = assureurs.first()
    print(f"🔧 Utilisation de l'assureur: {assureur_par_defaut}")
    
    agents = Agent.objects.all()
    compteur = 0
    
    for agent in agents:
        if agent.assureur is None:
            agent.assureur = assureur_par_defaut
            agent.save()
            compteur += 1
            print(f"   ✅ {agent.nom_complet} -> {assureur_par_defaut}")
    
    print(f"\n🎯 {compteur} agent(s) associé(s) à un assureur")
    
    # Vérification finale
    agents_sans_assureur = Agent.objects.filter(assureur__isnull=True).count()
    if agents_sans_assureur == 0:
        print("🎉 TOUS LES AGENTS ONT MAINTENANT UN ASSUREUR!")
    else:
        print(f"⚠️  Il reste {agents_sans_assureur} agent(s) sans assureur")

if __name__ == "__main__":
    associer_agents_automatiquement()