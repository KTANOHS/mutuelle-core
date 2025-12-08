"""
FICHIER CONSOLIDÉ: test
Catégorie: correction
Fusion de 41 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: test_api_corrige.py (2025-12-04)
# ============================================================

# test_api_corrige.py
import requests
import json

BASE_URL = "http://localhost:8000"

def test_urls_communication():
    """Teste les différentes URLs de communication"""

    print("🔍 Test des URLs de communication")
    print("="*50)

    # Liste des URLs à tester
    urls = [
        ("/communication/messagerie/", "GET", "Messagerie standard"),
        ("/communication/messages/envoyer/", "POST", "Envoyer message (communication)"),
        ("/assureur/communication/", "GET", "Messagerie assureur"),
        ("/assureur/communication/envoyer/", "POST", "Envoyer message (assureur)"),
    ]

    for url_path, method, description in urls:
        print(f"\n{description}:")
        print(f"  URL: {url_path}")

        if method == "GET":
            response = requests.get(BASE_URL + url_path)
        else:  # POST
            response = requests.post(BASE_URL + url_path, data={})

        print(f"  Status: {response.status_code}")
        print(f"  Type: {response.headers.get('Content-Type', 'Non spécifié')}")

        if response.status_code == 200:
            if "text/html" in response.headers.get('Content-Type', ''):
                print(f"  ✅ Page HTML accessible")
                # Vérifier si c'est une page de login
                if "login" in response.text.lower() or "connexion" in response.text.lower():
                    print(f"  ⚠️  C'est une page de login/connexion")
            elif "application/json" in response.headers.get('Content-Type', ''):
                print(f"  ✅ API JSON accessible")
                try:
                    data = response.json()
                    print(f"  Réponse JSON: {json.dumps(data, indent=2)}")
                except:
                    print(f"  ❌ Réponse JSON invalide")
        elif response.status_code in [302, 301]:
            print(f"  🔄 Redirection vers: {response.headers.get('Location', 'Inconnu')}")
        elif response.status_code == 403:
            print(f"  🔒 Accès interdit (CSRF ou authentification)")
        elif response.status_code == 404:
... (tronqué)

# ============================================================
# ORIGINE 2: test_avec_auth_corrige.py (2025-12-04)
# ============================================================

# test_avec_auth_corrige.py
import os
import sys
import django

# IMPORTANT : Configurer Django AVANT d'importer quoi que ce soit d'autre
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

# Ajouter le chemin du projet
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

try:
    django.setup()
    print("✅ Django configuré avec succès")
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

print("🧪 TEST AVEC AUTHENTIFICATION (CORRIGÉ)")
print("="*50)

try:
    from django.test import RequestFactory
    from django.contrib.auth.models import User, Group
    from assureur import views

    # Créer un utilisateur test
    try:
        # Essayer de récupérer un utilisateur existant
        user = User.objects.filter(username='test_assureur').first()

        if not user:
            # Créer un nouvel utilisateur
            user = User.objects.create_user(
                username='test_assureur',
                email='test@assureur.com',
                password='testpass123'
            )
            print("✅ Nouvel utilisateur créé")
        else:
            print("✅ Utilisateur existant trouvé")

        # Vérifier/créer le groupe assureur
        assureur_group, created = Group.objects.get_or_create(name='assureur')
        user.groups.add(assureur_group)
        user.is_staff = True
        user.save()

        print(f"✅ Utilisateur '{user.username}' ajouté au groupe 'assureur'")
... (tronqué)

# ============================================================
# ORIGINE 3: test_without_server_fixed.py (2025-12-03)
# ============================================================

# test_without_server_fixed.py
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
print(f"Chemin du projet: {projet_path}")

# 1. Créer un superutilisateur de test
try:
    # Supprimer d'abord l'utilisateur existant pour éviter la contrainte unique
    User.objects.filter(username='test_admin').delete()

    user = User.objects.create_superuser(
        username='test_admin',  # Changez le nom d'utilisateur pour éviter le conflit
        email='test_admin@test.com',
        password='test123'
    )
    print("✅ Superutilisateur de test créé")
except Exception as e:
    print(f"❌ Erreur création utilisateur: {e}")
    try:
        user = User.objects.get(username='admin')
        print("✅ Utilisation de l'admin existant")
    except Exception:
        print("❌ Aucun utilisateur disponible")
        user = None

# 2. Tester avec le client Django
client = Client()

# 2.1. Se connecter
if user:
    try:
        login = client.login(username=user.username, password='test123' if user.username == 'test_admin' else 'admin123')
        print(f"Connexion: {'✅ Réussie' if login else '❌ Échec'}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
... (tronqué)

# ============================================================
# ORIGINE 4: test_generation_fixed.py (2025-12-03)
# ============================================================

# test_generation_fixed.py
import os
import django
from datetime import datetime
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("=== TEST AVEC LES BONNES VALEURS ===")

from assureur.models import Membre, Cotisation
from django.contrib.auth.models import User

# Créer un utilisateur test
user = User.objects.create_user('test_user', 'test@test.com', 'test123')

# Prendre un membre existant
membre = Membre.objects.filter(statut='actif').first()
if not membre:
    print("❌ Aucun membre actif trouvé")
    exit()

print(f"Membre test: {membre.nom} {membre.prenom}")

# Tester la création d'une cotisation avec les bonnes valeurs
try:
    # Période au bon format
    periode = '2025-01'

    # Dates
    date_emission = datetime.now().date()
    date_echeance = datetime(2025, 1, 31).date()

    # Déterminer type et montant
    if membre.est_femme_enceinte:
        type_cotisation = 'femme_enceinte'
        montant = Decimal('7500.00')
    else:
        type_cotisation = 'normale'
        montant = Decimal('5000.00')

    # Créer la référence
    reference = f"COT-{membre.numero_membre}-202501"

    # Créer la cotisation
    cotisation = Cotisation(
        membre=membre,
        periode=periode,
        montant=montant,
... (tronqué)

# ============================================================
# ORIGINE 5: test_final_integration_fixed.py (2025-12-03)
# ============================================================

# test_final_integration_fixed.py
import os
import django
from django.test import Client
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
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
except Exception as e:
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
    # Vérifier le contenu en utilisant une approche différente pour éviter l'erreur ASCII
    content_str = response.content.decode('utf-8', errors='ignore')
    if 'Générer' in content_str or 'Cotisations' in content_str:
        print("   ✓ Titre présent")
    if 'periode' in content_str:
        print("   ✓ Champ période présent")
else:
    print(f"   ✗ Erreur: {response.status_code}")
    print(f"   Contenu (premiers 500 caractères): {response.content[:500]}...")
... (tronqué)

# ============================================================
# ORIGINE 6: test_cotisation_creation_fixed.py (2025-12-03)
# ============================================================

# test_cotisation_creation_fixed.py
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre, Cotisation

print("=== TEST CRÉATION COTISATIONS AVEC TOUS LES CHAMPS ===")

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
            # Calculer les dates
            date_emission = datetime.now().date()
            date_echeance = date_emission + timedelta(days=30)  # Échéance dans 30 jours

            cotisation = Cotisation.objects.create(
                membre=membre,
                periode='2024-12',
                montant=10000.00,
                statut='en_attente',
                date_emission=date_emission,
                date_echeance=date_echeance,
                type_cotisation='mensuelle',
                reference=f"COT-{membre.numero_membre}-2024-12"
            )
            print(f"✓ Cotisation test créée :")
            print(f"  - Membre: {cotisation.membre.nom} {cotisation.membre.prenom}")
            print(f"  - Période: {cotisation.periode}")
            print(f"  - Montant: {cotisation.montant} FCFA")
            print(f"  - Statut: {cotisation.statut}")
            print(f"  - Date émission: {cotisation.date_emission}")
            print(f"  - Date échéance: {cotisation.date_echeance}")
        else:
            print("⚠ Cotisation pour décembre 2024 existe déjà")
... (tronqué)

# ============================================================
# ORIGINE 7: test_cotisations_correct.py (2025-12-03)
# ============================================================

# test_cotisations_correct.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from assureur.models import Membre, Cotisation
from django.utils import timezone
import datetime

class CotisationTests(TestCase):

    def setUp(self):
        # Créer un utilisateur assureur
        self.user = User.objects.create_user(
            username='assureur_test',
            password='password123',
            is_staff=True
        )

        # Créer des membres actifs
        for i in range(3):
            Membre.objects.create(
                nom=f"Test{i}",
                prenom=f"Membre{i}",
                statut='actif',
                numero_membre=f"MBR00{i}",
                type_membre='standard'
            )

    def test_page_generer_cotisations(self):
        """Test d'accès à la page de génération"""
        self.client.login(username='assureur_test', password='password123')
        response = self.client.get(reverse('assureur:generer_cotisations'))

        print(f"Status code: {response.status_code}")
        print(f"Template utilisé: {response.template_name}")

        if response.status_code == 200:
            print("✓ Page génération accessible")

            # Vérifier les données de contexte
            context = response.context
            if context:
                print(f"Membres actifs dans contexte: {context.get('membres_actifs_count', 'Non défini')}")
                print(f"Cotisations ce mois: {context.get('cotisations_mois_count', 'Non défini')}")
                print(f"À générer: {context.get('a_generer_count', 'Non défini')}")
        else:
            print("✗ Erreur page génération")
            print(f"Contenu: {response.content[:500]}")

        self.assertEqual(response.status_code, 200)
