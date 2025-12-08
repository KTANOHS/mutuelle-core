
#!/usr/bin/env python
import os
import sys
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client

print("🧪 TEST FINAL DES CONNEXIONS")
print("=" * 40)

client = Client()

# Configuration du serveur
BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/accounts/login/"

print(f"\n🔗 URL de test: {LOGIN_URL}")

# Fonction pour tester une connexion
def test_login(username, password, expected_redirect=None):
    print(f"\n🔍 Test de {username}:")
    
    # Tenter la connexion
    login_success = client.login(username=username, password=password)
    
    if login_success:
        print(f"  ✅ Connexion réussie")
        
        # Tester la redirection
        response = client.get('/redirect-after-login/', follow=True)
        
        if response.redirect_chain:
            print(f"  🔗 Chaîne de redirection:")
            for i, (url, status) in enumerate(response.redirect_chain):
                print(f"    {i+1}. {status} -> {url}")
            
            # URL finale
            final_url = response.request['PATH_INFO']
            print(f"  🎯 URL finale: {final_url}")
            
            if expected_redirect and expected_redirect in final_url:
                print(f"  ✅ Redirection correcte vers {expected_redirect}")
            else:
                print(f"  ⚠️  Redirection inattendue")
        else:
            print(f"  ℹ️  Pas de redirection")
        
        # Déconnexion
        client.logout()
        return True
    else:
        print(f"  ❌ Échec de connexion")
        return False

# Liste des tests
tests = [
    ("DOUA", "DOUA", "/assureur/"),
    ("DOUA1", "DOUA1", "/assureur/"),
    ("ktanos", "ktanos", "/assureur/"),
    ("ORNELLA", "ORNELLA", "/agents/tableau-de-bord/"),
    ("Yacouba", "Yacouba", "/medecin/dashboard/"),
    ("GLORIA", "GLORIA", "/pharmacien/dashboard/"),
    ("ASIA", "ASIA", "/membres/dashboard/"),
]

# Exécuter tous les tests
results = []
for username, password, expected in tests:
    success = test_login(username, password, expected)
    results.append((username, success))

# Résumé
print("\n" + "=" * 40)
print("📊 RÉSUMÉ DES TESTS")
print("-" * 20)

success_count = sum(1 for _, success in results if success)
total_count = len(results)

for username, success in results:
    status = "✅" if success else "❌"
    print(f"{status} {username}")

print(f"\n📈 Score: {success_count}/{total_count} réussites")

if success_count == total_count:
    print("🎉 TOUTES LES CONNEXIONS FONCTIONNENT CORRECTEMENT!")
else:
    print("⚠️  Certaines connexions ont échoué")
    print("\n🔧 Prochaines étapes:")
    print("1. Vérifiez que le serveur tourne: python manage.py runserver")
    print("2. Testez manuellement dans le navigateur")
    print("3. Consultez les logs Django pour les erreurs")

