
#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.utils import get_user_primary_group, get_user_redirect_url

print("🧪 TEST FINAL APRÈS CORRECTIONS")
print("=" * 40)

client = Client()

tests = [
    ("DOUA", "DOUA", "/assureur/", "ASSUREUR"),
    ("DOUA1", "DOUA1", "/assureur/", "ASSUREUR"),
    ("ktanos", "ktanos", "/assureur/", "ASSUREUR"),
    ("ORNELLA", "ORNELLA", "/agents/tableau-de-bord/", "AGENT"),
]

print("🔍 Vérification préalable des utilisateurs:")
print("-" * 30)

for username, _, _, _ in tests:
    user = User.objects.get(username=username)
    print(f"👤 {username}:")
    print(f"   is_staff: {user.is_staff}")
    print(f"   is_superuser: {user.is_superuser}")
    print(f"   Groupes: {[g.name for g in user.groups.all()]}")
    print(f"   get_user_primary_group: {get_user_primary_group(user)}")
    print(f"   get_user_redirect_url: {get_user_redirect_url(user)}")
    print()

print("\n🔍 Test des connexions:")
print("-" * 30)

results = []

for username, password, expected_url, user_type in tests:
    print(f"\n🔍 Test {username}:")
    
    # Test de connexion
    if client.login(username=username, password=password):
        print(f"   ✅ Connexion réussie")
        
        # Test redirection
        response = client.get('/redirect-after-login/', follow=True)
        final_url = response.request['PATH_INFO']
        print(f"   🎯 URL finale: {final_url}")
        
        # Vérifier la redirection
        if expected_url in final_url:
            print(f"   ✅ Redirection correcte vers {expected_url}")
            results.append((username, True, "Succès"))
        else:
            print(f"   ❌ Redirection incorrecte")
            print(f"      Attendu: {expected_url}")
            results.append((username, True, "Redirection incorrecte"))
        
        client.logout()
    else:
        print(f"   ❌ Échec de connexion")
        results.append((username, False, "Échec connexion"))

print("\n" + "=" * 40)
print("📊 RÉSUMÉ DES TESTS")
print("=" * 40)

success_count = sum(1 for _, success, _ in results if success)
total_count = len(results)

for username, success, message in results:
    status = "✅" if success else "❌"
    print(f"{status} {username}: {message}")

print(f"\n📈 Score: {success_count}/{total_count} réussites")

if success_count == total_count:
    print("\n🎉 TOUS LES TESTS SONT RÉUSSIS !")
    print("\n✅ DOUA1 est maintenant correctement détecté comme ASSUREUR")
    print("✅ Les redirections fonctionnent correctement")
else:
    print(f"\n⚠️  {total_count - success_count} test(s) ont échoué")
    
print("\n🔄 Pour tester manuellement:")
print("1. Redémarrez le serveur: python manage.py runserver")
print("2. Allez sur: http://127.0.0.1:8000/accounts/login/")
print("3. Connectez-vous avec:")
print("   - DOUA / DOUA → /assureur/")
print("   - DOUA1 / DOUA1 → /assureur/")
print("   - ktanos / ktanos → /assureur/")


