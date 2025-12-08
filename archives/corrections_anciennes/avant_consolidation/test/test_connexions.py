#!/usr/bin/env python
"""
SCRIPT DE TEST DES CONNEXIONS ET REDIRECTIONS
Teste tous les utilisateurs et vérifie qu'ils vont sur le bon dashboard
"""
import os
import sys
import django
import requests
from django.test import Client
from django.contrib.auth.models import User

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Initialiser Django
django.setup()

print("=" * 80)
print("🧪 SCRIPT DE TEST DES CONNEXIONS ET REDIRECTIONS")
print("=" * 80)

def test_connexion_http():
    """Test des connexions via HTTP réel"""
    print("\n🌐 TEST DES CONNEXIONS HTTP")
    print("-" * 40)
    
    # Configuration
    base_url = "http://127.0.0.1:8000"
    login_url = f"{base_url}/accounts/login/"
    
    print(f"🔗 URL de login: {login_url}")
    print(f"ℹ️  Assurez-vous que le serveur tourne sur {base_url}")
    
    # Créer une session
    session = requests.Session()
    
    # Récupérer le token CSRF
    try:
        response = session.get(login_url)
        if response.status_code == 200:
            print("✅ Page de login accessible")
        else:
            print(f"❌ Erreur accès login: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Impossible d'accéder au serveur: {e}")
        print("   Lancez le serveur avec: python manage.py runserver")
        return
    
    # Liste des tests
    tests = [
        ("DOUA", "DOUA", "/assureur/", "ASSUREUR"),
        ("DOUA1", "DOUA1", "/assureur/", "ASSUREUR"),
        ("ktanos", "ktanos", "/assureur/", "ASSUREUR"),
        ("ORNELLA", "ORNELLA", "/agents/tableau-de-bord/", "AGENT"),
        ("Yacouba", "Yacouba", "/medecin/dashboard/", "MEDECIN"),
        ("GLORIA", "GLORIA", "/pharmacien/dashboard/", "PHARMACIEN"),
        ("ASIA", "ASIA", "/membres/dashboard/", "MEMBRE"),
        ("matrix", "matrix", "/admin/", "ADMIN"),
    ]
    
    results = []
    
    for username, password, expected_url, user_type in tests:
        print(f"\n🔍 Test {username} ({user_type}):")
        
        # Tenter la connexion
        login_data = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': session.cookies.get('csrftoken', '')
        }
        
        try:
            # Envoyer la requête POST
            response = session.post(
                login_url,
                data=login_data,
                headers={'Referer': login_url},
                allow_redirects=True
            )
            
            if response.status_code == 200:
                # Vérifier si on est sur la page de login (échec) ou redirigé (succès)
                if 'login' in response.url:
                    print(f"   ❌ Échec de connexion")
                    print(f"      URL finale: {response.url}")
                    results.append((username, False, "Échec de connexion", response.url))
                else:
                    print(f"   ✅ Connexion réussie")
                    print(f"   🔗 Redirection vers: {response.url}")
                    
                    # Vérifier la redirection
                    if expected_url in response.url:
                        print(f"   ✅ Redirection correcte vers {expected_url}")
                        results.append((username, True, "Succès", response.url))
                    else:
                        print(f"   ⚠️  Redirection inattendue")
                        print(f"      Attendu: {expected_url}")
                        print(f"      Reçu: {response.url}")
                        results.append((username, True, "Redirection incorrecte", response.url))
            
            elif response.status_code == 302 or response.status_code == 303:
                # Redirection après connexion réussie
                print(f"   ✅ Connexion réussie (redirection {response.status_code})")
                redirect_url = response.headers.get('Location', '')
                print(f"   🔗 Redirection vers: {redirect_url}")
                
                if expected_url in redirect_url:
                    print(f"   ✅ Redirection correcte vers {expected_url}")
                    results.append((username, True, "Succès", redirect_url))
                else:
                    print(f"   ⚠️  Redirection inattendue")
                    print(f"      Attendu: {expected_url}")
                    print(f"      Reçu: {redirect_url}")
                    results.append((username, True, "Redirection incorrecte", redirect_url))
            
            else:
                print(f"   ❌ Statut HTTP inattendu: {response.status_code}")
                results.append((username, False, f"HTTP {response.status_code}", response.url))
                
        except Exception as e:
            print(f"   ❌ Erreur lors de la connexion: {e}")
            results.append((username, False, str(e), ""))
        
        # Déconnexion pour le prochain test
        logout_url = f"{base_url}/logout/"
        try:
            session.get(logout_url)
        except:
            pass
        
        # Nouvelle session pour le prochain test
        session = requests.Session()
        session.get(login_url)
    
    return results

