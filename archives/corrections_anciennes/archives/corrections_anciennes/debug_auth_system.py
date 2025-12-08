#!/usr/bin/env python
"""
Script de debug du système d'authentification et redirection
"""

import os
import sys
import django
from pathlib import Path

def setup_django():
    """Configurer Django"""
    try:
        project_dir = Path.cwd()
        settings_path = None
        
        for path in project_dir.rglob('settings.py'):
            if 'env' not in str(path) and 'venv' not in str(path):
                settings_path = path
                break
        
        if not settings_path:
            return False
        
        project_root = settings_path.parent.parent
        sys.path.append(str(project_root))
        
        settings_module = f"{settings_path.parent.name}.settings"
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
        
        django.setup()
        return True
        
    except Exception as e:
        print(f"❌ Erreur configuration: {e}")
        return False

def test_authentication_flow():
    """Tester le flux d'authentification complet"""
    print("🔐 TEST DU FLUX D'AUTHENTIFICATION")
    print("=" * 50)
    
    try:
        from django.test import Client
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        client = Client()
        
        # 1. Test sans authentification
        print("1. 🔓 Accès sans authentification:")
        response = client.get('/dashboard/')
        print(f"   Status: {response.status_code}")
        print(f"   Redirection: {response.url}")
        
        # 2. Vérifier la page de login
        if response.status_code == 302 and 'login' in response.url:
            print("2. 🔑 Test de la page de login:")
            login_response = client.get(response.url)
            print(f"   Status login page: {login_response.status_code}")
        
        # 3. Créer un utilisateur de test
        print("3. 👤 Création utilisateur test:")
        try:
            user, created = User.objects.get_or_create(
                username='testuser',
                defaults={'email': 'test@example.com', 'password': 'testpass123'}
            )
            if created:
                user.set_password('testpass123')
                user.save()
                print("   ✅ Utilisateur test créé")
            else:
                print("   ✅ Utilisateur test existe déjà")
                
            # 4. Test de connexion
            print("4. 🔐 Test de connexion:")
            login_success = client.login(username='testuser', password='testpass123')
            print(f"   Login réussi: {login_success}")
            
            if login_success:
                # 5. Test accès dashboard après login
                print("5. 🎯 Accès dashboard après login:")
                dashboard_response = client.get('/dashboard/')
                print(f"   Status: {dashboard_response.status_code}")
                print(f"   Redirection: {getattr(dashboard_response, 'url', 'Aucune')}")
                
                if dashboard_response.status_code == 200:
                    print("   ✅ SUCCÈS: Dashboard accessible!")
                else:
                    print("   ❌ ÉCHEC: Problème après login")
                    
        except Exception as e:
            print(f"   ❌ Erreur création utilisateur: {e}")
            
    except Exception as e:
        print(f"❌ Erreur flux auth: {e}")

def analyze_login_redirect():
    """Analyser la configuration de redirection login"""
    print("\n🔄 ANALYSE REDIRECTION LOGIN")
    print("=" * 50)
    
    try:
        from django.conf import settings
        
        print("📋 Configuration auth:")
        print(f"   LOGIN_URL: {getattr(settings, 'LOGIN_URL', 'Non défini')}")
        print(f"   LOGIN_REDIRECT_URL: {getattr(settings, 'LOGIN_REDIRECT_URL', 'Non défini')}")
        print(f"   LOGOUT_REDIRECT_URL: {getattr(settings, 'LOGOUT_REDIRECT_URL', 'Non défini')}")
        
        # Vérifier les URLs d'auth Django
        print("\n📋 URLs d'authentification Django:")
        from django.urls import reverse, NoReverseMatch
        
        auth_urls = [
            'login',
            'logout', 
            'password_reset',
            'password_change'
        ]
        
        for url_name in auth_urls:
            try:
                url = reverse(url_name)
                print(f"   ✅ {url_name}: {url}")
            except NoReverseMatch:
                print(f"   ❌ {url_name}: NON CONFIGURÉE")
                
    except Exception as e:
        print(f"❌ Erreur analyse redirect: {e}")

def test_dashboard_with_authenticated_user():
    """Tester le dashboard avec un utilisateur connecté"""
    print("\n🎯 TEST DASHBOARD UTILISATEUR CONNECTÉ")
    print("=" * 50)
    
    try:
        from django.test import Client
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import Group
        
        User = get_user_model()
        client = Client()
        
        # Créer différents types d'utilisateurs
        test_users = [
            {'username': 'agent_test', 'group': 'AGENTS'},
            {'username': 'assureur_test', 'group': 'ASSUREUR'}, 
            {'username': 'membre_test', 'group': 'MEMBRE'}
        ]
        
        for user_info in test_users:
            print(f"\n👤 Test avec {user_info['username']}:")
            
            # Créer l'utilisateur
            user, created = User.objects.get_or_create(
                username=user_info['username'],
                defaults={'email': f"{user_info['username']}@test.com", 'password': 'test123'}
            )
            
            if created:
                user.set_password('test123')
                user.save()
                print("   ✅ Utilisateur créé")
            
            # Ajouter au groupe si nécessaire
            try:
                group, _ = Group.objects.get_or_create(name=user_info['group'])
                user.groups.add(group)
                print(f"   ✅ Ajouté au groupe {user_info['group']}")
            except:
                print(f"   ⚠️  Impossible d'ajouter au groupe {user_info['group']}")
            
            # Se connecter
            client.login(username=user_info['username'], password='test123')
            print(f"   🔐 Connecté: {client.session.get('_auth_user_id')}")
            
            # Tester le dashboard
            response = client.get('/dashboard/')
            print(f"   🎯 Dashboard - Status: {response.status_code}")
            
            if response.status_code == 302:
                print(f"   🔄 Redirection vers: {response.url}")
            elif response.status_code == 200:
                print("   ✅ SUCCÈS: Dashboard affiché!")
            else:
                print(f"   ❌ ÉCHEC: Status {response.status_code}")
                
    except Exception as e:
        print(f"❌ Erreur test users: {e}")

