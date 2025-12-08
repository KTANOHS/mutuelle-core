"""
FICHIER CONSOLIDÉ: debug
Catégorie: debug
Fusion de 10 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: debug_redirection_assureur.py (2025-12-06)
# ============================================================


#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

print("🔍 DÉBOGAGE REDIRECTION /assureur/")
print("=" * 40)

client = Client()

# Tester avec ktanos (qui fonctionne mais redirige mal)
print("\n🔍 Test avec ktanos:")
if client.login(username='ktanos', password='ktanos'):
    print("✅ Connexion réussie")

    # Tester directement l'accès à /assureur/
    response = client.get('/assureur/', follow=False)
    print(f"🔗 GET /assureur/ - Status: {response.status_code}")

    if response.status_code == 302:
        print(f"🔀 Redirection vers: {response.headers.get('Location')}")

        # Suivre la redirection
        response2 = client.get('/assureur/', follow=True)
        print(f"📄 Après suivi - Status: {response2.status_code}")
        print(f"📍 URL finale: {response2.request['PATH_INFO']}")

    client.logout()

# Vérifier la vue assureur
print("\n🔍 Vérification de la vue assureur...")
views_path = os.path.join(os.getcwd(), 'assureur', 'views.py')

if os.path.exists(views_path):
    with open(views_path, 'r') as f:
        content = f.read()

    print("📄 Analyse de la vue assureur:")

    # Chercher des décorateurs problématiques
    import re

    # Chercher @staff_member_required ou login_required avec vérification staff
... (tronqué)

# ============================================================
# ORIGINE 2: debug_redirections.py (2025-12-06)
# ============================================================


#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User, Group

print("🔍 DÉBOGAGE COMPLET DES REDIRECTIONS")
print("=" * 50)

# 1. Examiner la fonction get_user_redirect_url
print("\n1. ANALYSE DE LA FONCTION get_user_redirect_url")
print("-" * 30)

# Essayer d'importer et d'examiner la fonction
try:
    import inspect
    from core.utils import get_user_redirect_url

    print("✅ Fonction importée depuis core/utils")

    # Afficher le code source
    source = inspect.getsource(get_user_redirect_url)
    print("\n📝 Code source de get_user_redirect_url:")
    print("-" * 20)

    # Afficher seulement les premières lignes
    lines = source.split('\n')
    for i, line in enumerate(lines[:30]):
        print(f"{i+1:3}: {line}")

    if len(lines) > 30:
        print("   ... (tronqué)")

except Exception as e:
    print(f"❌ Erreur: {e}")

# 2. Tester avec chaque utilisateur
print("\n2. TEST MANUEL DE LA DÉTECTION")
print("-" * 30)

def test_user_detection(user):
    """Test manuel de la détection du type d'utilisateur"""
    print(f"\n👤 {user.username}:")

... (tronqué)

# ============================================================
# ORIGINE 3: debug_liste_membres.py (2025-12-04)
# ============================================================

# debug_liste_membres.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from assureur import views

print("🔍 DEBUG DE LA VUE liste_membres")
print("="*60)

# Créer une requête simulée
factory = RequestFactory()

# Créer un utilisateur test (ou utiliser un existant)
try:
    user = User.objects.get(username='DOUA')  # L'utilisateur de vos logs
    print(f"✅ Utilisateur trouvé: {user.username}")
except:
    user = User.objects.filter(is_superuser=True).first()
    if user:
        print(f"✅ Superuser utilisé: {user.username}")

# Test 1: Sans paramètre de recherche
print("\n1. Test sans recherche:")
request1 = factory.get('/assureur/membres/')
request1.user = user

try:
    response1 = views.liste_membres(request1)
    print(f"   Status: Simulé (pas de vrai HTTP)")

    # Extraire le contexte si possible
    if hasattr(response1, 'context_data'):
        ctx = response1.context_data
        print(f"   Context keys: {list(ctx.keys())}")

        if 'page_obj' in ctx:
            page_obj = ctx['page_obj']
            print(f"   page_obj: {len(page_obj)} éléments")
            for i, m in enumerate(page_obj[:3]):
                print(f"     {i+1}. {m.prenom} {m.nom} - {m.numero_unique}")
    else:
        print("   ❌ Pas de contexte disponible")

except Exception as e:
    print(f"   ❌ Erreur: {e}")
... (tronqué)

# ============================================================
# ORIGINE 4: debug_date_error.py (2025-12-03)
# ============================================================

# debug_date_error.py
import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("=== DIAGNOSTIC ERREUR DATE ===")

# 1. Vérifier le format attendu par le modèle Cotisation
from assureur.models import Cotisation
from datetime import datetime

# Test de création d'une cotisation avec différentes dates
test_data = [
    ('2025-12', 'Format YYYY-MM'),
    ('01/12/2025', 'Format dd/mm/yyyy'),
    ('12/2025', 'Format mm/yyyy'),
]

