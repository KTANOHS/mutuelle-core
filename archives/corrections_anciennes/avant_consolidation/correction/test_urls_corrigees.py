# test_urls_corrigees.py
import os
import sys
import django
from django.test import Client
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

def test_urls_apres_correction():
    print("🧪 TEST DES URLS APRÈS CORRECTION")
    print("=" * 50)
    
    client = Client()
    
    # Se connecter avec test_agent
    user = User.objects.get(username='test_agent')
    client.force_login(user)
    
    urls_a_tester = [
        '/agents/tableau-de-bord/',
        '/agents/creer-bon-soin/',
        '/agents/verification-cotisations/',
        '/agents/rapport-performance/',
        '/agents/historique-bons/',
    ]
    
    for url in urls_a_tester:
        response = client.get(url)
        statut = "✅" if response.status_code == 200 else "❌"
        print(f"{statut} {url:40} -> {response.status_code}")
        
        if response.status_code != 200:
            print(f"   Erreur: {getattr(response, 'content', '')[:100]}")

if __name__ == "__main__":
    test_urls_apres_corrigees()