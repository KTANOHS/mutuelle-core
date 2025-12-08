# test_assureur_final.py
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

print("🔧 TEST FINAL DE L'APPLICATION ASSUREUR")
print("="*50)

from django.test import Client
from django.contrib.auth.models import User
from assureur.models import Assureur

# Créer un client de test
client = Client()

# Tester l'accès aux pages principales
urls_to_test = [
    '/assureur/',
    '/assureur/membres/',
    '/assureur/bons/',
    '/assureur/soins/',
    '/assureur/paiements/',
    '/assureur/cotisations/',
    '/assureur/statistiques/',
    '/assureur/configuration/',
]

print("\n📋 Test des URLs (sans authentification) :")
for url in urls_to_test:
    response = client.get(url)
    if response.status_code in [200, 302, 403]:
        print(f"✅ {url} : {response.status_code}")
    else:
        print(f"❌ {url} : {response.status_code}")

# Tester la création d'un assureur de test
print("\n👤 Test de création d'assureur :")
try:
    user, created = User.objects.get_or_create(
        username='test_assureur',
        defaults={'email': 'test@assureur.com', 'password': 'test123'}
    )
    
    if created:
        assureur, assureur_created = Assureur.objects.get_or_create(
            user=user,
            defaults={'nom': 'Test Assureur', 'email': 'test@assureur.com'}
        )
        if assureur_created:
            print("✅ Assureur de test créé avec succès")
        else:
            print("ℹ️  Assureur de test déjà existant")
    else:
        print("ℹ️  Utilisateur de test déjà existant")
        
except Exception as e:
    print(f"❌ Erreur lors de la création : {e}")

print("\n🎉 Test terminé !")
print("\nPour lancer le serveur :")
print("  python manage.py runserver")
print("\nPour accéder à l'admin :")
print("  http://localhost:8000/admin")
print("\nPour accéder à l'assureur :")
print("  http://localhost:8000/assureur/")