def check_dashboard_logic():
    """Vérifier la logique de la vue dashboard"""
    print("\n🔍 ANALYSE LOGIQUE DASHBOARD")
    print("=" * 50)
    
    try:
        from mutuelle_core.views import dashboard, get_user_primary_group, get_user_redirect_url
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        
        print("📋 Test des fonctions utilitaires:")
        
        # Tester get_user_primary_group
        test_user = User(username='test')
        group = get_user_primary_group(test_user)
        print(f"   get_user_primary_group: {group}")
        
        # Tester get_user_redirect_url  
        redirect_url = get_user_redirect_url(test_user)
        print(f"   get_user_redirect_url: {redirect_url}")
        
        # Tester la vue avec différents types d'utilisateurs
        factory = RequestFactory()
        
        print("\n🎯 Test vue dashboard avec différents groupes:")
        
        test_cases = [
            {'username': 'admin_test', 'is_superuser': True},
            {'username': 'agent_test', 'group': 'AGENT'},
            {'username': 'assureur_test', 'group': 'ASSUREUR'},
            {'username': 'membre_test', 'group': 'MEMBRE'}
        ]
        
        for case in test_cases:
            print(f"\n   👤 {case['username']}:")
            
            user = User(username=case['username'])
            if case.get('is_superuser'):
                user.is_superuser = True
                
            request = factory.get('/dashboard/')
            request.user = user
            
            try:
                response = dashboard(request)
                print(f"      Status: {response.status_code}")
                if hasattr(response, 'url'):
                    print(f"      Redirection: {response.url}")
            except Exception as e:
                print(f"      ❌ Erreur: {e}")
                
    except Exception as e:
        print(f"❌ Erreur analyse logique: {e}")

def create_authentication_fix():
    """Créer un correctif pour l'authentification"""
    print("\n🔧 CORRECTIF AUTHENTIFICATION")
    print("=" * 50)
    
    fix_content = '''# CORRECTIF SYSTÈME AUTHENTIFICATION
# Ajoutez ceci dans settings.py

# Configuration d'authentification
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/redirect-after-login/'
LOGOUT_REDIRECT_URL = '/'

# OU pour un correctif temporaire, dans mutuelle_core/views.py :

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_simple(request):
    """Version simplifiée du dashboard"""
    return HttpResponse(f"""
    <h1>Dashboard de {request.user}</h1>
    <p>Bienvenue ! Cette page fonctionne.</p>
    <p><a href="/agents/dashboard/">Dashboard Agent</a></p>
    <p><a href="/assureur/dashboard/">Dashboard Assureur</a></p>
    <p><a href="/logout/">Déconnexion</a></p>
    """)

# Puis dans urls.py :
# path('dashboard/', dashboard_simple, name='dashboard'),
'''

    with open('auth_fix.py', 'w') as f:
        f.write(fix_content)
    
    print("📄 Fichier 'auth_fix.py' créé")

def main():
    print("🔍 DEBUG COMPLET SYSTÈME AUTHENTIFICATION")
    print("=" * 60)
    
    if not setup_django():
        return
    
    test_authentication_flow()
    analyze_login_redirect()
    test_dashboard_with_authenticated_user()
    check_dashboard_logic()
    create_authentication_fix()
    
    print("\n" + "=" * 60)
    print("🎯 DIAGNOSTIC FINAL")
    print("=" * 60)
    
    print("""
🚨 PROBLÈME IDENTIFIÉ :

Le dashboard redirige vers la page de login car l'utilisateur n'est pas connecté.
Mais il y a un problème dans le flux de redirection après authentification.

🔍 CAUSES POSSIBLES :

1. 🚨 La page de login Django n'est pas configurée correctement
2. 🚨 LOGIN_REDIRECT_URL ne pointe pas vers la bonne URL  
3. 🚨 Problème avec la vue redirect_after_login
4. 🚨 Utilisateur sans groupe/profil assigné

🚀 SOLUTIONS IMMÉDIATES :

1. TESTER la connexion manuellement :
   - Allez sur /accounts/login/
   - Connectez-vous avec un utilisateur existant
   - Vérifiez où vous êtes redirigé

2. UTILISER les URLs directes :
   - /agents/dashboard/ (si vous êtes agent)
   - /assureur/dashboard/ (si vous êtes assureur)

3. VÉRIFIER la configuration dans settings.py :
   - LOGIN_REDIRECT_URL = '/redirect-after-login/'
   - Assurez-vous que redirect_after_login fonctionne

4. TESTER avec différents utilisateurs (agent, assureur, membre)

📋 COMMANDES DE TEST :

# Tester la connexion
curl -X POST http://127.0.0.1:8000/accounts/login/ -d "username=test&password=test"

# Vérifier les sessions
python manage.py shell
>>> from django.contrib.sessions.models import Session
>>> Session.objects.all().count()
""")

if __name__ == "__main__":
    main()