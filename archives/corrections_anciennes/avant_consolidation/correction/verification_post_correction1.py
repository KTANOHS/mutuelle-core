# verification_post_correction.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_workflow_complet():
    """Teste le workflow complet après corrections"""
    print("🔄 TEST DU WORKFLOW COMPLET")
    
    client = Client()
    
    # Test avec les nouveaux mots de passe
    test_users = [
        ('test_agent', 'test123', 'Agent'),
        ('assureur_test', 'test123', 'Assureur'), 
        ('medecin_test', 'test123', 'Médecin'),
        ('test_pharmacien', 'test123', 'Pharmacien')
    ]
    
    for username, password, role in test_users:
        print(f"\n👤 Test {role} ({username})")
        
        # Test connexion
        if client.login(username=username, password=password):
            print(f"   ✅ Connexion réussie")
            
            # Test accès dashboard
            if role == 'Agent':
                urls = ['/agents/tableau-de-bord/', '/agents/creer-membre/']
            elif role == 'Assureur':
                urls = ['/assureur/dashboard/', '/assureur/cotisations/']
            elif role == 'Médecin':
                urls = ['/medecin/dashboard/', '/medecin/ordonnances/']
            elif role == 'Pharmacien':
                urls = ['/pharmacien/dashboard/', '/pharmacien/ordonnances/']
            
            for url in urls:
                response = client.get(url)
                if response.status_code == 200:
                    print(f"   ✅ Accès {url}")
                else:
                    print(f"   ❌ Accès refusé {url} (Status: {response.status_code})")
        else:
            print(f"   ❌ Échec connexion")

if __name__ == "__main__":
    test_workflow_complet()