# test_manuel_rapide.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from agents.models import Agent

# Test le plus simple
client = Client()
agent = Agent.objects.first()

if agent:
    client.force_login(agent.user)
    response = client.get(reverse('agents:creer_bon_soin'))
    print(f"✅ Page création accessible: {response.status_code}")
    
    response = client.get(reverse('agents:rechercher_membre') + '?q=test')
    print(f"✅ API recherche fonctionne: {response.status_code}")
else:
    print("❌ Aucun agent trouvé")