# test_direct_corrige.py
import os
import django
import sys

# Configuration Django - REMPLACEZ 'projet' par le VRAI nom de votre projet
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')  # ⚠️ À CORRIGER
django.setup()

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User

def test_simple():
    print("🧪 TEST DIRECT CORRIGÉ - CRÉATION BON DE SOIN")
    print("=" * 50)
    
    client = Client()
    
    # Test 1: Accès sans authentification
    print("1. Test accès sans auth...")
    try:
        response = client.get(reverse('agents:creer_bon_soin'))
        print(f"   Status: {response.status_code} (attendu: 302 ou 403)")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 2: Avec authentification
    print("2. Test avec authentification...")
    try:
        user = User.objects.create_user('test_direct', 'direct@test.com', 'testpass')
        client.force_login(user)
        
        response = client.get(reverse('agents:creer_bon_soin'))
        print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3: API recherche
    print("3. Test API recherche...")
    try:
        response = client.get(reverse('agents:rechercher_membre') + '?q=test')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Succès: {data.get('success')}")
            print(f"   Nombre résultats: {len(data.get('results', []))}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("✅ Tests directs terminés")

if __name__ == "__main__":
    test_simple()