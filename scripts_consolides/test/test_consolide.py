"""
FICHIER CONSOLIDÉ: test
Catégorie: test
Fusion de 143 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: test_api_simple.py (2025-12-06)
# ============================================================

#!/usr/bin/env python3
# test_api_simple.py - Test simplifié de l'API
import requests
import json
import sys

def test_api():
    base_url = "http://127.0.0.1:8000"

    # Test 1: JSON
    print("\n🔍 Test 1: Envoi JSON")
    url = f"{base_url}/communication/envoyer-message-api/"
    data = {
        "destinataire_id": 1,
        "contenu": "Test message via JSON API",
        "titre": "Test API"
    }

    try:
        response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Succès: {response.json()}")
        else:
            print(f"   ❌ Erreur: {response.text[:200]}")
    except Exception as e:
        print(f"   💥 Exception: {str(e)}")

    # Test 2: Form-Data
    print("\n🔍 Test 2: Envoi Form-Data")
    data_form = {
        "destinataire": 1,
        "contenu": "Test message via Form-Data",
        "titre": "Test Form"
    }

    try:
        response = requests.post(url, data=data_form)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Succès: {response.json()}")
        else:
            print(f"   ❌ Erreur: {response.text[:200]}")
    except Exception as e:
        print(f"   💥 Exception: {str(e)}")

if __name__ == "__main__":
    test_api()

# ============================================================
# ORIGINE 2: test_fonctionnalites_assureur.py (2025-12-06)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE TEST AUTOMATISÉ - FONCTIONNALITÉS ASSUREUR
Teste les principales fonctionnalités de l'application.
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from assureur.models import Assureur

def test_fonctionnalites_assureur():
    """Teste les fonctionnalités principales"""
    print("🧪 TESTS FONCTIONNALITÉS ASSUREUR")
    print("="*60)

    client = Client()

    # 1. Test de connexion avec différents utilisateurs
    print("\n1. TESTS DE CONNEXION:")

    test_users = ['DOUA', 'ktanos', 'DOUA1']

    for username in test_users:
        try:
            user = User.objects.get(username=username)
            # Simuler une connexion
            client.force_login(user)

            # Tester l'accès au dashboard
            response = client.get('/assureur/')
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {username}: Dashboard -> {response.status_code}")

            client.logout()

        except User.DoesNotExist:
            print(f"   ❌ {username}: Utilisateur non trouvé")

    # 2. Test des URLs principales (sans authentification)
... (tronqué)

# ============================================================
# ORIGINE 3: test_complet_finall.py (2025-12-06)
# ============================================================


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

... (tronqué)

# ============================================================
# ORIGINE 4: test_finall.py (2025-12-06)
# ============================================================


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
... (tronqué)

# ============================================================
# ORIGINE 5: test_mini.py (2025-12-06)
# ============================================================

#!/usr/bin/env python
"""
MINI-SCRIPT DE TEST DES CONNEXIONS
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.utils import get_user_primary_group, get_user_redirect_url

print("🧪 TEST RAPIDE DES CONNEXIONS")
print("=" * 40)

client = Client()

# Test spécial DOUA1
print("\n🔍 TEST SPÉCIAL DOUA1:")
doua1 = User.objects.get(username='DOUA1')
print(f"   Groupes Django: {[g.name for g in doua1.groups.all()]}")
print(f"   get_user_primary_group: {get_user_primary_group(doua1)}")
print(f"   get_user_redirect_url: {get_user_redirect_url(doua1)}")

if client.login(username='DOUA1', password='DOUA1'):
    print("   ✅ Connexion réussie")
    response = client.get('/redirect-after-login/', follow=True)
    final_url = response.request['PATH_INFO']
    print(f"   🎯 URL finale: {final_url}")

    if '/assureur/' in final_url or 'assureur' in final_url:
        print("   ✅ DOUA1 correctement redirigé vers l'espace assureur")
    else:
        print(f"   ❌ PROBLÈME: DOUA1 redirigé vers {final_url}")
else:
    print("   ❌ Échec de connexion")