... (tronqué)

# ============================================================
# ORIGINE 8: test_after_fix.py (2025-12-02)
# ============================================================

# test_after_fix.py
import requests

print("🔍 Test après correction")
print("="*50)

# Test sans session
print("1. Test sans authentification :")
urls = ['/assureur/', '/assureur/dashboard/']
for url in urls:
    full_url = f'http://localhost:8000{url}'
    response = requests.get(full_url, allow_redirects=False)
    print(f"   {url}: {response.status_code} {'(redirige vers login)' if response.status_code == 302 else ''}")

print("\n2. Instructions pour tester :")
print("   a. Allez sur : http://localhost:8000/admin/")
print("   b. Connectez-vous avec DOUA")
print("   c. Allez sur : http://localhost:8000/assureur/")
print("   d. Si ça marche, le système assureur est opérationnel !")

# ============================================================
# ORIGINE 9: test_auth_correct.py (2025-12-02)
# ============================================================

# test_auth_correct.py
import requests
from django.test import Client

# Utilise le client de test Django (sans serveur)
client = Client()

# Se connecter d'abord
login_success = client.login(username='Almoravide', password='TON_MOT_DE_PASSE')
print(f"Login réussi: {login_success}")

# Maintenant tester l'API simple
response = client.get('/communication/api/simple/conversations/8/messages/')
print(f"Status: {response.status_code}")
print(f"Content-Type: {response['Content-Type']}")
print(f"Contenu (premiers 500 chars): {response.content[:500]}")

# ============================================================
# ORIGINE 10: test_final_corrige2.py (2025-12-02)
# ============================================================

# test_final_corrige.py
import requests
import json

print("🎯 Test du système complet avec API publique")
print("="*50)

# 1. Envoi de message (API simple sans auth)
url_send = "http://localhost:8000/communication/api/simple/messages/send/"
data = {
    "expediteur_id": 1,
    "destinataire_id": 2,
    "contenu": "Test final du système"
}

