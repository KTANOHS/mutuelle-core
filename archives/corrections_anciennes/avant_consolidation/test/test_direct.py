# test_direct.py
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User

def test_simple():
    print("🧪 TEST SIMPLE - CRÉATION BON DE SOIN")
    print("=" * 50)
    
    client = Client()
    
    # Test 1: Accès sans authentification
    print("1. Test accès sans auth...")
    response = client.get(reverse('agents:creer_bon_soin'))
    print(f"   Status: {response.status_code} (attendu: 302 ou 403)")
    
    # Test 2: Créer un utilisateur et tester avec auth
    print("2. Test avec authentification...")
    user = User.objects.create_user('test_user', 'test@test.com', 'testpass')
    client.force_login(user)
    
    response = client.get(reverse('agents:creer_bon_soin'))
    print(f"   Status: {response.status_code} (attendu: 200)")
    
    # Test 3: API recherche
    print("3. Test API recherche...")
    response = client.get(reverse('agents:rechercher_membre') + '?q=test')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Données: {data.keys()}")
    
    print("✅ Tests basiques terminés")

if __name__ == "__main__":
    test_simple()