for periode, description in test_data:
    print(f"\nTest avec: {periode} ({description})")
    try:
        # Essayer de créer une cotisation test
        from assureur.models import Membre
        membre = Membre.objects.first()

        if membre:
            cotisation = Cotisation(
                membre=membre,
                periode=periode,
                montant=10000.00,
                statut='en_attente',
                date_emission=datetime.now().date(),
                date_echeance=datetime.now().date(),
                type_cotisation='mensuelle',
                reference='TEST-REF'
            )
            # Essayer de valider le modèle
            cotisation.full_clean()
            print(f"  ✅ Validation réussie")
        else:
            print("  ⚠ Aucun membre trouvé pour le test")
    except Exception as e:
        print(f"  ❌ Erreur: {e}")

# 2. Vérifier s'il y a des signaux ou des méthodes save() qui causent des problèmes
print("\n=== VÉRIFICATION DU MODÈLE COTISATION ===")
try:
... (tronqué)

# ============================================================
# ORIGINE 5: debug_urls.py (2025-12-03)
# ============================================================

# debug_urls.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.urls import reverse, NoReverseMatch
from django.template import Template, Context

print("=== DIAGNOSTIC FINAL ===")

# Test 1: L'URL existe-t-elle dans le système Django ?
try:
    url = reverse('assureur:preview_generation')
    print(f"1. ✅ reverse('assureur:preview_generation') = {url}")
except NoReverseMatch as e:
    print(f"1. ❌ reverse('assureur:preview_generation') échoue: {e}")
    # Vérifier toutes les URLs
    from django.urls import get_resolver
    resolver = get_resolver()
    all_urls = []
    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'name') and pattern.name:
            all_urls.append(pattern.name)
    print(f"   URLs disponibles: {all_urls}")

# Test 2: Le template tag fonctionne-t-il ?
try:
    template_code = """{% url "assureur:preview_generation" %}"""
    template = Template(template_code)
    result = template.render(Context({}))
    print(f"2. ✅ Template tag fonctionne: {result}")
except Exception as e:
    print(f"2. ❌ Template tag échoue: {e}")

# Test 3: Vérifier le contenu exact du template
print("\n3. Vérification du template :")
with open('templates/assureur/generer_cotisations.html', 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines, 1):
        if 'preview_generation' in line:
            print(f"   Ligne {i}: {line.rstrip()}")
            if 'assureur:preview_generation' in line:
                print("     ✅ Correct (avec namespace)")
            else:
                print("     ❌ Problème potentiel")

print("\n=== SOLUTION D'URGENCE ===")
print("Si l'erreur persiste, remplacez dans le template :")
... (tronqué)

# ============================================================
# ORIGINE 6: debug_dashboard.py (2025-12-01)
# ============================================================

#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from pharmacien.views import dashboard_pharmacien
from django.test import RequestFactory
from django.contrib.auth.models import User, AnonymousUser

# Créer une requête de test
factory = RequestFactory()

# 1. Créer une requête avec GLORIA1
gloria = User.objects.get(username='GLORIA1')
request = factory.get('/pharmacien/dashboard/')
request.user = gloria

print("🔍 DEBUG SIMULÉ DU DASHBOARD")
print("=" * 60)
print(f"Utilisateur: {request.user.username} (ID: {request.user.id})")

# Simuler la logique de la vue
from communication.models import Conversation, Notification
from pharmacien.models import Pharmacien
from django.utils import timezone
from datetime import date

try:
    # Récupérer le profil pharmacien
    pharmacien = Pharmacien.objects.get(user=request.user)
    print(f"✅ Pharmacien trouvé: ID {pharmacien.id}")
except Pharmacien.DoesNotExist:
    print("❌ Pharmacien non trouvé")
    pharmacien = None

# Conversations
conversations = Conversation.objects.filter(participants=request.user).order_by('-date_modification')[:5]
print(f"📊 Conversations trouvées: {conversations.count()}")
for conv in conversations:
    participants = [p.username for p in conv.participants.all()]
    print(f"   - Conv {conv.id}: {participants}")

# Notifications
notifications_non_lues = Notification.objects.filter(user=request.user, est_lue=False)
unread_count = notifications_non_lues.count()
print(f"📊 Notifications non lues: {unread_count}")
for notif in notifications_non_lues[:3]:
    print(f"   - '{notif.titre}' (type: {notif.type_notification})")
... (tronqué)

# ============================================================
# ORIGINE 7: debug_temps_reel.py (2025-11-27)
# ============================================================

# debug_temps_reel.py
import os
import django
import sys
import time

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User
from membres.models import Membre

def creer_utilisateur_test():
    """Crée un utilisateur de test avec un mot de passe connu"""
    print("🔧 CRÉATION D'UN UTILISATEUR DE TEST")
    print("=" * 50)

    username = "agent_test"
    password = "test123"

    try:
        # Vérifier si l'utilisateur existe déjà
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': 'Agent',
                'last_name': 'Test',
                'email': 'agent.test@example.com',
                'is_staff': True,
                'is_active': True
            }
        )

        if created:
            user.set_password(password)
            user.save()
            print(f"✅ Utilisateur créé: {username}")
            print(f"🔑 Mot de passe: {password}")
        else:
            # Réinitialiser le mot de passe
            user.set_password(password)
            user.save()
            print(f"✅ Utilisateur existant - mot de passe réinitialisé: {username}")
            print(f"🔑 Nouveau mot de passe: {password}")

        # Vérifier la connexion
        from django.contrib.auth import authenticate
        user_auth = authenticate(username=username, password=password)