# Test rapide de tous les utilisateurs
print("\n🔍 TEST DE TOUS LES UTILISATEURS:")
tests = [
    ("DOUA", "DOUA", "/assureur/"),
    ("ktanos", "ktanos", "/assureur/"),
    ("ORNELLA", "ORNELLA", "/agents/tableau-de-bord/"),
    ("Yacouba", "Yacouba", "/medecin/dashboard/"),
    ("GLORIA", "GLORIA", "/pharmacien/dashboard/"),
    ("ASIA", "ASIA", "/membres/dashboard/"),
... (tronqué)

# ============================================================
# ORIGINE 6: test_connexions.py (2025-12-06)
# ============================================================

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
... (tronqué)

# ============================================================
# ORIGINE 7: test_final_connexions.py (2025-12-06)
# ============================================================


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
... (tronqué)

# ============================================================
# ORIGINE 8: test_creation_cotisation.py (2025-12-04)
# ============================================================

# test_creation_cotisation.py
import os
import sys
import django
from datetime import datetime, timedelta

# Configuration Django
sys.path.append('/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from assureur.models import Cotisation
from membres.models import Membre
from decimal import Decimal
import json

class TestCreationCotisation(TestCase):
    """Tests complets pour la création de cotisations"""

    def setUp(self):
        """Configuration initiale pour les tests"""
        print("🧪 Configuration des tests...")

        # Créer un utilisateur assureur
        self.assureur_user = User.objects.create_user(
            username='test_assureur',
            email='assureur@test.com',
            password='test123'
        )

        # Créer un membre pour les tests
        self.membre = Membre.objects.create(
            nom="Test",
            prenom="Membre",
            numero_unique="MEMTEST001",
            email="membre@test.com",
            telephone="0123456789",
            statut="actif"
        )

        # Client de test
        self.client = Client()

        print(f"✅ Utilisateur créé: {self.assureur_user.username}")
        print(f"✅ Membre créé: {self.membre.prenom} {self.membre.nom}")

    def test_creation_cotisation_api(self):
... (tronqué)

# ============================================================
# ORIGINE 9: test_api_avec_login.py (2025-12-04)
# ============================================================

# test_api_avec_login.py
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:8000"

def login_and_test():
    """Se connecte puis teste l'API"""

    session = requests.Session()

    # 1. Obtenir la page de login et le CSRF token
    print("1. Obtention du CSRF token...")
    login_url = BASE_URL + "/accounts/login/"
    response = session.get(login_url)

    # Parser le HTML pour trouver le CSRF token
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = None

    csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    if csrf_input:
        csrf_token = csrf_input.get('value')

    if not csrf_token:
        print("   ❌ CSRF token non trouvé")
        return

    print(f"   ✅ CSRF token trouvé: {csrf_token[:20]}...")

    # 2. Se connecter (remplacer avec vos identifiants)
    print("\n2. Connexion...")
    login_data = {
        'username': 'test_assureur',  # À remplacer
        'password': 'password123',    # À remplacer
        'csrfmiddlewaretoken': csrf_token
    }

    response = session.post(login_url, data=login_data)

    if response.status_code == 200 and "dashboard" in response.url:
        print("   ✅ Connexion réussie")
    else:
        print(f"   ❌ Échec de connexion: Status {response.status_code}")
        print(f"   URL après login: {response.url}")
        # Afficher la page pour voir l'erreur
        print(f"   Page: {response.text[:500]}")
        return

    # 3. Tester l'envoi de message
... (tronqué)

# ============================================================
# ORIGINE 10: test_api_debug.py (2025-12-04)
# ============================================================

# test_api_debug.py
import requests

def test_api_sans_auth():
    """Test sans authentification pour voir ce que l'API retourne"""
    url = "http://localhost:8000/api/messages/envoyer/"

    # Test GET pour voir la réponse
    print("🔍 Test GET (pour voir si l'API existe):")
    response = requests.get(url)
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type')}")
    print(f"   Premiers 200 caractères: {response.text[:200]}")

    # Test POST vide
    print("\n🔍 Test POST vide:")
    response = requests.post(url, data={})
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type')}")
    print(f"   Réponse complète:\n{response.text}")

if __name__ == "__main__":
    test_api_sans_auth()

# ============================================================
# ORIGINE 11: test_communication.py (2025-12-04)
# ============================================================

#!/usr/bin/env python3
"""
SCRIPT DE TEST - Communication Assureur
Teste les URLs et templates de communication
"""

import requests
import sys

BASE_URL = "http://localhost:8000"

def test_url(url, expected_status=200):
    """Teste une URL"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == expected_status:
            print(f"✅ {url} - {response.status_code}")
            return True
        else:
            print(f"❌ {url} - {response.status_code} (attendu: {expected_status})")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {url} - Serveur non disponible")
        return False
    except Exception as e:
        print(f"❌ {url} - Erreur: {e}")
        return False

print("🔧 TEST DES URLS DE COMMUNICATION")
print("="*60)

# URLs à tester
urls_to_test = [
    f"{BASE_URL}/assureur/communication/",
    f"{BASE_URL}/assureur/communication/envoyer/",
    f"{BASE_URL}/communication/messagerie/",
    f"{BASE_URL}/communication/notifications/",
    f"{BASE_URL}/assureur/",
    f"{BASE_URL}/assureur/membres/",
]

success_count = 0
for url in urls_to_test:
    if test_url(url):
        success_count += 1

print("
" + "="*60)
print(f"📊 RÉSULTATS: {success_count}/{len(urls_to_test)} URLs fonctionnent")

... (tronqué)

# ============================================================
# ORIGINE 12: test_communication_urls.py (2025-12-04)
# ============================================================

"""
URLs de test pour la communication assureur
À intégrer dans votre fichier assureur/urls.py
"""

from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # Page de messagerie
    path('communication/',
         TemplateView.as_view(template_name='assureur/communication/messagerie.html'),
         name='messagerie_assureur'),

    # Page d'envoi de message
    path('communication/envoyer/',
         TemplateView.as_view(template_name='assureur/communication/envoyer_message.html'),
         name='envoyer_message_assureur'),

    # Page de liste des messages
    path('communication/messages/',
         TemplateView.as_view(template_name='assureur/communication/liste_messages.html'),
         name='liste_messages_assureur'),

    # Page de notifications
    path('communication/notifications/',
         TemplateView.as_view(template_name='assureur/communication/liste_notifications.html'),
         name='liste_notifications_assureur'),
]

# ============================================================
# ORIGINE 13: test_recherche_live.py (2025-12-04)
# ============================================================

# test_recherche_live.py
import requests

# Test avec session pour gérer l'authentification
session = requests.Session()

# URL de connexion (à adapter si nécessaire)
login_url = "http://127.0.0.1:8000/accounts/login/"
search_url = "http://127.0.0.1:8000/assureur/membres/?q=ASIA"

print("🔍 TEST DE RECHERCHE EN DIRECT")
print("="*50)

# Si vous avez besoin de vous connecter (remplacez par vos identifiants)
credentials = {
    'username': 'DOUA',  # ou l'utilisateur que vous voyez dans les logs
    'password': 'votre_mot_de_passe'  # à remplacer
}

try:
    print("1. Tentative de connexion...")
    # Récupérer le token CSRF
    login_page = session.get(login_url)

    # Si vous avez besoin d'authentification, décommentez :
    # from bs4 import BeautifulSoup
    # soup = BeautifulSoup(login_page.text, 'html.parser')
    # csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    # credentials['csrfmiddlewaretoken'] = csrf_token
    # response = session.post(login_url, data=credentials)
    # print(f"   Status login: {response.status_code}")

    print("\n2. Test de recherche 'ASIA'...")
    response = session.get(search_url)

    print(f"   Status: {response.status_code}")
    print(f"   Taille: {len(response.text)} caractères")

    if response.status_code == 200:
        # Analyse rapide du contenu
        content = response.text

        # Vérifications
        checks = [
            ('ASIA', 'Terme recherché'),
            ('DRAMANE', 'Membre 1'),
            ('Koné', 'Membre 2'),
            ('numero_unique', 'Champ numéro'),
            ('date_inscription', 'Champ date'),
            ('2 résultat', 'Nombre de résultats'),
... (tronqué)

# ============================================================
# ORIGINE 14: test_ultra_simple.py (2025-12-04)
# ============================================================

# test_ultra_simple.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

print("🔍 TEST ULTRA SIMPLE")
print("="*50)

# Vérification la plus basique
from agents.models import Membre
from django.db.models import Q

# Recherche dans la base
asia_count = Membre.objects.filter(
    Q(nom__icontains='ASIA') | Q(prenom__icontains='ASIA')
).count()

print(f"✅ Recherche 'ASIA' en base : {asia_count} résultat(s)")

if asia_count == 2:
    print("✅ CORRECT : DRAMANE ASIA et Koné Asia")

    # Afficher les détails
    membres = Membre.objects.filter(
        Q(nom__icontains='ASIA') | Q(prenom__icontains='ASIA')
    )

    for m in membres:
        print(f"  • {m.id}: {m.prenom} {m.nom} - {m.numero_unique}")
else:
    print(f"❌ ATTENDU : 2 résultats, obtenu : {asia_count}")

print("\n🚀 Pour tester dans le navigateur :")
print("1. python manage.py runserver")
print("2. http://127.0.0.1:8000/assureur/membres/?q=ASIA")
print("="*50)

# ============================================================
# ORIGINE 15: test_simple2.py (2025-12-04)
# ============================================================

# test_simple.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("🔍 TEST SIMPLIFIÉ")
print("="*50)

# 1. Vérifier le template
import os
template_path = 'templates/assureur/liste_membres.html'
if os.path.exists(template_path):
    print(f"✅ Template trouvé: {template_path}")

    with open(template_path, 'r') as f:
        content = f.read()

    if 'numero_unique' in content:
        print("✅ Template utilise 'numero_unique'")
    else:
        print("❌ Template n'utilise PAS 'numero_unique'")

    if 'date_inscription' in content:
        print("✅ Template utilise 'date_inscription'")
    else:
        print("❌ Template n'utilise PAS 'date_inscription'")
else:
    print(f"❌ Template non trouvé: {template_path}")

# 2. Vérifier la vue
try:
    from assureur import views
    print("\n✅ Module assureur.views importé")

    # Vérifier la fonction liste_membres
    if hasattr(views, 'liste_membres'):
        print("✅ Fonction liste_membres() existe")
    else:
        print("❌ Fonction liste_membres() n'existe pas")

except Exception as e:
    print(f"❌ Erreur import: {e}")

# 3. Vérifier les URLs
try:
    from django.urls import reverse
    print("\n🔗 Test des URLs:")

    urls_to_test = [
... (tronqué)

# ============================================================
# ORIGINE 16: test_avec_authentification.py (2025-12-04)
# ============================================================

# test_avec_authentification.py
import os
import django
from django.test import RequestFactory
from django.contrib.auth.models import User, Group

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur import views

print("🧪 TEST AVEC AUTHENTIFICATION")
print("="*50)

# Créer un utilisateur test
try:
    user, created = User.objects.get_or_create(
        username='test_assureur',
        defaults={'email': 'test@assureur.com', 'password': 'test123'}
    )

    # Ajouter au groupe assureur
    assureur_group, _ = Group.objects.get_or_create(name='assureur')
    user.groups.add(assureur_group)
    user.is_staff = True
    user.save()

    print(f"✅ Utilisateur créé: {user.username}")

except Exception as e:
    print(f"⚠️  Erreur création utilisateur: {e}")
    # Utiliser un utilisateur existant
    user = User.objects.filter(groups__name='assureur').first()
    if user:
        print(f"✅ Utilisation de l'utilisateur existant: {user.username}")
    else:
        user = User.objects.filter(is_superuser=True).first()
        if user:
            print(f"✅ Utilisation du superuser: {user.username}")

# Tester la vue
factory = RequestFactory()

print("\n🔍 Test 1: Requête sans filtre")
request = factory.get('/assureur/membres/')
request.user = user

try:
    response = views.liste_membres(request)
    print("✅ Vue exécutée sans erreur")
... (tronqué)

# ============================================================
# ORIGINE 17: test_rapide3.py (2025-12-04)
# ============================================================

# test_rapide.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Membre
from django.db.models import Q

print("🔍 TEST RAPIDE DE LA RECHERCHE")
print("="*50)

# 1. Compter les données
print(f"Total membres: {Membre.objects.count()}")

# 2. Tester différentes recherches
test_cases = [
    ('ASIA', 'nom/prénom'),
    ('Jean', 'nom/prénom'),
    ('Dupont', 'nom'),
    ('test', 'email'),
    ('MEM', 'numéro'),
    ('@', 'tous les emails'),
]

for term, description in test_cases:
    count = Membre.objects.filter(
        Q(nom__icontains=term) |
        Q(prenom__icontains=term) |
        Q(email__icontains=term) |
        Q(numero_unique__icontains=term) |
        Q(telephone__icontains=term)
    ).count()

    print(f"• '{term}' ({description}): {count} résultat(s)")

# 3. Afficher quelques exemples
print("\n📋 EXEMPLES DE DONNÉES:")
for m in Membre.objects.all()[:3]:
    print(f"  • {m.prenom} {m.nom} - {m.numero_unique} - {m.email}")

# 4. Vérifier les champs critiques
print("\n✅ VÉRIFICATION DES CHAMPS:")
sample = Membre.objects.first()
if sample:
    fields = ['numero_unique', 'date_inscription', 'statut', 'nom', 'prenom']
    for field in fields:
        exists = hasattr(sample, field)
        value = getattr(sample, field, 'N/A')
        status = "✓" if exists else "✗"
... (tronqué)

# ============================================================
# ORIGINE 18: test_vue_membres.py (2025-12-04)
# ============================================================

# test_vue_membres.py
import os
import sys
import django
from django.test import RequestFactory

# Configuration Django
projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("="*70)
print("🧪 TEST DIRECT DE LA VUE liste_membres")
print("="*70)

# Créer une requête simulée
factory = RequestFactory()

# Créer un utilisateur de test
from django.contrib.auth.models import User
user = User.objects.create_user(username='testuser', password='testpass')

try:
    # Importer la vue
    from assureur.views import liste_membres

    print("✅ Vue importée avec succès")

    # Tester différentes requêtes
    tests = [
        ("Sans filtres", {}),
        ("Recherche 'ASIA'", {'q': 'ASIA'}),
        ("Filtre statut 'actif'", {'statut': 'actif'}),
        ("Combinaison", {'q': 'Jean', 'statut': 'en_retard'}),
    ]

    for test_name, params in tests:
        print(f"\n🔍 Test: {test_name}")
        print(f"   Paramètres: {params}")

        # Créer la requête
        request = factory.get('/assureur/membres/', params)
        request.user = user

        # Ajouter la session
        from django.contrib.sessions.middleware import SessionMiddleware
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
... (tronqué)

# ============================================================
# ORIGINE 19: test_recherche_membres.py (2025-12-03)
# ============================================================

# test_recherche_membres.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre
from django.db.models import Q

print("="*70)
print("🔍 TEST DE LA RECHERCHE SUR LE MODÈLE ASSUREUR")
print("="*70)

# Vérifier combien de membres existent
total = Membre.objects.count()
print(f"Total membres dans assureur.models.Membre: {total}")

# Tester la recherche "ASIA" comme dans l'URL
search_term = "ASIA"
print(f"\n🔍 Recherche pour le terme: '{search_term}'")

results = Membre.objects.filter(
    Q(nom__icontains=search_term) |
    Q(prenom__icontains=search_term) |
    Q(numero_membre__icontains=search_term) |
    Q(email__icontains=search_term) |
    Q(telephone__icontains=search_term)
)

print(f"Nombre de résultats: {results.count()}")

if results.count() > 0:
    print("\n📋 Résultats trouvés:")
    for membre in results:
        print(f"  • {membre.id}: {membre.nom} {membre.prenom}")
        print(f"    - Email: {membre.email}")
        print(f"    - Téléphone: {membre.telephone}")
        print(f"    - Numéro membre: {membre.numero_membre}")
        print(f"    - Statut: {membre.statut}")
else:
    print("\n❌ Aucun résultat trouvé")
    print("\n📋 Tous les membres (pour debug):")
    for membre in Membre.objects.all()[:5]:
        print(f"  • {membre.id}: {membre.nom} {membre.prenom}")

... (tronqué)

# ============================================================
# ORIGINE 20: test_membres_direct.py (2025-12-03)
# ============================================================

# test_membres_direct.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Membre
from django.db.models import Q

print("="*70)
print("🔍 TEST DIRECT DE LA RECHERCHE DE MEMBRES")
print("="*70)

# Test 1: Tous les membres
print("\n1. Tous les membres:")
membres = Membre.objects.all()
print(f"   Total: {membres.count()}")
for m in membres[:3]:  # Afficher 3 premiers
    print(f"   - {m.nom} {m.prenom} ({m.statut})")

# Test 2: Recherche par nom
print("\n2. Recherche 'Bernard':")
results = Membre.objects.filter(
    Q(nom__icontains='Bernard') |
    Q(prenom__icontains='Bernard')
)
print(f"   Résultats: {results.count()}")
for m in results:
    print(f"   - {m.nom} {m.prenom}")

# Test 3: Filtre par statut
print("\n3. Membres avec statut 'actif':")
actifs = Membre.objects.filter(statut='actif')
print(f"   Total actifs: {actifs.count()}")
for m in actifs[:3]:
    print(f"   - {m.nom} {m.prenom}")

# Test 4: Combinaison recherche + filtre
print("\n4. Recherche 'Jean' avec statut 'en_retard':")
results = Membre.objects.filter(
    Q(nom__icontains='Jean') | Q(prenom__icontains='Jean'),
    statut='en_retard'
)
print(f"   Résultats: {results.count()}")
for m in results:
... (tronqué)

# ============================================================
# ORIGINE 21: test_membres_view.py (2025-12-03)
# ============================================================

# test_membres_view.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import RequestFactory
from assureur.views import liste_membres
from django.contrib.auth.models import User

# Créer une requête simulée
factory = RequestFactory()

# Créer un utilisateur de test
user = User.objects.create_user(username='testuser', password='testpass')
user.save()

# Créer une requête GET avec des paramètres
request = factory.get('/assureur/membres/', {'q': 'test', 'statut': 'actif'})
request.user = user

# Exécuter la vue
try:
    response = liste_membres(request)
    print("✅ Vue exécutée avec succès")
    print(f"Status code: {response.status_code}")

    # Vérifier le contexte
    if hasattr(response, 'context_data'):
        print(f"Nombre de membres: {len(response.context_data.get('page_obj', []))}")
        print(f"Filtres appliqués: {response.context_data.get('filters', {})}")
    else:
        print("Aucun contexte retourné")

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

# ============================================================
# ORIGINE 22: test_complet_agents.py (2025-12-03)
# ============================================================

# test_complet_agents.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User, Group

print("="*70)
print("🧪 TEST COMPLET DES FONCTIONNALITÉS AGENTS")
print("="*70)

# 1. Créer un utilisateur agent
agent_user, created = User.objects.get_or_create(
    username='agent_complet_test',
    defaults={'email': 'agent_complet@test.com'}
)

if created:
    agent_user.set_password('agent123')
    agent_user.save()
    print("✅ Utilisateur agent_complet_test créé")
else:
    print("✅ Utilisateur agent_complet_test existant")
    agent_user.set_password('agent123')
    agent_user.save()

# 2. Ajouter au groupe Agents
groupe_agents, _ = Group.objects.get_or_create(name='Agents')
agent_user.groups.add(groupe_agents)
print("✅ Ajouté au groupe Agents")

# 3. Tester les URLs
client = Client()
login_success = client.login(username='agent_complet_test', password='agent123')
print(f"🔐 Connexion: {'✅ Réussie' if login_success else '❌ Échec'}")

if not login_success:
    print("❌ Impossible de continuer sans connexion")
    exit()

# 4. Test des URLs agents
urls_agents = [
    # Dashboard et membres
... (tronqué)

# ============================================================
# ORIGINE 23: test_acces_agent.py (2025-12-03)
# ============================================================

# test_acces_agent.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client, TestCase
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from assureur.models import Cotisation, Membre

print("="*70)
print("🧪 TEST PRATIQUE - ACCÈS AGENT")
print("="*70)

# 1. Créer ou récupérer un groupe Agents
groupe_agents, created = Group.objects.get_or_create(name='Agents')
print(f"Groupe Agents: {'✅ Créé' if created else '✅ Existant'}")

# 2. Donner des permissions au groupe
cotisation_ct = ContentType.objects.get_for_model(Cotisation)
membre_ct = ContentType.objects.get_for_model(Membre)

# Permissions de base pour les cotisations
permissions_cotisation = Permission.objects.filter(
    content_type=cotisation_ct,
    codename__in=['view_cotisation', 'change_cotisation']
)

# Permissions de base pour les membres
permissions_membre = Permission.objects.filter(
    content_type=membre_ct,
    codename__in=['view_membre', 'change_membre']
)

# Ajouter les permissions au groupe
groupe_agents.permissions.add(*permissions_cotisation)
groupe_agents.permissions.add(*permissions_membre)

print(f"\n🔐 Permissions ajoutées au groupe Agents:")
for perm in groupe_agents.permissions.all():
    print(f"   - {perm.codename} ({perm.content_type.model})")

# 3. Créer un utilisateur agent
agent_user, created = User.objects.get_or_create(
... (tronqué)

# ============================================================
# ORIGINE 24: test_nouvelle_periode.py (2025-12-03)
# ============================================================

# test_nouvelle_periode.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
import re

print("="*60)
print("TEST NOUVELLE PÉRIODE - 2025-04")
print("="*60)

# Connexion
client = Client()
client.login(username='admin', password='admin123')
print("✅ Connexion réussie")

# Récupérer CSRF
response = client.get('/assureur/cotisations/generer/')
content = response.content.decode('utf-8')
csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)
csrf_token = csrf_match.group(1)
print("✅ Token CSRF obtenu")

# Tester prévisualisation pour nouvelle période
print("\n📋 Prévisualisation pour 2025-04...")
response = client.get('/assureur/cotisations/preview/?periode=2025-04')
print(f"Status: {response.status_code}")

# Tester génération
print("\n🚀 Génération pour 2025-04...")
from assureur.models import Cotisation

# Compter avant
avant = Cotisation.objects.count()
print(f"Cotisations avant: {avant}")

# Générer pour nouvelle période
response = client.post('/assureur/cotisations/generer/', {
    'periode': '2025-04',
    'csrfmiddlewaretoken': csrf_token
})

... (tronqué)

# ============================================================
# ORIGINE 25: test_generation_simple.py (2025-12-03)
# ============================================================

# test_generation_simple.py
import os
import django
import sys

# Configuration Django
projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

print("="*60)
print("TEST SIMPLIFIÉ - GÉNÉRATION DE COTISATIONS")
print("="*60)

# 1. Utiliser l'utilisateur existant (éviter les erreurs de création)
try:
    user = User.objects.get(username='admin')
    print(f"✅ Utilisation de l'utilisateur existant: {user.username}")
except:
    print("❌ Aucun utilisateur admin trouvé")
    exit(1)

# 2. Connexion
client = Client()
client.login(username='admin', password='admin123')
print("✅ Connexion réussie")

# 3. Récupérer la page génération
print("\n1. Accès page génération...")
response = client.get('/assureur/cotisations/generer/')
print(f"   Status: {response.status_code} - {'✅ OK' if response.status_code == 200 else '❌ Échec'}")

# 4. Extraire CSRF token
import re
content = response.content.decode('utf-8')
csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)

if not csrf_match:
    print("❌ Token CSRF non trouvé")
    exit(1)

csrf_token = csrf_match.group(1)
print(f"✅ Token CSRF obtenu")

# 5. Tester la prévisualisation
... (tronqué)

# ============================================================
# ORIGINE 26: test_sans_erreurs.py (2025-12-03)
# ============================================================

# test_sans_erreurs.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

# Désactiver temporairement le signal problématique
from django.db.models import signals
from django.contrib.auth.models import User
from assureur.models import creer_profil_assureur
from medecin.models import creer_profil_medecin
from pharmacien.models import creer_profil_pharmacien

# Désactiver les signaux
signals.post_save.disconnect(creer_profil_assureur, sender=User)
signals.post_save.disconnect(creer_profil_medecin, sender=User)
signals.post_save.disconnect(creer_profil_pharmacien, sender=User)

# Maintenant exécutez votre test
from django.test import Client

client = Client()
client.login(username='admin', password='admin123')

# ... le reste de votre test ...

# ============================================================
# ORIGINE 27: test_generation_complet.py (2025-12-03)
# ============================================================

# test_generation_complet.py
import os
import django
import sys
import re

# Configuration Django
projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

print("=== TEST COMPLET DE GÉNÉRATION ===")
print(f"Chemin: {projet_path}")

# 1. Création utilisateur de test
try:
    # Supprimer l'utilisateur test s'il existe
    User.objects.filter(username='test_gen').delete()

    user = User.objects.create_superuser(
        username='test_gen',
        email='test@generation.com',
        password='test123'
    )
    print("✅ Utilisateur de test créé")
except Exception as e:
    print(f"⚠ Erreur création: {e}")
    user = User.objects.get(username='admin')
    print("✅ Utilisation de l'admin existant")

# 2. Connexion
client = Client()
login = client.login(username=user.username, password='test123' if user.username == 'test_gen' else 'admin123')
print(f"Connexion: {'✅ Réussie' if login else '❌ Échec'}")

if not login:
    exit(1)

# 3. Test GET de la page génération
print(f"\n{'='*50}")
print("1. Récupération de la page génération")
response = client.get('/assureur/cotisations/generer/')
print(f"Status: {response.status_code}")

if response.status_code != 200:
... (tronqué)

# ============================================================
# ORIGINE 28: test_avec_messages.py (2025-12-03)
# ============================================================

# test_avec_messages.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import TestCase
from django.contrib.auth.models import User

class TestGenerationCotisations(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_page_generation(self):
        """Test de la page de génération"""
        response = self.client.get('/assureur/cotisations/generer/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'periode')
        print("✅ Test page génération: PASSÉ")

    def test_preview(self):
        """Test de la prévisualisation"""
        response = self.client.get('/assureur/cotisations/preview/?periode=2025-03')
        self.assertEqual(response.status_code, 200)
        print("✅ Test prévisualisation: PASSÉ")

    def test_generation_post(self):
        """Test de la génération par POST"""
        # D'abord GET pour obtenir le CSRF token
        response = self.client.get('/assureur/cotisations/generer/')
        csrf_token = self._extract_csrf(response.content.decode('utf-8'))

        # Ensuite POST
        response = self.client.post('/assureur/cotisations/generer/', {
            'periode': '2025-03',
            'csrfmiddlewaretoken': csrf_token
        })

        # La réponse devrait être 302 (redirection) ou 200 avec succès
... (tronqué)

# ============================================================
# ORIGINE 29: test_simple1.py (2025-12-03)
# ============================================================

# test_simple.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
try:
    django.setup()
    print("✅ Django configuré avec succès")

    from django.conf import settings
    print(f"✅ INSTALLED_APPS: {settings.INSTALLED_APPS[:3]}...")

except Exception as e:
    print(f"❌ Erreur: {e}")

# ============================================================
# ORIGINE 30: test_without_server.py (2025-12-03)
# ============================================================

# test_without_server.py
import os
import django
import sys

# Ajoutez le chemin du projet à sys.path
projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

# Configurez Django AVANT d'importer quoi que ce soit
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

# MAINTENANT vous pouvez importer les modèles Django
from django.test import Client
from django.contrib.auth.models import User

print("=== TEST SANS SERVEUR (Client Django) ===")

# 1. Créer un superutilisateur de test
try:
    user = User.objects.create_superuser(
        username='admin',
        email='admin@test.com',
        password='admin123'
    )
    print("✅ Superutilisateur créé")
except Exception as e:
    try:
        user = User.objects.get(username='admin')
        print("✅ Superutilisateur existant")
    except Exception:
        print(f"❌ Erreur avec l'utilisateur: {e}")
        user = None

# 2. Tester avec le client Django
client = Client()

# 2.1. Se connecter
if user:
    login = client.login(username='admin', password='admin123')
    print(f"Connexion: {'✅ Réussie' if login else '❌ Échec'}")
else:
    print("❌ Impossible de se connecter - pas d'utilisateur")
    login = False

# 2.2. Tester la page de génération
if login:
    response = client.get('/assureur/cotisations/generer/')
    print(f"\n1. Page génération - Status: {response.status_code}")
... (tronqué)

# ============================================================
# ORIGINE 31: test_generation_web.py (2025-12-03)
# ============================================================

# test_generation_web.py
import os
import django
import requests
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("=== TEST DE GÉNÉRATION VIA WEB ===")

# Créer une session
session = requests.Session()

# 1. Se connecter
login_url = 'http://127.0.0.1:8000/accounts/login/'
response = session.get(login_url)

if response.status_code != 200:
    print(f"❌ Impossible d'accéder à la page de login: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})

if not csrf_token:
    print("❌ Token CSRF non trouvé")
    # Essayer de trouver dans une autre balise
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    if not csrf_token:
        print("❌ Aucun token CSRF trouvé")
        exit()

csrf_token = csrf_token['value']

# Données de connexion
login_data = {
    'username': 'admin',  # Remplacez par vos identifiants
    'password': 'admin123',  # Remplacez par votre mot de passe
    'csrfmiddlewaretoken': csrf_token
}

response = session.post(login_url, data=login_data, allow_redirects=True)

if 'login' in response.url:
    print("❌ Échec de la connexion - redirigé vers login")
    print(f"Contenu: {response.text[:500]}")
    exit()
else:
    print("✅ Connexion réussie")
... (tronqué)

# ============================================================
# ORIGINE 32: test_web_interface.py (2025-12-03)
# ============================================================

# test_web_interface.py
import os
import django
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("=== TEST DE L'INTERFACE WEB ===")

# Option 1: Test avec Selenium (si vous l'avez installé)
try:
    # Configuration du navigateur
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Mode sans interface
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    # Aller à la page de connexion
    driver.get('http://127.0.0.1:8000/accounts/login/')

    # Se connecter (remplacez par vos identifiants)
    username = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')

    username.send_keys('admin')  # Remplacez par votre username
    password.send_keys('admin123')  # Remplacez par votre password

    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Attendre la redirection
    time.sleep(2)

    # Aller à la page de génération des cotisations
    driver.get('http://127.0.0.1:8000/assureur/cotisations/generer/')

    # Vérifier que la page charge
    wait = WebDriverWait(driver, 10)
    try:
        title = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        print(f"✅ Page chargée: {title.text}")

        # Vérifier les statistiques
... (tronqué)

# ============================================================
# ORIGINE 33: test_date_conversion.py (2025-12-03)
# ============================================================

# Créez un fichier de test

import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def normaliser_periode(periode_input):
    """Même fonction que ci-dessus"""
    if not periode_input:
        return datetime.now().strftime('%Y-%m')

    if '-' in periode_input and len(periode_input) == 7:
        try:
            datetime.strptime(periode_input, '%Y-%m')
            return periode_input
        except:
            pass

    if '/' in periode_input:
        try:
            if len(periode_input.split('/')) == 3:
                date_obj = datetime.strptime(periode_input, '%d/%m/%Y')
                return date_obj.strftime('%Y-%m')
            elif len(periode_input.split('/')) == 2:
                date_obj = datetime.strptime(periode_input, '%m/%Y')
                return date_obj.strftime('%Y-%m')
        except:
            pass

    if '-' in periode_input and len(periode_input.split('-')) == 2:
        try:
            date_obj = datetime.strptime(periode_input, '%m-%Y')
            return date_obj.strftime('%Y-%m')
        except:
            pass

    return datetime.now().strftime('%Y-%m')

# Tests
test_cases = [
    '2025-12',
    '01/12/2025',
    '12/2025',
    '12-2025',
    'invalid',
    '',
    '2025/12',
... (tronqué)

# ============================================================
# ORIGINE 34: test_final_integration1.py (2025-12-03)
# ============================================================

# test_final_integration.py
import os
import django
import requests
from django.test import Client
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("=== TEST D'INTÉGRATION FINAL ===")

# 1. Vérifier les données
from assureur.models import Membre, Cotisation
print("1. Données dans la base :")
print(f"   - Membres actifs: {Membre.objects.filter(statut='actif').count()}")
print(f"   - Cotisations totales: {Cotisation.objects.count()}")

# 2. Créer un superutilisateur pour les tests
try:
    user = User.objects.create_user(
        username='test_admin',
        password='test123',
        is_staff=True,
        is_superuser=True
    )
    print("2. Utilisateur de test créé")
except:
    user = User.objects.get(username='test_admin')
    print("2. Utilisateur de test existe déjà")

# 3. Tester avec le client Django
client = Client()
login = client.login(username='test_admin', password='test123')
print(f"3. Connexion réussie: {login}")

# 4. Tester la page de génération
response = client.get('/assureur/cotisations/generer/')
print(f"4. Page génération - Status: {response.status_code}")

if response.status_code == 200:
    print("   ✓ Page accessible")
    # Vérifier le contenu
    if b'Générer les Cotisations' in response.content:
        print("   ✓ Titre présent")
    if b'periode' in response.content:
        print("   ✓ Champ période présent")
else:
    print(f"   ✗ Erreur: {response.status_code}")
    print(f"   Contenu: {response.content[:500]}...")
... (tronqué)

# ============================================================
# ORIGINE 35: test_cotisation_creation.py (2025-12-03)
# ============================================================

# test_cotisation_creation.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre, Cotisation
from datetime import datetime

print("=== TEST CRÉATION COTISATIONS ===")

# Vérifier les membres
membres_actifs = Membre.objects.filter(statut='actif')
print(f"Membres actifs: {membres_actifs.count()}")

# Créer une cotisation test
if membres_actifs.exists():
    membre = membres_actifs.first()
    try:
        # Vérifier si une cotisation existe déjà pour décembre 2024
        cotisation_existante = Cotisation.objects.filter(
            membre=membre,
            periode='2024-12'
        ).exists()

        if not cotisation_existante:
            cotisation = Cotisation.objects.create(
                membre=membre,
                periode='2024-12',
                montant=10000.00,
                statut='en_attente',
                date_emission=datetime.now().date()
            )
            print(f"✓ Cotisation test créée :")
            print(f"  - Membre: {cotisation.membre.nom} {cotisation.membre.prenom}")
            print(f"  - Période: {cotisation.periode}")
            print(f"  - Montant: {cotisation.montant} FCFA")
            print(f"  - Statut: {cotisation.statut}")
        else:
            print("⚠ Cotisation pour décembre 2024 existe déjà")
    except Exception as e:
        print(f"✗ Erreur création cotisation : {e}")
        import traceback
        traceback.print_exc()
else:
    print("✗ Aucun membre actif trouvé")

print(f"\nTotal cotisations : {Cotisation.objects.count()}")

# ============================================================
# ORIGINE 36: test_preview_view.py (2025-12-03)
# ============================================================

# test_preview_view.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import RequestFactory
from assureur.views import preview_generation
from django.contrib.auth.models import User

# Créer une requête simulée
factory = RequestFactory()

# Créer un utilisateur de test (simplifié)
user, _ = User.objects.get_or_create(
    username='view_test_user',
    defaults={'is_staff': True}
)
user.set_password('test123')
user.save()

# Tester la vue
try:
    request = factory.get('/preview/', {'periode': '2024-12'})
    request.user = user

    response = preview_generation(request)
    print(f"Status: {response.status_code}")
    print(f"Content type: {response['Content-Type'] if 'Content-Type' in response else 'N/A'}")

except Exception as e:
    print(f"Erreur: {e}")
    import traceback
    traceback.print_exc()

# ============================================================
# ORIGINE 37: test_cotisations.py (2025-12-03)
# ============================================================

# test_cotisations.py
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_preview_generation():
    """Test de l'API de prévisualisation"""
    url = f"{BASE_URL}/assureur/cotisations/preview/"
    params = {"periode": "2024-12"}

    try:
        response = requests.get(url, params=params)
        print(f"Status: {response.status_code}")
        print(f"Contenu: {response.text[:200]}...")

        if response.status_code == 200:
            print("✓ Prévisualisation OK")
        else:
            print("✗ Erreur prévisualisation")
    except Exception as e:
        print(f"✗ Exception: {e}")

def test_generate_cotisations():
    """Test de la génération de cotisations"""
    url = f"{BASE_URL}/assureur/cotisations/generer/"
    data = {
        "periode": "2024-12",
        "csrfmiddlewaretoken": "get_from_browser"
    }

    # Note: Vous devez d'abord vous connecter pour obtenir le token CSRF
    # Ce test nécessite une session authentifiée

    print("Note: Ce test nécessite une session authentifiée")
    print("Testez manuellement via le formulaire web")

def test_list_cotisations():
    """Test de la liste des cotisations"""
    url = f"{BASE_URL}/assureur/cotisations/"

    try:
        response = requests.get(url)
        print(f"Liste cotisations - Status: {response.status_code}")

        if response.status_code == 200:
            print("✓ Liste des cotisations accessible")
        else:
            print("✗ Erreur liste des cotisations")
... (tronqué)

# ============================================================
# ORIGINE 38: test_immediat.py (2025-12-03)
# ============================================================

#!/usr/bin/env python3
"""
TEST IMMÉDIAT - Mutuelle Core
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

print("🔧 TEST IMMÉDIAT DU SYSTÈME")
print("=" * 50)

# Test 1: Vérifier Django
try:
    sys.path.insert(0, str(BASE_DIR))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    import django
    django.setup()
    print("✅ Django configuré")
except Exception as e:
    print(f"❌ Erreur Django: {e}")

# Test 2: Vérifier les modèles
print("\n2. Test des modèles:")
try:
    from soins.models import BonDeSoin
    print(f"   ✅ BonDeSoin: {BonDeSoin.objects.count()} enregistrements")
except ImportError:
    try:
        from soins.models import BonSoin
        print(f"   ✅ BonSoin: {BonSoin.objects.count()} enregistrements")
    except ImportError as e:
        print(f"   ❌ Erreur: {e}")

# Test 3: Vérifier les répertoires
print("\n3. Répertoires:")
dirs = ['media', 'staticfiles', 'logs']
for d in dirs:
    path = BASE_DIR / d
    if path.exists():
        print(f"   ✅ {d}: Existe")
    else:
        print(f"   ⚠️  {d}: Absent (créer avec: mkdir {d})")

# Test 4: Vérifier la base de données
print("\n4. Base de données:")
db_path = BASE_DIR / 'db.sqlite3'
if db_path.exists():
... (tronqué)

# ============================================================
# ORIGINE 39: test_assureur_final.py (2025-12-03)
# ============================================================

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

... (tronqué)

# ============================================================
# ORIGINE 40: test_assureur_login.py (2025-12-02)
# ============================================================

# test_assureur_login.py
import requests
from bs4 import BeautifulSoup

print("🔐 Test de connexion et accès assureur")
print("="*50)

session = requests.Session()

# 1. Obtenir la page de login
login_url = "http://localhost:8000/accounts/login/"
print("1. Accès à la page de login...")
response = session.get(login_url)

if response.status_code == 200:
    # Extraire le token CSRF
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})

    if csrf_token:
        token = csrf_token['value']
        print(f"   ✅ Token CSRF trouvé")

        # 2. Tentative de connexion
        print("\n2. Tentative de connexion avec DOUA...")
        login_data = {
            'username': 'DOUA',
            'password': 'TON_MOT_DE_PASSE',  # Remplace par le vrai mot de passe
            'csrfmiddlewaretoken': token
        }

        login_response = session.post(login_url, data=login_data, allow_redirects=False)

        if login_response.status_code == 302:
            print(f"   ✅ Connexion réussie (redirection)")
            location = login_response.headers.get('Location', '')
            print(f"   📍 Redirection vers: {location}")

            # 3. Test d'accès au dashboard
            print("\n3. Test d'accès au dashboard assureur...")
            urls_to_test = [
                '/assureur/',
                '/assureur/dashboard/',
                '/assureur/membres/',
                '/assureur/bons/',
                '/assureur/statistiques/',
            ]

            for url in urls_to_test:
                full_url = f"http://localhost:8000{url}"
... (tronqué)

# ============================================================
# ORIGINE 41: test_login_assureur.py (2025-12-02)
# ============================================================

# test_login_assureur.py
import requests
from bs4 import BeautifulSoup

print("🔐 Test de connexion pour l'assureur")
print("="*50)

# 1. Obtenir la page de login et le token CSRF
login_url = "http://localhost:8000/accounts/login/"
session = requests.Session()

try:
    # GET pour obtenir le token CSRF
    response = session.get(login_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})

        if csrf_token:
            token = csrf_token.get('value')
            print(f"✅ Token CSRF trouvé")

            # 2. Tentative de login
            login_data = {
                'username': 'assureur_system',
                'password': 'assureur123',  # Mot de passe défini dans le script
                'csrfmiddlewaretoken': token
            }

            login_response = session.post(login_url, data=login_data)

            if login_response.status_code == 200:
                if "Bienvenue" in login_response.text or "Dashboard" in login_response.text:
                    print(f"✅ Connexion réussie !")

                    # 3. Test d'accès au dashboard assureur
                    dashboard_url = "http://localhost:8000/assureur/"
                    dashboard_response = session.get(dashboard_url)

                    print(f"\n📊 Test du dashboard assureur:")
                    print(f"  URL: {dashboard_url}")
                    print(f"  Status: {dashboard_response.status_code}")

                    if dashboard_response.status_code == 200:
                        print(f"  ✅ Dashboard accessible !")
                        print(f"  Titre trouvé: {'Dashboard' in dashboard_response.text}")
                    elif dashboard_response.status_code == 302:
                        print(f"  🔄 Redirection détectée")
                        print(f"  Location: {dashboard_response.headers.get('Location')}")
... (tronqué)

# ============================================================
# ORIGINE 42: test_access_assureur.1py (2025-12-02)
# ============================================================

# test_access_assureur.py
import requests

# Test d'accès aux pages assureur sans authentification
print("🌐 Test d'accès aux pages assureur")
print("="*50)

endpoints = [
    "/assureur/dashboard/",
    "/assureur/liste_membres/",
    "/assureur/liste_bons/",
    "/assureur/statistiques/",
    "/assureur/communication/",
]

for endpoint in endpoints:
    url = f"http://localhost:8000{endpoint}"
    print(f"\nTesting: {endpoint}")
    try:
        response = requests.get(url, allow_redirects=False)
        print(f"  Status: {response.status_code}")
        if response.status_code == 302:
            print(f"  🔒 Redirection vers: {response.headers.get('Location')}")
        elif response.status_code == 200:
            print(f"  ✅ Accessible")
        else:
            print(f"  ❓ Code: {response.status_code}")
    except Exception as e:
        print(f"  💥 Error: {e}")

# ============================================================
# ORIGINE 43: test_permissions1.py (2025-12-02)
# ============================================================

# test_permissions.py
import os
import django
import sys

sys.path.append('/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

print("🔐 Vérification des permissions assureur")
print("="*50)

# Chercher le groupe assureur
try:
    assureur_group = Group.objects.get(name='assureur')
    print(f"✅ Groupe 'assureur' trouvé")
    print(f"   Membres: {[u.username for u in assureur_group.user_set.all()]}")
    print(f"   Permissions: {assureur_group.permissions.count()}")
except Group.DoesNotExist:
    print("❌ Groupe 'assureur' non trouvé")

# Vérifier les permissions de l'utilisateur assureur_system
try:
    user = User.objects.get(username='assureur_system')
    print(f"\n👤 Utilisateur: {user.username}")
    print(f"   Groupes: {[g.name for g in user.groups.all()]}")
    print(f"   Permissions: {user.user_permissions.count()}")
    print(f"   Toutes permissions: {user.get_all_permissions()}")
except User.DoesNotExist:
    print("❌ Utilisateur assureur_system non trouvé")

# ============================================================
# ORIGINE 44: test_assureur_models.py (2025-12-02)
# ============================================================

# test_assureur_models.py
import os
import django
import sys

# Configuration Django
sys.path.append('/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import *
from django.contrib.auth.models import User

print("🔍 Diagnostic des modèles assureur")
print("="*50)

# Vérifier les modèles existants
try:
    # Liste tous les modèles de l'application assureur
    from django.apps import apps
    assureur_app = apps.get_app_config('assureur')
    print(f"📊 Modèles dans l'app 'assureur':")
    for model in assureur_app.get_models():
        print(f"  ✅ {model.__name__}: {model._meta.db_table}")
        print(f"     Champs: {[f.name for f in model._meta.fields]}")
except Exception as e:
    print(f"  ❌ Erreur: {e}")

print("\n👥 Vérification des utilisateurs assureur:")
try:
    assureurs = User.objects.filter(username__icontains='assureur')
    for user in assureurs:
        print(f"  - {user.id}: {user.username} ({user.email})")
except Exception as e:
    print(f"  ❌ Erreur: {e}")

# ============================================================
# ORIGINE 45: test_final1.py (2025-12-02)
# ============================================================

# test_final.py
import requests
import json

# Crée une session
session = requests.Session()

# Simule une connexion Django
login_url = "http://localhost:8000/admin/login/"
response = session.get(login_url)
csrf_token = None

# Essaye de te connecter (remplace avec tes vraies infos)
login_data = {
    'username': 'Almoravide',
    'password': 'ton_mot_de_passe',
    'csrfmiddlewaretoken': csrf_token
}

# Teste l'API de conversations après login
api_url = "http://localhost:8000/communication/api/simple/conversations/8/messages/"
response = session.get(api_url)

print(f"Status: {response.status_code}")
if response.text:
    print(f"Response: {response.text[:1000]}")
else:
    print("Empty response")

# ============================================================
# ORIGINE 46: test_with_session.py (2025-12-02)
# ============================================================

# test_with_session.py
from django.test import Client

client = Client()
client.login(username='Almoravide', password='ton_mot_de_passe')

response = client.get('/communication/api/simple/conversations/8/messages/')
print(f"Status: {response.status_code}")
print(f"Content: {response.content[:500]}")

# ============================================================
# ORIGINE 47: test_with_auth.py (2025-12-02)
# ============================================================

# test_with_auth.py
import requests
from requests.auth import HTTPBasicAuth

url = "http://localhost:8000/communication/api/simple/conversations/8/messages/"

# Essayer avec authentification basique
response = requests.get(url, auth=HTTPBasicAuth('Almoravide', 'ton_mot_de_passe'))
print(f"Status avec auth: {response.status_code}")
print(f"Response: {response.text[:500]}")

# ============================================================
# ORIGINE 48: test_api_public.py (2025-12-02)
# ============================================================

# test_api_public.py
import requests

# Test de l'API publique
url = "http://localhost:8000/communication/api/public/conversations/8/messages/"
print(f"Testing public API: {url}")

try:
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Text: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

# ============================================================
# ORIGINE 49: test_endpoints.py (2025-12-02)
# ============================================================

# test_endpoints.py
import requests

print("🔍 Test des endpoints de récupération")
print("="*50)

endpoints = [
    "/communication/api/conversations/",
    "/communication/api/simple/conversations/8/messages/",
    "/communication/api/public/conversations/8/messages/",
    "/communication/conversations/",
]

for endpoint in endpoints:
    url = f"http://localhost:8000{endpoint}"
    print(f"\nTesting: {endpoint}")
    try:
        response = requests.get(url)
        print(f"  Status: {response.status_code}")
        print(f"  Content-Type: {response.headers.get('Content-Type')}")
        print(f"  First 200 chars: {response.text[:200]}")
    except Exception as e:
        print(f"  Error: {e}")

# ============================================================
# ORIGINE 50: test_flux_complet.py (2025-12-02)
# ============================================================

# test_flux_complet.py
import requests
import json
import time

print("🔄 Test complet du flux de messagerie")
print("="*50)

url_send = "http://localhost:8000/communication/api/simple/messages/send/"

# 1. Envoi d'un message
print("1. Envoi d'un nouveau message...")
data = {
    "expediteur_id": 1,      # Almoravide
    "destinataire_id": 3,    # medecin_test
    "contenu": "Test de flux complet à " + time.strftime("%H:%M:%S")
}

response = requests.post(url_send, headers={"Content-Type": "application/json"},
                         data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    print(f"   ✅ Message envoyé (ID: {result['message_id']}, Conv: {result['conversation_id']})")

    # 2. Récupération de la conversation
    conv_id = result['conversation_id']
    time.sleep(1)  # Petite attente

    print(f"\n2. Récupération de la conversation {conv_id}...")
    url_conv = f"http://localhost:8000/communication/api/simple/conversations/{conv_id}/messages/"
    response2 = requests.get(url_conv)

    if response2.status_code == 200:
        messages = response2.json()
        print(f"   ✅ {len(messages)} message(s) trouvé(s)")
        for msg in messages:
            print(f"      - {msg.get('expediteur')}: {msg.get('contenu')}")
    else:
        print(f"   ❌ Erreur: {response2.text}")

else:
    print(f"   ❌ Erreur d'envoi: {response.text}")

print("\n" + "="*50)
print("🎯 Système de messagerie fonctionnel !")

# ============================================================
# ORIGINE 51: test_get_messages.py (2025-12-02)
# ============================================================

# test_get_messages.py
import requests
import json

print("📱 Test de récupération des messages")
print("="*50)

# Récupérer les messages de la conversation 6
url_conversation = "http://localhost:8000/communication/api/simple/conversations/6/messages/"

try:
    response = requests.get(url_conversation)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        messages = response.json()
        print(f"✅ {len(messages)} messages dans la conversation 6")
        for msg in messages:
            print(f"   - ID: {msg.get('id')}, De: {msg.get('expediteur')}, Contenu: {msg.get('contenu')[:50]}...")
    else:
        print(f"❌ Erreur: {response.text}")

except Exception as e:
    print(f"💥 Exception: {e}")

# ============================================================
# ORIGINE 52: test_users.py (2025-12-02)
# ============================================================

# test_users.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User

print("👥 Utilisateurs existants :")
for user in User.objects.all():
    print(f"  ID: {user.id}, Username: {user.username}, Email: {user.email}")

# ============================================================
# ORIGINE 53: test_messages_api1.py (2025-12-02)
# ============================================================

# test_messages_api.py - VERSION CORRIGÉE
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_get_messages(conversation_id=5):
    """Teste la récupération des messages"""
    print(f"📨 Récupération des messages de la conversation {conversation_id}...")

    urls = [
        f"/communication/api/public/conversations/{conversation_id}/messages/",
        f"/communication/api/simple/conversations/{conversation_id}/messages/",
        f"/communication/api/test/messages/",
    ]

    for url_path in urls:
        url = BASE_URL + url_path
        print(f"\n🔗 Test URL: {url}")

        try:
            response = requests.get(url, timeout=10)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()

                    if isinstance(data, dict):
                        if 'messages' in data:
                            messages = data['messages']
                            print(f"   ✅ {len(messages)} messages trouvés")

                            # Afficher les messages
                            for i, msg in enumerate(messages[:3]):
                                print(f"   📝 Message {i+1}: {msg.get('titre', 'Sans titre')}")
                                print(f"      Contenu: {msg.get('contenu', '')[:50]}...")
                                print(f"      De: {msg.get('expediteur', {}).get('username', 'Inconnu')}")
                                print()
                        elif 'status' in data:
                            print(f"   ✅ Message: {data.get('status', 'API fonctionne')}")
                        else:
                            print(f"   📊 Données: {json.dumps(data, indent=2)[:200]}...")
                    else:
                        print(f"   ✅ Réponse: {json.dumps(data, indent=2)[:200]}...")

                except json.JSONDecodeError:
                    print(f"   ❌ Réponse non-JSON: {response.text[:200]}")
            elif response.status_code == 403:
                print(f"   🔒 Accès refusé (authentification requise)")
... (tronqué)

# ============================================================
# ORIGINE 54: test_messages_api.py (2025-12-02)
# ============================================================

#!/usr/bin/env python3
"""
Script de test pour l'API de messages
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_get_messages(conversation_id=5):
    """Teste la récupération des messages"""
    print(f"📨 Récupération des messages de la conversation {conversation_id}...")

    urls = [
        f"/communication/api/simple/conversations/{conversation_id}/messages/",
        f"/api/communication/conversations/{conversation_id}/messages/",
        f"/communication/conversations/{conversation_id}/messages/json/",
    ]

    for url_path in urls:
        url = BASE_URL + url_path
        print(f"
🔗 Test URL: {url}")

        try:
            response = requests.get(url, timeout=10)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict) and 'messages' in data:
                        messages = data['messages']
                        print(f"   ✅ {len(messages)} messages trouvés")

                        # Afficher les messages
                        for i, msg in enumerate(messages[:5]):  # Afficher les 5 premiers
                            print(f"   📝 Message {i+1}: {msg.get('titre', 'Sans titre')}")
                            print(f"      Contenu: {msg.get('contenu', '')[:50]}...")
                            print(f"      De: {msg.get('expediteur', {}).get('username', 'Inconnu')}")
                            print(f"      À: {msg.get('destinataire', {}).get('username', 'Inconnu')}")
                            print()
                    elif isinstance(data, list):
                        print(f"   ✅ {len(data)} messages trouvés (liste directe)")

                        # Afficher les messages
                        for i, msg in enumerate(data[:3]):  # Afficher les 3 premiers
                            print(f"   📝 Message {i+1}: {msg.get('titre', 'Sans titre')}")
... (tronqué)

# ============================================================
# ORIGINE 55: test_api_urls.py (2025-12-02)
# ============================================================

# test_api_urls.py
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_urls():
    """Teste toutes les URLs API possibles"""

    urls_to_test = [
        # URLs directes
        ("/communication/conversations/5/messages/", "Messages direct"),
        ("/api/communication/conversations/5/messages/", "API Messages"),
        ("/api/v1/communication/conversations/5/messages/", "API v1 Messages"),
        ("/communication/api/conversations/5/messages/", "Communication API"),
        ("/communication/conversations/5/api/messages/", "Conversation API"),

        # URLs avec JSON
        ("/communication/conversations/5/messages/json/", "Messages JSON"),
        ("/communication/conversations/5/json/", "Conversation JSON"),

        # URLs de l'application existante
        ("/communication/api_messages/5/", "API Messages direct"),
        ("/communication/conversation/5/messages/", "Conversation messages"),

        # URLs avec format
        ("/communication/conversations/5/?format=json", "Format JSON"),
        ("/communication/conversations/5/messages/?format=json", "Messages format JSON"),
    ]

    print("🔍 Test de toutes les URLs API possibles...")
    print("=" * 60)

    working_urls = []

    for url_path, description in urls_to_test:
        url = BASE_URL + url_path
        print(f"\n📡 Testing: {description}")
        print(f"   URL: {url}")

        try:
            response = requests.get(url, timeout=5)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                print(f"   Content-Type: {content_type}")

                if 'application/json' in content_type:
... (tronqué)

# ============================================================
# ORIGINE 56: test_simple.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
import os
import sys
import django

# Trouver le bon settings module
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

# Essayer plusieurs noms de settings
settings_modules = [
    'settings',
    'projet.settings',
    'app.settings',
    'config.settings',
    'mutuelle_core.settings'
]

for settings_module in settings_modules:
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
        django.setup()
        print(f"✅ Settings module trouvé: {settings_module}")
        break
    except:
        continue

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

print("\n🔍 TEST SIMPLIFIÉ DES PERMISSIONS")
print("=" * 40)

# Option 1: Tester directement sans authentification
try:
    user = User.objects.get(username='GLORIA1')
    print(f"✅ Utilisateur trouvé: {user.username}")
    print(f"   Actif: {user.is_active}")
    print(f"   Superutilisateur: {user.is_superuser}")

    # Tester les permissions directement
    print("\n🔐 PERMISSIONS DIRECTES:")
    print("-" * 30)

    # Recharger l'utilisateur pour éviter le cache
    user = User.objects.get(pk=user.pk)

    permissions = [
        'medecin.view_ordonnance',
        'medecin.change_ordonnance',
... (tronqué)

# ============================================================
# ORIGINE 57: test_final3.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import authenticate

# Test d'authentification
user = authenticate(username='GLORIA1', password='Pharmacien123!')

if user:
    print(f"✅ Authentifié: {user.username}")

    # Test des permissions critiques
    tests = [
        ('medecin.view_ordonnance', 'Peut voir les ordonnances'),
        ('medecin.change_ordonnance', 'Peut modifier les ordonnances'),
        ('pharmacien.view_ordonnancepharmacien', 'Peut voir ordonnances pharmacien'),
    ]

    for perm, desc in tests:
        result = user.has_perm(perm)
        print(f"{'✅' if result else '❌'} {desc}: {'OUI' if result else 'NON'}")
else:
    print("❌ Échec d'authentification")

# ============================================================
# ORIGINE 58: test_simple_permissions.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
"""
TEST SIMPLE DES PERMISSIONS
"""
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mutuelle_core.settings")
django.setup()

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Permission, Group

def test_permissions():
    print("🧪 TEST DES PERMISSIONS DE GLORIA1")
    print("=" * 50)

    # Authentification
    user = authenticate(username="GLORIA1", password="Pharmacien123!")

    if not user:
        print("❌ Échec d'authentification")
        return

    print(f"✅ Authentifié: {user.username}")
    print(f"Groupes: {[g.name for g in user.groups.all()]}")

    # Test des permissions spécifiques
    print("\n🔍 TEST DES PERMISSIONS:")

    permissions_to_test = [
        ("view_ordonnance", "Voir les ordonnances"),
        ("change_ordonnance", "Modifier les ordonnances"),
        ("view_stockpharmacie", "Voir le stock"),
        ("change_stockpharmacie", "Modifier le stock"),
        ("view_pharmacien", "Voir le profil pharmacien"),
    ]

    for perm_codename, description in permissions_to_test:
        # Essaie avec différents app_labels
        found = False
        app_labels = ["ordonnances", "pharmacien", "soins", "ordonnance"]

        for app_label in app_labels:
            if user.has_perm(f"{app_label}.{perm_codename}"):
                print(f"✅ {description}: OUI ({app_label}.{perm_codename})")
                found = True
                break

... (tronqué)

# ============================================================
# ORIGINE 59: test_complet_final.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
"""
TEST COMPLET FINAL - Vérification de tous les systèmes
"""

import os
import sys
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group

def test_authentification():
    """Test d'authentification de tous les utilisateurs clés"""
    print("🔐 TESTS D'AUTHENTIFICATION")
    print("=" * 60)

    User = get_user_model()

    # Liste des utilisateurs à tester
    test_users = [
        {'username': 'GLORIA1', 'password': 'Pharmacien123!', 'description': 'Pharmacien'},
        {'username': 'Almoravide', 'password': 'Almoravide1084', 'description': 'Admin'},
        {'username': 'GLORIA', 'password': 'GLORIA', 'description': 'Médecin'},
        {'username': 'medecin_test', 'password': 'medecin123', 'description': 'Médecin test'},
        {'username': 'agent_test', 'password': 'agent123', 'description': 'Agent'},
        {'username': 'pharmacien_test', 'password': 'pharmacien123', 'description': 'Pharmacien test'},
    ]

    for user_info in test_users:
        username = user_info['username']
        password = user_info['password']
        description = user_info['description']

        print(f"\n🧪 {description} ({username}):")

        # Vérifie si l'utilisateur existe
        try:
            user = User.objects.get(username=username)
            print(f"   ✅ Existe dans la DB")
            print(f"      Actif: {user.is_active}, Staff: {user.is_staff}")

            # Test d'authentification
            auth_user = authenticate(username=username, password=password)
            if auth_user:
                print(f"   ✅ Authentification réussie")
... (tronqué)

# ============================================================
# ORIGINE 60: test_simple_login1.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
"""
TEST SIMPLE DE CONNEXION GLORIA1
"""

import os
import sys
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import authenticate, get_user_model

print("🧪 TEST SIMPLE DE CONNEXION GLORIA1")
print("==================================")

# Test 1: Avec point d'exclamation
print("\nTest 1: Avec 'Pharmacien123!'")
user = authenticate(username='GLORIA1', password='Pharmacien123!')
if user:
    print('✅ SUCCÈS avec Pharmacien123!')
    print(f'   User: {user.username}')
else:
    print('❌ ÉCHEC avec Pharmacien123!')

# Test 2: Sans point d'exclamation
print("\nTest 2: Sans point d'exclamation")
user = authenticate(username='GLORIA1', password='Pharmacien123')
if user:
    print('✅ SUCCÈS avec Pharmacien123')
    print(f'   User: {user.username}')
else:
    print('❌ ÉCHEC avec Pharmacien123')

# Test 3: Vérification directe
print("\nTest 3: Vérification directe")
User = get_user_model()
try:
    user = User.objects.get(username='GLORIA1')
    print(f'User: {user.username}')
    print(f'Password hash: {user.password[:50]}...')
    print(f'is_active: {user.is_active}')

    # Test tous les mots de passe possibles
    passwords = ['Pharmacien123!', 'Pharmacien123', 'GLORIA1', '', 'Gloria123']
    for pwd in passwords:
        if user.check_password(pwd):
            print(f'✅ Mot de passe trouvé: "{pwd}"')
... (tronqué)

# ============================================================
# ORIGINE 61: test_simple_login.py (2025-12-02)
# ============================================================

#!/bin/bash
echo "🧪 TEST SIMPLE DE CONNEXION GLORIA1"
echo "=================================="

# Test 1: Avec point d'exclamation
echo "Test 1: Avec 'Pharmacien123!'"
python manage.py shell -c "
from django.contrib.auth import authenticate
user = authenticate(username='GLORIA1', password='Pharmacien123!')
if user:
    print('✅ SUCCÈS avec Pharmacien123!')
    print(f'   User: {user.username}')
else:
    print('❌ ÉCHEC avec Pharmacien123!')
"

echo ""
echo "Test 2: Sans point d'exclamation"
python manage.py shell -c "
from django.contrib.auth import authenticate
user = authenticate(username='GLORIA1', password='Pharmacien123')
if user:
    print('✅ SUCCÈS avec Pharmacien123')
    print(f'   User: {user.username}')
else:
    print('❌ ÉCHEC avec Pharmacien123')
"

echo ""
echo "Test 3: Vérification directe"
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='GLORIA1')
print(f'User: {user.username}')
print(f'Password hash: {user.password[:50]}...')
print(f'is_active: {user.is_active}')

# Test tous les mots de passe possibles
passwords = ['Pharmacien123!', 'Pharmacien123', 'GLORIA1', '']
for pwd in passwords:
    if user.check_password(pwd):
        print(f'✅ Mot de passe trouvé: \"{pwd}\"')
        break
else:
    print('❌ Aucun mot de passe ne correspond')
"

# ============================================================
# ORIGINE 62: test_final2.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE TEST FINAL - API Messagerie
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_api_direct():
    """Test direct de l'API sans interface web"""
    print("🧪 TEST DIRECT DE L'API MESSAGERIE")
    print("=" * 50)

    # 1. Récupérer un token CSRF
    print("\n1. Récupération token CSRF...")
    session = requests.Session()

    try:
        response = session.get(f"{BASE_URL}/accounts/login/")
        csrf_token = None

        # Extrait le token CSRF
        import re
        csrf_match = re.search(r'csrfmiddlewaretoken[\'"] value=[\'"]([^\'"]+)', response.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)
            print(f"✅ Token CSRF trouvé: {csrf_token[:20]}...")
        else:
            print("⚠ Token CSRF non trouvé, tentative sans...")

        # 2. Connexion avec GLORIA1
        print("\n2. Connexion avec GLORIA1...")
        login_data = {
            'username': 'GLORIA1',
            'password': 'Pharmacien123',
        }

        if csrf_token:
            login_data['csrfmiddlewaretoken'] = csrf_token

        response = session.post(
            f"{BASE_URL}/accounts/login/",
            data=login_data,
            headers={'Referer': f'{BASE_URL}/accounts/login/'},
            allow_redirects=False
        )

... (tronqué)

# ============================================================
# ORIGINE 63: test_api_enhanced.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
"""
Script de test API amélioré avec gestion automatique du serveur
"""

import subprocess
import time
import sys
import requests
import json
from threading import Thread
import signal
import atexit

# Variables globales
SERVER_URL = "http://127.0.0.1:8000"
SERVER_PROCESS = None

def start_server():
    """Démarre le serveur Django en arrière-plan"""
    global SERVER_PROCESS

    print("🚀 Démarrage du serveur Django...")

    try:
        # Vérifie si le serveur est déjà en cours d'exécution
        response = requests.get(f"{SERVER_URL}/", timeout=2)
        if response.status_code < 500:
            print("✅ Serveur déjà en cours d'exécution")
            return True
    except:
        pass  # Le serveur n'est pas démarré, continuons

    # Démarre le serveur
    SERVER_PROCESS = subprocess.Popen(
        [sys.executable, "manage.py", "runserver", "--noreload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Attends que le serveur soit prêt
    print("⏳ Attente du démarrage du serveur...")
    for i in range(30):  # 30 secondes maximum
        try:
            response = requests.get(f"{SERVER_URL}/", timeout=2)
            if response.status_code < 500:
                print("✅ Serveur démarré avec succès!")
                return True
        except:
... (tronqué)

# ============================================================
# ORIGINE 64: test_api.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
"""
Script de test pour l'API de messagerie
"""
import requests
import json
import sys

BASE_URL = 'http://127.0.0.1:8000'

def test_login(username, password):
    """Teste la connexion"""
    print(f"\n🔐 Test de connexion pour {username}...")

    # Récupère d'abord le token CSRF
    session = requests.Session()
    response = session.get(f'{BASE_URL}/accounts/login/')

    # Extrait le token CSRF (simplifié)
    csrf_token = None
    if 'csrfmiddlewaretoken' in response.text:
        # Recherche simplifiée du token
        import re
        match = re.search(r"name='csrfmiddlewaretoken' value='([^']+)'", response.text)
        if match:
            csrf_token = match.group(1)

    if not csrf_token:
        print("⚠ Impossible de récupérer le token CSRF")
        return None

    # Tente la connexion
    login_data = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }

    headers = {
        'Referer': f'{BASE_URL}/accounts/login/'
    }

    response = session.post(
        f'{BASE_URL}/accounts/login/',
        data=login_data,
        headers=headers,
        allow_redirects=False
    )

    if response.status_code == 302:
... (tronqué)

# ============================================================
# ORIGINE 65: test_api_auth.py (2025-12-02)
# ============================================================


#!/usr/bin/env python3
# test_api_auth.py - Test avec authentification
import requests
from requests.cookies import RequestsCookieJar
import json
import sys

def get_auth_session():
    """Créer une session authentifiée"""
    session = requests.Session()

    # URL de login
    login_url = "http://127.0.0.1:8000/accounts/login/"

    # D'abord, récupérer le token CSRF
    print("🔐 Récupération du token CSRF...")
    response = session.get(login_url)

    # Chercher le token CSRF dans la réponse HTML
    csrf_token = None
    if 'csrfmiddlewaretoken' in response.text:
        import re
        match = re.search(r"name='csrfmiddlewaretoken' value='([^']+)'", response.text)
        if match:
            csrf_token = match.group(1)
            print(f"✅ Token CSRF trouvé: {csrf_token[:20]}...")

    # Se connecter avec l'utilisateur GLORIA1
    login_data = {
        'username': 'GLORIA1',
        'password': '1234',  # Mot de passe par défaut
        'csrfmiddlewaretoken': csrf_token,
        'next': '/communication/'
    }

    print("🔐 Connexion en tant que GLORIA1...")
    response = session.post(login_url, data=login_data, headers={'Referer': login_url})

    if response.status_code == 200 and 'GLORIA1' in response.text:
        print("✅ Connecté avec succès!")
        return session
    else:
        print(f"❌ Échec de la connexion: {response.status_code}")
        print(f"   Redirection vers: {response.url}")
        return None

def test_api_with_auth():
    """Tester l'API avec authentification"""
    print("🔍 TEST API AVEC AUTHENTIFICATION")
... (tronqué)

# ============================================================
# ORIGINE 66: test_final_simple.sh (2025-12-01)
# ============================================================

#!/bin/bash

echo "🧪 TEST FINAL SIMPLIFIÉ"
echo "======================"

# Vérifier la syntaxe d'abord
echo "🔍 Vérification syntaxe Python:"
python3 -m py_compile communication/views.py 2>&1 | head -20

if [ $? -eq 0 ]; then
    echo "✅ Syntaxe Python OK"
else
    echo "❌ Erreur de syntaxe"
    exit 1
fi

# Test rapide avec Django
python3 -c "
import sys
import os
sys.path.insert(0, '.')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    import django
    django.setup()

    print('✅ Django configuré')

    # Importer la vue pour vérifier
    from communication.views import envoyer_message_api
    print('✅ Vue envoyer_message_api importée')

    # Vérifier les décorateurs
    import inspect
    source = inspect.getsource(envoyer_message_api)

    if '@csrf_exempt' in source:
        print('✅ Décorateur @csrf_exempt présent')
    else:
        print('❌ Décorateur @csrf_exempt manquant')

    if '@login_required' in source:
        print('✅ Décorateur @login_required présent')
    else:
        print('❌ Décorateur @login_required manquant')

except Exception as e:
    print(f'❌ Erreur: {e}')
... (tronqué)

# ============================================================
# ORIGINE 67: test_com_api.sh (2025-12-01)
# ============================================================

#!/bin/bash

echo "🔧 TEST COMPLET DES APIs COMMUNICATION"
echo "====================================="

# Démarrer le serveur si nécessaire
if ! ps aux | grep -q "python manage.py runserver"; then
    echo "🚀 Démarrage du serveur..."
    python manage.py runserver 0.0.0.0:8000 > /tmp/com_api_test.log 2>&1 &
    SERVER_PID=$!
    sleep 5
    echo "✅ Serveur démarré (PID: $SERVER_PID)"
fi

# Test Python complet
python -c "
import sys
import os
import json
sys.path.insert(0, '.')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    import django
    django.setup()

    from django.test import Client
    from django.contrib.auth.models import User
    from communication.models import Message, Notification, Conversation

    print('🧪 TEST COMPLET DES APIs')
    print('=' * 50)

    client = Client()

    # 1. Authentification
    try:
        user = User.objects.get(username='GLORIA1')
        print(f'1. ✅ Authentification: {user.username}')
        client.force_login(user)
    except User.DoesNotExist:
        print('1. ❌ GLORIA1 non trouvé')
        exit(1)

    # 2. Test API notifications
    print('\\n2. 📊 API Notifications:')
    response = client.get('/communication/notifications/count/')
    if response.status_code == 200:
        data = json.loads(response.content)
... (tronqué)

# ============================================================
# ORIGINE 68: test_communication_simple.sh (2025-12-01)
# ============================================================

#!/bin/bash

echo "🧪 TEST SIMPLE DU MODULE COMMUNICATION"
echo "======================================"

# Arrêter tout serveur existant
echo "🛑 Arrêt des serveurs existants..."
pkill -f "python manage.py runserver" 2>/dev/null
sleep 2

# Vérifier les vues
echo ""
echo "🔍 VÉRIFICATION DES VUES:"
python -c "
import sys
sys.path.insert(0, '.')
try:
    import communication.views as v

    print('📋 Vues disponibles (messagerie_*):')
    views = [attr for attr in dir(v) if 'messagerie' in attr.lower() and callable(getattr(v, attr))]

    for view in sorted(views):
        print(f'   ✅ {view}')

    print(f'\\n📊 Total: {len(views)} vues messagerie')

    # Vérifier les vues critiques
    critical_views = ['messagerie_pharmacien', 'messagerie', 'communication_home']
    for cv in critical_views:
        if hasattr(v, cv):
            print(f'   ✅ {cv} → OK')
        else:
            print(f'   ❌ {cv} → MANQUANTE')

except Exception as e:
    print(f'❌ Erreur: {e}')
"

# Démarrer le serveur
echo ""
echo "🚀 Démarrage du serveur..."
python manage.py runserver 0.0.0.0:8000 > /tmp/django_com_test.log 2>&1 &
SERVER_PID=$!
echo "✅ Serveur démarré (PID: $SERVER_PID)"

# Attendre
echo "⏳ Attente du démarrage..."
sleep 5

... (tronqué)

# ============================================================
# ORIGINE 69: test_final_pharmacien.py (2025-12-01)
# ============================================================

#!/usr/bin/env python
"""
TEST FINAL - INTERFACE PHARMACIEN COMPLÈTE
"""
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_final():
    """Test final complet de l'interface pharmacien"""
    print("🚀 TEST FINAL - INTERFACE PHARMACIEN COMPLÈTE")
    print("=" * 60)

    # 1. Vérifier tous les templates
    print("1. 📄 VÉRIFICATION DES TEMPLATES:")
    templates_essentiels = [
        ('base_pharmacien.html', 'Template de base'),
        ('liste_ordonnances.html', 'Template des ordonnances'),
        ('_navbar_pharmacien.html', 'Navigation'),
        ('_sidebar_pharmacien.html', 'Sidebar'),
        ('_sidebar_mobile.html', 'Sidebar mobile'),
    ]

    for template, description in templates_essentiels:
        path = BASE_DIR / 'templates' / 'pharmacien' / template
        if path.exists():
            size = path.stat().st_size
            status = "✅" if size > 100 else "⚠️"
            print(f"   {status} {template}: {description} ({size} octets)")
        else:
            print(f"   ❌ {template}: {description} - MANQUANT")

    # 2. Vérifier le contenu du template liste_ordonnances
    print("\n2. 🔍 ANALYSE DU TEMPLATE liste_ordonnances.html:")
    liste_path = BASE_DIR / 'templates' / 'pharmacien' / 'liste_ordonnances.html'
    if liste_path.exists():
        with open(liste_path, 'r', encoding='utf-8') as f:
            content = f.read()

        checks = [
            ('{% extends', 'Héritage du template de base'),
            ('{% block content', 'Block content défini'),
            ('ordonnances', 'Variable ordonnances utilisée'),
            ('{% for', 'Boucle for présente'),
... (tronqué)

# ============================================================
# ORIGINE 70: test_systeme_complet1.py (2025-12-01)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE TEST COMPLET - SYSTÈME MUTUELLE CORE
Teste toutes les fonctionnalités du projet
"""
import os
import sys
import django
from pathlib import Path
from datetime import datetime, timedelta

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def print_section(title):
    """Affiche une section de test"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def test_base_donnees():
    """Test de la base de données"""
    print_section("TEST BASE DE DONNÉES")

    from django.db import connection

    try:
        with connection.cursor() as cursor:
            # Test connexion
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Connexion DB: {result[0] == 1}")

            # Test tables critiques
            cursor.execute("SELECT COUNT(*) FROM auth_user")
            users = cursor.fetchone()[0]
            print(f"✅ Table auth_user: {users} utilisateurs")

            cursor.execute("SELECT COUNT(*) FROM medecin_ordonnance")
            ordonnances = cursor.fetchone()[0]
            print(f"✅ Table medecin_ordonnance: {ordonnances} ordonnances")

            cursor.execute("SELECT COUNT(*) FROM ordonnance_partage")
            partages = cursor.fetchone()[0]
            print(f"✅ Table ordonnance_partage: {partages} partages")

            cursor.execute("SELECT COUNT(*) FROM pharmacien_ordonnances_view")
... (tronqué)

# ============================================================
# ORIGINE 71: test_ordonnance_flow.py (2025-11-30)
# ============================================================

# test_ordonnance_flow.py
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_real_ordonnance_flow():
    """Tester le flux réel ordonnance médecin → pharmacien"""
    print("🧪 TEST RÉEL FLUX ORDONNANCE")
    print("=" * 50)

    try:
        # 1. Créer une ordonnance médecin
        from medecin.models import Ordonnance as OrdonnanceMedecin
        from membres.models import Membre

        # Prendre un membre existant
        membre = Membre.objects.first()

        # Créer ordonnance médecin
        ordonnance_medecin = OrdonnanceMedecin.objects.create(
            membre=membre,
            date_prescription=timezone.now().date(),
            diagnostic="Test diagnostic",
            instructions="Prendre 3 fois par jour",
            duree_traitement=7,
            renouvelable=False
        )
        print(f"✅ Ordonnance médecin créée: ID {ordonnance_medecin.id}")

        # 2. Vérifier si elle est visible par pharmacien
        from pharmacien.models import Ordonnance as OrdonnancePharmacien

        try:
            # Vérifier si une version pharmacien existe
            ordonnance_pharmacien = OrdonnancePharmacien.objects.filter(
                ordonnance_medecin=ordonnance_medecin
            ).first()

            if ordonnance_pharmacien:
                print(f"✅ Ordonnance visible par pharmacien: ID {ordonnance_pharmacien.id}")
            else:
                print("❌ Ordonnance NON visible par pharmacien")
                print("💡 Le partage automatique ne fonctionne pas")

        except Exception as e:
            print(f"❌ Erreur vérification pharmacien: {e}")

... (tronqué)

# ============================================================
# ORIGINE 72: test_sync_only.py (2025-11-30)
# ============================================================

# test_sync_only.py
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_current_state():
    """Tester l'état actuel du système"""
    print("🔍 ÉTAT ACTUEL DU SYSTÈME")
    print("=" * 50)

    with connection.cursor() as cursor:
        # Membres
        cursor.execute("SELECT COUNT(*) FROM membres_membre")
        membres = cursor.fetchone()[0]

        # Cotisations
        cursor.execute("SELECT COUNT(*) FROM assureur_cotisation")
        cotisations = cursor.fetchone()[0]

        # Vérifications
        cursor.execute("SELECT COUNT(*) FROM agents_verificationcotisation")
        verifications = cursor.fetchone()[0]

        print(f"📊 STATISTIQUES:")
        print(f"   👥 Membres: {membres}")
        print(f"   💰 Cotisations: {cotisations}")
        print(f"   ✅ Vérifications: {verifications}")

def simulate_sync():
    """Simuler la synchronisation avec des données de test"""
    print("\n🎭 SIMULATION SYNCHRONISATION")
    print("=" * 50)

    with connection.cursor() as cursor:
        # Mettre à jour toutes les vérifications avec un statut simulé
        cursor.execute("""
            UPDATE agents_verificationcotisation
            SET statut_cotisation = 'ACTIVE',
                observations = 'Sync simulée: Données de test'
        """)

        print(f"✅ {cursor.rowcount} vérifications mises à jour avec statut simulé")

if __name__ == "__main__":
    test_current_state()
    simulate_sync()
    print("\n🎯 Synchronisation simulée terminée!")
... (tronqué)

# ============================================================
# ORIGINE 73: test_final_complet3.py (2025-11-30)
# ============================================================

# test_final_complet.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from scoring.calculators import CalculateurScoreMembre
from scoring.models import HistoriqueScore
from relances.models import TemplateRelance
from relances.services import ServiceRelances

print("🎯 TEST FINAL COMPLET")
print("=" * 50)

# 1. Test du scoring
print("\\n1. 🧪 TEST DU SCORING")
membre = Membre.objects.first()
if membre:
    print(f"👤 Membre test: {membre.nom}")

    calculateur = CalculateurScoreMembre()
    resultat = calculateur.calculer_score_complet(membre)

    print(f"✅ Score calculé: {resultat['score_final']}")
    print(f"✅ Niveau risque: {resultat['niveau_risque']}")

    # Vérifier que le membre est mis à jour
    membre.refresh_from_db()
    if hasattr(membre, 'score_risque'):
        print(f"✅ Membre mis à jour - Score: {membre.score_risque}, Risque: {membre.niveau_risque}")
    else:
        print("❌ Champs manquants dans le modèle Membre")
else:
    print("❌ Aucun membre trouvé")

# 2. Test des relances
print("\\n2. 📧 TEST DES RELANCES")
service = ServiceRelances()
membres_a_relancer = service.identifier_membres_a_relancer()
print(f"✅ Membres à relancer: {len(membres_a_relancer)}")

# 3. Vérification des données
print("\\n3. 📊 VÉRIFICATION DES DONNÉES")
print(f"✅ Historiques scores: {HistoriqueScore.objects.count()}")
print(f"✅ Templates relance: {TemplateRelance.objects.count()}")

# 4. Test de tous les membres
print("\\n4. 👥 SCORES DE TOUS LES MEMBRES")
membres = Membre.objects.all()[:5]  # Premiers 5 seulement
... (tronqué)

# ============================================================
# ORIGINE 74: test_simplifie.py (2025-11-30)
# ============================================================

# test_simplifie.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from scoring.calculators import CalculateurScoreMembre

print("🧪 TEST SIMPLIFIÉ DU SCORING")
print("=" * 40)

membre = Membre.objects.first()
if membre:
    print(f"👤 Test avec: {membre.nom}")

    calculateur = CalculateurScoreMembre()
    resultat = calculateur.calculer_score_complet(membre)

    print(f"✅ Score: {resultat['score_final']}")
    print(f"✅ Niveau risque: {resultat['niveau_risque']}")
    print(f"✅ Détails: {resultat['details_scores']}")

    # Vérifier que le membre est mis à jour
    membre.refresh_from_db()
    print(f"✅ Membre mis à jour - Score: {membre.score_risque}, Risque: {membre.niveau_risque}")
else:
    print("❌ Aucun membre trouvé")

# ============================================================
# ORIGINE 75: test_complet_fonctionnalites.py (2025-11-30)
# ============================================================

# test_complet_fonctionnalites.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import TestCase
from membres.models import Membre
from agents.models import VerificationCotisation, Agent
from relances.models import TemplateRelance, RelanceProgrammee
from scoring.models import RegleScoring, HistoriqueScore
from scoring.calculators import CalculateurScoreMembre
from relances.services import ServiceRelances

class TestNouvellesFonctionnalites:
    def __init__(self):
        self.resultats = []

    def tester_scoring(self):
        """Teste le système de scoring"""
        print("🧪 Test du système de scoring...")

        try:
            # Vérifier les règles
            regles = RegleScoring.objects.all()
            assert regles.count() > 0, "Aucune règle de scoring"
            print(f"✅ {regles.count()} règles de scoring")

            # Tester le calculateur
            calculateur = CalculateurScoreMembre()
            membre = Membre.objects.first()

            if membre:
                resultat = calculateur.calculer_score_complet(membre)
                assert 'score_final' in resultat, "Score final manquant"
                assert 'niveau_risque' in resultat, "Niveau risque manquant"
                assert 'details_scores' in resultat, "Détails scores manquants"

                print(f"✅ Scoring fonctionnel: {membre.nom} → {resultat['score_final']}")
                self.resultats.append(("Scoring", "✅ FONCTIONNEL"))
            else:
                print("⚠️  Aucun membre pour tester le scoring")
                self.resultats.append(("Scoring", "⚠️  AUCUN MEMBRE"))

        except Exception as e:
            print(f"❌ Erreur scoring: {e}")
            self.resultats.append(("Scoring", f"❌ ERREUR: {e}"))

    def tester_relances(self):
        """Teste le système de relances"""
... (tronqué)

# ============================================================
# ORIGINE 76: test_acces_temps_reel.py (2025-11-28)
# ============================================================

# test_acces_temps_reel.py

import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def tester_acces_utilisateur(username, password, urls_a_tester):
    """Teste l'accès d'un utilisateur à différentes URLs"""
    client = Client()

    print(f"\n🔐 TEST ACCÈS: {username}")
    print("-" * 30)

    # Connexion
    login_success = client.login(username=username, password=password)
    if not login_success:
        print(f"❌ Échec connexion pour {username}")
        return

    print(f"✅ Connexion réussie")

    # Test des URLs
    for url_name, description in urls_a_tester:
        try:
            url = reverse(url_name)
            response = client.get(url)

            if response.status_code == 200:
                print(f"   ✅ {description}: ACCÈS AUTORISÉ")
            elif response.status_code == 403:
                print(f"   ❌ {description}: ACCÈS REFUSÉ")
            elif response.status_code == 302:
                print(f"   🔄 {description}: REDIRECTION")
            else:
                print(f"   ⚠️  {description}: CODE {response.status_code}")

        except Exception as e:
            print(f"   💥 {description}: ERREUR - {e}")

def test_complet_acces():
    """Test complet des accès pour tous les rôles"""
... (tronqué)

# ============================================================
# ORIGINE 77: test_votre_configuration.py (2025-11-28)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from assureur.models import Assureur
from django.contrib.auth.models import User
from django.db.models import Q

def test_votre_configuration():
    print("🎯 TEST DE VOTRE CONFIGURATION ACTUELLE")
    print("=" * 50)

    # 1. Vérifier les utilisateurs existants
    print("1. 👤 UTILISATEURS EXISTANTS")
    users = User.objects.all()
    print(f"   📊 Total utilisateurs: {users.count()}")

    # Afficher seulement les utilisateurs importants
    users_importants = ['DOUA', 'GLORIA', 'Almoravide', 'ASIA']
    for username in users_importants:
        try:
            user = User.objects.get(username=username)
            print(f"      👤 {user.username} ({user.email})")
        except User.DoesNotExist:
            print(f"      ❌ {username} - Non trouvé")

    # 2. Vérifier les membres
    print("\n2. 👥 MEMBRES DANS LA BASE")
    membres = Membre.objects.all()
    print(f"   📊 Total membres: {membres.count()}")

    # Test recherche avec les BONS champs
    print("\n3. 🔍 TESTS RECHERCHE (avec champs corrects)")
    tests = ["DRAMANE", "Pierre", "Martin", "ASIA", "Marie", "Sophie"]

    for query in tests:
        # UTILISER numero_unique qui existe dans votre modèle
        resultats = Membre.objects.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(numero_unique__icontains=query) |  # ⬅️ CHAMP CORRECT
            Q(email__icontains=query)
        )
        print(f"   🔎 '{query}': {resultats.count()} résultat(s)")
        for r in resultats:
... (tronqué)

# ============================================================
# ORIGINE 78: test_final_complet2.py (2025-11-28)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from django.db.models import Q

def test_avec_champs_reels():
    print("🎯 TEST AVEC CHAMPS RÉELS")
    print("=" * 35)

    # Test avec les VRAIS champs de votre modèle
    query = "DRAMANE"
    resultats = Membre.objects.filter(
        Q(nom__icontains=query) |
        Q(prenom__icontains=query) |
        Q(numero_membre__icontains=query) |  # ⬅️ CHAMP RÉEL
        Q(email__icontains=query)
    )

    print(f"🔍 Recherche '{query}': {resultats.count()} résultat(s)")
    for r in resultats:
        print(f"   ✅ {r.prenom} {r.nom}")
        print(f"      Numéro membre: {r.numero_membre}")
        print(f"      Date adhésion: {r.date_adhesion}")
        print(f"      Email: {r.email}")

def verifier_tri():
    print("\n📋 TEST TRI PAR DATE ADHÉSION")
    print("=" * 35)

    # Tester le tri
    membres_tries = Membre.objects.all().order_by('-date_adhesion')[:3]
    print("3 derniers membres (par date adhésion):")
    for m in membres_tries:
        print(f"   👤 {m.prenom} {m.nom} - {m.date_adhesion}")

if __name__ == "__main__":
    test_avec_champs_reels()
    verifier_tri()

# ============================================================
# ORIGINE 79: test_recherche_reel.py (2025-11-28)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from django.db.models import Q

def test_recherche_avec_champs_corrects():
    print("🎯 TEST RECHERCHE AVEC CHAMPS CORRECTS")
    print("=" * 45)

    # Test avec les VRAIS champs de votre modèle
    query = "DRAMANE"
    resultats = Membre.objects.filter(
        Q(nom__icontains=query) |
        Q(prenom__icontains=query) |
        Q(numero_unique__icontains=query) |  # ⬅️ CHAMP CORRECT
        Q(email__icontains=query)
    )

    print(f"🔍 Recherche '{query}': {resultats.count()} résultat(s)")
    for r in resultats:
        print(f"   ✅ {r.prenom} {r.nom}")
        print(f"      Numéro unique: {r.numero_unique}")
        print(f"      Email: {r.email}")

def test_multiple_recherches():
    print("\n🔍 TESTS MULTIPLES")
    print("=" * 30)

    tests = ["DRAMANE", "Pierre", "Martin", "ASIA", "Marie"]

    for query in tests:
        resultats = Membre.objects.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(numero_unique__icontains=query) |
            Q(email__icontains=query)
        )
        print(f"🔎 '{query}': {resultats.count()} résultat(s)")
        for r in resultats:
            print(f"   👤 {r.prenom} {r.nom}")

def verifier_membre_dramane():
    print("\n📋 VÉRIFICATION ASIA DRAMANE")
    print("=" * 35)
... (tronqué)

# ============================================================
# ORIGINE 80: test_template_ameliore.py (2025-11-28)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    from django.test import Client
    from medecin.models import Medecin

    def test_template_ameliore():
        print("🧪 TEST AVEC TEMPLATE COMPLET")
        print("=" * 40)

        client = Client()

        # Connexion
        print("🔑 Connexion...")
        if not client.login(username='medecin_test', password='password123'):
            print("❌ Échec connexion")
            return

        print("✅ Connecté")

        # Test de la page
        print("\n🚀 Test page suivi chronique...")
        response = client.get('/medecin/suivi-chronique/')

        if response.status_code == 200:
            print("✅ Page accessible (status 200)")

            content = response.content.decode('utf-8')
            print(f"📏 Taille: {len(content)} caractères")

            # Vérifications du template complet
            checks = [
                ("Interface complète", len(content) > 5000),
                ("Cartes statistiques", "card border-left-primary" in content),
                ("Tableau", "table table-hover" in content),
                ("Boutons d'action", "btn btn-primary" in content),
                ("Icônes FontAwesome", "fas fa-" in content),
            ]

            print("\n🔍 Vérifications template complet:")
            for check_name, check_result in checks:
                status = "✅" if check_result else "⚠️"
                print(f"   {status} {check_name}")
... (tronqué)

# ============================================================
# ORIGINE 81: test_template_suivi.py (2025-11-28)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    from django.test import Client
    from medecin.models import Medecin

    def test_template_suivi():
        print("🧪 TEST DU TEMPLATE SUIVI CHRONIQUE")
        print("=" * 40)

        client = Client()

        # Vérifier médecin
        try:
            medecin = Medecin.objects.get(user__username='medecin_test')
            print(f"✅ Médecin: Dr {medecin.user.first_name} {medecin.user.last_name}")
        except Medecin.DoesNotExist:
            print("❌ Médecin non trouvé")
            return

        # Connexion
        print("🔑 Connexion...")
        if not client.login(username='medecin_test', password='password123'):
            print("❌ Échec connexion")
            return
        print("✅ Connecté")

        # Test de la page suivi chronique
        print("\n🚀 Test page suivi chronique...")
        response = client.get('/medecin/suivi-chronique/')

        if response.status_code == 200:
            print("✅ Page accessible (status 200)")

            # Vérifier le contenu
            content = response.content.decode('utf-8')

            # Vérifications importantes
            checks = [
                ('Structure HTML', '<html' in content.lower() or '<!DOCTYPE' in content.lower()),
                ('Titre', 'suivi' in content.lower() or 'chronique' in content.lower()),
                ('Développement', 'développement' in content.lower() or 'development' in content.lower()),
                ('Bouton retour', 'tableau de bord' in content.lower() or 'dashboard' in content.lower())
... (tronqué)

# ============================================================
# ORIGINE 82: test_interface_complet.py (2025-11-28)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    from django.test import Client
    from medecin.models import Medecin

    def test_interface_complet():
        print("🎯 TEST COMPLET INTERFACE MÉDECIN")
        print("=" * 50)

        client = Client()

        # Vérifier que le médecin existe
        try:
            medecin = Medecin.objects.get(user__username='medecin_test')
            print(f"✅ Médecin de test trouvé: Dr {medecin.user.first_name} {medecin.user.last_name}")
        except Medecin.DoesNotExist:
            print("❌ Médecin de test non trouvé")
            print("📋 Exécutez d'abord: python creer_medecin_exact.py")
            return

        # URLs principales à tester (basées sur medecin/urls.py)
        urls_principales = [
            ('/medecin/dashboard/', 'Dashboard principal'),
            ('/medecin/', 'Accueil (redirection)'),
            ('/medecin/bons/', 'Liste des bons'),
            ('/medecin/bons/attente/', 'Bons en attente'),
            ('/medecin/ordonnances/', 'Mes ordonnances'),
            ('/medecin/profil/', 'Profil médecin'),
            ('/medecin/statistiques/', 'Statistiques'),
        ]

        print("\n1. 🔐 TESTS SANS CONNEXION (redirections attendues):")
        for url, description in urls_principales[:3]:  # Tester seulement 3 URLs
            response = client.get(url)
            if response.status_code == 302:
                print(f"   ✅ {description}: Redirection vers → {response.url}")
            else:
                print(f"   ❌ {description}: Status {response.status_code} (attendu: 302)")

        print("\n2. 🔑 CONNEXION AU COMPTE MÉDECIN...")
        login_success = client.login(username='medecin_test', password='password123')
        print(f"   ✅ Connexion réussie: {login_success}")
... (tronqué)

# ============================================================
# ORIGINE 83: test_interface_medecin_complet.py (2025-11-27)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    from django.test import Client
    from django.contrib.auth.models import User
    from medecin.models import Medecin

    def test_interface_medecin_complet():
        print("🎯 TEST COMPLET INTERFACE MÉDECIN")
        print("=" * 50)

        client = Client()

        # 1. Vérifier que le médecin existe
        print("1. 🔍 Vérification médecin...")
        try:
            user = User.objects.get(username='medecin_test')
            medecin = Medecin.objects.get(user=user)
            print(f"   ✅ Médecin prêt: Dr {medecin.prenom} {medecin.nom}")
        except (User.DoesNotExist, Medecin.DoesNotExist):
            print("   ❌ Médecin de test non trouvé")
            print("   📋 Exécutez d'abord: python creer_medecin_corrige.py")
            return

        # 2. Test sans connexion (doit rediriger vers login)
        print("\n2. 🔒 Test accès sans connexion...")
        urls_sans_connexion = [
            '/medecin/dashboard/',
            '/medecin/bons/',
            '/medecin/ordonnances/'
        ]

        for url in urls_sans_connexion:
            response = client.get(url)
            status_icon = "✅" if response.status_code == 302 else "❌"
            print(f"   {status_icon} {url} -> Status: {response.status_code}", end="")
            if response.status_code == 302:
                print(f" (Redirection vers: {response.url})")
            else:
                print()

        # 3. Connexion
        print("\n3. 🔑 Connexion...")
... (tronqué)

# ============================================================
# ORIGINE 84: test_template_direct.py (2025-11-27)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    from django.test import Client
    from django.contrib.auth.models import User

    def test_connexion_medecin():
        print("🔐 TEST CONNEXION MÉDECIN:")
        print("=" * 40)

        client = Client()

        # 1. Essayer d'accéder sans connexion
        print("1. Accès sans connexion...")
        response = client.get('/medecin/tableau-de-bord/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 302:
            print(f"   Redirection vers: {response.url}")

        # 2. Se connecter
        print("2. Connexion...")
        user = User.objects.get(username='medecin_test')
        login_success = client.login(username='medecin_test', password='password123')
        print(f"   Login réussi: {login_success}")

        if login_success:
            # 3. Accéder après connexion
            print("3. Accès après connexion...")
            response = client.get('/medecin/tableau-de-bord/')
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                print("   ✅ SUCCÈS - Template affiché")
                print(f"   Content-Type: {response.get('Content-Type', 'Non spécifié')}")
                print(f"   Taille du contenu: {len(response.content)} bytes")
            else:
                print(f"   ❌ Échec - Status: {response.status_code}")
                if response.status_code == 302:
                    print(f"   Redirection vers: {response.url}")

    test_connexion_medecin()

except Exception as e:
... (tronqué)

# ============================================================
# ORIGINE 85: test_systeme_propre.py (2025-11-27)
# ============================================================

#!/usr/bin/env python
"""
TEST FINAL - SYSTÈME PROPRE
"""

import os
import sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre, Bon
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

def test_systeme_propre():
    print("🎯 TEST SYSTÈME PROPRE")
    print("=" * 40)

    try:
        # 1. Vérifier les utilisateurs
        medecin = User.objects.get(username='medecin_test')
        agent = User.objects.get(username='test_agent')
        membre = Membre.objects.first()

        print(f"👨‍⚕️ Médecin: {medecin.username}")
        print(f"👤 Agent: {agent.username}")
        print(f"👥 Membre: {membre.nom} {membre.prenom}")

        # 2. Créer un bon avec la nouvelle structure
        bon = Bon.objects.create(
            membre=membre,
            type_soin='CONSULT',
            description='Test système propre - consultation générale',
            lieu_soins='Centre Médical Principal',
            date_soins=timezone.now().date(),
            medecin_traitant=medecin,  # ✅ ForeignKey fonctionnelle
            montant_total=12500,
            statut='BROUILLON'
        )

        print(f"\n✅ BON CRÉÉ:")
        print(f"   📋 Numéro: {bon.numero_bon}")
        print(f"   👨‍⚕️ Médecin: {bon.medecin_traitant.username}")
        print(f"   💰 Montant: {bon.montant_total} FCFA")
        print(f"   📊 Statut: {bon.statut}")

        # 3. Test de filtrage par médecin
... (tronqué)

# ============================================================
# ORIGINE 86: test_nouvelle_relation.py (2025-11-27)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT AVEC NOUVEAU MODÈLE - TEST RELATION MÉDECIN
"""

import os
import sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre, Bon
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

def test_nouvelle_relation():
    print("🔧 TEST AVEC NOUVELLE RELATION MÉDECIN")
    print("=" * 45)

    try:
        medecin = User.objects.get(username='medecin_test')
        membre = Membre.objects.first()

        print(f"👨‍⚕️ Médecin: {medecin.username}")
        print(f"👥 Membre: {membre.nom} {membre.prenom}")

        # Création avec la nouvelle relation
        bon = Bon.objects.create(
            membre=membre,
            type_soin='CONSULT',
            description='Test avec relation médecin',
            medecin_traitant=medecin,  # ✅ Maintenant un objet User
            montant_total=7500,
            statut='BROUILLON'
        )

        print(f"\n✅ BON CRÉÉ AVEC RELATION:")
        print(f"   📋 Numéro: {bon.numero_bon}")
        print(f"   👨‍⚕️ Médecin: {bon.medecin_traitant.username}")
        print(f"   📊 Statut: {bon.statut}")

        # Test: Vérifier que le médecin peut voir ses bons
        print(f"\n🔍 BONS DU MÉDECIN {medecin.username}:")
        bons_medecin = Bon.objects.filter(medecin_traitant=medecin)
        print(f"   Nombre de bons: {bons_medecin.count()}")

        for bon_med in bons_medecin:
            print(f"   - {bon_med.numero_bon} | {bon_med.membre.nom} | {bon_med.statut}")
... (tronqué)

# ============================================================
# ORIGINE 87: test_workflow_bon.py (2025-11-27)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE TEST WORKFLOW BON DE SOIN
Création par Agent → Réception par Médecin → Validation
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre, Bon
from soins.models import Soin
from medecin.models import Ordonnance
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class TestWorkflowBon:
    """Classe de test pour le workflow complet des bons de soin"""

    def __init__(self):
        self.client = Client()
        self.agent = None
        self.medecin = None
        self.membre = None
        self.bon_created = None

    def print_step(self, step, message):
        """Affiche une étape du test"""
        print(f"\n{'='*60}")
        print(f"📋 ÉTAPE {step}: {message}")
        print(f"{'='*60}")

    def print_success(self, message):
        """Affiche un succès"""
        print(f"✅ {message}")

    def print_error(self, message):
        """Affiche une erreur"""
        print(f"❌ {message}")

    def print_info(self, message):
        """Affiche une information"""
... (tronqué)

# ============================================================
# ORIGINE 88: test_workflow_complet.py (2025-11-27)
# ============================================================

#!/usr/bin/env python
import os
import sys
import django
from django.test import Client
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from membres.models import Membre, Bon

User = get_user_model()

def reinitialiser_mots_de_passe():
    """Réinitialise les mots de passe des utilisateurs de test"""
    print("🔑 RÉINITIALISATION DES MOTS DE PASSE")

    users_to_reset = ['test_agent', 'assureur_test', 'medecin_test', 'test_pharmacien']

    for username in users_to_reset:
        try:
            user = User.objects.get(username=username)
            user.password = make_password('pass123')
            user.save()
            print(f"✅ {username}: Mot de passe réinitialisé à 'pass123'")
        except User.DoesNotExist:
            print(f"❌ {username}: N'existe pas")

def test_complet_avec_mots_de_passe():
    print("🔄 TEST COMPLET AVEC MOTS DE PASSE CORRIGÉS")

    # 1. RÉINITIALISER LES MOTS DE PASSE
    reinitialiser_mots_de_passe()

    # 2. TEST DES CONNEXIONS
    print("\n1. 🔐 TEST DES CONNEXIONS")
    client = Client()

    tests = [
        ('test_agent', 'pass123', '/agents/tableau-de-bord/', 'Agent'),
        ('assureur_test', 'pass123', '/assureur/dashboard/', 'Assureur'),
        ('medecin_test', 'pass123', '/medecin/dashboard/', 'Médecin'),
        ('test_pharmacien', 'pass123', '/pharmacien/dashboard/', 'Pharmacien')
    ]

    for username, password, url, role in tests:
        print(f"   {role} ({username}):", end=" ")

... (tronqué)

# ============================================================
# ORIGINE 89: test_interactions_temps_reel.py (2025-11-27)
# ============================================================

# test_interactions_temps_reel.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_vue_acteur(utilisateur, url, nom_acteur):
    """Teste l'accès d'un acteur à une vue spécifique"""
    client = Client()

    # Simuler la connexion
    if client.login(username=utilisateur.username, password='test123'):
        response = client.get(url)
        if response.status_code == 200:
            print(f"   ✅ {nom_acteur} peut accéder à {url}")
            return True
        else:
            print(f"   ❌ {nom_acteur} ne peut pas accéder à {url} (Status: {response.status_code})")
            return False
    else:
        print(f"   ❌ {nom_acteur} - Échec connexion")
        return False

print("🔐 TEST DES PERMISSIONS EN TEMPS RÉEL")

# Test avec différents utilisateurs
try:
    # Récupérer un utilisateur de test pour chaque rôle
    test_agent = User.objects.filter(username__icontains='agent').first()
    test_assureur = User.objects.filter(username__icontains='assureur').first()
    test_medecin = User.objects.filter(username__icontains='medecin').first()
    test_pharmacien = User.objects.filter(username__icontains='pharmacien').first()

    if test_agent:
        test_vue_acteur(test_agent, '/agents/tableau-de-bord/', 'Agent')
        test_vue_acteur(test_agent, '/agents/verification-cotisations/', 'Agent')

    if test_assureur:
        test_vue_acteur(test_assureur, '/assureur/dashboard/', 'Assureur')
        test_vue_acteur(test_assureur, '/assureur/cotisations/', 'Assureur')

    if test_medecin:
        test_vue_acteur(test_medecin, '/medecin/dashboard/', 'Médecin')
... (tronqué)

# ============================================================
# ORIGINE 90: test_reel_avec_votre_compte.py (2025-11-27)
# ============================================================

# test_reel_avec_votre_compte.py
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre

def test_reel_avec_votre_compte():
    """Test pour vérifier que vous pouvez créer des membres avec votre compte réel"""
    print("🎯 TEST RÉEL - CRÉATION AVEC VOTRE COMPTE")
    print("=" * 50)

    # Vérifier l'état actuel
    total_avant = Membre.objects.count()
    print(f"📊 Membres en base: {total_avant}")

    print("\n💡 INSTRUCTIONS:")
    print("1. Allez sur: http://127.0.0.1:8000/agents/creer-membre/")
    print("2. Connectez-vous avec votre compte agent")
    print("3. Créez un nouveau membre avec ces données:")
    print("   - Nom: TestReel")
    print("   - Prénom: VotrePrenom")
    print("   - Téléphone: 0100000000")
    print("   - Email: test.reel@example.com")
    print("4. Revenez ici et appuyez sur Entrée...")

    input("\n⏳ Appuyez sur Entrée après avoir créé le membre...")

    # Vérifier le résultat
    total_apres = Membre.objects.count()
    print(f"\n📊 Résultat:")
    print(f"   Membres avant: {total_avant}")
    print(f"   Membres après: {total_apres}")

    if total_apres > total_avant:
        print("🎉 SUCCÈS ! Le membre a été créé via l'interface web")

        # Trouver le nouveau membre
        nouveau_membre = Membre.objects.filter(nom="TestReel").first()
        if nouveau_membre:
            print(f"📋 Détails du membre créé:")
            print(f"   - ID: {nouveau_membre.id}")
            print(f"   - Nom: {nouveau_membre.prenom} {nouveau_membre.nom}")
            print(f"   - Numéro: {getattr(nouveau_membre, 'numero_unique', 'N/A')}")
            print(f"   - Téléphone: {nouveau_membre.telephone}")
... (tronqué)

# ============================================================
# ORIGINE 91: test_manuel_creation.py (2025-11-27)
# ============================================================

# test_manuel_creation.py
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre

def test_manuel_rapide():
    """Test manuel rapide de la création de membre"""
    print("🎯 TEST MANUEL RAPIDE - CRÉATION MEMBRE")
    print("=" * 50)

    # 1. Vérifier l'état actuel
    total_avant = Membre.objects.count()
    print(f"1. Membres en base avant test: {total_avant}")

    # 2. Créer un membre de test manuellement
    try:
        nouveau_membre = Membre.objects.create(
            nom="TEST_MANUEL",
            prenom="Diagnostic",
            telephone="0100000000",
            email="test.manuel@example.com",
            numero_unique="MEMTEST123",
            statut="actif"
        )
        print("2. ✅ Membre de test créé manuellement")
        print(f"   ID: {nouveau_membre.id}")
        print(f"   Numéro: {nouveau_membre.numero_unique}")

        # 3. Vérifier la persistance
        total_apres = Membre.objects.count()
        print(f"3. Membres en base après création: {total_apres}")

        if total_apres > total_avant:
            print("   ✅ Données persistées en base")
        else:
            print("   ❌ Données non persistées")

        # 4. Nettoyer (optionnel)
        nouveau_membre.delete()
        print("4. ✅ Membre de test supprimé (nettoyage)")

    except Exception as e:
        print(f"❌ Erreur création manuelle: {e}")
... (tronqué)

# ============================================================
# ORIGINE 92: test_integration_finale.py (2025-11-27)
# ============================================================

# test_integration_finale.py - VERSION CORRIGÉE AVEC MATRICULE UNIQUE
import os
import django
import sys
from datetime import date
import random
import string

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from membres.models import Membre
from agents.models import Agent, VerificationCotisation

def generer_matricule_unique():
    """Génère un matricule unique pour les tests"""
    lettres = ''.join(random.choices(string.ascii_uppercase, k=3))
    chiffres = ''.join(random.choices(string.digits, k=3))
    return f"TEST-{lettres}{chiffres}"

class TestIntegrationAffichageUnifie(TestCase):
    def setUp(self):
        self.client = Client()

        # Générer des identifiants uniques pour éviter les conflits
        timestamp = str(random.randint(1000, 9999))
        username = f"agent_test_{timestamp}"
        matricule = generer_matricule_unique()
        numero_membre = f"TESTMEM{timestamp}"

        self.user = User.objects.create_user(
            username=username,
            password='password123',
            first_name='Jean',
            last_name='Agent'
        )

        # CORRECTION : Matricule unique
        self.agent = Agent.objects.create(
            user=self.user,
            matricule=matricule,
            poste='Agent de terrain',
            date_embauche=date.today(),
            limite_bons_quotidienne=10,
            est_actif=True
        )
... (tronqué)

# ============================================================
# ORIGINE 93: test_systeme_rapide.py (2025-11-27)
# ============================================================

# test_systeme_rapide.py
import os
import django
import sys
from datetime import date

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from membres.models import Membre
from agents.models import Agent

def test_systeme_rapide():
    print("🚀 TEST RAPIDE DU SYSTÈME")
    print("=" * 50)

    client = Client()

    # Test 1: Vérification des URLs principales
    print("1. 🔗 TEST DES URLs:")

    urls = [
        '/',
        '/agents/tableau-de-bord/',
        '/agents/liste-membres/',
        '/agents/verification-cotisations/',
    ]

    for url in urls:
        try:
            response = client.get(url)
            status = "✅ 200" if response.status_code == 200 else f"⚠️ {response.status_code}"
            print(f"   {url} -> {status}")
        except Exception as e:
            print(f"   {url} -> ❌ {e}")

    # Test 2: Vérification des modèles
    print("\n2. 📊 TEST DES MODÈLES:")

    try:
        user_count = User.objects.count()
        print(f"   👥 Utilisateurs: {user_count}")
    except Exception as e:
        print(f"   👥 Utilisateurs: ❌ {e}")

    try:
... (tronqué)

# ============================================================
# ORIGINE 94: test_flux_cotisations.py (2025-11-27)
# ============================================================

# test_flux_cotisations.py
import os
import sys
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

print("🧪 TEST DU FLUX COTISATIONS ASSUREUR → AGENT")
print("=" * 50)

class TestFluxCotisations:
    def __init__(self):
        self.resultats = []

    def tester_import_modeles(self):
        """Teste l'importation des modèles nécessaires"""
        print("1. 🔧 TEST IMPORT MODÈLES...")

        try:
            from membres.models import Membre
            self.resultats.append(('Membre', '✅ Importé'))
            print("   ✅ Membre importé")
        except ImportError as e:
            self.resultats.append(('Membre', f'❌ {e}'))
            print(f"   ❌ Membre: {e}")

        try:
            from membres.models import Cotisation
            self.resultats.append(('Cotisation', '✅ Importé'))
            print("   ✅ Cotisation importé")
        except ImportError as e:
            self.resultats.append(('Cotisation', f'❌ {e}'))
            print(f"   ❌ Cotisation: {e}")

        try:
            from assureur.models import Assureur
            self.resultats.append(('Assureur', '✅ Importé'))
            print("   ✅ Assureur importé")
        except ImportError as e:
            self.resultats.append(('Assureur', f'❌ {e}'))
            print(f"   ❌ Assureur: {e}")

        try:
            from agents.models import Agent, VerificationCotisation
            self.resultats.append(('Agent', '✅ Importé'))
            self.resultats.append(('VerificationCotisation', '✅ Importé'))
... (tronqué)

# ============================================================
# ORIGINE 95: test_creation_membre.py (2025-11-26)
# ============================================================

# test_creation_membre.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from django.utils import timezone
import random
import string

def test_creation_membre():
    print("🧪 TEST CRÉATION MEMBRE")
    print("=" * 40)

    # Compter avant
    avant = Membre.objects.count()
    print(f"📊 Membres avant: {avant}")

    # Créer un membre
    try:
        # Générer numéro unique
        lettres = ''.join(random.choices(string.ascii_uppercase, k=3))
        chiffres = ''.join(random.choices(string.digits, k=3))
        numero_unique = f"TEST{lettres}{chiffres}"

        nouveau_membre = Membre.objects.create(
            nom="TEST",
            prenom="Roger",
            telephone="0102030405",
            numero_unique=numero_unique,
            statut='actif'
        )

        print(f"✅ Membre créé - ID: {nouveau_membre.id}")
        print(f"   📝 Nom: {nouveau_membre.prenom} {nouveau_membre.nom}")
        print(f"   🔑 Numéro: {numero_unique}")

        # Compter après
        apres = Membre.objects.count()
        print(f"📊 Membres après: {apres}")
        print(f"📈 Différence: {apres - avant}")

        # Test recherche immédiate
        from django.db.models import Q
        resultats = Membre.objects.filter(
            Q(nom__icontains="TEST") |
            Q(prenom__icontains="Roger")
        )
... (tronqué)

# ============================================================
# ORIGINE 96: test_recherche_temps_reel.py (2025-11-26)
# ============================================================

#!/usr/bin/env python
"""
TEST EN TEMPS RÉEL - CRÉATION/RECHERCHE MEMBRE (CORRIGÉ)
"""

import os
import sys
import django
from django.db.models import Q
import random
import string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from membres.models import Membre
from django.utils import timezone
import time

def generer_numero_unique():
    """Génère un numéro unique aléatoire pour éviter les conflits"""
    lettres = ''.join(random.choices(string.ascii_uppercase, k=3))
    chiffres = ''.join(random.choices(string.digits, k=3))
    return f"MEM{lettres}{chiffres}"

def test_temps_reel():
    """Test de création et recherche immédiate d'un membre"""

    print("🧪 TEST TEMPS RÉEL - CRÉATION/RECHERCHE (CORRIGÉ)")
    print("=" * 60)

    # 1. Compter les membres avant
    avant = Membre.objects.count()
    print(f"📊 Membres avant test: {avant}")

    # 2. Créer un membre unique avec numéro unique aléatoire
    timestamp = int(time.time())
    numero_unique = generer_numero_unique()

    try:
        membre_test = Membre.objects.create(
            nom=f"TEST_{timestamp}",
            prenom=f"Recherche_{timestamp}",
            telephone=f"01{timestamp % 100000000:08d}",
            numero_unique=numero_unique,  # NUMÉRO UNIQUE UNIQUE !
            statut="actif"
        )

... (tronqué)

# ============================================================
# ORIGINE 97: test_validation_finale.py (2025-11-20)
# ============================================================

import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate
from soins.models import BonDeSoin
import json

def test_validation_finale():
    """Test de validation finale complète du système"""
    print("🎯 VALIDATION FINALE DU SYSTÈME")
    print("===============================")

    client = Client()
    user = authenticate(username='agent_operateur', password='agent123')

    if not user:
        print("❌ Authentification échouée")
        return False

    client.force_login(user)
    print("✅ Authentification réussie")

    # 1. Test de l'API details_bon_soin_api
    print("\n1. 🔍 TEST API DÉTAILS BONS")
    bon = BonDeSoin.objects.first()

    response = client.get(f'/api/agents/bons/{bon.id}/details/')
    if response.status_code == 200:
        data = json.loads(response.content)
        if data.get('success'):
            bon_data = data['bon']
            print(f"   ✅ API fonctionnelle - Bon #{bon_data.get('code')}")

            # Vérifier que tous les champs sont présents et non "undefined"
            champs_requis = ['code', 'membre', 'montant_max', 'statut', 'date_creation',
                           'date_expiration', 'temps_restant', 'motif', 'type_soin', 'urgence']

            champs_manquants = []
            for champ in champs_requis:
                if champ not in bon_data or bon_data[champ] is None:
                    champs_manquants.append(champ)

            if not champs_manquants:
... (tronqué)

# ============================================================
# ORIGINE 98: test_route_globale.py (2025-11-20)
# ============================================================

import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate
from soins.models import BonDeSoin
import json

def test_route_globale():
    """Tester la route globale de l'API"""
    print("🧪 TEST ROUTE GLOBALE API")
    print("========================")

    client = Client()
    user = authenticate(username='agent_operateur', password='agent123')

    if not user:
        print("❌ Authentification échouée")
        return False

    client.force_login(user)
    print("✅ Authentification réussie")

    # Récupérer un bon existant
    bon = BonDeSoin.objects.first()
    if not bon:
        print("❌ Aucun bon de soin trouvé")
        return False

    print(f"🔍 Test avec le bon ID: {bon.id}")

    # Tester l'ancienne route (devrait fonctionner)
    print("\n1. 🔗 TEST ANCIENNE ROUTE (/agents/api/...)")
    response_ancienne = client.get(f'/agents/api/bons/{bon.id}/details/')
    print(f"   📡 Statut: {response_ancienne.status_code}")

    # Tester la nouvelle route globale (celle que l'interface utilise)
    print("\n2. 🔗 TEST NOUVELLE ROUTE (/api/agents/...)")
    response_nouvelle = client.get(f'/api/agents/bons/{bon.id}/details/')
    print(f"   📡 Statut: {response_nouvelle.status_code}")

    if response_nouvelle.status_code == 200:
        try:
            data = json.loads(response_nouvelle.content)
... (tronqué)

# ============================================================
# ORIGINE 99: test_details_bons.py (2025-11-20)
# ============================================================

import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate
from soins.models import BonDeSoin
import json

def test_details_bons():
    """Tester l'API des détails des bons"""
    print("🧪 TEST API DÉTAILS BONS")
    print("========================")

    client = Client()
    user = authenticate(username='agent_operateur', password='agent123')

    if not user:
        print("❌ Authentification échouée")
        return False

    client.force_login(user)
    print("✅ Authentification réussie")

    # Récupérer un bon existant
    bon = BonDeSoin.objects.first()
    if not bon:
        print("❌ Aucun bon de soin trouvé")
        return False

    print(f"🔍 Test avec le bon ID: {bon.id}")

    # Tester l'API
    response = client.get(f'/agents/api/bons/{bon.id}/details/')
    print(f"📡 Statut API: {response.status_code}")

    if response.status_code == 200:
        try:
            data = json.loads(response.content)
            print("✅ API fonctionnelle!")
            print(f"📋 Données reçues:")
            if data.get('success'):
                bon_data = data['bon']
                print(f"   👤 Patient: {bon_data.get('patient')}")
                print(f"   📅 Date soin: {bon_data.get('date_soin')}")
... (tronqué)

# ============================================================
# ORIGINE 100: test_final_complet.py (2025-11-20)
# ============================================================

import os
import django
import sys
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate
from soins.models import BonDeSoin
from membres.models import Membre
from agents.models import Agent
import json

def test_final_complet():
    """Test final complet du système"""
    print("🎯 TEST FINAL COMPLET")
    print("====================")

    client = Client()

    # 1. Authentification
    print("\n1. 🔐 AUTHENTIFICATION AGENT")
    user = authenticate(username='agent_operateur', password='agent123')

    if not user:
        print("   ❌ Échec authentification agent")
        return False

    client.force_login(user)
    print("   ✅ Authentification agent réussie")

    # Vérifier l'agent associé
    try:
        agent = Agent.objects.get(user=user)
        print(f"   👨‍💼 Agent: {agent.matricule} - {agent.poste}")
    except:
        print("   ❌ Aucun agent associé")
        return False

    # 2. Test des pages principales
    print("\n2. 🌐 TEST PAGES PRINCIPALES")

    pages = {
        '/agents/tableau-de-bord/': 'Tableau de bord',
        '/agents/creer-bon-soin/': 'Création bons',
        '/agents/liste-membres/': 'Liste membres'
... (tronqué)

# ============================================================
# ORIGINE 101: test_interface_web.py (2025-11-20)
# ============================================================

import os
import django
import sys
import time
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate
from soins.models import BonDeSoin

def test_interface_web_complete():
    """Test complet de l'interface web"""
    print("🌐 TEST INTERFACE WEB COMPLÈTE")
    print("==============================")

    client = Client()

    # 1. Authentification
    print("\n1. 🔐 AUTHENTIFICATION")
    user = authenticate(username='agent_operateur', password='agent123')

    if not user:
        print("   ❌ Échec authentification")
        return False

    client.force_login(user)
    print("   ✅ Authentification réussie")

    # 2. Test du tableau de bord
    print("\n2. 📊 TEST TABLEAU DE BORD")
    response = client.get('/agents/tableau-de-bord/')
    print(f"   Status: {response.status_code}")

    if response.status_code == 200:
        print("   ✅ Tableau de bord accessible")
        # Vérifier le contenu
        content = response.content.decode('utf-8')
        if 'tableau de bord' in content.lower():
            print("   ✅ Contenu correct détecté")
    else:
        print("   ❌ Tableau de bord inaccessible")

    # 3. Test de la liste des membres
    print("\n3. 👥 TEST LISTE MEMBRES")
    response = client.get('/agents/liste-membres/')
... (tronqué)

# ============================================================
# ORIGINE 102: test_complet_final.sh (2025-11-20)
# ============================================================

#!/bin/bash

echo "🚀 TEST COMPLET FINAL - SYSTÈME MUTUELLE"
echo "========================================"

# 1. Vérification de base
echo ""
echo "1. 🔍 VÉRIFICATION BASE DE DONNÉES"
python scripts/test_final_validation.py

# 2. Correction redirections
echo ""
echo "2. 🔧 CORRECTION REDIRECTIONS"
python scripts/correction_redirection_admin.py

# 3. Test création avec médecin
echo ""
echo "3. 🧪 TEST CRÉATION AVEC MÉDECIN"
python scripts/correction_medecin_final.py

# 4. Résumé final
echo ""
echo "4. 📊 RÉSUMÉ FINAL"
python manage.py shell << EOF
from soins.models import BonDeSoin
from membres.models import Membre
from agents.models import Agent

print("📈 STATISTIQUES FINALES:")
print(f"   👤 Membres: {Membre.objects.count()}")
print(f"   👨‍💼 Agents: {Agent.objects.count()}")
print(f"   📄 Bons de soin: {BonDeSoin.objects.count()}")

# Derniers bons créés
derniers = BonDeSoin.objects.order_by('-id')[:5]
print(f"   🆕 5 derniers bons:")
for bon in derniers:
    medecin = bon.medecin.username if bon.medecin else "Aucun"
    print(f"      - #{bon.id}: {bon.patient.nom_complet} | Médecin: {medecin} | Statut: {bon.statut}")
EOF

echo ""
echo "🎉 SYSTÈME PRÊT POUR LA PRODUCTION!"
echo "🌐 URLS DISPONIBLES:"
echo "   - Interface Admin: http://localhost:8000/admin/"
echo "   - Liste membres: http://localhost:8000/agents/liste-membres/"
echo "   - Création bons: http://localhost:8000/agents/creer-bon-soin/"
echo ""
echo "🔑 COMPTES TEST:"
echo "   - Superuser: koffitanoh / nouveau_mot_de_passe"
... (tronqué)

# ============================================================
# ORIGINE 103: test_final_validation.py (2025-11-20)
# ============================================================

import os
import django
import sys
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from soins.models import BonDeSoin
from membres.models import Membre
from agents.models import Agent
from django.contrib.auth.models import User

def test_final_validation():
    """Test final de validation du système"""
    print("🎯 TEST FINAL DE VALIDATION")
    print("===========================")

    print("📊 ÉTAT DU SYSTÈME:")
    print(f"   👤 Membres: {Membre.objects.count()}")
    print(f"   👨‍💼 Agents: {Agent.objects.count()}")
    print(f"   👨‍⚕️ Users: {User.objects.count()}")
    print(f"   📄 Bons de soin: {BonDeSoin.objects.count()}")

    # Test de création simple
    print("\n🧪 TEST CRÉATION SIMPLE:")
    try:
        membre = Membre.objects.first()

        bon = BonDeSoin.objects.create(
            patient=membre,
            date_soin=datetime.now().date(),
            symptomes="Test final de validation",
            diagnostic="Système opérationnel",
            statut="EN_ATTENTE",
            montant=15000.0
        )

        print(f"   ✅ Création réussie!")
        print(f"   🆕 Nouveau bon: #{bon.id}")

    except Exception as e:
        print(f"   ❌ Échec création: {e}")

    # Vérification finale
    print(f"\n📈 RÉSULTAT FINAL:")
    print(f"   📄 Total bons de soin: {BonDeSoin.objects.count()}")

... (tronqué)

# ============================================================
# ORIGINE 104: test_creation_simple.py (2025-11-20)
# ============================================================

import os
import django
import sys
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("🧪 TEST CRÉATION SIMPLIFIÉ")
print("==========================")

# Utiliser l'import direct comme dans le shell
try:
    # Ces imports fonctionnent dans le shell, utilisons la même méthode
    from django.apps import apps

    # Récupérer les modèles
    Membre = apps.get_model('member', 'Membre')
    BonDeSoin = apps.get_model('bon_soin', 'BonDeSoin')
    Agent = apps.get_model('agents', 'Agent')

    print("✅ Modèles chargés avec succès")

    # Compter les données
    print(f"📊 Membres: {Membre.objects.count()}")
    print(f"📊 Agents: {Agent.objects.count()}")
    print(f"📊 Bons de soin: {BonDeSoin.objects.count()}")

    # Créer un nouveau bon de soin
    membre = Membre.objects.first()
    agent = Agent.objects.first()

    print(f"👤 Membre: {membre.nom} {membre.prenom}")
    print(f"👨‍💼 Agent: {agent.nom_complet}")

    # Créer le bon
    bon = BonDeSoin.objects.create(
        membre=membre,
        agent_createur=agent,
        type_soin="Consultation générale",
        montant_total=15000.0,
        montant_remboursable=12000.0,
        date_soin=datetime.now().date(),
        statut="EN_ATTENTE",
        description="Test de création manuelle"
    )

    print(f"✅ BON CRÉÉ: {bon.numero_bon}")
... (tronqué)

# ============================================================
# ORIGINE 105: test_creation_manuel.py (2025-11-20)
# ============================================================

import os
import django
import sys
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from members.models import Membre
from bons_soins.models import BonDeSoin
from agents.models import Agent
from django.contrib.auth.models import User

def test_creation_bon_manuel():
    """Test manuel de création d'un bon de soin"""
    print("🧪 TEST MANUEL CRÉATION BON DE SOIN")
    print("===================================")

    # 1. Récupérer un membre
    try:
        membre = Membre.objects.first()
        print(f"👤 Membre sélectionné: {membre.nom} {membre.prenom}")
    except:
        print("❌ Aucun membre trouvé")
        return False

    # 2. Récupérer un agent
    try:
        agent = Agent.objects.first()
        print(f"👨‍💼 Agent sélectionné: {agent.nom_complet}")
    except:
        print("❌ Aucun agent trouvé")
        return False

    # 3. Créer un bon de soin directement
    try:
        bon = BonDeSoin.objects.create(
            membre=membre,
            agent_createur=agent,
            type_soin="Consultation générale",
            montant_total=15000.0,
            montant_remboursable=12000.0,
            date_soin=datetime.now().date(),
            statut="EN_ATTENTE",
            description="Consultation de routine"
        )
        print(f"✅ BON DE SOIN CRÉÉ AVEC SUCCÈS!")
        print(f"   Numéro: {bon.numero_bon}")
... (tronqué)

# ============================================================
# ORIGINE 106: test_manuel_rapide.py (2025-11-20)
# ============================================================

# test_manuel_rapide.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from agents.models import Agent

# Test le plus simple
client = Client()
agent = Agent.objects.first()

if agent:
    client.force_login(agent.user)
    response = client.get(reverse('agents:creer_bon_soin'))
    print(f"✅ Page création accessible: {response.status_code}")

    response = client.get(reverse('agents:rechercher_membre') + '?q=test')
    print(f"✅ API recherche fonctionne: {response.status_code}")
else:
    print("❌ Aucun agent trouvé")

# ============================================================
# ORIGINE 107: test_creation_bons.py (2025-11-20)
# ============================================================

# agents/tests/test_creation_bons.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class TestCreationBonSoin(TestCase):
    """Tests pour la création de bons de soin"""

    def setUp(self):
        """Configuration initiale"""
        self.client = Client()

        # Créer un utilisateur agent
        self.user_agent = User.objects.create_user(
            username='test_agent',
            password='test123',
            first_name='Test',
            last_name='Agent',
            email='test@agent.com'
        )

    def test_acces_sans_authentification(self):
        """Test d'accès sans authentification"""
        response = self.client.get(reverse('agents:creer_bon_soin'))
        self.assertIn(response.status_code, [302, 403])  # Redirection ou accès refusé

    def test_acces_avec_authentification(self):
        """Test d'accès avec authentification"""
        self.client.force_login(self.user_agent)
        response = self.client.get(reverse('agents:creer_bon_soin'))
        self.assertNotEqual(response.status_code, 500)  # Pas d'erreur serveur

    def test_api_recherche(self):
        """Test de l'API de recherche"""
        self.client.force_login(self.user_agent)
        response = self.client.get(reverse('agents:rechercher_membre') + '?q=test')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('success', data)

    def test_urls_existantes(self):
        """Test que les URLs principales existent"""
        urls = [
            'agents:dashboard',
            'agents:creer_bon_soin',
            'agents:rechercher_membre',
        ]

        for url_name in urls:
... (tronqué)

# ============================================================
# ORIGINE 108: test_fonctionnel_bons.py (2025-11-20)
# ============================================================

# scripts/test_fonctionnel_bons.py
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from agents.models import Agent, BonSoin
from membres.models import Membre

def test_fonctionnel_complet():
    print("🧪 TEST FONCTIONNEL COMPLET - CRÉATION BONS DE SOIN")
    print("=" * 60)

    client = Client()

    # 1. Trouver un agent existant
    agents = Agent.objects.all()
    if not agents.exists():
        print("❌ Aucun agent trouvé dans la base")
        return

    agent = agents.first()
    print(f"🎯 Agent sélectionné: {agent.user.get_full_name()} ({agent.matricule})")

    # 2. Se connecter en tant qu'agent
    client.force_login(agent.user)
    print("✅ Authentification réussie")

    # 3. Test de l'API de recherche
    print("\n🔍 TEST API RECHERCHE")
    print("-" * 30)

    # Test avec différents termes
    termes_recherche = ['Jean', 'Marie', 'MEM', '06']

    for terme in termes_recherche:
        response = client.get(reverse('agents:rechercher_membre') + f'?q={terme}')
        print(f"Recherche '{terme}': Status {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ {len(data['results'])} résultat(s) trouvé(s)")
                for result in data['results'][:3]:  # Afficher les 3 premiers
                    print(f"      - {result.get('nom_complet', 'N/A')}")
... (tronqué)

# ============================================================
# ORIGINE 109: test_creation_bons_macos.sh (2025-11-20)
# ============================================================

#!/bin/bash
# scripts/test_creation_bons_macos.sh

echo "🧪 SCRIPT DE TEST macOS - CRÉATION BONS DE SOIN"
echo "================================================"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️ $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️ $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Vérification Django
log_info "Vérification environnement Django..."
python -c "import django; print('Django version:', django.get_version())" || {
    log_error "Django non configuré"
    exit 1
}
log_success "Environnement Django OK"

# Diagnostic des modèles
log_info "Diagnostic des modèles..."
python diagnostic_models.py

# Test des URLs
log_info "Test des URLs..."
python manage.py shell << 'EOF'
from django.urls import reverse, NoReverseMatch

urls_a_tester = [
    'agents:dashboard',
    'agents:creer_bon_soin',
    'agents:rechercher_membre',
    'agents:details_membre',
]

print("🔗 Test des URLs agents:")
for url_name in urls_a_tester:
    try:
        url = reverse(url_name)
        print(f"   ✅ {url_name} -> {url}")
    except NoReverseMatch as e:
        print(f"   ❌ {url_name} -> Non trouvée: {e}")

... (tronqué)

# ============================================================
# ORIGINE 110: test_rapide.py (2025-11-20)
# ============================================================

# test_rapide.py
import os
import django
import sys

# Trouver automatiquement le nom du projet
current_dir = os.path.dirname(os.path.abspath(__file__))
project_name = None

for item in os.listdir(current_dir):
    if os.path.isdir(item) and 'settings.py' in os.listdir(item):
        project_name = item
        break

if project_name:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
    print(f"🎯 Projet détecté: {project_name}")
else:
    print("❌ Impossible de détecter le projet")
    sys.exit(1)

django.setup()

print("🧪 TEST RAPIDE - SYSTÈME AGENTS")
print("=" * 40)

from django.contrib.auth.models import User
from django.urls import reverse

print("1. Vérification des modèles...")
try:
    from agents.models import Agent
    from membres.models import Membre
    print("   ✅ Modèles importés")
except Exception as e:
    print(f"   ❌ Erreur modèles: {e}")

print("2. Vérification des URLs...")
try:
    urls = [
        ('Dashboard', 'agents:dashboard'),
        ('Créer bon', 'agents:creer_bon_soin'),
        ('Recherche', 'agents:rechercher_membre'),
    ]

    for nom, url_name in urls:
        try:
            url = reverse(url_name)
            print(f"   ✅ {nom}: {url}")
        except:
... (tronqué)

# ============================================================
# ORIGINE 111: test_creation_bons.py (2025-11-20)
# ============================================================

# agents/tests/test_creation_bons.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class TestCreationBonSoin(TestCase):
    """Tests pour la création de bons de soin"""

    def setUp(self):
        """Configuration initiale"""
        print("🔧 Configuration des tests...")
        self.client = Client()

    def test_basic_math(self):
        """Test mathématique basique"""
        self.assertEqual(1 + 1, 2)
        print("✅ Test mathématique basique réussi")

    def test_acces_sans_auth(self):
        """Test d'accès sans authentification"""
        response = self.client.get(reverse('agents:creer_bon_soin'))
        # Doit rediriger vers login (302) ou refuser l'accès (403)
        self.assertIn(response.status_code, [302, 403])
        print("✅ Accès sans auth correctement refusé")

    def test_acces_avec_auth(self):
        """Test d'accès avec authentification"""
        # Créer un utilisateur et se connecter
        user = User.objects.create_user('test_user', 'test@test.com', 'testpass')
        self.client.force_login(user)

        response = self.client.get(reverse('agents:creer_bon_soin'))
        # Peut être 200 (accès) ou 302/403 (pas agent)
        self.assertNotEqual(response.status_code, 500)
        print("✅ Pas d'erreur serveur avec auth")

    def test_api_recherche(self):
        """Test de l'API de recherche"""
        user = User.objects.create_user('test_user2', 'test2@test.com', 'testpass')
        self.client.force_login(user)

        response = self.client.get(reverse('agents:rechercher_membre') + '?q=test')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('success', data)
        print("✅ API recherche fonctionnelle")

# ============================================================
# ORIGINE 112: test_creation_bons_simple.sh (2025-11-20)
# ============================================================

#!/bin/bash
# scripts/test_creation_bons_simple.sh

echo "🧪 SCRIPT DE TEST SIMPLIFIÉ - CRÉATION BONS DE SOIN"
echo "==================================================="

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️ $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️ $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Vérification Django
log_info "Vérification environnement Django..."
python -c "import django; print('Django version:', django.get_version())" || {
    log_error "Django non configuré"
    exit 1
}
log_success "Environnement Django OK"

# Test des URLs de base
log_info "Test des URLs agents..."
python manage.py shell << EOF
from django.urls import reverse, NoReverseMatch

urls_a_tester = [
    'agents:dashboard',
    'agents:creer_bon_soin',
    'agents:rechercher_membre',
]

for url_name in urls_a_tester:
    try:
        url = reverse(url_name)
        print(f"✅ {url_name} -> {url}")
    except NoReverseMatch as e:
        print(f"❌ {url_name} -> ERREUR: {e}")
EOF

# Test des modèles
log_info "Test des modèles..."
python manage.py shell << EOF
try:
    from agents.models import Agent, BonSoin
... (tronqué)

# ============================================================
# ORIGINE 113: test_direct.py (2025-11-20)
# ============================================================

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

# ============================================================
# ORIGINE 114: test_creation_bons.py (2025-11-20)
# ============================================================

#!/bin/bash
# scripts/test_creation_bons.sh

echo "🧪 SCRIPT DE TEST MANUEL - CRÉATION BONS DE SOIN"
echo "================================================"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier que Django est configuré
log_info "Vérification de l'environnement Django..."
python -c "import django; print('Django version:', django.get_version())" || {
    log_error "Django n'est pas correctement configuré"
    exit 1
}

log_success "Environnement Django vérifié"

# Lancer les tests automatiques
log_info "Lancement des tests automatiques..."
python manage.py test agents.tests.test_creation_bons || {
    log_error "Les tests automatiques ont échoué"
    exit 1
}

log_success "Tests automatiques terminés avec succès"

echo ""
echo "🔍 TESTS MANUELS - CRÉATION DE BONS DE SOIN"
... (tronqué)

# ============================================================
# ORIGINE 115: test_charge_bons.py (2025-11-20)
# ============================================================

# scripts/test_charge_bons.py
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor
import threading

class TestChargeCreationBons:
    """Test de charge pour la création de bons de soin"""

    def __init__(self, base_url, nombre_utilisateurs=10, nombre_requetes=100):
        self.base_url = base_url
        self.nombre_utilisateurs = nombre_utilisateurs
        self.nombre_requetes = nombre_requetes
        self.resultats = []
        self.lock = threading.Lock()

    def creer_session_utilisateur(self, user_id):
        """Créer une session pour un utilisateur simulé"""
        session = requests.Session()
        # Ici, vous devriez implémenter la logique d'authentification
        return session

    def test_creation_bon(self, session, bon_id):
        """Tester la création d'un bon de soin"""
        debut = time.time()

        try:
            # Données du bon
            data = {
                'type_soin': 'consultation',
                'montant': '10000',
                'symptomes': f'Test charge {bon_id}',
                'diagnostic': f'Diagnostic charge {bon_id}'
            }

            # URL de création (à adapter)
            url = f"{self.base_url}/agents/creer-bon-soin/1/"  # ID membre 1 pour les tests

            response = session.post(url, data=data)
            duree = time.time() - debut

            with self.lock:
                self.resultats.append({
                    'bon_id': bon_id,
                    'statut': response.status_code,
                    'duree': duree,
                    'succes': response.status_code == 302  # Redirection après succès
                })

... (tronqué)

# ============================================================
# ORIGINE 116: test_actual_urls.py (2025-11-19)
# ============================================================

#!/usr/bin/env python
"""
Test mis à jour pour les URLs agents actuelles
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(str(Path(__file__).parent))

django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

def test_actual_agent_urls():
    """Teste les URLs agents réelles"""
    print("🔍 TEST DES URLs AGENTS RÉELLES")
    print("=" * 50)

    client = Client()

    # Utiliser l'utilisateur test_agent
    User = get_user_model()
    agent_user = User.objects.filter(username='test_agent').first()

    if not agent_user:
        print("❌ Utilisateur test_agent non trouvé")
        return

    print(f"👤 Utilisateur de test: {agent_user.username}")
    client.force_login(agent_user)

    # URLs réelles de votre configuration
    urls_to_test = [
        ('/agents/tableau-de-bord/', 'Tableau de bord'),
        ('/agents/creer-membre/', 'Créer membre'),
        ('/agents/liste-membres/', 'Liste membres'),
        ('/agents/verification-cotisations/', 'Vérification cotisations'),
        ('/agents/creer-bon-soin/', 'Créer bon de soin'),
        ('/agents/messages/', 'Messages'),
        ('/agents/notifications/', 'Notifications'),
        ('/agents/envoyer-message/', 'Envoyer message'),
    ]

    success_count = 0
... (tronqué)

# ============================================================
# ORIGINE 117: test_agent_urls.py (2025-11-19)
# ============================================================

#!/usr/bin/env python
"""
Test complet de toutes les URLs agents
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(str(Path(__file__).parent))

django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

def test_all_agent_urls():
    """Teste toutes les URLs agents avec un utilisateur connecté"""
    print("🔍 TEST COMPLET DES URLs AGENTS")
    print("=" * 60)

    client = Client()

    # Trouver un utilisateur agent pour se connecter
    User = get_user_model()
    agent_user = User.objects.filter(
        groups__name='Agents',
        is_active=True
    ).first()

    if not agent_user:
        print("❌ Aucun utilisateur agent trouvé pour les tests")
        # Essayer avec un utilisateur staff comme fallback
        agent_user = User.objects.filter(is_staff=True, is_active=True).first()
        if agent_user:
            print(f"⚠️  Utilisation d'un utilisateur staff comme fallback: {agent_user.username}")
        else:
            print("❌ Aucun utilisateur disponible pour les tests")
            return

    print(f"👤 Utilisateur de test: {agent_user.username}")
    client.force_login(agent_user)

    # Liste des URLs à tester
    urls_to_test = [
        ('/agents/', 'Accueil agents'),
        ('/agents/tableau-de-bord/', 'Tableau de bord'),
... (tronqué)

# ============================================================
# ORIGINE 118: test_connexion_manuel.py (2025-11-19)
# ============================================================

#!/usr/bin/env python
"""
Script de test manuel pour la connexion médecin
Usage: python test_connexion_manuel.py
"""

import os
import django
import sys
import requests
import json
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from medecin.models import MedecinProfile
from django.utils import timezone

User = get_user_model()

class TesteurConnexionMedecin:
    """Classe pour tester manuellement la connexion médecin"""

    def __init__(self, base_url="http://localhost:8000"):
        self.client = Client()
        self.base_url = base_url
        self.resultats = []

    def afficher_resultat(self, test_name, success, details=""):
        """Affiche le résultat d'un test"""
        statut = "✅ SUCCÈS" if success else "❌ ÉCHEC"
        print(f"{statut} {test_name}")
        if details:
            print(f"   Détails: {details}")
        print("-" * 50)

        self.resultats.append({
            'test': test_name,
            'success': success,
            'details': details,
            'timestamp': timezone.now().isoformat()
        })

    def test_connexion_valide(self):
        """Test de connexion avec des identifiants valides"""
... (tronqué)

# ============================================================
# ORIGINE 119: test_bon_soin.py (2025-11-19)
# ============================================================

# test_bon_soin.py
import os
import sys
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

try:
    django.setup()

    from membres.models import Membre
    from soins.models import BonDeSoin
    from django.contrib.auth.models import User
from django.utils import timezone

    def test_creation_bon_soin():
        print("🧪 TEST DE CRÉATION DE BON DE SOIN")
        print("-" * 50)

        # 1. Vérifier qu'il y a des membres
        membres = Membre.objects.all()[:5]
        if not membres:
            print("❌ Aucun membre trouvé dans la base de données")
            return

        print(f"✅ {len(membres)} membre(s) disponible(s)")

        # 2. Tester avec chaque membre
        for i, membre in enumerate(membres, 1):
            print(f"\n--- Test {i} avec {membre.prenom} {membre.nom} ---")

            try:
                # Essayer de créer un bon de soin
                bon = BonDeSoin.objects.create(
                    patient=membre,
                    date_soin=timezone.now().date(),
                    symptomes="Toux et fièvre",
                    diagnostic="Infection respiratoire",
                    montant=75.50,
                    statut='attente'
                )
                print(f"✅ SUCCÈS - Bon créé (ID: {bon.id})")

                # Afficher les détails du bon créé
                print(f"   Détails:")
                print(f"   - Patient: {bon.patient.prenom} {bon.patient.nom}")
                print(f"   - Montant: {bon.montant}")
                print(f"   - Statut: {bon.statut}")
... (tronqué)

# ============================================================
# ORIGINE 120: test_urls.py (2025-11-18)
# ============================================================

from django.test import TestCase
from django.urls import reverse

class URLTests(TestCase):
    """Tests pour les URLs de l'application assureur - VERSION CORRIGÉE"""

    def test_repondre_message_url(self):
        """Test que l'URL de réponse aux messages est correcte - VERSION CORRIGÉE"""
        # ✅ CORRECTION : Utiliser l'URL que vous avez réellement définie
        url = reverse('assureur:repondre_message', args=[1])
        # Votre URL est : 'repondre_message/<int:message_id>/'
        self.assertEqual(url, '/assureur/repondre_message/1/')

    def test_dashboard_url(self):
        """Test que l'URL du dashboard est correcte"""
        url = reverse('assureur:dashboard')
        self.assertEqual(url, '/assureur/dashboard/')

    def test_liste_membres_url(self):
        """Test que l'URL de la liste des membres est correcte"""
        url = reverse('assureur:liste_membres')
        self.assertEqual(url, '/assureur/membres/')

    def test_creer_membre_url(self):
        """Test que l'URL de création de membre est correcte"""
        url = reverse('assureur:creer_membre')
        self.assertEqual(url, '/assureur/creer-membre/')

    def test_liste_bons_url(self):
        """Test que l'URL de la liste des bons est correcte"""
        url = reverse('assureur:liste_bons')
        self.assertEqual(url, '/assureur/bons/')

    def test_creer_bon_url(self):
        """Test que l'URL de création de bon est correcte"""
        url = reverse('assureur:creer_bon', args=[1])
        self.assertEqual(url, '/assureur/bons/creer/1/')

    def test_liste_paiements_url(self):
        """Test que l'URL de la liste des paiements est correcte"""
        url = reverse('assureur:liste_paiements')
        self.assertEqual(url, '/assureur/paiements/')

    def test_liste_cotisations_url(self):
        """Test que l'URL de la liste des cotisations est correcte"""
        url = reverse('assureur:liste_cotisations')
        self.assertEqual(url, '/assureur/cotisations/')

    def test_configuration_url(self):
        """Test que l'URL de configuration est correcte"""
... (tronqué)

# ============================================================
# ORIGINE 121: test_assureur.py (2025-11-18)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE TEST DES FONCTIONNALITÉS ASSUREUR
Teste l'accès aux pages principales
"""

import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

def test_fonctionnalites():
    """Teste l'accès aux principales fonctionnalités"""
    print("🧪 TEST DES FONCTIONNALITÉS ASSUREUR")
    print("="*50)

    from django.test import Client
    from django.contrib.auth.models import User
    from assureur.models import Membre, Cotisation

    client = Client()

    # Trouver un utilisateur assureur
    user = User.objects.filter(assureur__isnull=False).first()
    if not user:
        user = User.objects.filter(is_staff=True).first()

    if not user:
        print("❌ Aucun utilisateur assureur trouvé pour les tests")
        return

    client.force_login(user)
    print(f"🔐 Utilisateur de test: {user.username}")

    # Pages à tester
    pages = [
        ('/assureur/dashboard/', 'Dashboard'),
        ('/assureur/membres/', 'Liste membres'),
        ('/assureur/bons/', 'Liste bons'),
        ('/assureur/paiements/', 'Liste paiements'),
        ('/assureur/cotisations/', 'Liste cotisations'),
        ('/assureur/configuration/', 'Configuration'),
        ('/assureur/messages/', 'Messages'),
    ]
... (tronqué)

# ============================================================
# ORIGINE 122: test_final_template.py (2025-11-17)
# ============================================================

# test_final_template.py
import os
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

def test_template_affichage():
    print("🎯 TEST FINAL DU TEMPLATE MÉDECIN")
    print("==================================================")

    # Vérifier que le template est accessible
    template_path = "templates/medecin/template2.html"
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Vérifications critiques
        checks = {
            "Extends base.html": '{% extends "base.html" %}' in content,
            "Block content": '{% block content %}' in content,
            "Conversation items": 'conversation-item' in content,
            "Nouveau message modal": 'nouveauMessageModal' in content,
            "Badges": 'badge bg-' in content,
            "Statistiques": 'patients_count' in content,
            "Bouton action": 'Nouveau Message' in content,
        }

        print("📋 VÉRIFICATION DU TEMPLATE:")
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"   {status} {check}")

        score = sum(checks.values())
        total = len(checks)

        print(f"📊 SCORE FINAL: {score}/{total} ({score/total*100:.0f}%)")

        if score == total:
            print("🎉 TEMPLATE 100% FONCTIONNEL ET PRÊT!")
            print("🌐 Accédez à: http://localhost:8000/medecin/tableau-de-bord/")
        else:
            print("⚠️  Quelques éléments manquent encore")

    # Vérifier les URLs médicin
    print("\n🔗 VÉRIFICATION DES URLs MÉDECIN:")
    urls_medecin = [
        '/medecin/tableau-de-bord/',
        '/medecin/bons-soin/',
        '/medecin/ordonnances/',
        '/medecin/rendez-vous/',
... (tronqué)

# ============================================================
# ORIGINE 123: test_simple_messagerie.py (2025-11-17)
# ============================================================

# test_simple_messagerie.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_simple():
    from django.contrib.auth.models import User
    from communication.models import Message

    print("🔍 TEST SIMPLE MESSAGERIE")
    print("=" * 40)

    # Compter les messages pour test_pharmacien
    try:
        pharmacien = User.objects.get(username='test_pharmacien')
        messages_recus = Message.objects.filter(destinataire=pharmacien).count()
        messages_envoyes = Message.objects.filter(expediteur=pharmacien).count()

        print(f"👤 Utilisateur: test_pharmacien")
        print(f"📥 Messages reçus: {messages_recus}")
        print(f"📤 Messages envoyés: {messages_envoyes}")
        print(f"📊 Total messages: {messages_recus + messages_envoyes}")

        if messages_recus + messages_envoyes == 0:
            print("\n💡 ASTUCE: Aucun message trouvé. Créez des messages de test.")
            print("   Allez sur: http://127.0.0.1:8000/agents/envoyer-message/")
            print("   Envoyez un message à test_pharmacien")

    except User.DoesNotExist:
        print("❌ Utilisateur test_pharmacien non trouvé")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_simple()

# ============================================================
# ORIGINE 124: test_solution.py (2025-11-17)
# ============================================================

# test_solution.py
import os
import django
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def tester_solution():
    print("TEST DE LA SOLUTION")
    print("=" * 50)

    # URLs qui fonctionnent MAINTENANT
    urls_valides = [
        'agents:liste_messages',
        'communication:envoyer_message',
        'communication:conversations',
        'communication:message_list'
    ]

    for url_name in urls_valides:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name:30} → {url}")
        except Exception as e:
            print(f"❌ {url_name:30} → ERREUR: {e}")

    print("\nUTILISEZ CES URLs DANS VOS TEMPLATES !")

if __name__ == "__main__":
    tester_solution()

# ============================================================
# ORIGINE 125: test_simple.html (2025-11-17)
# ============================================================

{% extends "base.html" %}

{% block title %}Test Messagerie Simplifié{% endblock %}

{% block content %}
<div class="container-fluid py-4">
    <div class="row">
        <div class="col-12">
            <div class="card shadow-lg">
                <div class="card-header bg-success text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-check me-2"></i>Test Messagerie - Version Simplifiée
                    </h4>
                </div>
                <div class="card-body">
                    <div class="alert alert-info">
                        <h5>✅ Système de Messagerie Opérationnel</h5>
                        <p class="mb-0">Cette page fonctionne ! Le problème était dans les URLs des autres templates.</p>
                    </div>

                    <div class="row text-center">
                        <div class="col-md-3 mb-3">
                            <div class="card border-primary">
                                <div class="card-body">
                                    <i class="fas fa-user fa-2x text-primary mb-2"></i>
                                    <h6>Membre</h6>
                                    <a href="{% url \'communication:messagerie_membre\' %}" class="btn btn-primary btn-sm">
                                        Accéder
                                    </a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="card border-success">
                                <div class="card-body">
                                    <i class="fas fa-shield-alt fa-2x text-success mb-2"></i>
                                    <h6>Assureur</h6>
                                    <a href="{% url \'communication:messagerie_assureur\' %}" class="btn btn-success btn-sm">
                                        Accéder
                                    </a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="card border-info">
                                <div class="card-body">
                                    <i class="fas fa-user-md fa-2x text-info mb-2"></i>
                                    <h6>Médecin</h6>
                                    <a href="/communication/medecin/messagerie/" class="btn btn-info btn-sm">
                                        Accéder
... (tronqué)

# ============================================================
# ORIGINE 126: test_urgence.html (2025-11-17)
# ============================================================

{% extends "base.html" %}

{% block title %}Test Messagerie - Correctif d'urgence{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="alert alert-warning">
        <h4>Correctif d'urgence - Système de Messagerie</h4>
        <p>Cette page fonctionne même si le reste du système a des problèmes.</p>
    </div>

    <div class="row">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5>Test du Modal</h5>
                </div>
                <div class="card-body text-center">
                    <button type="button" class="btn btn-success btn-lg"
                            data-bs-toggle="modal" data-bs-target="#testModal">
                        <i class="fas fa-bolt me-2"></i>Test Modal d'urgence
                    </button>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h5>Instructions</h5>
                </div>
                <div class="card-body">
                    <p>Si ce modal fonctionne, le problème vient des templates spécifiques.</p>
                    <p>Si ce modal ne fonctionne pas, le problème vient de Bootstrap.</p>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Modal de test d'urgence -->
<div class="modal fade" id="testModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header bg-success text-white">
                <h5 class="modal-title">✅ Modal de test</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Félicitations ! Le modal fonctionne correctement.</p>
                <p>Le problème vient probablement des templates spécifiques à la messagerie.</p>
... (tronqué)

# ============================================================
# ORIGINE 127: test_messagerie.html (2025-11-17)
# ============================================================

{% extends "base.html" %}
{% load static %}

{% block title %}Test Messagerie Multi-Acteurs{% endblock %}

{% block content %}
<div class="container-fluid py-4">
    <div class="row">
        <div class="col-12">
            <div class="card shadow-lg">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-envelope me-2"></i>Test des Interfaces Messagerie
                    </h4>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-3 mb-4">
                            <div class="card text-center border-primary">
                                <div class="card-body">
                                    <i class="fas fa-user fa-3x text-primary mb-3"></i>
                                    <h5>Membre</h5>
                                    <p class="text-muted">Interface pour les membres</p>
                                    <a href="{% url 'communication:messagerie_membre' %}" class="btn btn-primary">
                                        Tester Messagerie Membre
                                    </a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 mb-4">
                            <div class="card text-center border-success">
                                <div class="card-body">
                                    <i class="fas fa-shield-alt fa-3x text-success mb-3"></i>
                                    <h5>Assureur</h5>
                                    <p class="text-muted">Interface pour les assureurs</p>
                                    <a href="{% url 'communication:messagerie_assureur' %}" class="btn btn-success">
                                        Tester Messagerie Assureur
                                    </a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 mb-4">
                            <div class="card text-center border-info">
                                <div class="card-body">
                                    <i class="fas fa-user-md fa-3x text-info mb-3"></i>
                                    <h5>Médecin</h5>
                                    <p class="text-muted">Interface pour les médecins</p>
                                    <a href="{% url 'communication:messagerie_medecin' %}" class="btn btn-info">
                                        Tester Messagerie Médecin
                                    </a>
... (tronqué)

# ============================================================
# ORIGINE 128: test_urls1.py (2025-11-17)
# ============================================================

# test_urls.py
import os
import django
from django.urls import reverse, NoReverseMatch
from django.test import TestCase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def tester_urls_communication():
    """Tester toutes les URLs potentielles pour liste_messages"""

    print("TEST DES URLs COMMUNICATION")
    print("=" * 50)

    # Noms d'URL à tester
    test_cases = [
        # Sans namespace
        'liste_messages',
        'envoyer_message',
        'detail_message',
        'conversations',

        # Avec namespace communication
        'communication:liste_messages',
        'communication:envoyer_message',
        'communication:detail_message',
        'communication:conversations',

        # Avec namespace agents
        'agents:liste_messages',
        'agents:envoyer_message',
        'agents:detail_message',

        # Autres variations
        'communication_liste_messages',
        'message_list',
        'communication_message_list'
    ]

    results = []

    for name in test_cases:
        try:
            url = reverse(name)
            status = "✓ SUCCÈS"
            results.append((name, url, status))
        except NoReverseMatch as e:
            status = "✗ ÉCHEC"
            results.append((name, str(e), status))
... (tronqué)

# ============================================================
# ORIGINE 129: test_formulaire_final.py (2025-11-16)
# ============================================================

# test_formulaire_final.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_formulaire_final():
    from communication.forms import MessageForm
    from django.contrib.auth import get_user_model

    User = get_user_model()

    print("=== TEST FORMULAIRE FINAL ===")

    # Trouver les utilisateurs
    expediteur = User.objects.filter(username='assureur_test').first()
    destinataire = User.objects.filter(username='koffitanoh').first()

    if not expediteur or not destinataire:
        print("❌ Utilisateurs de test non trouvés")
        return

    print(f"✅ Expéditeur: {expediteur.username}")
    print(f"✅ Destinataire: {destinataire.username}")

    # Données de test
    test_data = {
        'destinataire': destinataire.id,
        'titre': 'Test formulaire corrigé',
        'contenu': 'Ce message teste le formulaire avec gestion automatique de la conversation',
        'type_message': 'MESSAGE',
    }

    # Tester le formulaire avec l'expéditeur
    form = MessageForm(data=test_data, expediteur=expediteur)

    print(f"Formulaire valide: {form.is_valid()}")

    if not form.is_valid():
        print("❌ Erreurs de validation:")
        for field, errors in form.errors.items():
            print(f"   - {field}: {errors}")
    else:
        print("✅ Formulaire valide!")

        # Sauvegarder le message
        try:
            message = form.save()
... (tronqué)

# ============================================================
# ORIGINE 130: test_integration_complet.py (2025-11-16)
# ============================================================

# test_integration_complet.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_integration_complet():
    from django.contrib.auth import get_user_model
    from communication.models import Message, Conversation
    from communication.utils import creer_message_automatique, get_conversations_utilisateur

    User = get_user_model()

    print("=== TEST INTÉGRATION COMPLET ===")

    # 1. Vérifier les utilisateurs
    assureur = User.objects.filter(username='assureur_test').first()
    agent = User.objects.filter(username='koffitanoh').first()

    if not assureur or not agent:
        print("❌ Utilisateurs de test non trouvés")
        return

    print("✅ Utilisateurs trouvés:")
    print(f"   - Assureur: {assureur.username} (groupes: {[g.name for g in assureur.groups.all()]})")
    print(f"   - Agent: {agent.username} (groupes: {[g.name for g in agent.groups.all()]})")

    # 2. Test avec la fonction utilitaire
    print("\n2. TEST FONCTION UTILITAIRE:")
    try:
        message_auto = creer_message_automatique(
            expediteur=assureur,
            destinataire=agent,
            titre="Test intégration fonction utilitaire",
            contenu="Ce message est créé via la fonction utilitaire",
            type_message="MESSAGE"
        )
        print("✅ Message créé via fonction utilitaire")
        print(f"   - ID: {message_auto.id}")
        print(f"   - Conversation: {message_auto.conversation.id}")
    except Exception as e:
        print(f"❌ Erreur fonction utilitaire: {e}")

    # 3. Vérifier les conversations
    print("\n3. CONVERSATIONS DE L'ASSUREUR:")
    conversations_assureur = get_conversations_utilisateur(assureur)
    print(f"   {conversations_assureur.count()} conversation(s) trouvée(s)")

... (tronqué)

# ============================================================
# ORIGINE 131: test_systeme_complet.py (2025-11-16)
# ============================================================

# test_systeme_complet.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_systeme_complet():
    from django.contrib.auth import get_user_model
    from communication.models import Message
    from django.contrib.auth.models import Group

    User = get_user_model()

    print("=== TEST SYSTÈME COMPLET ===")

    # 1. Vérifier l'utilisateur assureur_test
    assureur = User.objects.filter(username='assureur_test').first()
    if assureur:
        print("✅ Utilisateur assureur_test trouvé")
        print(f"   - Groupes: {[g.name for g in assureur.groups.all()]}")
    else:
        print("❌ Utilisateur assureur_test non trouvé")
        return

    # 2. Vérifier un destinataire
    destinataire = User.objects.filter(groups__name='Agent').first()
    if not destinataire:
        destinataire = User.objects.exclude(username='assureur_test').first()

    if destinataire:
        print(f"✅ Destinataire trouvé: {destinataire.username}")
    else:
        print("❌ Aucun destinataire trouvé")
        return

    # 3. Créer un message directement via le modèle
    try:
        message = Message.objects.create(
            expediteur=assureur,
            destinataire=destinataire,
            titre="Test système complet",
            contenu="Ce message teste le système de communication",
            type_message="MESSAGE"
        )
        print("✅ Message créé directement via modèle")
        print(f"   - ID: {message.id}")
        print(f"   - Titre: {message.titre}")
        print(f"   - Type: {message.type_message}")
... (tronqué)

# ============================================================
# ORIGINE 132: test_formulaire_message1.py (2025-11-16)
# ============================================================

# test_formulaire_message.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_formulaire_message():
    from communication.forms import MessageForm  # CORRECTION : import absolu
    from django.contrib.auth import get_user_model

    User = get_user_model()

    print("=== TEST FORMULAIRE MESSAGE ===")

    # Créer des données de test
    test_data = {
        'titre': 'Test de message',
        'contenu': 'Ceci est un test',
        'type_message': 'MESSAGE',
    }

    # Essayer de trouver un utilisateur pour le destinataire
    try:
        user = User.objects.first()
        test_data['destinataire'] = user.id
        print(f"✅ Destinataire de test: {user.username}")
    except:
        print("⚠️  Aucun utilisateur trouvé pour le test")
        test_data['destinataire'] = None

    # Tester le formulaire
    form = MessageForm(data=test_data)

    print(f"Formulaire valide: {form.is_valid()}")

    if not form.is_valid():
        print("❌ Erreurs de validation:")
        for field, errors in form.errors.items():
            print(f"   - {field}: {errors}")
    else:
        print("✅ Formulaire valide!")

        # Essayer de sauvegarder
        try:
            if user:
                form.instance.expediteur = user
            message = form.save()
            print(f"✅ Message créé avec succès: {message.titre}")
... (tronqué)

# ============================================================
# ORIGINE 133: test_formulaire_message.py (2025-11-16)
# ============================================================

# communication/forms.py - FORMULAIRE CORRIGÉ
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['type_message', 'destinataire', 'titre', 'contenu']  # 'titre' au lieu de 'sujet'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre le champ type_message obligatoire avec une valeur par défaut
        self.fields['type_message'].required = True
        self.fields['type_message'].initial = 'MESSAGE'  # Valeur par défaut
        self.fields['type_message'].widget.attrs.update({
            'class': 'form-control',
            'required': 'required'
        })

        self.fields['titre'].required = True
        self.fields['titre'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Sujet du message'
        })

        self.fields['contenu'].widget.attrs.update({
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Contenu du message'
        })

# ============================================================
# ORIGINE 134: test_consultation.py (2025-11-15)
# ============================================================

#!/usr/bin/env python
import os
import sys
import django
from django.test import RequestFactory
from django.contrib.auth.models import User

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from medecin.views import creer_consultation
from medecin.models import Medecin

def test_consultation_view():
    """
    Test unitaire de la vue creer_consultation
    """
    print("=" * 50)
    print("🧪 TEST VUE CREER_CONSULTATION")
    print("=" * 50)

    # Créer une requête factice
    factory = RequestFactory()

    # 1. Test avec utilisateur normal (sans profil médecin)
    print("\n1. Test utilisateur sans profil médecin:")
    try:
        user = User.objects.filter(medecin_profile__isnull=True).first()
        if user:
            request = factory.get('/medecin/creer-consultation/')
            request.user = user
            request.method = 'GET'

            response = creer_consultation(request)
            print(f"   Status: {response.status_code}")
            print(f"   Redirection: {getattr(response, 'url', 'Non')}")
        else:
            print("   ⚠ Aucun utilisateur sans profil médecin trouvé")
    except Exception as e:
        print(f"   ✗ ERREUR: {e}")

    # 2. Test avec utilisateur médecin
    print("\n2. Test utilisateur avec profil médecin:")
    try:
        medecin_user = User.objects.filter(medecin_profile__isnull=False).first()
        if medecin_user:
            request = factory.get('/medecin/creer-consultation/')
            request.user = medecin_user
            request.method = 'GET'
... (tronqué)

# ============================================================
# ORIGINE 135: test_vues_rapide.py (2025-11-14)
# ============================================================

# test_vues_rapide.py
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("🔍 TEST RAPIDE DES VUES MEMBRES")
print("=" * 40)

try:
    from membres.views import creer_membre, liste_membres_agent, upload_documents_membre
    print("✅ SUCCÈS: Toutes les vues importées")

    # Test des URLs
    from django.urls import reverse
    print("📋 URLs configurées:")
    print(f"  • creer_membre: {reverse('membres:creer_membre')}")
    print(f"  • liste_membres_agent: {reverse('membres:liste_membres_agent')}")
    print(f"  • upload_documents: {reverse('membres:upload_documents', args=[1])}")

    # Test des formulaires
    from membres.forms import MembreCreationForm, MembreDocumentForm
    print("✅ Formulaires importés")

    # Test des modèles
    from membres.models import Membre
    from agents.models import Agent
    print(f"📊 Données: {Membre.objects.count()} membres, {Agent.objects.count()} agents")

    print("\n🎉 SYSTÈME PRÊT !")

except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()

# ============================================================
# ORIGINE 136: test_reel_dashboard.py (2025-11-12)
# ============================================================

# test_reel_dashboard.py
import os
import sys
import django
from django.urls import reverse, NoReverseMatch

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/VERIFICATION/projet')

try:
    django.setup()
    print("✅ Django configuré")
except Exception as e:
    print(f"❌ Erreur Django: {e}")
    sys.exit(1)

def test_urls_reelles():
    print("🌐 TEST DES URLs RÉELLES")
    print("=" * 40)

    urls_a_tester = [
        ('agents:dashboard', 'Dashboard agent'),
        ('agents:creer_bon_soin', 'Créer bon de soin'),
        ('agents:liste_membres', 'Liste membres'),
        ('agents:historique_bons', 'Historique bons'),
        ('agents:verification_cotisations', 'Vérification cotisations')
    ]

    toutes_valides = True

    for url_name, description in urls_a_tester:
        try:
            url = reverse(url_name)
            print(f"✅ {description:25} -> {url}")
        except NoReverseMatch as e:
            print(f"❌ {description:25} -> ERREUR: {e}")
            toutes_valides = False

    return toutes_valides

def test_vue_dashboard():
    print("\n👁️ TEST DE LA VUE DASHBOARD")
    print("-" * 30)

    try:
        from agents.views import dashboard
        print("✅ Vue dashboard importée")

        # Vérifier que c'est une fonction callable
... (tronqué)

# ============================================================
# ORIGINE 137: test_final_simple.py (2025-11-12)
# ============================================================

# test_final_simple.py
import os
import sys

# Ajouter le chemin du projet
sys.path.append('/Users/koffitanohsoualiho/Documents/VERIFICATION/projet')

def test_templates():
    print("🧪 TEST FINAL - TEMPLATES")
    print("=" * 40)

    # Vérifier les templates critiques
    templates_critiques = [
        'templates/agents/base_agent.html',
        'templates/agents/dashboard.html',
        'templates/agents/creer_bon_soin.html',
        'templates/agents/error.html'
    ]

    probleme_trouve = False

    for template_relatif in templates_critiques:
        template_path = os.path.join(
            '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet',
            template_relatif
        )

        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                content = f.read()

            # Vérifier les problèmes
            if 'tableau_de_bord_agent' in content:
                print(f"❌ {template_relatif}: Contient 'tableau_de_bord_agent'")
                probleme_trouve = True
            elif "{% url 'agents:dashboard' %}" in content or '{% url "agents:dashboard" %}' in content:
                print(f"✅ {template_relatif}: URLs corrigées")
            else:
                print(f"⚠️  {template_relatif}: Aucune URL dashboard détectée")
        else:
            print(f"⚠️  {template_relatif}: Non trouvé")

    return not probleme_trouve

def test_urls_config():
    print("\n🔗 TEST CONFIGURATION URLs")
    print("-" * 30)

    # Vérifier agents/urls.py
    urls_path = '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/agents/urls.py'
... (tronqué)

# ============================================================
# ORIGINE 138: test_final_complet1.py (2025-11-12)
# ============================================================

# test_final_complet.py
import os
import sys
import django
from django.urls import reverse, NoReverseMatch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/VERIFICATION/projet')

django.setup()

def test_complet():
    print("🧪 TEST FINAL COMPLET")
    print("=" * 40)

    # Test des URLs
    print("\n📋 TEST DES URLs:")
    print("-" * 20)

    urls_a_tester = [
        'agents:dashboard',
        'agents:verification_cotisations',
        'agents:creer_bon_soin',
        'agents:historique_bons',
        'agents:liste_membres'
    ]

    toutes_valides = True
    for url_name in urls_a_tester:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name:30} -> {url}")
        except NoReverseMatch:
            print(f"❌ {url_name:30} -> NON TROUVÉ")
            toutes_valides = False

    # Test de l'accès dashboard
    print("\n🌐 TEST ACCÈS DASHBOARD:")
    print("-" * 25)

    try:
        from agents.views import dashboard
        print("✅ Vue dashboard importable")

        # Vérifier que la fonction existe
        if hasattr(dashboard, '__call__'):
            print("✅ Vue dashboard est callable")
        else:
            print("❌ Vue dashboard n'est pas callable")
            toutes_valides = False
... (tronqué)

# ============================================================
# ORIGINE 139: test_creation_reelle.py (2025-11-06)
# ============================================================

# test_creation_reelle.py
import os
import sys
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

def test_creation_reelle_bon_soin():
    print("🧪 TEST DE CRÉATION RÉELLE DE BON DE SOIN")
    print("=" * 50)

    try:
        from membres.models import Membre
        from soins.models import BonDeSoin

        # Prendre un membre existant
        membre = Membre.objects.first()
        print(f"📋 Membre sélectionné: {membre.prenom} {membre.nom}")

        # Créer un bon de soin complet
        bon_soin = BonDeSoin.objects.create(
            patient=membre,
            date_soin=date.today(),
            symptomes="Fièvre, toux et maux de tête",
            diagnostic="Infection respiratoire supérieure",
            montant=75.50,
            statut='attente'
        )

        print(f"✅ BON DE SOIN CRÉÉ AVEC SUCCÈS!")
        print(f"   📝 Référence: {bon_soin.id}")
        print(f"   👤 Patient: {bon_soin.patient.prenom} {bon_soin.patient.nom}")
        print(f"   💰 Montant: {bon_soin.montant} FCFA")
        print(f"   📅 Date: {bon_soin.date_soin}")
        print(f"   🏥 Diagnostic: {bon_soin.diagnostic}")
        print(f"   📊 Statut: {bon_soin.statut}")

        # Laisser le bon dans la base pour vérification
        print(f"\n💾 Bon de soin conservé dans la base (ID: {bon_soin.id})")

        return bon_soin

    except Exception as e:
        print(f"❌ ERREUR lors de la création: {e}")
        return None

... (tronqué)

# ============================================================
# ORIGINE 140: test_apres_modification.py (2025-11-06)
# ============================================================

# test_apres_modification.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

from django.contrib.auth.models import User
from core.utils import est_agent

def test_definitif():
    print("🎯 TEST DÉFINITIF APRÈS MODIFICATION")
    print("=" * 50)

    # Test koffitanoh
    koffitanoh = User.objects.get(username='koffitanoh')
    resultat = est_agent(koffitanoh)

    print(f"👤 koffitanoh:")
    print(f"   - Superuser: {koffitanoh.is_superuser}")
    print(f"   - Est agent (BD): OUI")
    print(f"   - Est agent (fonction): {resultat}")

    if resultat:
        print("   ✅ PEUT créer des bons de soin")
        print("\n🎉 FÉLICITATIONS! Le problème est résolu.")
        print("\n📝 Pour tester dans l'interface:")
        print("   1. Allez sur: http://localhost:8000/agents/creer-bon-soin/")
        print("   2. Sélectionnez un membre")
        print("   3. Remplissez le formulaire")
        print("   4. Cliquez sur 'Créer le bon de soin'")
    else:
        print("   ❌ NE peut PAS créer des bons de soin")
        print("\n🔧 Action requise:")
        print("   Modifiez MANUELLEMENT core/utils.py")
        print("   Ajoutez cette condition au début de est_agent():")
        print("   if user.is_superuser: return True")

if __name__ == "__main__":
    test_definitif()

# ============================================================
# ORIGINE 141: test_final_complet.py (2025-11-06)
# ============================================================

# test_final_complet.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

from django.contrib.auth.models import User
from core.utils import est_agent

def test_complet():
    print("🎯 TEST COMPLET APRÈS CORRECTION")
    print("=" * 50)

    # Test des utilisateurs principaux
    users_to_test = ['koffitanoh', 'test_agent']

    for username in users_to_test:
        try:
            user = User.objects.get(username=username)
            est_agent_result = est_agent(user)

            print(f"\n👤 {username}:")
            print(f"   - Superuser: {user.is_superuser}")
            print(f"   - Staff: {user.is_staff}")
            print(f"   - Est agent: {est_agent_result}")

            if est_agent_result:
                print("   ✅ PEUT créer des bons de soin")
            else:
                print("   ❌ NE peut PAS créer des bons de soin")

        except User.DoesNotExist:
            print(f"❌ Utilisateur {username} non trouvé")

    # Recommandation finale
    print("\n" + "=" * 50)
    koffitanoh = User.objects.get(username='koffitanoh')
    if est_agent(koffitanoh):
        print("🎉 TOUT EST FONCTIONNEL! koffitanoh peut créer des bons de soin.")
        print("\n📝 Procédure de test:")
        print("   1. Allez sur: http://localhost:8000/agents/creer-bon-soin/")
        print("   2. Sélectionnez un membre")
        print("   3. Remplissez le formulaire")
        print("   4. Cliquez sur 'Créer le bon de soin'")
    else:
        print("❌ koffitanoh ne peut toujours pas créer de bons de soin.")
... (tronqué)

# ============================================================
# ORIGINE 142: test_permissions.py (2025-11-06)
# ============================================================

# test_permissions.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

from django.contrib.auth.models import User
from core.utils import est_agent

def tester_permissions():
    print("🔐 TEST DES PERMISSIONS")
    print("=" * 50)

    # Tester koffitanoh
    try:
        koffitanoh = User.objects.get(username='koffitanoh')
        print(f"👤 koffitanoh:")
        print(f"   - Superuser: {koffitanoh.is_superuser}")
        print(f"   - Staff: {koffitanoh.is_staff}")
        print(f"   - Est agent: {est_agent(koffitanoh)}")
        print()
    except User.DoesNotExist:
        print("❌ koffitanoh non trouvé")

    # Tester test_agent
    try:
        test_agent_user = User.objects.get(username='test_agent')
        print(f"👤 test_agent:")
        print(f"   - Superuser: {test_agent_user.is_superuser}")
        print(f"   - Staff: {test_agent_user.is_staff}")
        print(f"   - Est agent: {est_agent(test_agent_user)}")
        print()
    except User.DoesNotExist:
        print("❌ test_agent non trouvé")

    # Recommandation
    print("💡 RECOMMANDATION:")
    if est_agent(koffitanoh):
        print("✅ koffitanoh peut créer des bons de soin")
    else:
        print("❌ koffitanoh NE peut PAS créer des bons de soin")
        print("   Exécutez: python ajouter_koffitanoh_agent.py")

if __name__ == "__main__":
    tester_permissions()

# ============================================================
# ORIGINE 143: test_formulaire.py (2025-11-06)
# ============================================================

# test_formulaire.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

try:
    django.setup()

    from django.test import RequestFactory
    from django.contrib.auth.models import User
    from agents.views import creer_bon_soin_membre
    from membres.models import Membre

    def test_formulaire_bon_soin():
        print("📝 TEST DU FORMULAIRE DE BON DE SOIN")
        print("-" * 50)

        # Créer une requête POST simulée
        factory = RequestFactory()

        # Récupérer un membre de test
        membre = Membre.objects.first()
        if not membre:
            print("❌ Aucun membre disponible pour le test")
            return

        print(f"✅ Membre de test: {membre.prenom} {membre.nom} (ID: {membre.id})")

        # Créer un utilisateur de test
        user, created = User.objects.get_or_create(
            username='test_agent',
            defaults={'is_staff': True, 'is_active': True}
        )

        # Données du formulaire
        form_data = {
            'type_soin': 'consultation',
            'montant': '150.75',
            'symptomes': 'Fièvre et maux de tête',
            'diagnostic': 'Grippe',
            'description': 'Consultation générale'
        }

        # Créer la requête POST
        request = factory.post(f'/agents/creer-bon-soin/{membre.id}/', form_data)
        request.user = user

... (tronqué)

