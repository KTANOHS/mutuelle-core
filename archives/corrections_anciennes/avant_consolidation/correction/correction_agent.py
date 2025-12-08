import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Agent
from django.contrib.auth.models import User

def verifier_structure_agent():
    """Vérifier la structure du modèle Agent"""
    print("🔍 VÉRIFICATION STRUCTURE AGENT")
    print("===============================")
    
    # Vérifier un agent
    agent = Agent.objects.first()
    print(f"👤 Agent exemple: {agent}")
    
    # Lister tous les attributs disponibles
    print("\n📋 ATTRIBUTS DISPONIBLES:")
    for field in agent._meta.fields:
        print(f"  - {field.name}: {getattr(agent, field.name, 'N/A')}")
    
    # Vérifier les méthodes
    print("\n🛠️ MÉTHODES DISPONIBLES:")
    methods = [method for method in dir(agent) if not method.startswith('_')]
    for method in methods[:10]:  # Premier 10 seulement
        print(f"  - {method}")

if __name__ == "__main__":
    verifier_structure_agent()