def test_connexion_django_client():
    """Test des connexions avec le client de test Django (plus rapide)"""
    print("\n⚡ TEST AVEC CLIENT DJANGO (sans serveur)")
    print("-" * 40)
    
    client = Client()
    
    tests = [
        ("DOUA", "DOUA", "/assureur/", "ASSUREUR"),
        ("DOUA1", "DOUA1", "/assureur/", "ASSUREUR"),
        ("ktanos", "ktanos", "/assureur/", "ASSUREUR"),
        ("ORNELLA", "ORNELLA", "/agents/tableau-de-bord/", "AGENT"),
        ("Yacouba", "Yacouba", "/medecin/dashboard/", "MEDECIN"),
        ("GLORIA", "GLORIA", "/pharmacien/dashboard/", "PHARMACIEN"),
        ("ASIA", "ASIA", "/membres/dashboard/", "MEMBRE"),
        ("matrix", "matrix", "/admin/", "ADMIN"),
    ]
    
    results = []
    
    for username, password, expected_url, user_type in tests:
        print(f"\n🔍 Test {username} ({user_type}):")
        
        try:
            # Tenter la connexion
            login_success = client.login(username=username, password=password)
            
            if not login_success:
                print(f"   ❌ Échec de connexion")
                results.append((username, False, "Échec de connexion", ""))
                continue
            
            print(f"   ✅ Connexion réussie")
            
            # Tester la redirection après login
            response = client.get('/redirect-after-login/', follow=True)
            
            if response.redirect_chain:
                print(f"   🔗 Chaîne de redirection:")
                for i, (url, status) in enumerate(response.redirect_chain):
                    print(f"      {i+1}. {status} -> {url}")
            
            # URL finale
            final_url = response.request['PATH_INFO']
            print(f"   🎯 URL finale: {final_url}")
            
            # Vérifier la redirection
            expected_found = False
            for pattern in [expected_url, expected_url.replace('/', '')]:
                if pattern in final_url:
                    expected_found = True
                    break
            
            if expected_found:
                print(f"   ✅ Redirection correcte vers {expected_url}")
                results.append((username, True, "Succès", final_url))
            else:
                print(f"   ⚠️  Redirection inattendue")
                print(f"      Attendu: {expected_url}")
                print(f"      Reçu: {final_url}")
                results.append((username, True, "Redirection incorrecte", final_url))
            
            # Déconnexion
            client.logout()
            
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            results.append((username, False, str(e), ""))
    
    return results