... (tronqué)

# ============================================================
# ORIGINE 8: debug_recherche.html (2025-11-20)
# ============================================================

{% extends 'agents/base_agent.html' %}
{% load static %}

{% block title %}Debug Recherche - Agent{% endblock %}
{% block page_title %}Debug Recherche Membres{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-bug me-2"></i>Debug Recherche Membres
                </h5>
            </div>
            <div class="card-body">
                <h6>Statut de la base de données :</h6>
                <ul class="list-unstyled">
                    <li><strong>Module Membres disponible :</strong> {{ MEMBRE_MODEL_AVAILABLE|yesno:"✅,❌" }}</li>
                    <li><strong>Total membres :</strong> {{ total_membres|default:"N/A" }}</li>
                </ul>

                {% if premier_membre %}
                <hr>
                <h6>Premier membre (exemple) :</h6>
                <div class="table-responsive">
                    <table class="table table-sm">
                        <tr><th>ID</th><td>{{ premier_membre.id }}</td></tr>
                        <tr><th>Nom</th><td>{{ premier_membre.nom|default:"N/A" }}</td></tr>
                        <tr><th>Prénom</th><td>{{ premier_membre.prenom|default:"N/A" }}</td></tr>
                        <tr><th>Numéro unique</th><td>{{ premier_membre.numero_unique|default:"N/A" }}</td></tr>
                        <tr><th>Téléphone</th><td>{{ premier_membre.telephone|default:"N/A" }}</td></tr>
                    </table>
                </div>

                <h6>Champs disponibles :</h6>
                <div style="max-height: 200px; overflow-y: auto;">
                    <code class="small">
                        {% for champ in champs_premier_membre %}
                            {% if not champ.startswith '_' %}{{ champ }}{% if not forloop.last %}, {% endif %}{% endif %}
                        {% endfor %}
                    </code>
                </div>
                {% endif %}

                {% if erreur_bdd %}
                <hr>
                <div class="alert alert-danger">
                    <strong>Erreur base de données :</strong> {{ erreur_bdd }}
                </div>
... (tronqué)

# ============================================================
# ORIGINE 9: debug_urls_issue.py (2025-11-19)
# ============================================================

#!/usr/bin/env python
import os
import sys
import django
from django.urls import reverse, NoReverseMatch

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré avec succès")
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def debug_urls():
    """Déboguer les URLs manquantes"""

    print("🔍 DÉBOGAGE DES URLs MANQUANTES")
    print("=" * 50)

    # URLs à vérifier
    urls_to_check = [
        'agents:creer_bon_soin_membre',
        'agents:confirmation_bon_soin'
    ]

    for url_name in urls_to_check:
        try:
            # Essayer avec des arguments
            if 'membre_id' in url_name:
                url = reverse(url_name, args=[1])
            elif 'bon_id' in url_name:
                url = reverse(url_name, args=[1])
            else:
                url = reverse(url_name)

            print(f"✅ {url_name:45} -> {url}")

        except NoReverseMatch as e:
            print(f"❌ {url_name:45} -> NON TROUVÉE: {e}")

        except Exception as e:
            print(f"⚠️  {url_name:45} -> ERREUR: {e}")

def check_urls_file():
    """Vérifier le contenu du fichier agents/urls.py"""

... (tronqué)

# ============================================================
# ORIGINE 10: debug_consultation.py (2025-11-15)
# ============================================================

#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.template.loader import get_template
from django.urls import reverse, resolve
from medecin.models import Consultation, Medecin
from membres.models import Membre
from django.contrib.auth.models import User

def debug_consultation_error():
    """
    Script de diagnostic pour l'erreur de création de consultation
    """
    print("=" * 60)
    print("🔍 DIAGNOSTIC ERREUR CREATION CONSULTATION")
    print("=" * 60)

    # 1. Vérifier les templates
    print("\n1. ✅ VÉRIFICATION DES TEMPLATES")
    try:
        template = get_template('medecin/creer_consultation.html')
        print("   ✓ Template creer_consultation.html trouvé")
    except Exception as e:
        print(f"   ✗ ERREUR Template: {e}")

    try:
        template = get_template('base_medecin.html')
        print("   ✓ Template base_medecin.html trouvé")
    except Exception as e:
        print(f"   ✗ ERREUR Template base: {e}")

    # 2. Vérifier les URLs
    print("\n2. ✅ VÉRIFICATION DES URLs")
    try:
        url = reverse('medecin:creer_consultation')
        print(f"   ✓ URL creer_consultation: {url}")
    except Exception as e:
        print(f"   ✗ ERREUR URL: {e}")

    # 3. Vérifier les modèles
    print("\n3. ✅ VÉRIFICATION DES MODÈLES")
    try:
        medecin_count = Medecin.objects.count()
... (tronqué)