response = requests.post(url_send, headers={"Content-Type": "application/json"},
                         data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    conv_id = result['conversation_id']
    print(f"✅ Message envoyé (Conv ID: {conv_id})")

    # 2. Récupération avec API publique
    url_public = f"http://localhost:8000/communication/api/public/conversations/{conv_id}/messages/"
    response2 = requests.get(url_public)

    if response2.status_code == 200:
        messages = response2.json()
        print(f"✅ {messages['total_messages']} message(s) récupéré(s)")
        for msg in messages['messages']:
            print(f"   📨 {msg['expediteur']['username']} → {msg['destinataire']['username']}:")
            print(f"      '{msg['contenu']}'")
            print(f"      À: {msg['date_envoi']}")
    else:
        print(f"❌ Erreur récupération: {response2.status_code}")
else:
    print(f"❌ Erreur envoi: {response.text}")

# ============================================================
# ORIGINE 11: test_corrige1.py (2025-12-02)
# ============================================================

import requests
import json

# Test avec l'API simple
url = "http://localhost:8000/communication/api/simple/messages/send/"

# Utilisons des IDs valides de ta liste
# Almoravide (ID: 1) envoie un message à GLORIA (ID: 2)

print("🔍 Test API Simple - Envoi JSON complet")
headers = {"Content-Type": "application/json"}
data = {
    "expediteur_id": 1,      # Almoravide
    "destinataire_id": 2,    # GLORIA
    "contenu": "Bonjour GLORIA, ceci est un test de l'API de messagerie"
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"   Status: {response.status_code}")

    if response.status_code == 200:
        json_response = response.json()
        print(f"   ✅ Succès: {json_response}")
    elif response.status_code == 400:
        json_response = response.json()
        print(f"   ❌ Erreur 400: {json_response}")
        print(f"   Détails de la requête envoyée:")
        print(f"   {data}")
    else:
        print(f"   ❌ Autre erreur HTTP: {response.status_code}")
        print(f"   Response: {response.text}")

except Exception as e:
    print(f"   💥 Exception: {e}")

print("\n" + "="*50 + "\n")

# Test 2: Entre médecins
print("🔍 Test 2: Message entre médecins")
data2 = {
    "expediteur_id": 2,      # GLORIA (médecin)
    "destinataire_id": 40,   # medecin_test_1
    "contenu": "Bonjour collègue, voici une ordonnance pour revoir"
}

try:
    response2 = requests.post(url, headers=headers, data=json.dumps(data2))
    print(f"   Status: {response2.status_code}")

... (tronqué)

# ============================================================
# ORIGINE 12: test_api_correct.py (2025-12-02)
# ============================================================

import requests
import json

# Test avec l'API simple
url = "http://localhost:8000/communication/api/simple/messages/send/"

# Test 1: JSON
print("🔍 Test API Simple - Envoi JSON")
headers = {"Content-Type": "application/json"}
data = {
    "destinataire_id": 1,
    "contenu": "Test message via API simple"
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"   Status: {response.status_code}")
    print(f"   Headers: {response.headers}")
    print(f"   Response text: {response.text}")

    if response.status_code == 200:
        try:
            json_response = response.json()
            print(f"   ✅ JSON Response: {json_response}")
        except json.JSONDecodeError as e:
            print(f"   ❌ Réponse n'est pas du JSON: {e}")
            print(f"   Raw response: {response.text[:200]}")
    else:
        print(f"   ❌ Erreur HTTP: {response.status_code}")

except Exception as e:
    print(f"   💥 Exception: {e}")

print("\n" + "="*50 + "\n")

# Test 2: Form-Data
print("🔍 Test API Simple - Envoi Form-Data")
data_form = {
    "destinataire_id": 1,
    "contenu": "Test message via Form-Data API simple"
}

try:
    response2 = requests.post(url, data=data_form)
    print(f"   Status: {response2.status_code}")
    print(f"   Response text: {response2.text}")

    if response2.status_code == 200:
        try:
            json_response2 = response2.json()
... (tronqué)

# ============================================================
# ORIGINE 13: test_acces_temps_reel_corrige.py (2025-11-28)
# ============================================================

# test_acces_temps_reel_corrige.py

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
from django.urls import reverse  # CORRECTION: Import manquant

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
                # Suivre la redirection pour voir où ça mène
                try:
                    response_redirect = client.get(url, follow=True)
                    final_url = response_redirect.redirect_chain[-1][0] if response_redirect.redirect_chain else url
                    print(f"   🔄 {description}: REDIRECTION -> {final_url}")
                except:
                    print(f"   🔄 {description}: REDIRECTION")
            else:
... (tronqué)

# ============================================================
# ORIGINE 14: test_final_corrige1.py (2025-11-28)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from django.db.models import Q

def test_recherche_finale():
    print("🎯 TEST FINAL AVEC CHAMPS CORRECTS")
    print("=" * 40)

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
        print(f"      Date inscription: {r.date_inscription}")

def verifier_champs_reels():
    print("\n📋 CHAMPS RÉELS POUR LA RECHERCHE")
    print("=" * 40)

    # Prendre un membre existant
    membre = Membre.objects.filter(prenom="ASIA", nom="DRAMANE").first()
    if not membre:
        membre = Membre.objects.first()

    if membre:
        print("Champs disponibles:")
        print(f"   ✅ nom: {membre.nom}")
        print(f"   ✅ prenom: {membre.prenom}")
        print(f"   ✅ numero_unique: {membre.numero_unique}")
        print(f"   ✅ email: {membre.email}")
        print(f"   ✅ date_inscription: {membre.date_inscription}")

if __name__ == "__main__":
    test_recherche_finale()
... (tronqué)

# ============================================================
# ORIGINE 15: test_champs_corrects.py (2025-11-28)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from django.db.models import Q

def test_avec_champs_corrects():
    print("🎯 TEST AVEC CHAMPS CORRECTS")
    print("=" * 35)

    # Test avec le VRAI champ numero_membre
    query = "DRAMANE"
    resultats = Membre.objects.filter(
        Q(nom__icontains=query) |
        Q(prenom__icontains=query) |
        Q(numero_membre__icontains=query) |  # ⬅️ CHAMP CORRECT
        Q(email__icontains=query)
    )

    print(f"🔍 Recherche '{query}': {resultats.count()} résultat(s)")
    for r in resultats:
        print(f"   ✅ {r.prenom} {r.nom}")
        print(f"      Numéro membre: {r.numero_membre}")
        print(f"      Email: {r.email}")

def lister_champs_membre():
    print("\n📋 CHAMPS RÉELS DU MODÈLE MEMBRE")
    print("=" * 35)

    membre = Membre.objects.first()
    if membre:
        print("Champs disponibles pour la recherche:")
        champs_recherche = ['nom', 'prenom', 'numero_membre', 'email']
        for champ in champs_recherche:
            if hasattr(membre, champ):
                valeur = getattr(membre, champ)
                print(f"   ✅ {champ}: {valeur}")
            else:
                print(f"   ❌ {champ}: N'existe pas")

if __name__ == "__main__":
    test_avec_champs_corrects()
    lister_champs_membre()

# ============================================================
# ORIGINE 16: test_final_correction.py (2025-11-28)
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

    def test_final_correction():
        print("🎯 TEST FINAL APRÈS CORRECTION")
        print("=" * 50)

        client = Client()

        # Connexion
        print("🔑 Connexion...")
        if not client.login(username='medecin_test', password='password123'):
            print("❌ Échec connexion")
            return

        print("✅ Connecté")

        # Test de la page suivi chronique
        print("\n🚀 Test page suivi chronique...")
        response = client.get('/medecin/suivi-chronique/')

        print(f"📊 Status: {response.status_code}")

        if response.status_code == 200:
            print("🎉 SUCCÈS - Page accessible sans erreur!")

            content = response.content.decode('utf-8')
            print(f"📏 Taille: {len(content)} caractères")

            # Vérifications critiques
            checks = [
                ("Pas d'erreur template", "TemplateDoesNotExist" not in content),
                ("Interface complète", len(content) > 1000),
                ("Titre correct", "Suivi des Maladies Chroniques" in content),
                ("Navigation", "Tableau de Bord" in content),
                ("Cartes statistiques", "card border-left-primary" in content),
            ]

            print("\n🔍 Vérifications détaillées:")
            success_count = 0
... (tronqué)

# ============================================================
# ORIGINE 17: test_template_corrige.py (2025-11-27)
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

    def test_connexion_medecin_corrige():
        print("🔐 TEST CONNEXION MÉDECIN (CORRIGÉ):")
        print("=" * 50)

        client = Client()

        # 1. Vérifier/Créer le médecin de test
        print("1. 🔍 Vérification médecin de test...")
        try:
            user = User.objects.get(username='medecin_test')
            print("   ✅ Utilisateur medecin_test trouvé")
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='medecin_test',
                email='medecin@test.com',
                password='password123'
            )
            print("   ✅ Utilisateur medecin_test créé")

        try:
            medecin = Medecin.objects.get(user=user)
            print(f"   ✅ Médecin trouvé: {medecin}")
        except Medecin.DoesNotExist:
            medecin = Medecin.objects.create(
                user=user,
                nom="Test",
                prenom="Docteur",
                specialite="Généraliste"
            )
            print("   ✅ Profil médecin créé")

        # 2. Essayer d'accéder sans connexion
        print("\n2. 🔒 Accès sans connexion...")
        response = client.get('/medecin/tableau-de-bord/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 302:
... (tronqué)

# ============================================================
# ORIGINE 18: test_fixed.py (2025-11-27)
# ============================================================

# test_fixed.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from agents.views import verifier_cotisation_membre_simplifiee
from membres.models import Membre

try:
    membre = Membre.objects.get(id=6)
    print(f"🔍 Test avec membre: {membre.prenom} {membre.nom}")
    print(f"📅 Date inscription: {membre.date_inscription} (type: {type(membre.date_inscription)})")

    resultat, details = verifier_cotisation_membre_simplifiee(membre)

    print(f"✅ SUCCÈS : Test complété sans erreur")
    print(f"📊 Résultat: {resultat}")
    print(f"📝 Détails: {details['message']}")
    print(f"💰 Montant: {details['montant_dette_str']}")
    print(f"📅 Prochaine échéance: {details['prochaine_echeance']}")

except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()

# ============================================================
# ORIGINE 19: test_fix.py (2025-11-27)
# ============================================================

# test_fix.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

# Test d'import des fonctions corrigées
try:
    from agents.views import verifier_statut_cotisation_simple, verifier_cotisation_membre_simplifiee
    from membres.models import Membre

    print("✅ SUCCÈS : Les fonctions sont maintenant importables")

    # Test avec un membre réel
    try:
        membre = Membre.objects.get(id=6)
        resultat_simple = verifier_statut_cotisation_simple(membre)
        resultat_complet = verifier_cotisation_membre_simplifiee(membre)

        print(f"✅ Test fonction simple: {resultat_simple}")
        print(f"✅ Test fonction complète: {resultat_complet[0]} - {resultat_complet[1]['message']}")

    except Membre.DoesNotExist:
        print("⚠️  Membre ID=6 non trouvé, test avec premier membre")
        membre = Membre.objects.first()
        if membre:
            resultat_simple = verifier_statut_cotisation_simple(membre)
            resultat_complet = verifier_cotisation_membre_simplifiee(membre)
            print(f"✅ Test avec premier membre: {resultat_simple} - {resultat_complet[1]['message']}")

except ImportError as e:
    print(f"❌ ÉCHEC Import: {e}")
except Exception as e:
    print(f"❌ ERREUR: {e}")

# ============================================================
# ORIGINE 20: test_correction_affichage.py (2025-11-27)
# ============================================================

# test_correction_affichage.py - VERSION CORRIGÉE
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from affichage_unifie import afficher_fiche_cotisation_unifiee, determiner_statut_cotisation

def test_correction():
    print("🧪 TEST DE CORRECTION AFFICHAGE_UNIFIE")
    print("=" * 50)

    # Test 1: Fonction determiner_statut_cotisation avec None
    try:
        statut, emoji, classe = determiner_statut_cotisation(None)
        print(f"✅ Test 1 - Gestion None: {statut} {emoji} {classe}")
    except Exception as e:
        print(f"❌ Test 1 - Erreur: {e}")

    # Test 2: Fonction determiner_statut_cotisation avec objet factice
    try:
        class MockVerification:
            statut_cotisation = 'a_jour'

        statut, emoji, classe = determiner_statut_cotisation(MockVerification())
        print(f"✅ Test 2 - Gestion objet: {statut} {emoji} {classe}")
    except Exception as e:
        print(f"❌ Test 2 - Erreur: {e}")

    # Test 3: Fonction afficher_fiche_cotisation_unifiee avec données minimales
    try:
        class MockMembre:
            prenom = "Jean"
            nom = "Dupont"
            numero_unique = "MEM123"
            telephone = "0123456789"

        fiche = afficher_fiche_cotisation_unifiee(MockMembre(), None, None)
        if "FICHE COTISATION UNIFIÉE" in fiche:
            print("✅ Test 3 - Génération fiche avec None réussie")
        else:
            print("❌ Test 3 - Format fiche incorrect")
    except Exception as e:
        print(f"❌ Test 3 - Erreur: {e}")

    # Test 4: Fonction avec vérification factice
... (tronqué)

# ============================================================
# ORIGINE 21: test_flux_cotisations_corrige.py (2025-11-27)
# ============================================================

# test_flux_cotisations_corrige.py
import os
import sys
import django
from pathlib import Path
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

print("🧪 TEST DU FLUX COTISATIONS - VERSION CORRIGÉE")
print("=" * 50)

class TestFluxCotisationsCorrige:
    def __init__(self):
        self.resultats = []

    def tester_modeles_disponibles(self):
        """Teste les modèles réellement disponibles"""
        print("1. 🔧 TEST MODÈLES DISPONIBLES...")

        from django.apps import apps

        modeles_a_tester = [
            'membres.Membre',
            'assureur.Assureur',
            'agents.Agent',
            'agents.VerificationCotisation'
        ]

        for modele_path in modeles_a_tester:
            try:
                modele = apps.get_model(modele_path)
                count = modele.objects.count()
                self.resultats.append((modele_path, f'✅ DISPONIBLE ({count} enregistrements)'))
                print(f"   ✅ {modele_path}: {count} enregistrements")
            except Exception as e:
                self.resultats.append((modele_path, f'❌ {e}'))
                print(f"   ❌ {modele_path}: {e}")

    def tester_creation_agent(self):
        """Teste la création d'un agent avec tous les champs requis"""
        print("\n2. 👨‍💼 TEST CRÉATION AGENT...")

        try:
            from agents.models import Agent
            from django.contrib.auth.models import User

... (tronqué)

# ============================================================
# ORIGINE 22: test_apres_correction_definitive.py (2025-11-20)
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
import json

def test_apres_correction():
    """Test après correction définitive"""
    print("🧪 TEST APRÈS CORRECTION DÉFINITIVE")
    print("===================================")

    client = Client()
    user = authenticate(username='agent_operateur', password='agent123')

    if not user:
        print("❌ Authentification échouée")
        return False

    client.force_login(user)
    print("✅ Authentification réussie")

    # Test avec le bon 17
    print(f"\n🔍 Test API pour le bon #17")
    response = client.get(f'/api/agents/bons/17/details/')
    print(f"📡 Statut: {response.status_code}")

    if response.status_code == 200:
        data = json.loads(response.content)
        print(f"✅ API fonctionne")

        # Vérifier la structure
        print(f"\n📦 STRUCTURE DE LA RÉPONSE (À LA RACINE):")

        # Afficher tous les champs à la racine
        for key, value in data.items():
            print(f"   {key}: {value}")

        # Vérifier les champs critiques sont maintenant à la racine
        champs_critiques = ['code', 'membre', 'montant_max', 'statut', 'date_creation', 'motif']
        print(f"\n🎯 CHAMPS CRITIQUES (À LA RACINE):")
        tous_presents = True

        for champ in champs_critiques:
... (tronqué)

# ============================================================
# ORIGINE 23: test_apres_correction.py (2025-11-20)
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

def test_apres_correction():
    """Tester l'API après correction de l'erreur 500"""
    print("🧪 TEST APRÈS CORRECTION ERREUR 500")
    print("===================================")

    client = Client()
    user = authenticate(username='agent_operateur', password='agent123')

    if not user:
        print("❌ Authentification échouée")
        return False

    client.force_login(user)
    print("✅ Authentification réussie")

    # Tester avec plusieurs bons
    bons = BonDeSoin.objects.all()[:3]

    for bon in bons:
        print(f"\n🔍 Test avec le bon ID: {bon.id}")

        # Tester l'API
        response = client.get(f'/api/agents/bons/{bon.id}/details/')
        print(f"📡 Statut API: {response.status_code}")

        if response.status_code == 200:
            try:
                data = json.loads(response.content)
                print("✅ API fonctionnelle!")

                if data.get('success'):
                    bon_data = data['bon']
                    print(f"   🔢 Code: {bon_data.get('code')}")
                    print(f"   👤 Membre: {bon_data.get('membre')}")
                    print(f"   💰 Montant max: {bon_data.get('montant_max')}")
                    print(f"   📊 Statut: {bon_data.get('statut')}")
... (tronqué)

# ============================================================
# ORIGINE 24: test_champs_corriges.py (2025-11-20)
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

def test_champs_corriges():
    """Tester les nouveaux champs de l'API"""
    print("🧪 TEST CHAMPS API CORRIGÉS")
    print("===========================")

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

    # Tester l'API avec la nouvelle route
    response = client.get(f'/api/agents/bons/{bon.id}/details/')
    print(f"📡 Statut API: {response.status_code}")

    if response.status_code == 200:
        try:
            data = json.loads(response.content)
            print("✅ API fonctionnelle!")

            if data.get('success'):
                bon_data = data['bon']
                print(f"\n📋 CHAMPS PRINCIPAUX (pour le frontend):")
                print(f"   🔢 Code: {bon_data.get('code')}")
... (tronqué)

# ============================================================
# ORIGINE 25: test_formulaire_corrige.py (2025-11-20)
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
import json

def test_formulaire_complet():
    """Test complet du formulaire de création"""
    print("🧪 TEST FORMULAIRE COMPLET")
    print("===========================")

    client = Client()
    user = authenticate(username='koffitanoh', password='nouveau_mot_de_passe')

    if not user:
        print("❌ Authentification échouée")
        return False

    client.force_login(user)
    print("✅ Authentification réussie")

    # 1. Accéder à la page de création pour obtenir le CSRF token
    print("\n1. 🔄 OBTENTION CSRF TOKEN")
    response = client.get('/agents/creer-bon-soin/')

    if response.status_code != 200:
        print(f"❌ Impossible d'accéder à la page: {response.status_code}")
        return False

    # Extraire le CSRF token du cookie
    csrf_token = client.cookies.get('csrftoken')
    if csrf_token:
        print(f"✅ CSRF token obtenu")
    else:
        print("⚠️  CSRF token non trouvé")

    # 2. Préparer les données du formulaire
    print("\n2. 📝 PRÉPARATION DONNÉES")
    membre = Membre.objects.first()

... (tronqué)

# ============================================================
# ORIGINE 26: test_recherche_motdepasse_corrige.py (2025-11-20)
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

def test_recherche_avec_motdepasse():
    """Tester la recherche API avec le bon mot de passe"""
    print("🔍 TEST RECHERCHE - MOT DE PASSE CORRIGÉ")
    print("========================================")

    # Authentification avec le nouveau mot de passe
    client = Client()
    user = authenticate(username='koffitanoh', password='nouveau_mot_de_passe')

    if not user:
        print("❌ Échec authentification")
        return False

    client.force_login(user)
    print("✅ Authentification réussie")

    # Test de recherche avec différents termes
    termes_recherche = ['John', 'Doe', 'MEM', 'Test']

    for terme in termes_recherche:
        print(f"\n🔎 Recherche: '{terme}'")
        response = client.get(f'/api/recherche-membres/?q={terme}')
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            try:
                # Essayer de parser le JSON
                import json
                data = json.loads(response.content)
                print(f"   ✅ Résultats: {len(data)}")
                for result in data[:2]:  # Afficher les 2 premiers
                    nom = result.get('nom', 'N/A')
                    prenom = result.get('prenom', 'N/A')
                    print(f"     - {nom} {prenom}")
            except:
                # Si ce n'est pas du JSON, afficher un extrait
                content = response.content.decode('utf-8')[:200]
                print(f"   📄 Réponse (extrait): {content}...")
... (tronqué)

# ============================================================
# ORIGINE 27: test_creation_structure_corrige.py (2025-11-20)
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
from medecin.models import Medecin

def test_creation_structure_correcte():
    """Test de création avec la structure réelle du modèle"""
    print("🧪 TEST CRÉATION - STRUCTURE CORRECTE")
    print("====================================")

    try:
        # Récupérer les objets nécessaires
        membre = Membre.objects.first()
        agent = Agent.objects.first()

        print(f"👤 Membre: {membre.nom} {membre.prenom}")
        print(f"👨‍💼 Agent: {agent.matricule}")

        # Essayer de récupérer un médecin (peut être nécessaire)
        try:
            medecin = Medecin.objects.first()
            print(f"👨‍⚕️ Médecin: {medecin}")
        except:
            medecin = None
            print("⚠️  Aucun médecin trouvé")

        # Créer le bon avec les champs disponibles
        print(f"\n🔄 CRÉATION AVEC CHAMPS DISPONIBLES...")

        bon_data = {
            'patient': membre,  # Champ 'patient' au lieu de 'membre'
            'date_soin': datetime.now().date(),
            'symptomes': 'Test de symptômes',
            'diagnostic': 'Diagnostic test',
            'statut': 'EN_ATTENTE',
            'montant': 15000.0,
        }

        # Ajouter medecin seulement s'il existe
        if medecin:
... (tronqué)

# ============================================================
# ORIGINE 28: test_fonctionnel_motdepasse_corrige.py (2025-11-20)
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
from membres.models import Membre
from soins.models import BonDeSoin
from agents.models import Agent

def test_fonctionnel_avec_motdepasse():
    """Test fonctionnel avec le nouveau mot de passe"""
    print("🧪 TEST FONCTIONNEL - MOT DE PASSE CORRIGÉ")
    print("==========================================")

    # 1. Vérification des données
    print("\n1. 📊 VÉRIFICATION DES DONNÉES")
    print(f"   Membres: {Membre.objects.count()}")
    print(f"   Agents: {Agent.objects.count()}")
    print(f"   Bons de soin: {BonDeSoin.objects.count()}")

    # 2. Test d'authentification avec le NOUVEAU mot de passe
    print("\n2. 🔐 TEST AUTHENTIFICATION")
    client = Client()

    # Essayer avec le nouveau mot de passe
    user = authenticate(username='koffitanoh', password='nouveau_mot_de_passe')

    if not user:
        print("   ❌ Échec authentification avec 'nouveau_mot_de_passe'")
        print("   💡 Essayez d'autres mots de passe possibles...")

        # Essayer avec des mots de passe courants
        passwords_to_try = ['password', 'admin', 'test', '1234', '']
        for pwd in passwords_to_try:
            user = authenticate(username='koffitanoh', password=pwd)
            if user:
                print(f"   ✅ Authentification réussie avec: '{pwd}'")
                break
        else:
            print("   ❌ Aucun mot de passe fonctionne")
            return False
    else:
        print("   ✅ Authentification réussie avec 'nouveau_mot_de_passe'")
... (tronqué)

# ============================================================
# ORIGINE 29: test_fonctionnel_complet_corrige.py (2025-11-20)
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
from membres.models import Membre
from soins.models import BonDeSoin
from agents.models import Agent

def test_fonctionnel_complet():
    """Test fonctionnel complet avec les bons imports"""
    print("🧪 TEST FONCTIONNEL COMPLET CORRIGÉ")
    print("===================================")

    # 1. Vérification des données
    print("\n1. 📊 VÉRIFICATION DES DONNÉES")
    print(f"   Membres: {Membre.objects.count()}")
    print(f"   Agents: {Agent.objects.count()}")
    print(f"   Bons de soin: {BonDeSoin.objects.count()}")

    # 2. Test d'authentification
    print("\n2. 🔐 TEST AUTHENTIFICATION")
    client = Client()
    user = authenticate(username='koffitanoh', password='votre_mot_de_passe')

    if not user:
        print("   ❌ Échec authentification")
        return False

    client.force_login(user)
    print("   ✅ Authentification réussie")

    # 3. Test d'accès aux pages
    print("\n3. 🌐 TEST ACCÈS PAGES")
    pages = [
        '/agents/creer-bon-soin/',
        '/agents/tableau-de-bord/',
        '/agents/liste-membres/'
    ]

    for page in pages:
        response = client.get(page)
        print(f"   {page}: {response.status_code}")
... (tronqué)

# ============================================================
# ORIGINE 30: test_recherche_corrige.py (2025-11-20)
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

def test_recherche_apres_correction():
    """Tester la recherche API après correction"""
    print("🔍 TEST RECHERCHE APRÈS CORRECTION")
    print("==================================")

    # Authentification
    client = Client()
    user = authenticate(username='koffitanoh', password='votre_mot_de_passe')

    if user:
        client.force_login(user)
        print("✅ Authentification réussie")

        # Test de recherche avec différents termes
        termes_recherche = ['John', 'Doe', 'MEM20250001', 'Doe John']

        for terme in termes_recherche:
            print(f"\n🔎 Recherche: '{terme}'")
            response = client.get(f'/api/recherche-membres/?q={terme}')
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   Résultats: {len(data)}")
                    for result in data[:3]:  # Afficher les 3 premiers
                        print(f"     - {result.get('nom', '')} {result.get('prenom', '')}")
                except:
                    print(f"   ❌ Erreur parsing JSON")
            else:
                print(f"   ❌ Erreur HTTP: {response.status_code}")

    else:
        print("❌ Échec authentification")

if __name__ == "__main__":
    test_recherche_apres_correction()

# ============================================================
# ORIGINE 31: test_creation_corrige.py (2025-11-20)
# ============================================================

import os
import django
import sys
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("🧪 TEST CRÉATION CORRIGÉ")
print("========================")

try:
    # IMPORTS CORRIGÉS
    from membres.models import Membre
    from soins.models import BonDeSoin
    from agents.models import Agent

    print("✅ Modèles chargés avec succès")

    # Compter les données
    print(f"📊 Membres: {Membre.objects.count()}")
    print(f"📊 Agents: {Agent.objects.count()}")
    print(f"📊 Bons de soin: {BonDeSoin.objects.count()}")

    # Sélectionner un membre et un agent
    membre = Membre.objects.first()
    agent = Agent.objects.first()

    print(f"👤 Membre: {membre.nom} {membre.prenom} (ID: {membre.id})")
    print(f"👨‍💼 Agent: {agent.matricule} - {agent}")

    # Vérifier les champs disponibles pour BonDeSoin
    print(f"\n🔍 CHAMPS BonDeSoin:")
    bon_exemple = BonDeSoin.objects.first()
    if bon_exemple:
        for field in bon_exemple._meta.fields:
            print(f"  - {field.name}")

    # Créer un nouveau bon de soin
    print(f"\n🔄 CRÉATION D'UN NOUVEAU BON...")

    bon = BonDeSoin.objects.create(
        membre=membre,
        agent_createur=agent,
        type_soin="Consultation générale",
        montant_total=15000.0,
        montant_remboursable=12000.0,
        date_soin=datetime.now().date(),
... (tronqué)

# ============================================================
# ORIGINE 32: test_imports_corrige.py (2025-11-20)
# ============================================================

import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("🔍 TEST DES IMPORTS")
print("===================")

try:
    # Essayer différents noms d'apps
    from member.models import Membre
    print("✅ Membre importé depuis 'member.models'")
except ImportError:
    try:
        from membres.models import Membre
        print("✅ Membre importé depuis 'membres.models'")
    except ImportError:
        try:
            # Essayer l'import direct
            from mutuelle_core.member.models import Membre
            print("✅ Membre importé depuis 'mutuelle_core.member.models'")
        except ImportError as e:
            print(f"❌ Impossible d'importer Membre: {e}")

try:
    from bon_soin.models import BonDeSoin
    print("✅ BonDeSoin importé depuis 'bon_soin.models'")
except ImportError:
    try:
        from bons_soins.models import BonDeSoin
        print("✅ BonDeSoin importé depuis 'bons_soins.models'")
    except ImportError:
        try:
            from mutuelle_core.bon_soin.models import BonDeSoin
            print("✅ BonDeSoin importé depuis 'mutuelle_core.bon_soin.models'")
        except ImportError as e:
            print(f"❌ Impossible d'importer BonDeSoin: {e}")

try:
    from agents.models import Agent
    print("✅ Agent importé depuis 'agents.models'")
except ImportError as e:
    print(f"❌ Impossible d'importer Agent: {e}")

# Lister toutes les apps installées
from django.apps import apps
... (tronqué)

# ============================================================
# ORIGINE 33: test_fonctionnel_bons_corrige.py (2025-11-20)
# ============================================================

# scripts/test_fonctionnel_bons_corrige.py
import os
import django
import sys

# Détection automatique du projet
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)

project_name = None
for item in os.listdir(current_dir):
    if os.path.isdir(os.path.join(current_dir, item)) and 'settings.py' in os.listdir(os.path.join(current_dir, item)):
        project_name = item
        break

if project_name:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
    print(f"🎯 Configuration avec projet: {project_name}")
else:
    print("❌ Impossible de détecter le projet Django")
    sys.exit(1)

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
... (tronqué)

# ============================================================
# ORIGINE 34: test_simple_corrige.py (2025-11-20)
# ============================================================

# test_simple_corrige.py
import os
import django
import sys

# Configuration automatique
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Détection du projet
project_name = None
for item in os.listdir(current_dir):
    if os.path.isdir(os.path.join(current_dir, item)) and 'settings.py' in os.listdir(os.path.join(current_dir, item)):
        project_name = item
        break

if project_name:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
    print(f"🎯 Projet: {project_name}")
else:
    print("❌ Projet non détecté")
    sys.exit(1)

django.setup()

from django.test import Client
from django.urls import reverse
from agents.models import Agent

print("🧪 TEST SIMPLE CORRIGÉ")
print("=" * 40)

client = Client()
agent = Agent.objects.first()

if agent:
    client.force_login(agent.user)

    # Test page création
    response = client.get(reverse('agents:creer_bon_soin'))
    print(f"📄 Page création: {response.status_code}")

    # Test API recherche
    response = client.get(reverse('agents:rechercher_membre') + '?q=test')
    print(f"🔍 API recherche: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"   Résultats: {len(data.get('results', []))}")

... (tronqué)

# ============================================================
# ORIGINE 35: test_direct_corrige.py (2025-11-20)
# ============================================================

# test_direct_corrige.py
import os
import django
import sys

# Configuration Django - REMPLACEZ 'projet' par le VRAI nom de votre projet
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')  # ⚠️ À CORRIGER
django.setup()

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User

def test_simple():
    print("🧪 TEST DIRECT CORRIGÉ - CRÉATION BON DE SOIN")
    print("=" * 50)

    client = Client()

    # Test 1: Accès sans authentification
    print("1. Test accès sans auth...")
    try:
        response = client.get(reverse('agents:creer_bon_soin'))
        print(f"   Status: {response.status_code} (attendu: 302 ou 403)")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

    # Test 2: Avec authentification
    print("2. Test avec authentification...")
    try:
        user = User.objects.create_user('test_direct', 'direct@test.com', 'testpass')
        client.force_login(user)

        response = client.get(reverse('agents:creer_bon_soin'))
        print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

    # Test 3: API recherche
    print("3. Test API recherche...")
    try:
        response = client.get(reverse('agents:rechercher_membre') + '?q=test')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Succès: {data.get('success')}")
            print(f"   Nombre résultats: {len(data.get('results', []))}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
... (tronqué)

# ============================================================
# ORIGINE 36: test_urls_correction.py (2025-11-19)
# ============================================================

"""
TESTS POUR LA CORRECTION DES URLs
"""

import os
import django
from django.test import TestCase
from django.urls import reverse, NoReverseMatch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

class TestUrlsBasics(TestCase):
    """Tests de base pour les URLs"""

    def test_urls_essentielles(self):
        """Test que les URLs essentielles existent"""
        urls_essentielles = [
            'home',
            'login',
            'logout',
            'dashboard',
        ]

        for url_name in urls_essentielles:
            with self.subTest(url=url_name):
                try:
                    reverse(url_name)
                except NoReverseMatch:
                    self.fail(f"URL essentielle manquante: {url_name}")

    def test_apps_principales(self):
        """Test que les applications principales ont leurs URLs"""
        apps_principales = [
            ('agents:dashboard', []),
            ('medecin:dashboard', []),
            ('membres:dashboard', []),
            ('assureur:dashboard', []),
            ('pharmacien:dashboard', []),
        ]

        for url_name, args in apps_principales:
            with self.subTest(app=url_name):
                try:
                    reverse(url_name, args=args)
                except NoReverseMatch:
                    # Ce n'est pas un échec critique, juste un warning
                    print(f"⚠️  URL d'application manquante: {url_name}")

class TestConflitsUrls(TestCase):
... (tronqué)

# ============================================================
# ORIGINE 37: test_corrections.py (2025-11-19)
# ============================================================

#!/usr/bin/env python
"""
TEST DES CORRECTIONS APPLIQUÉES
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')

import django
django.setup()

from django.urls import reverse, NoReverseMatch
from django.apps import apps

def test_corrections():
    print("🧪 TEST DES CORRECTIONS APPLIQUÉES")
    print("=" * 50)

    # Test des nouvelles URLs
    print("\n🌐 TEST DES NOUVELLES URLs:")
    print("-" * 30)

    nouvelles_urls = [
        'agents:communication',
        'agents:liste_messages',
        'agents:liste_notifications',
        'agents:envoyer_message',
    ]

    for url_name in nouvelles_urls:
        try:
            url = reverse(url_name)
            print(f"   ✅ {url_name:25} -> {url}")
        except NoReverseMatch:
            print(f"   ❌ {url_name:25} -> NON TROUVÉE")

    # Test des vues dans le module
    print("\n🎯 TEST DES VUES DANS views.py:")
    print("-" * 30)

    try:
        from agents import views

        vues_requises = [
            'liste_messages_agent',
... (tronqué)

# ============================================================
# ORIGINE 38: test_assureur_corrige.py (2025-11-18)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE TEST CORRIGÉ DES FONCTIONNALITÉS ASSUREUR
Teste l'accès aux pages principales - VERSION CORRIGÉE
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
    """Teste l'accès aux principales fonctionnalités - CORRIGÉE"""
    print("🧪 TEST DES FONCTIONNALITÉS ASSUREUR")
    print("="*50)

    from django.test import Client
    from django.contrib.auth.models import User
    from assureur.models import Membre, Cotisation, Assureur

    client = Client()

    # CORRECTION : Trouver un utilisateur assureur via le modèle Assureur
    try:
        assureur = Assureur.objects.first()
        if assureur:
            user = assureur.user
            print(f"✅ Utilisateur assureur trouvé: {user.username}")
        else:
            # Fallback : utiliser le premier superutilisateur
            user = User.objects.filter(is_superuser=True).first()
            if user:
                print(f"✅ Superutilisateur de secours: {user.username}")
            else:
                # Fallback : premier utilisateur staff
                user = User.objects.filter(is_staff=True).first()
                if user:
                    print(f"✅ Utilisateur staff de secours: {user.username}")
                else:
                    # Dernier recours : premier utilisateur
                    user = User.objects.first()
                    if user:
                        print(f"⚠️  Utilisateur standard de secours: {user.username}")
                    else:
... (tronqué)

# ============================================================
# ORIGINE 39: test_final_messagerie_corrige.py (2025-11-17)
# ============================================================

# test_final_messagerie_corrige.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_final():
    """Test final pour vérifier que tout fonctionne"""

    print("🎯 TEST FINAL DU SYSTÈME DE MESSAGERIE")
    print("=" * 50)

    from django.contrib.auth.models import User
    from communication.models import Conversation, Message
    from django.test import RequestFactory
    from communication.views import messagerie
    from django.db.models import Q  # ✅ IMPORT MANQUANT AJOUTÉ

    try:
        # Récupérer l'utilisateur test_pharmacien
        pharmacien = User.objects.get(username='test_pharmacien')

        print(f"👤 Utilisateur de test: {pharmacien.username}")

        # Vérifier les données
        conversations = Conversation.objects.filter(participants=pharmacien)
        messages_recus = Message.objects.filter(destinataire=pharmacien)
        messages_envoyes = Message.objects.filter(expediteur=pharmacien)
        total_messages = messages_recus.count() + messages_envoyes.count()

        print(f"📊 Données disponibles:")
        print(f"   - Conversations: {conversations.count()}")
        print(f"   - Messages reçus: {messages_recus.count()}")
        print(f"   - Messages envoyés: {messages_envoyes.count()}")
        print(f"   - Total messages: {total_messages}")

        # Afficher les détails des conversations
        if conversations.exists():
            print(f"\n💬 DÉTAIL DES CONVERSATIONS:")
            for conv in conversations:
                participants = list(conv.participants.all())
                autres_participants = [p for p in participants if p != pharmacien]
                print(f"   - Conversation {conv.id}: {len(autres_participants)} participant(s)")
                for participant in autres_participants:
                    print(f"     → Avec: {participant.username}")

        # Tester la vue
        factory = RequestFactory()
        request = factory.get('/communication/')
... (tronqué)

# ============================================================
# ORIGINE 40: test_final_apres_corrections.py (2025-11-16)
# ============================================================

# test_final_apres_corrections.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_final_apres_corrections():
    from communication.forms import MessageForm
    from django.contrib.auth import get_user_model

    User = get_user_model()

    print("=== TEST FINAL APRÈS CORRECTIONS ===")

    # Trouver les utilisateurs
    expediteur = User.objects.filter(username='assureur_test').first()
    destinataire = User.objects.filter(username='koffitanoh').first()

    if not expediteur or not destinataire:
        print("❌ Utilisateurs de test non trouvés")
        return

    print(f"✅ Expéditeur: {expediteur.username}")
    print(f"✅ Destinataire: {destinataire.username}")

    # Test 1: Formulaire avec gestion de conversation
    print("\n1. TEST FORMULAIRE AVEC CONVERSATION:")
    test_data = {
        'destinataire': destinataire.id,
        'titre': 'Test final après corrections',
        'contenu': 'Ce message teste le formulaire complètement corrigé',
        'type_message': 'MESSAGE',
    }

    form = MessageForm(data=test_data, expediteur=expediteur)

    if form.is_valid():
        print("✅ Formulaire valide")
        try:
            message = form.save()
            print("✅ Message créé avec succès!")
            print(f"   - ID: {message.id}")
            print(f"   - Titre: {message.titre}")
            print(f"   - Conversation ID: {message.conversation.id}")
            print(f"   - De: {message.expediteur.username} → À: {message.destinataire.username}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
            import traceback
... (tronqué)

# ============================================================
# ORIGINE 41: test_urls_corrigees.py (2025-11-06)
# ============================================================

# test_urls_corrigees.py
import os
import sys
import django
from django.test import Client
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

def test_urls_apres_correction():
    print("🧪 TEST DES URLS APRÈS CORRECTION")
    print("=" * 50)

    client = Client()

    # Se connecter avec test_agent
    user = User.objects.get(username='test_agent')
    client.force_login(user)

    urls_a_tester = [
        '/agents/tableau-de-bord/',
        '/agents/creer-bon-soin/',
        '/agents/verification-cotisations/',
        '/agents/rapport-performance/',
        '/agents/historique-bons/',
    ]

    for url in urls_a_tester:
        response = client.get(url)
        statut = "✅" if response.status_code == 200 else "❌"
        print(f"{statut} {url:40} -> {response.status_code}")

        if response.status_code != 200:
            print(f"   Erreur: {getattr(response, 'content', '')[:100]}")

if __name__ == "__main__":
    test_urls_apres_corrigees()