def test_fonctions_utilitaires():
    """Test des fonctions utilitaires de core/utils.py"""
    print("\n🔧 TEST DES FONCTIONS UTILITAIRES")
    print("-" * 40)
    
    try:
        from core.utils import (
            get_user_primary_group,
            get_user_type,
            get_user_redirect_url,
            user_is_assureur,
            est_assureur,
            user_is_membre,
            est_membre
        )
        
        print("✅ Module core/utils importé avec succès")
        
        users_to_test = User.objects.filter(is_active=True)
        
        for user in users_to_test:
            print(f"\n👤 {user.username}:")
            
            primary_group = get_user_primary_group(user)
            user_type = get_user_type(user)
            redirect_url = get_user_redirect_url(user)
            
            print(f"   • get_user_primary_group: {primary_group}")
            print(f"   • get_user_type: {user_type}")
            print(f"   • get_user_redirect_url: {redirect_url}")
            
            # Tests spécifiques
            if user.username == 'DOUA1':
                print(f"   🔍 Tests spécifiques DOUA1:")
                print(f"      • user_is_assureur: {user_is_assureur(user)}")
                print(f"      • est_assureur: {est_assureur(user)}")
                print(f"      • user_is_membre: {user_is_membre(user)}")
                print(f"      • est_membre: {est_membre(user)}")
                
                if primary_group == 'ASSUREUR':
                    print("      ✅ DOUA1 correctement détecté comme ASSUREUR")
                else:
                    print(f"      ❌ PROBLÈME: DOUA1 détecté comme {primary_group}")
    
    except Exception as e:
        print(f"❌ Erreur lors du test des fonctions: {e}")
        import traceback
        traceback.print_exc()

def verifier_donnees_utilisateurs():
    """Vérification des données utilisateurs"""
    print("\n📊 VÉRIFICATION DES DONNÉES UTILISATEURS")
    print("-" * 40)
    
    users = User.objects.all().order_by('id')
    
    print(f"📋 {users.count()} utilisateurs trouvés:")
    print("-" * 30)
    
    for user in users:
        print(f"\n👤 {user.username} (ID: {user.id}):")
        print(f"   📧 Email: {user.email or 'Non défini'}")
        print(f"   👑 Superuser: {user.is_superuser}")
        print(f"   🏢 Staff: {user.is_staff}")
        print(f"   🔐 Actif: {user.is_active}")
        
        # Groupes
        user_groups = user.groups.all()
        if user_groups:
            print(f"   🏷️  Groupes: {[g.name for g in user_groups]}")
        else:
            print(f"   🏷️  Groupes: Aucun")
        
        # Vérifications spéciales
        if user.username in ['DOUA', 'DOUA1', 'ktanos']:
            print(f"   🔍 Spécifique assureur:")
            print(f"      • Dans groupe 'Assureur': {user.groups.filter(name='Assureur').exists()}")
            print(f"      • is_staff: {user.is_staff}")
            print(f"      • is_superuser: {user.is_superuser}")
    
    # Statistiques
    print(f"\n📈 STATISTIQUES:")
    from django.contrib.auth.models import Group
    
    for group in Group.objects.all():
        count = group.user_set.count()
        print(f"   • {group.name}: {count} utilisateur(s)")

def test_urls_accessibles():
    """Test que les URLs principales sont accessibles"""
    print("\n🌐 TEST D'ACCÈS AUX URLs PRINCIPALES")
    print("-" * 40)
    
    client = Client()
    
    urls_to_test = [
        ("/", "Page d'accueil"),
        ("/accounts/login/", "Page de login"),
        ("/admin/", "Admin Django"),
        ("/assureur/", "Dashboard assureur"),
        ("/agents/tableau-de-bord/", "Dashboard agent"),
        ("/medecin/dashboard/", "Dashboard médecin"),
        ("/pharmacien/dashboard/", "Dashboard pharmacien"),
        ("/membres/dashboard/", "Dashboard membre"),
    ]
    
    for url, description in urls_to_test:
        try:
            response = client.get(url, follow=True)
            status = response.status_code
            
            if status == 200:
                print(f"✅ {description}: {url} - HTTP {status}")
            elif status == 302 or status == 301:
                redirect_url = response.headers.get('Location', '')
                print(f"🔀 {description}: {url} - Redirection {status} vers {redirect_url}")
            elif status == 403:
                print(f"🔒 {description}: {url} - Accès interdit (HTTP {status})")
            elif status == 404:
                print(f"❌ {description}: {url} - Non trouvé (HTTP {status})")
            else:
                print(f"⚠️  {description}: {url} - Statut inattendu {status}")
                
        except Exception as e:
            print(f"💥 {description}: {url} - Erreur: {e}")

