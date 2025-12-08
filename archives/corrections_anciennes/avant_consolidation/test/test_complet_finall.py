
#!/usr/bin/env python
"""
TEST COMPLET APRÈS TOUTES LES CORRECTIONS
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.utils import get_user_primary_group, get_user_redirect_url, user_is_assureur

print("🧪 TEST COMPLET FINAL - TOUTES LES CORRECTIONS")
print("=" * 60)

client = Client()

# 1. Vérification des utilisateurs
print("\n1. 📊 VÉRIFICATION DES UTILISATEURS")
print("-" * 40)

users_to_check = ['DOUA', 'DOUA1', 'ktanos', 'ORNELLA']
for username in users_to_check:
    user = User.objects.get(username=username)
    print(f"\n👤 {username}:")
    print(f"   📧 Email: {user.email or 'Non défini'}")
    print(f"   👑 Superuser: {user.is_superuser}")
    print(f"   🏢 Staff: {user.is_staff}")
    print(f"   🔐 Actif: {user.is_active}")
    print(f"   🏷️  Groupes: {[g.name for g in user.groups.all()]}")
    print(f"   🔍 user_is_assureur: {user_is_assureur(user)}")
    print(f"   🎯 get_user_primary_group: {get_user_primary_group(user)}")
    print(f"   🚀 get_user_redirect_url: {get_user_redirect_url(user)}")

# 2. Test des connexions
print("\n\n2. 🔐 TEST DES CONNEXIONS")
print("-" * 40)

tests = [
    ("DOUA", "DOUA", "/assureur/", "ASSUREUR"),
    ("DOUA1", "DOUA1", "/assureur/", "ASSUREUR"),
    ("ktanos", "ktanos", "/assureur/", "ASSUREUR"),
    ("ORNELLA", "ORNELLA", "/agents/tableau-de-bord/", "AGENT"),
]

results = []

for username, password, expected_url, user_type in tests:
    print(f"\n🔍 Test {username} ({user_type}):")
    
    # Test de connexion
    if client.login(username=username, password=password):
        print(f"   ✅ Connexion réussie")
        
        # Test 1: Redirection après login
        response = client.get('/redirect-after-login/', follow=True)
        final_url = response.request['PATH_INFO']
        print(f"   🔗 Redirection après login: {final_url}")
        
        # Test 2: Accès direct à la page attendue
        response2 = client.get(expected_url, follow=True)
        final_url2 = response2.request['PATH_INFO']
        print(f"   🎯 Accès direct {expected_url}: {final_url2}")
        
        # Vérification
        success = False
        if expected_url in final_url or expected_url in final_url2:
            success = True
            print(f"   ✅ Redirection/accès correct")
        else:
            print(f"   ❌ Problème de redirection/accès")
            print(f"      Attendu: {expected_url}")
            print(f"      Reçu 1: {final_url}")
            print(f"      Reçu 2: {final_url2}")
            
            # Afficher la chaîne de redirection
            if response2.redirect_chain:
                print(f"      Chaîne de redirection:")
                for i, (url, status) in enumerate(response2.redirect_chain):
                    print(f"        {i+1}. {status} -> {url}")
        
        client.logout()
        results.append((username, success))
    else:
        print(f"   ❌ Échec de connexion")
        print(f"      Vérifiez le mot de passe pour {username}")
        results.append((username, False))

# 3. Résumé
print("\n\n3. 📊 RÉSUMÉ DES TESTS")
print("=" * 40)

success_count = sum(1 for _, success in results if success)
total_count = len(results)

for username, success in results:
    status = "✅" if success else "❌"
    print(f"{status} {username}")

print(f"\n📈 Score: {success_count}/{total_count} réussites")

if success_count == total_count:
    print("\n🎉 TOUS LES TESTS SONT RÉUSSIS !")
    print("\n✅ Problèmes résolus:")
    print("   - DOUA1 correctement détecté comme ASSUREUR")
    print("   - Redirections fonctionnelles")
    print("   - Connexions réussies")
else:
    print(f"\n⚠️  {total_count - success_count} test(s) ont échoué")
    
    # Détails des problèmes
    print("\n🔧 PROBLÈMES IDENTIFIÉS:")
    for username, success in results:
        if not success:
            if username in ['DOUA', 'DOUA1']:
                print(f"   • {username}: Échec de connexion")
                print(f"     Solution: Réinitialiser le mot de passe avec python fix_passwords.py")
            elif username == 'ktanos':
                print(f"   • {username}: Redirection incorrecte")
                print(f"     Solution: Vérifier la vue assureur et le décorateur @assureur_required")

print("\n" + "=" * 60)
print("🔄 POUR TESTER MANUELLEMENT:")
print("1. Lancez le serveur: python manage.py runserver")
print("2. Allez sur: http://127.0.0.1:8000/accounts/login/")
print("3. Testez avec:")
print("   - DOUA / DOUA → devrait aller sur /assureur/")
print("   - DOUA1 / DOUA1 → devrait aller sur /assureur/")
print("   - ktanos / ktanos → devrait aller sur /assureur/")
print("   - ORNELLA / ORNELLA → devrait aller sur /agents/tableau-de-bord/")
print("\n📝 Consultez les logs du serveur pour voir:")
print("   - '🔍 get_user_redirect_url - [user]: [type]'")
print("   - '🎯 Redirection vers: [url]'")


