# debug_navigateur.py
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

def debug_navigateur():
    print("🐛 DEBUG NAVIGATEUR")
    print("==================")
    
    client = Client()
    
    # Simuler exactement ce que fait le navigateur
    print("1. 🔄 SIMULATION NAVIGATEUR COMPLÈTE")
    
    # Étape 1: Page login
    print("\n📄 Étape 1: GET /accounts/login/")
    response1 = client.get('/accounts/login/')
    print(f"   Status: {response1.status_code}")
    print(f"   Template: {response1.templates[0].name if response1.templates else 'Aucun'}")
    
    # Étape 2: POST login
    print("\n🔐 Étape 2: POST /accounts/login/")
    response2 = client.post('/accounts/login/', {
        'username': 'agent_test',
        'password': 'password123',
        'next': '/agents/dashboard/'  # Important pour la redirection
    }, follow=True)
    
    print(f"   Status: {response2.status_code}")
    print(f"   URL finale: {response2.request['PATH_INFO']}")
    
    # Étape 3: Vérifier toutes les URLs importantes
    print("\n🧭 Étape 3: TEST TOUTES LES URLs AGENTS")
    
    urls_agents = [
        '/agents/',
        '/agents/dashboard/',
        '/agents/membres/',
        '/agents/verifier-cotisations/',
        '/agents/bons-soin/creer/',
        '/agents/bons-soin/historique/',
        '/agents/notifications/',
    ]
    
    for url in urls_agents:
        response = client.get(url)
        if response.status_code == 200:
            print(f"   ✅ {url:35} → OK")
        elif response.status_code == 302:
            redirect_url = response.url
            print(f"   🔁 {url:35} → REDIRECTION vers {redirect_url}")
        else:
            print(f"   ❌ {url:35} → Status {response.status_code}")
    
    print("\n🎯 DEBUG TERMINÉ")

if __name__ == "__main__":
    debug_navigateur()