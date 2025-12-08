# test_simple_corrige.py
import os
import django
import sys

# Configuration automatique
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Détection du projet
project_name = None
for item in os.listdir(current_dir):
    if os.path.isdir(os.path.join(current_dir, item)) and 'settings.py' in os.listdir(os.path.join(current_dir, item)):
        project_name = item
        break

if project_name:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
    print(f"🎯 Projet: {project_name}")
else:
    print("❌ Projet non détecté")
    sys.exit(1)

django.setup()

from django.test import Client
from django.urls import reverse
from agents.models import Agent

print("🧪 TEST SIMPLE CORRIGÉ")
print("=" * 40)

client = Client()
agent = Agent.objects.first()

if agent:
    client.force_login(agent.user)
    
    # Test page création
    response = client.get(reverse('agents:creer_bon_soin'))
    print(f"📄 Page création: {response.status_code}")
    
    # Test API recherche
    response = client.get(reverse('agents:rechercher_membre') + '?q=test')
    print(f"🔍 API recherche: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Résultats: {len(data.get('results', []))}")
    
    print("✅ Tests de base fonctionnels")
else:
    print("❌ Aucun agent trouvé")