def executer_tous_les_tests():
    """Exécute tous les tests"""
    print("\n🎯 EXÉCUTION DE TOUS LES TESTS")
    print("=" * 40)
    
    # 1. Vérification des données
    verifier_donnees_utilisateurs()
    
    # 2. Test des fonctions utilitaires
    test_fonctions_utilitaires()
    
    # 3. Test avec client Django
    print("\n" + "=" * 80)
    print("⚡ PHASE 1: TESTS RAPIDES (Client Django)")
    print("=" * 80)
    results_django = test_connexion_django_client()
    
    # 4. Test URLs accessibles
    test_urls_accessibles()
    
    # 5. Résumé
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 80)
    
    total = len(results_django)
    succes = sum(1 for _, success, _, _ in results_django if success)
    
    print(f"\n📈 Résultats tests Django Client: {succes}/{total} réussites")
    
    for username, success, message, url in results_django:
        status = "✅" if success else "❌"
        print(f"{status} {username}: {message}")
        if url and "incorrecte" in message:
            print(f"   ↳ URL: {url}")
    
    # Recommandations
    print("\n🔧 RECOMMANDATIONS:")
    
    # Vérifier DOUA1
    doua1 = User.objects.filter(username='DOUA1').first()
    if doua1:
        from core.utils import get_user_primary_group
        if get_user_primary_group(doua1) != 'ASSUREUR':
            print("❌ DOUA1 n'est pas détecté comme ASSUREUR")
            print("   Solution: Vérifiez core/utils.py et que DOUA1 est dans le groupe 'Assureur'")
    
    # Vérifier les redirections
    print("\n🎯 POUR TESTER MANUELLEMENT:")
    print("1. Lancez le serveur: python manage.py runserver")
    print("2. Allez sur: http://127.0.0.1:8000/accounts/login/")
    print("3. Testez avec:")
    print("   - DOUA / DOUA → /assureur/")
    print("   - DOUA1 / DOUA1 → /assureur/")
    print("   - ORNELLA / ORNELLA → /agents/tableau-de-bord/")
    
    return results_django

def test_connexion_manuel():
    """Test manuel avec des instructions détaillées"""
    print("\n🛠️  TEST MANUEL - INSTRUCTIONS DÉTAILLÉES")
    print("=" * 40)
    
    print("""
📋 PRÉ-REQUIS:
1. Le serveur doit être lancé:
   $ python manage.py runserver
   
2. Ouvrez votre navigateur et allez sur:
   http://127.0.0.1:8000/accounts/login/

3. Testez chaque compte:

   ┌─────────────────┬────────────┬─────────────────────────────────────┐
   │ Utilisateur    │ Mot de passe│ Redirection attendue               │
   ├─────────────────┼────────────┼─────────────────────────────────────┤
   │ DOUA           │ DOUA        │ /assureur/                         │
   │ DOUA1          │ DOUA1       │ /assureur/                         │
   │ ktanos         │ ktanos      │ /assureur/                         │
   │ ORNELLA        │ ORNELLA     │ /agents/tableau-de-bord/           │
   │ Yacouba        │ Yacouba     │ /medecin/dashboard/                │
   │ GLORIA         │ GLORIA      │ /pharmacien/dashboard/             │
   │ ASIA           │ ASIA        │ /membres/dashboard/                │
   │ matrix         │ matrix      │ /admin/                            │
   └─────────────────┴────────────┴─────────────────────────────────────┘

4. Vérifiez dans la console du serveur les messages:
   - "🔍 get_user_redirect_url - [USER]: [TYPE]"
   - "🎯 Redirection vers: [URL]"
   
5. Signalez tout problème:
   - Redirection incorrecte
   - Erreur de connexion
   - Page non trouvée (404)
   
6. Pour DOUA1 spécifiquement:
   - Il doit montrer "DOUA1: ASSUREUR"
   - Redirection vers "/assureur/"
   - S'il montre "MEMBRE", il y a un problème dans core/utils.py
   
⚠️  EN CAS DE PROBLÈME AVEC DOUA1:
   Vérifiez dans la console Django:
   - Les groupes de DOUA1
   - Le résultat de get_user_primary_group()
   
   Vous pouvez aussi exécuter:
   $ python manage.py shell -c "
     from django.contrib.auth.models import User
     from core.utils import get_user_primary_group
     doua1 = User.objects.get(username='DOUA1')
     print(f'Groupes: {[g.name for g in doua1.groups.all()]}')
     print(f'Primary group: {get_user_primary_group(doua1)}')
     "
    """)

