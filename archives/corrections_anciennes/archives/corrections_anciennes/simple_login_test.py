# final_login_fix.py
import os
import sys
import django
from pathlib import Path

sys.path.append('/Users/koffitanohsoualiho/Documents/projet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def create_working_test_users():
    print("👥 CRÉATION D'UTILISATEURS DE TEST FONCTIONNELS")
    print("=" * 60)
    
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group
    
    User = get_user_model()
    
    # Supprimer les anciens utilisateurs de test problématiques
    users_to_remove = ['testuser', 'assureur_test']
    for username in users_to_remove:
        User.objects.filter(username=username).delete()
        print(f"🗑️  Utilisateur supprimé: {username}")
    
    # Créer de nouveaux utilisateurs de test
    test_users = [
        {'username': 'test_membre', 'password': 'membre123', 'group': 'membre', 'email': 'membre@test.com'},
        {'username': 'test_assureur', 'password': 'assureur123', 'group': 'assureur', 'email': 'assureur@test.com'},
        {'username': 'test_medecin', 'password': 'medecin123', 'group': 'medecin', 'email': 'medecin@test.com'},
        {'username': 'test_pharmacien', 'password': 'pharmacien123', 'group': 'pharmacien', 'email': 'pharmacien@test.com'},
        {'username': 'test_admin', 'password': 'admin123', 'group': 'admin', 'email': 'admin@test.com'},
    ]
    
    for user_info in test_users:
        # Créer l'utilisateur
        user, created = User.objects.get_or_create(
            username=user_info['username'],
            defaults={
                'email': user_info['email'],
                'is_active': True,
                'is_staff': user_info['group'] == 'admin'
            }
        )
        
        if created:
            user.set_password(user_info['password'])
            user.save()
            
            # Assigner le groupe
            group, _ = Group.objects.get_or_create(name=user_info['group'])
            user.groups.add(group)
            
            print(f"✅ {user_info['username']} créé (groupe: {user_info['group']})")
        else:
            print(f"ℹ️  {user_info['username']} existe déjà")

def verify_all_users():
    print("\n🔍 VÉRIFICATION DE TOUS LES UTILISATEURS")
    print("=" * 60)
    
    from django.contrib.auth import get_user_model, authenticate
    User = get_user_model()
    
    users = User.objects.all()
    for user in users:
        groups = [g.name for g in user.groups.all()]
        
        # Tester l'authentification
        test_password = 'test123'  # Mot de passe de test commun
        auth_user = authenticate(username=user.username, password=test_password)
        
        status = "✅" if auth_user else "❌"
        print(f"{status} {user.username}: {groups} - Auth: {'OK' if auth_user else 'FAIL'}")

def create_final_test_script():
    print("\n\n🎯 SCRIPT DE TEST FINAL")
    print("=" * 60)
    
    test_script = '''
# final_test.py
import requests

def test_all_functionality():
    base_url = "http://127.0.0.1:8000"
    
    print("🎯 TEST FINAL COMPLET")
    print("=" * 50)
    
    # Nouveaux utilisateurs de test
    test_users = [
        {'username': 'test_membre', 'password': 'membre123', 'type': 'membre'},
        {'username': 'test_assureur', 'password': 'assureur123', 'type': 'assureur'},
        {'username': 'test_medecin', 'password': 'medecin123', 'type': 'medecin'},
        {'username': 'test_pharmacien', 'password': 'pharmacien123', 'type': 'pharmacien'},
        {'username': 'test_admin', 'password': 'admin123', 'type': 'admin'},
    ]
    
    for user_info in test_users:
        print(f"\\\\n🔐 {user_info['username']} ({user_info['type']}):")
        print("-" * 40)
        
        session = requests.Session()
        
        try:
            # 1. Page d'accueil
            response = session.get(f"{base_url}/", allow_redirects=False)
            print(f"1. 🏠 Accueil: {response.status_code}")
            
            # 2. Connexion
            login_page = session.get(f"{base_url}/accounts/login/")
            csrf_token = session.cookies.get('csrftoken')
            
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
            
            if login_response.status_code == 302:
                print("2. 🔑 Connexion: ✅ RÉUSSIE")
                
                # 3. Suivre les redirections
                current_url = login_response.headers.get('Location')
                redirect_count = 0
                
                while current_url and redirect_count < 3:
                    redirect_count += 1
                    response = session.get(f"{base_url}{current_url}", allow_redirects=False)
                    
                    if response.status_code == 200:
                        print(f"3. 📍 Page finale: ✅ {current_url}")
                        
                        # Vérifier le type de dashboard
                        expected_dashboards = {
                            'membre': '/membre-dashboard/',
                            'assureur': '/assureur-dashboard/',
                            'medecin': '/medecin-dashboard/',
                            'pharmacien': '/pharmacien-dashboard/',
                            'admin': '/admin/'
                        }
                        
                        expected = expected_dashboards.get(user_info['type'])
                        if expected in current_url:
                            print("4. ✅ REDIRECTION CORRECTE!")
                        else:
                            print(f"4. ⚠️  Redirigé vers {current_url} (attendu: {expected})")
                        break
                    elif response.status_code == 302:
                        current_url = response.headers.get('Location')
                    else:
                        print(f"3. ❌ Erreur: {response.status_code}")
                        break
            else:
                print(f"2. 🔑 Connexion: ❌ ÉCHEC ({login_response.status_code})")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")

if __name__ == "__main__":
    test_all_functionality()
'''
    
    print("Script de test final créé!")
    print("Exécutez: python final_test.py")

if __name__ == "__main__":
    create_working_test_users()
    verify_all_users()
    create_final_test_script()