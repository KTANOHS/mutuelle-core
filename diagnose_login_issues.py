# diagnose_login_issues.py
import os
import sys
import django
from pathlib import Path

sys.path.append('/Users/koffitanohsoualiho/Documents/projet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnose_login_problems():
    print("🔍 DIAGNOSTIC DES PROBLÈMES DE CONNEXION")
    print("=" * 60)
    
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group
    
    User = get_user_model()
    
    # 1. Vérifier tous les utilisateurs et leurs mots de passe
    print("1. 👥 UTILISATEURS ET MOTS DE PASSE:")
    users = User.objects.all()
    
    for user in users:
        groups = [g.name for g in user.groups.all()]
        has_password = bool(user.password) and user.password.startswith('pbkdf2_')
        
        print(f"   👤 {user.username}:")
        print(f"      Groupes: {groups}")
        print(f"      Mot de passe défini: {'✅' if has_password else '❌'}")
        print(f"      Actif: {'✅' if user.is_active else '❌'}")
        
        # Tester l'authentification
        from django.contrib.auth import authenticate
        auth_result = authenticate(username=user.username, password='wrong_password')
        if auth_result:
            print(f"      ⚠️  Authentification avec mauvais mot de passe réussie!")
        else:
            print(f"      🔐 Authentification échoue avec mauvais mot de passe (normal)")
    
    # 2. Vérifier la vue de login
    print("\n2. 👁️ VÉRIFICATION VUE LOGIN:")
    try:
        from mutuelle_core import views
        if hasattr(views, 'view'):
            print("   ✅ Vue 'view' pour l'authentification trouvée")
        else:
            print("   ❌ Vue 'view' manquante")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 3. Vérifier les URLs d'authentification
    print("\n3. 🔗 URLS AUTHENTIFICATION:")
    from django.urls import reverse, resolve
    
    auth_urls = ['login', 'logout']
    for url_name in auth_urls:
        try:
            url_path = reverse(url_name)
            print(f"   ✅ {url_name}: {url_path}")
        except Exception as e:
            print(f"   ❌ {url_name}: {e}")

def reset_test_users_passwords():
    print("\n\n🔧 RÉINITIALISATION DES MOTS DE PASSE TEST")
    print("=" * 60)
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Définir des mots de passe simples pour le test
    test_users_passwords = {
        'testuser': 'test123',
        'assureur': 'assureur123', 
        'medecin': 'medecin123',
        'pharmacien': 'pharmacien123',
        'membre': 'membre123',
        'ktanos': 'admin123'
    }
    
    for username, password in test_users_passwords.items():
        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            print(f"✅ {username}: mot de passe défini à '{password}'")
        except User.DoesNotExist:
            print(f"❌ Utilisateur non trouvé: {username}")

def test_authentication():
    print("\n\n🧪 TEST AUTHENTIFICATION DIRECTE")
    print("=" * 60)
    
    from django.contrib.auth import get_user_model, authenticate
    User = get_user_model()
    
    test_credentials = [
        ('testuser', 'test123'),
        ('assureur', 'assureur123'),
        ('medecin', 'medecin123'), 
        ('pharmacien', 'pharmacien123'),
        ('membre', 'membre123'),
        ('ktanos', 'admin123')
    ]
    
    for username, password in test_credentials:
        user = authenticate(username=username, password=password)
        if user:
            print(f"✅ {username}: Authentification RÉUSSIE")
            print(f"   Groupes: {[g.name for g in user.groups.all()]}")
        else:
            print(f"❌ {username}: Authentification ÉCHOUÉE")

def create_simple_login_test():
    print("\n\n🌐 TEST DE CONNEXION SIMPLE")
    print("=" * 60)
    
    test_code = '''
import requests

def simple_login_test():
    base_url = "http://127.0.0.1:8000"
    
    # Utilisateurs de test avec nouveaux mots de passe
    test_users = [
        {'username': 'testuser', 'password': 'test123'},
        {'username': 'assureur', 'password': 'assureur123'},
        {'username': 'medecin', 'password': 'medecin123'},
        {'username': 'pharmacien', 'password': 'pharmacien123'},
        {'username': 'ktanos', 'password': 'admin123'},
    ]
    
    for user_info in test_users:
        print(f"🔐 Test {user_info['username']}:")
        
        session = requests.Session()
        
        # 1. Récupérer la page de login
        login_page = session.get(f"{base_url}/accounts/login/")
        csrf_token = session.cookies.get('csrftoken')
        
        # 2. Tentative de connexion
        login_data = {
            'username': user_info['username'],
            'password': user_info['password'],
            'csrfmiddlewaretoken': csrf_token,
        }
        
        login_response = session.post(
            f"{base_url}/accounts/login/",
            data=login_data,
            allow_redirects=False
        )
        
        print(f"   Status: {login_response.status_code}")
        
        if login_response.status_code == 302:
            print(f"   ✅ CONNEXION RÉUSSIE!")
            redirect_url = login_response.headers.get('Location')
            print(f"   Redirection: {redirect_url}")
            
            # Suivre la redirection
            if redirect_url:
                final_response = session.get(f"{base_url}{redirect_url}", allow_redirects=False)
                print(f"   Page finale: {final_response.status_code}")
        else:
            print(f"   ❌ ÉCHEC CONNEXION")
        
        print()

if __name__ == "__main__":
    simple_login_test()
'''
    
    print("Code de test à exécuter:")
    print(test_code)

if __name__ == "__main__":
    diagnose_login_problems()
    reset_test_users_passwords()
    test_authentication()
    create_simple_login_test()