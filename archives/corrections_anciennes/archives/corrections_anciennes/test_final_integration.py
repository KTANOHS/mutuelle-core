# test_final_integration.py
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_fonctionnalite_complete():
    """Teste la fonctionnalité complète"""
    print("🧪 TEST FONCTIONNALITÉ COMPLÈTE")
    print("=" * 50)
    
    client = Client()
    
    # Se connecter avec un utilisateur staff
    try:
        user = User.objects.filter(is_staff=True).first()
        if user:
            client.force_login(user)
            print(f"✅ Connecté en tant que: {user.username}")
            
            # Tester l'accès à la page
            response = client.get('/agents/verification-cotisations/')
            if response.status_code == 200:
                print("✅ Page vérification accessible")
            else:
                print(f"❌ Page vérification: HTTP {response.status_code}")
            
            # Tester l'API de recherche
            response = client.get('/agents/api/recherche-membres/?q=test')
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API recherche fonctionnelle: {len(data.get('membres', []))} résultats")
            else:
                print(f"❌ API recherche: HTTP {response.status_code}")
                
        else:
            print("❌ Aucun utilisateur staff trouvé pour le test")
            
    except Exception as e:
        print(f"❌ Erreur test: {e}")
    
    print("\n🎯 POUR TESTER MANUELLEMENT:")
    print("1. Démarrez le serveur: python manage.py runserver")
    print("2. Connectez-vous avec un compte staff/agent")
    print("3. Visitez: http://localhost:8000/agents/verification-cotisations/")
    print("4. Recherchez un membre existant dans la base")

if __name__ == "__main__":
    test_fonctionnalite_complete()