def creer_script_de_test_simple():
    """Crée un script de test simple pour exécution rapide"""
    script_content = '''
#!/usr/bin/env python
"""
SCRIPT DE TEST SIMPLE - Vérification rapide des connexions
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.utils import get_user_primary_group

print("🧪 TEST RAPIDE DES CONNEXIONS")
print("=" * 40)

client = Client()
tests = [
    ("DOUA", "DOUA", "/assureur/", "ASSUREUR"),
    ("DOUA1", "DOUA1", "/assureur/", "ASSUREUR"),
    ("ORNELLA", "ORNELLA", "/agents/tableau-de-bord/", "AGENT"),
]

for username, password, expected_url, user_type in tests:
    print(f"\\n🔍 Test {username}:")
    
    # Vérification groupe
    user = User.objects.get(username=username)
    primary_group = get_user_primary_group(user)
    print(f"   Groupe détecté: {primary_group} (attendu: {user_type})")
    
    # Test connexion
    if client.login(username=username, password=password):
        print("   ✅ Connexion réussie")
        
        response = client.get('/redirect-after-login/', follow=True)
        final_url = response.request['PATH_INFO']
        
        if expected_url in final_url:
            print(f"   ✅ Redirection correcte: {final_url}")
        else:
            print(f"   ❌ Redirection incorrecte")
            print(f"      Attendu: {expected_url}")
            print(f"      Reçu: {final_url}")
        
        client.logout()
    else:
        print("   ❌ Échec de connexion")

print("\\n✅ TEST TERMINÉ")
'''
    
    test_file = "test_connexion_rapide.py"
    with open(test_file, 'w') as f:
        f.write(script_content)
    
    print(f"\n📄 Script de test rapide créé: {test_file}")
    print(f"   Exécutez-le avec: python {test_file}")
    
    return test_file

if __name__ == "__main__":
    print("""
🔧 OPTIONS DE TEST:
1. Tests complets (recommandé)
2. Test rapide uniquement
3. Test manuel (instructions)
4. Créer script de test
5. Quitter
""")
    
    choix = input("Votre choix (1-5): ").strip()
    
    if choix == "1":
        print("\n🎯 LANCEMENT DES TESTS COMPLETS...")
        executer_tous_les_tests()
        test_connexion_manuel()
        
    elif choix == "2":
        print("\n⚡ LANCEMENT DU TEST RAPIDE...")
        test_connexion_django_client()
        
    elif choix == "3":
        test_connexion_manuel()
        
    elif choix == "4":
        script_file = creer_script_de_test_simple()
        print(f"\n✅ Script créé: {script_file}")
        print("Exécutez-le maintenant? (o/N): ", end="")
        if input().lower() == 'o':
            os.system(f"python {script_file}")
            
    elif choix == "5":
        print("Au revoir!")
        sys.exit(0)
    
    print("\n" + "=" * 80)
    print("✅ TESTS TERMINÉS")
    print("=" * 80)