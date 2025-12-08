"""
FICHIER CONSOLIDÉ: diagnostic
Catégorie: diagnostic
Fusion de 98 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: diagnostic_rapide_applications.py (2025-12-06)
# ============================================================

#!/usr/bin/env python
"""
DIAGNOSTIC RAPIDE - TOUTES LES APPLICATIONS
Version rapide en ligne de commande.
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

from django.conf import settings
from django.apps import apps
from django.db import connection

def diagnostic_rapide_applications():
    """Diagnostic rapide de toutes les applications"""
    print("🔧 DIAGNOSTIC RAPIDE - TOUTES LES APPLICATIONS")
    print("="*60)

    # 1. Lister toutes les applications
    print(f"\n📊 APPLICATIONS INSTALLÉES ({len(settings.INSTALLED_APPS)}):")

    custom_apps = []
    django_apps = []
    third_party_apps = []

    third_party_prefixes = [
        'rest_framework', 'corsheaders', 'crispy_forms', 'channels',
        'django_extensions', 'rest_framework_simplejwt'
    ]

    for app_name in settings.INSTALLED_APPS:
        if app_name.startswith('django.'):
            django_apps.append(app_name)
        elif any(app_name.startswith(prefix) for prefix in third_party_prefixes):
            third_party_apps.append(app_name)
        else:
            custom_apps.append(app_name)

    print(f"  • Applications Django: {len(django_apps)}")
    print(f"  • Applications tierces: {len(third_party_apps)}")
    print(f"  • Applications personnalisées: {len(custom_apps)}")

... (tronqué)

# ============================================================
# ORIGINE 2: diagnostic_ultra_assureur.py (2025-12-06)
# ============================================================

#!/usr/bin/env python
"""
DIAGNOSTIC ULTRA-COMPLET - APPLICATION ASSUREUR
Vérifie absolument tout : du code source à la base de données.
"""

import os
import sys
import django
import ast
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def print_header(title):
    print(f"\n{'='*80}")
    print(f"🔍 {title}")
    print(f"{'='*80}")

def print_check(name, status, details=""):
    """Affiche une vérification avec statut"""
    icons = {"✅": "✅", "⚠️": "⚠️ ", "❌": "❌"}
    icon = icons.get(status, "🔸")
    print(f"{icon} {name}")
    if details:
        print(f"   {details}")

def diagnostic_ultra_complet():
    """Diagnostic ultra-complet de l'application Assureur"""
    print(f"\n{'='*80}")
    print("🎯 DIAGNOSTIC ULTRA-COMPLET - APPLICATION ASSUREUR")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")

    app_name = 'assureur'
    app_path = BASE_DIR / app_name

    if not app_path.exists():
        print(f"❌ L'application '{app_name}' n'existe pas!")
        return

    # 1. STRUCTURE DE L'APPLICATION
    print_header("1. STRUCTURE DE L'APPLICATION")
... (tronqué)

# ============================================================
# ORIGINE 3: diagnostic_assureur_global.py (2025-12-06)
# ============================================================

#!/usr/bin/env python
"""
CORRECTION MINIMALE - SYSTÈME ASSUREUR
Nettoie les groupes et corrige les incohérences sans toucher au superutilisateur.
"""

import os
import sys
import django
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from assureur.models import Assureur

print("🔧 CORRECTION MINIMALE - SYSTÈME ASSUREUR")
print("="*60)
print("⚠️  Le superutilisateur 'matrix' sera préservé")
print("="*60)

corrections = []

# 1. Supprimer le groupe vide "ASSUREUR" (majuscules)
try:
    groupe_vide = Group.objects.get(name='ASSUREUR')
    if groupe_vide.user_set.count() == 0:
        groupe_vide.delete()
        corrections.append("✅ Groupe vide 'ASSUREUR' supprimé")
    else:
        corrections.append("⚠️  Groupe 'ASSUREUR' non vide, conservé")
except Group.DoesNotExist:
    corrections.append("✅ Pas de groupe 'ASSUREUR' à supprimer")

# 2. S'assurer qu'on a le groupe "Assureur" (avec A majuscule)
try:
    groupe_assureur = Group.objects.get(name='Assureur')
    corrections.append(f"✅ Groupe 'Assureur' existe déjà")
except Group.DoesNotExist:
    groupe_assureur = Group.objects.create(name='Assureur')
    corrections.append("✅ Groupe 'Assureur' créé")

# 3. Pour TOUS les profils Assureur (sauf superusers), vérifier qu'ils sont dans le groupe
assureurs = Assureur.objects.select_related('user').all()
for assureur in assureurs:
    user = assureur.user

    if user.is_superuser:
... (tronqué)

# ============================================================
# ORIGINE 4: diagnostic_assureur2.py (2025-12-06)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET - SYSTÈME ASSUREUR
Vérifie tous les aspects du système Assureur et corrige les problèmes.
"""

import os
import sys
import django
from datetime import date, datetime
import logging

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

# Imports Django
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from assureur.models import Assureur
from membres.models import Membre
from soins.models import Bon
from paiements.models import Paiement

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def print_section(title):
    """Affiche une section de diagnostic"""
    print("\n" + "="*80)
    print(f"🔍 {title}")
    print("="*80)

def diagnostic_complet_assureur():
    """
    Diagnostic complet du système Assureur
    """
    print("🎯 DIAGNOSTIC COMPLET DU SYSTÈME ASSUREUR")
    print("="*80)

    # 1. VÉRIFICATION DES GROUPES
    print_section("1. GROUPES D'UTILISATEURS")

    # Liste tous les groupes
    groupes = Group.objects.all().order_by('name')
    print(f"Groupes existants ({groupes.count()}):")
    for groupe in groupes:
        users_count = groupe.user_set.count()
... (tronqué)

# ============================================================
# ORIGINE 5: diagnostic_permissions.txt (2025-12-05)
# ============================================================

================================================================================
RAPPORT DE DIAGNOSTIC DES PERMISSIONS
================================================================================

Problèmes identifiés:
1. DOUA1: Assureur détecté comme Membre
2. Assureurs redirigés vers /admin/ au lieu de /assureur/
3. ORNELLA: Pas de profil Agent associé

Solutions recommandées:
1. Exécuter le script de correction
2. Vérifier les fonctions dans core/utils.py
3. Tester les redirections après correction

# ============================================================
# ORIGINE 6: diagnostic_permissions.py (2025-12-05)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC DES PERMISSIONS ET REDIRECTIONS
Analyse complète du système d'authentification et de permissions
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Initialiser Django
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse, resolve, Resolver404
from django.test import Client
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
import json

print("=" * 80)
print("DIAGNOSTIC COMPLET DES PERMISSIONS")
print("=" * 80)

# ============================================================================
# SECTION 1: VÉRIFICATION DES GROUPES ET PERMISSIONS
# ============================================================================

print("\n🔐 SECTION 1: GROUPES ET PERMISSIONS")
print("-" * 40)

# Lister tous les groupes
print("\n📋 GROUPES DISPONIBLES:")
print("-" * 30)
groups = Group.objects.all()
for group in groups:
    permissions = group.permissions.all()
    print(f"• {group.name} ({group.user_set.count()} utilisateurs)")
    for perm in permissions[:3]:  # Afficher seulement 3 permissions
        print(f"  - {perm.codename}")
    if permissions.count() > 3:
        print(f"  ... et {permissions.count() - 3} autres permissions")

# ============================================================================
# SECTION 2: ANALYSE DES UTILISATEURS
... (tronqué)

# ============================================================
# ORIGINE 7: diagnostic_assureur1.py (2025-12-05)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET - PROFIL ASSUREUR
Version: 1.0
Auteur: Système Mutuelle
Date: 2025-12-05
"""

import os
import sys
import django
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("="*80)
print("DIAGNOSTIC COMPLET - PROFIL ASSUREUR")
print("="*80)

# ==================== SECTION 1: VÉRIFICATION DU SYSTÈME ====================

print("\n🔍 SECTION 1: VÉRIFICATION DU SYSTÈME")
print("-"*40)

try:
    from django.contrib.auth.models import User, Group
    print("✅ Module auth importé avec succès")
except Exception as e:
    print(f"❌ Erreur import auth: {e}")

try:
    from core.utils import get_user_primary_group, get_user_redirect_url
    print("✅ Module core.utils importé avec succès")
except Exception as e:
    print(f"❌ Erreur import core.utils: {e}")

# ==================== SECTION 2: VÉRIFICATION UTILISATEURS ====================

print("\n👥 SECTION 2: VÉRIFICATION DES UTILISATEURS")
print("-"*40)

# Lister tous les utilisateurs
print("\n📋 Liste complète des utilisateurs:")
print("-"*30)
users = User.objects.all()
for user in users:
    groups = [g.name for g in user.groups.all()]
    print(f"• {user.username} (ID: {user.id})")
... (tronqué)

# ============================================================
# ORIGINE 8: diagnostic_communication3.py (2025-12-04)
# ============================================================

#!/usr/bin/env python3
"""
SCRIPT DE DIAGNOSTIC DU SYSTÈME DE COMMUNICATION - VERSION CORRIGÉE
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.urls import reverse, NoReverseMatch
from django.conf import settings

def print_header(title):
    """Affiche un en-tête de section"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def check_sessions():
    """Vérifie les sessions actives"""
    print_header("SESSIONS ACTIVES")
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    print(f"   {sessions.count()} session(s) active(s)")

    for session in sessions[:10]:  # Afficher seulement 10 sessions
        session_data = session.get_decoded()
        if session_data:
            print(f"   - Session {session.session_key}: {session_data}")

def check_users():
    """Vérifie les utilisateurs"""
    print_header("UTILISATEURS")

    total_users = User.objects.count()
    print(f"   Total utilisateurs: {total_users}")

    # Utilisateurs dans le groupe 'assureur'
    try:
        assureur_group = Group.objects.get(name='assureur')
        assureurs = assureur_group.user_set.all()
        print(f"   {assureurs.count()} assureur(s) trouvé(s)")

        for user in assureurs[:5]:  # Afficher seulement 5 assureurs
... (tronqué)

# ============================================================
# ORIGINE 9: diagnostic_communication2.py (2025-12-04)
# ============================================================

#!/usr/bin/env python3
"""
DIAGNOSTIC ET CORRECTION DE LA COMMUNICATION ASSUREUR
Version 1.0 - Vérifications complètes
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré avec succès")
except Exception as e:
    print(f"❌ Erreur Django: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("DIAGNOSTIC COMMUNICATION ASSUREUR")
print("="*80)

# ============================================================================
# PARTIE 1: VÉRIFICATION DES VUES DE COMMUNICATION
# ============================================================================

print("\n🔍 VÉRIFICATION DES VUES DE COMMUNICATION")

try:
    from assureur.views import (
        messagerie_assureur,
        envoyer_message_assureur,
        detail_message,
        repondre_message
    )
    print("✅ Vues de communication trouvées dans assureur.views")
except ImportError as e:
    print(f"❌ Vues de communication non trouvées: {e}")

# ============================================================================
# PARTIE 2: VÉRIFICATION DES URLS
# ============================================================================

print("\n🔍 VÉRIFICATION DES URLS DE COMMUNICATION")

... (tronqué)

# ============================================================
# ORIGINE 10: diagnostic_simple.py (2025-12-04)
# ============================================================

#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré avec succès")
except Exception as e:
    print(f"❌ Erreur Django setup: {e}")
    sys.exit(1)

from django.urls import reverse, NoReverseMatch

print("\n🔍 DIAGNOSTIC DES URLs PROBLEMATIQUES")
print("="*50)

# Liste des URLs à vérifier
urls_a_verifier = [
    ('assureur:creer_bon_pour_membre', [21]),
    ('assureur:creer_bon', []),
    ('assureur:liste_membres', []),
    ('assureur:detail_membre', [21]),
    ('assureur:detail_bon', [1]),
]

print("\n1. Vérification des URLs par nom:")
for url_name, args in urls_a_verifier:
    try:
        if args:
            url = reverse(url_name, args=args)
        else:
            url = reverse(url_name)
        print(f"   ✅ {url_name} -> {url}")
    except NoReverseMatch as e:
        print(f"   ❌ {url_name}: {e}")

# Vérifier l'URL spécifique avec arguments
print("\n2. Test spécifique de 'creer_bon_pour_membre':")
try:
    url = reverse('assureur:creer_bon_pour_membre', args=[21])
    print(f"   ✅ creer_bon_pour_membre(21) -> {url}")
except NoReverseMatch as e:
    print(f"   ❌ creer_bon_pour_membre(21): {e}")
... (tronqué)

# ============================================================
# ORIGINE 11: diagnostic_comple.py (2025-12-04)
# ============================================================


#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET POUR PROJET DJANGO
Vérifie : URLs, vues, templates, modèles et configurations
"""

import os
import sys
import django
import traceback
from pathlib import Path

# ============================================================================
# CONFIGURATION INITIALE
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent
print(f"📁 Répertoire de base: {BASE_DIR}")

# Ajouter le répertoire du projet au path
sys.path.insert(0, str(BASE_DIR))

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()
except Exception as e:
    print(f"❌ Erreur Django setup: {e}")
    sys.exit(1)

from django.urls import get_resolver, reverse, NoReverseMatch
from django.template.loader import get_template
from django.apps import apps
from django.conf import settings

# ============================================================================
# FONCTIONS DE DIAGNOSTIC
# ============================================================================

def verifier_urls_app(app_name='assureur'):
    """Vérifie les URLs de l'application"""
    print(f"\n🔗 VÉRIFICATION DES URLs DE L'APP: {app_name}")
    print("-" * 50)

    resolver = get_resolver()
    urls_trouvees = []
    erreurs = []

    # Parcourir toutes les URLs
    for pattern in resolver.url_patterns:
... (tronqué)

# ============================================================
# ORIGINE 12: diagnostic_assureur7.py (2025-12-03)
# ============================================================

"""
SCRIPT DE DIAGNOSTIC ASSUREUR - Mutuelle Core v2
Ce script vérifie la configuration de l'environnement Django pour l'assureur
"""

import os
import sys
import django
from pathlib import Path
from datetime import datetime

# Ajouter le chemin du projet Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def setup_django():
    """Configurer l'environnement Django"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        django.setup()
        print("✅ Django configuré avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du chargement de Django: {e}")
        return False

def diagnostic_assureur():
    """Exécute un diagnostic complet de la configuration assureur"""

    print("🔍 DIAGNOSTIC ASSUREUR - Mutuelle Core v2")
    print("=" * 60)
    print(f"Date du diagnostic: {datetime.now()}")
    print(f"Répertoire de base: {BASE_DIR}")

    if not setup_django():
        return

    from django.conf import settings

    print(f"Mode DEBUG: {settings.DEBUG}")
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print()

    # 1. Vérifier les applications installées
    print("📦 1. VÉRIFICATION DES APPLICATIONS")
    print("-" * 40)

    apps_assureur = [
        'assureur',
        'agents',
... (tronqué)

# ============================================================
# ORIGINE 13: diagnostic_assureur6.py (2025-12-03)
# ============================================================

"""
SCRIPT DE DIAGNOSTIC ASSUREUR - Mutuelle Core
Ce script vérifie la configuration de l'environnement Django pour l'assureur
"""

import os
import sys
import django
from pathlib import Path
from datetime import datetime

# Ajouter le chemin du projet Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors du chargement de Django: {e}")
    sys.exit(1)

from django.conf import settings

def diagnostic_assureur():
    """Exécute un diagnostic complet de la configuration assureur"""

    print("🔍 DIAGNOSTIC ASSUREUR - Mutuelle Core")
    print("=" * 50)
    print(f"Date du diagnostic: {datetime.now()}")
    print(f"Répertoire de base: {BASE_DIR}")
    print(f"Mode DEBUG: {settings.DEBUG}")
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print()

    # 1. Vérifier les applications installées
    print("📦 1. VÉRIFICATION DES APPLICATIONS")
    print("-" * 30)

    apps_assureur = [
        'assureur',
        'agents',
        'membres',
        'inscription',
        'paiements',
        'soins',
        'notifications',
        'communication',
... (tronqué)

# ============================================================
# ORIGINE 14: diagnostic_assureur5.py (2025-12-03)
# ============================================================

#!/usr/bin/env python3
"""
Script de diagnostic complet pour l'application assureur
Analyse la structure, les modèles, les vues, les URLs et les templates
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    DJANGO_LOADED = True
except Exception as e:
    print(f"⚠️  Django non chargé: {e}")
    DJANGO_LOADED = False

BASE_DIR = Path(__file__).resolve().parent.parent

def analyse_structure_assureur():
    """Analyse la structure de l'application assureur"""
    print("\n" + "="*80)
    print("DIAGNOSTIC ASSUREUR - ANALYSE STRUCTURELLE")
    print("="*80)

    assureur_dir = BASE_DIR / "assureur"
    templates_assureur_dir = BASE_DIR / "templates" / "assureur"
    apps_assureur_dir = BASE_DIR / "apps" / "assureur"

    print(f"\n📁 Répertoire assureur principal: {assureur_dir}")
    print(f"📁 Templates assureur: {templates_assureur_dir}")
    print(f"📁 Apps assureur: {apps_assureur_dir}")

    # Vérifier l'existence des répertoires
    for nom, chemin in [
        ("assureur", assureur_dir),
        ("templates/assureur", templates_assureur_dir),
        ("apps/assureur", apps_assureur_dir)
    ]:
        if chemin.exists():
            print(f"✅ {nom}: EXISTE")
            # Lister les fichiers
            fichiers = list(chemin.rglob("*"))
            print(f"   {len(fichiers)} éléments trouvés")
            for f in fichiers:
... (tronqué)

# ============================================================
# ORIGINE 15: diagnostic_assureur4.py (2025-12-03)
# ============================================================

#!/usr/bin/env python
"""
Script de diagnostic pour l'application assureur
Vérifie les vues, URLs, templates et leurs correspondances
"""

import os
import sys
import inspect
import django
from django.urls import resolve, Resolver404
from django.core.management import execute_from_command_line
from pathlib import Path

# Configuration Django
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation de Django: {e}")
    sys.exit(1)

# Importations après Django setup
from django.urls import get_resolver
from assureur import views
from assureur import urls as assureur_urls
from django.template.loader import get_template
from django.template import TemplateDoesNotExist

class AssureurDiagnostic:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.template_dir = self.base_dir / 'templates' / 'assureur'
        self.views_module = views
        self.urls_module = assureur_urls

    def get_all_views(self):
        """Récupère toutes les vues du module assureur.views"""
        views_list = []

        for name, obj in inspect.getmembers(self.views_module):
            if inspect.isfunction(obj) and obj.__module__ == 'assureur.views':
                views_list.append({
                    'name': name,
                    'function': obj,
                    'file': inspect.getfile(obj),
                    'line': inspect.getsourcelines(obj)[1]
                })
... (tronqué)

# ============================================================
# ORIGINE 16: diagnostic_assureur3.py (2025-12-03)
# ============================================================

#!/usr/bin/env python3
"""
SCRIPT DE DIAGNOSTIC COMPLET POUR L'APPLICATION ASSUREUR

Ce script vérifie tous les composants de l'application assureur :
1. Models, Views, URLs, Admin, Forms, Templates
2. Vérifie la cohérence entre les vues et les URLs
3. Vérifie l'existence des templates nécessaires
4. Vérifie les permissions et décorateurs
"""

import os
import sys
import django
from pathlib import Path

# Configuration de Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation de Django: {e}")
    sys.exit(1)

# ============================================================================
# IMPORTATIONS APRÈS LA CONFIGURATION DJANGO
# ============================================================================

from django.apps import apps
from django.urls import URLPattern, URLResolver, get_resolver
from django.core.checks import run_checks
from django.db import connection
from django.db.models import Model
from django.contrib import admin
from django.contrib.auth.models import Group, Permission

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def print_header(title):
    """Affiche un en-tête de section"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def print_success(message):
... (tronqué)

# ============================================================
# ORIGINE 17: diagnostic_assureu.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
"""
Script de diagnostic pour l'application Assureur
Exécution: python manage.py shell < diagnostic_assureur.py
ou: python diagnostic_assureur.py
"""

import os
import sys
import django
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

from django.contrib.auth.models import User
from django.db import models
from assureur.models import Assureur, Membre, Cotisation, BonPriseEnCharge
from django.urls import reverse, NoReverseMatch
from django.test import Client

class DiagnosticAssureur:
    """Classe de diagnostic pour l'application Assureur"""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success = []
        self.test_user = None

    def print_header(self, title):
        """Affiche un en-tête de section"""
        print(f"\n{'='*60}")
        print(f" {title}")
        print(f"{'='*60}")

    def check_model(self, model_class, model_name):
        """Vérifie si un modèle existe et a des données"""
        self.print_header(f"Vérification du modèle: {model_name}")

        try:
            # Vérifier si la table existe
            table_name = model_class._meta.db_table
... (tronqué)

# ============================================================
# ORIGINE 18: diagnostic_communication1.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
# diagnostic_communication.py - Script complet de diagnostic
import os
import sys
import django
from pathlib import Path

# Ajouter le chemin du projet
project_path = Path(__file__).parent.parent
sys.path.append(str(project_path))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation de Django: {e}")
    sys.exit(1)

print("🔍 DIAGNOSTIC COMPLET - MODULE COMMUNICATION")
print("=" * 60)

# =============================================================================
# 1. VÉRIFICATION DES MODÈLES
# =============================================================================
print("\n📦 1. VÉRIFICATION DES MODÈLES")
print("-" * 40)

try:
    from communication import models
    from django.apps import apps
    from django.db import connection

    # Vérifier si le modèle est enregistré
    app_config = apps.get_app_config('communication')
    print(f"✅ Application 'communication' trouvée")

    # Lister tous les modèles de l'application
    print(f"📋 Modèles dans l'application:")
    for model in app_config.get_models():
        print(f"   • {model.__name__}")

        # Vérifier le nombre d'objets
        try:
            count = model.objects.count()
            print(f"     → {count} objet(s) en base")

            # Vérifier les 3 premiers objets
            if count > 0:
... (tronqué)

# ============================================================
# ORIGINE 19: diagnostic_results.txt (2025-12-02)
# ============================================================

=== DIAGNOSTIC SYSTÈME DE COMMUNICATION ===

1. SESSIONS ACTIVES:
   27 session(s) active(s)
   - Session dypj9pv8fybagdm6ksl2f2i24v7vpibm: {}
   - Session jtulxqe0uo93i874ylpucjiulxch49v6: {}
   - Session 09b8p1zsa7aztrt60li5r9wod6xny3nr: {}
   - Session n3vk38shx6kgbgrmgccn0q705ehfnu5h: {}
   - Session l0n8u1ats8tbsgtz4nkbv81djrg4v00m: {}
   - Session ud12ai4h5dhfiscbsc0hiedvpyaxcfop: {}
   - Session crswggfax1ng24zvlwx0rkoufyyxzx33: {}
   - Session 630i5m4rztenbgz22f86xloz3vly9zes: {}
   - Session mkwjd6wv5fvfuobzp6abl0ti23lo9k2l: {}
   - Session au5vdb2qo21gfn4cxpt8mn9r91xyziig: {}
   - Session zkn9rk7tmppxq8dxcgevbql86hfdafh5: {}
   - Session zf5b5b3ux3018ewvhew72wsxdekmcvu5: {}
   - Session 4yuta3lpvfndd58z6f6k88x83m1emzvp: {}
   - Session c7e3lnfhuh1wc9m7q798mkjsa6hlhno4: {}
   - Session 4r8hyc7gdsq2ilwz2gjek8zb46l2d76f: {}
   - Session oc7ongg3sq4gyco949bt5szown7nbxs7: {}
   - Session wl7iwpex6frjfgjokrwdqyjb8dkxt03a: {}
   - Session zflvz3z8fweycqlrryk0bope8mkomwrs: {}
   - Session y7tu9a6lw8vq6ejsb57g490ag4gmvd8h: {}
   - Session 112ci5ffv48ddkdp2ymzi43xexv8j9ys: {}
   - Session hm4vdwvozmdp4jbcw34wekc85dievacp: {}
   - Session 3ft4x248vhvcp2u15g05ilag5fiwomfr: {}
   - Session 23x8xgih8vurcv5fx9i4h9qlqygoa8j9: {}
   - Session 34tij7mubbowt5xur38dnkl2vh4u99xn: {}
   - Session jocsd0pryrw5xo54v5regii2f98hdd6m: {}
   - Session y4z0frnmk54069ez5zmm54zapt1mti58: {}
   - Session i5ji4snqmkpsm45qnab4iwz2g2qh4q8u: {}

2. UTILISATEURS:
   0 assureur(s) trouvé(s)

3. MESSAGES:
   24 message(s) dans la base

# ============================================================
# ORIGINE 20: diagnostic_ultra_simple.py (2025-12-02)
# ============================================================

# diagnostic_ultra_simple.py
import requests
import json

def main():
    print("🚀 DIAGNOSTIC ULTRA-SIMPLE - Conversation 5")
    print("="*60)

    url = "http://127.0.0.1:8000/communication/api/public/conversations/5/messages/"

    print(f"\n🔗 Test de l'API: {url}")

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data.get('success'):
                total = data.get('total_messages', 0)
                print(f"✅ SUCCÈS: {total} messages récupérés")

                print(f"\n📊 MESSAGES TROUVÉS:")
                messages = data.get('messages', [])

                # Messages recherchés
                searched = [
                    "Test diagnostique",
                    "Test API diagnostique",
                    "Test API",
                    "Shell Test",
                    "Test Diagnostic",
                    "CAPTURE",
                    "Message via API"
                ]

                found_count = 0
                for search in searched:
                    found = False
                    for msg in messages:
                        if search in msg.get('titre', '') or search in msg.get('contenu', ''):
                            found = True
                            break

                    if found:
                        print(f"   ✅ {search}")
                        found_count += 1
                    else:
                        print(f"   ❌ {search}")

... (tronqué)

# ============================================================
# ORIGINE 21: diagnostic_fina.py (2025-12-02)
# ============================================================

# diagnostic_final.py - Version finale sans erreurs
import requests
import json

BASE_URL = "http://127.0.0.1:8000"
CONVERSATION_ID = 5

def test_conversation():
    """Test simple de l'API"""
    print("=" * 60)
    print("DIAGNOSTIC FINAL - Conversation 5")
    print("=" * 60)

    # URL de l'API
    url = f"{BASE_URL}/communication/api/public/conversations/{CONVERSATION_ID}/messages/"

    print(f"\n🔗 URL testée: {url}")

    try:
        print(f"\n📨 Récupération des messages...")
        response = requests.get(url, timeout=10)

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            if data.get('success'):
                total = data.get('total_messages', 0)
                print(f"   ✅ SUCCÈS: {total} messages récupérés")

                # Afficher les titres
                messages = data.get('messages', [])
                print(f"\n📝 Liste des messages:")
                for msg in messages:
                    print(f"   • ID {msg['id']}: {msg['titre']}")
                    print(f"     De: {msg['expediteur']['username']}")
                    print(f"     À: {msg['destinataire']['username']}")
                    print(f"     Date: {msg['date_envoi'][:19]}")
                    print()

                # Exporter
                with open('conversation_5_export.json', 'w') as f:
                    json.dump(data, f, indent=2)

                print(f"💾 Export: conversation_5_export.json")

                # Vérifier les messages spécifiques
                print(f"\n🔍 VÉRIFICATION DES MESSAGES DEMANDÉS:")

... (tronqué)

# ============================================================
# ORIGINE 22: diagnostic_conversation_complet.py (2025-12-02)
# ============================================================

# diagnostic_conversation_complet.py - VERSION CORRIGÉE
import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
CONVERSATION_ID = 5

def print_section(title):
    """Affiche une section avec style"""
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print(f"{'='*60}")

def test_conversation_api():
    """Teste l'API de conversation 5"""
    print_section("TEST DE L'API DE CONVERSATION 5")

    # URL de l'API publique
    api_url = f"{BASE_URL}/communication/api/public/conversations/{CONVERSATION_ID}/messages/"

    print(f"🔗 URL testée: {api_url}")

    try:
        # Test GET - Récupération des messages
        print(f"\n1. Test GET - Récupération des messages...")
        response = requests.get(api_url, timeout=10)

        print(f"   Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            if data.get('success'):
                messages = data.get('messages', [])
                total_messages = data.get('total_messages', 0)

                print(f"   ✅ SUCCÈS: {total_messages} messages récupérés")
                print(f"   📊 Conversation ID: {data.get('conversation_id')}")

                # Afficher un résumé des messages
                print(f"\n   📝 Résumé des messages:")
                for i, msg in enumerate(messages[:5]):  # Afficher les 5 premiers
                    print(f"      {i+1}. ID {msg['id']}: {msg['titre'][:30]}...")
                    print(f"         De: {msg['expediteur']['username']} → À: {msg['destinataire']['username']}")
                    print(f"         Contenu: {msg['contenu'][:50]}...")

                if total_messages > 5:
                    print(f"      ... et {total_messages - 5} autres messages")
... (tronqué)

# ============================================================
# ORIGINE 23: diagnostic_report.json (2025-12-02)
# ============================================================

{
  "timestamp": "2025-12-02",
  "base_url": "http://127.0.0.1:8000",
  "conversation_id": 5,
  "endpoints_tested": 4,
  "results": [
    {
      "endpoint": "/communication/api/public/test/",
      "status": "SUCCESS",
      "data": {
        "status": "API publique fonctionnelle",
        "timestamp": "test",
        "instructions": "Utilisez /api/public/conversations/5/messages/ pour les messages"
      }
    },
    {
      "endpoint": "/communication/api/public/conversations/5/messages/",
      "status": "SUCCESS",
      "message_count": 13,
      "messages": [
        {
          "id": 10,
          "titre": "Test diagnostique",
          "contenu": "Message de test via formulaire",
          "expediteur": {
            "id": 28,
            "username": "GLORIA1",
            "email": ""
          },
          "destinataire": {
            "id": 1,
            "username": "Almoravide",
            "email": "ktanohsoualio@gmail.com"
          },
          "date_envoi": "2025-12-01T11:32:01.037112+00:00",
          "est_lu": false,
          "type_message": "MESSAGE"
        },
        {
          "id": 11,
          "titre": "Test diagnostique",
          "contenu": "Message de test via formulaire",
          "expediteur": {
            "id": 28,
            "username": "GLORIA1",
            "email": ""
          },
          "destinataire": {
            "id": 1,
            "username": "Almoravide",
... (tronqué)

# ============================================================
# ORIGINE 24: diagnostic_complet_final.py (2025-12-02)
# ============================================================

# diagnostic_complet_final.py
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def test_all_endpoints():
    """Teste tous les endpoints API"""
    print("=" * 60)
    print("DIAGNOSTIC COMPLET - API DE COMMUNICATION")
    print("=" * 60)

    endpoints = [
        {
            "url": "/communication/api/public/test/",
            "description": "Test API publique",
            "method": "GET"
        },
        {
            "url": "/communication/api/public/conversations/5/messages/",
            "description": "Messages conversation 5 (API publique)",
            "method": "GET"
        },
        {
            "url": "/communication/api/simple/conversations/5/messages/",
            "description": "Messages conversation 5 (avec auth)",
            "method": "GET"
        },
        {
            "url": "/communication/api/test/messages/",
            "description": "Test API simple",
            "method": "GET"
        }
    ]

    results = []

    for endpoint in endpoints:
        url = BASE_URL + endpoint["url"]
        print(f"\n🔍 Testing: {endpoint['description']}")
... (tronqué)

# ============================================================
# ORIGINE 25: diagnostic_api_approfondi.py (2025-12-02)
# ============================================================

import requests
import json
import sys
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:8000"

def test_all_endpoints():
    """Teste tous les endpoints possibles pour comprendre la structure de l'API"""

    print("🔍 Exploration de la structure de l'API...")
    print("=" * 60)

    endpoints_to_test = [
        ("/api/", "Root API"),
        ("/api/communication/", "Communication API"),
        ("/api/communication/conversations/", "Liste des conversations"),
        ("/api/communication/conversations/5/", "Conversation 5"),
        ("/api/communication/conversations/5/messages/", "Messages conversation 5"),
        ("/api/v1/", "API v1"),
        ("/api/v1/communication/", "Communication API v1"),
        ("/communication/api/", "Communication API endpoint"),
        ("/communication/api/conversations/5/messages/", "Messages via communication API"),
    ]

    found_endpoints = []

    for endpoint, description in endpoints_to_test:
        url = urljoin(BASE_URL, endpoint)
        print(f"\nTesting: {description}")
        print(f"URL: {url}")

        try:
            # Test GET
            response = requests.get(url, timeout=5)

            content_type = response.headers.get('content-type', '')

            print(f"  Status: {response.status_code}")
            print(f"  Content-Type: {content_type}")

            if response.status_code == 200:
                if 'application/json' in content_type:
                    try:
                        data = response.json()
                        print(f"  ✅ JSON valide")
                        if isinstance(data, list):
                            print(f"  📊 Nombre d'éléments: {len(data)}")
                        found_endpoints.append((endpoint, "JSON API"))
                    except:
... (tronqué)

# ============================================================
# ORIGINE 26: diagnostic_complet1.py (2025-12-02)
# ============================================================

import requests
import json
import subprocess
import sys
import os
import time
from urllib.error import URLError

def check_server_status():
    """Vérifie si le serveur Django est en cours d'exécution"""
    print("🔍 Vérification du serveur Django...")

    ports_to_check = [8000, 8080, 8001, 9000]

    for port in ports_to_check:
        url = f"http://127.0.0.1:{port}"
        try:
            response = requests.get(url, timeout=3)
            print(f"   ✅ Serveur trouvé sur le port {port}")
            print(f"      Statut: {response.status_code}")
            print(f"      Réponse: {response.text[:100]}...")
            return port
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Port {port}: Aucun serveur")
        except Exception as e:
            print(f"   ⚠️  Port {port}: Erreur - {e}")

    return None

def check_django_process():
    """Vérifie les processus Django en cours d'exécution"""
    print("\n🔍 Recherche de processus Django...")

    try:
        # Pour Mac/Linux
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        django_processes = [line for line in result.stdout.split('\n') if 'python' in line and ('manage.py' in line or 'django' in line.lower())]

        if django_processes:
            print("   ✅ Processus Django trouvés:")
            for proc in django_processes[:3]:  # Afficher seulement les 3 premiers
                print(f"      - {proc[:80]}")
        else:
            print("   ❌ Aucun processus Django trouvé")

    except Exception as e:
        print(f"   ⚠️  Erreur lors de la recherche des processus: {e}")

def check_database():
    """Vérifie l'état de la base de données"""
... (tronqué)

# ============================================================
# ORIGINE 27: diagnostic_api.py (2025-12-02)
# ============================================================

import requests
import json

BASE_URL = "http://127.0.0.1:8000"
CONVERSATION_ID = 5

def test_endpoint(method, endpoint, data=None):
    """Test un endpoint de l'API"""
    url = f"{BASE_URL}{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            return {"error": f"Méthode {method} non supportée"}

        return {
            "status_code": response.status_code,
            "success": response.status_code in [200, 201],
            "data": response.json() if response.content else None,
            "headers": dict(response.headers)
        }

    except requests.exceptions.ConnectionError:
        return {"error": "Impossible de se connecter au serveur"}
    except requests.exceptions.Timeout:
        return {"error": "Timeout - Le serveur ne répond pas"}
    except json.JSONDecodeError:
        return {"error": "Réponse JSON invalide"}
    except Exception as e:
        return {"error": f"Erreur inattendue: {str(e)}"}

def run_diagnostics():
    """Exécute tous les tests de diagnostic"""
    print("=" * 60)
    print(f"DIAGNOSTIC API - Conversation {CONVERSATION_ID}")
    print("=" * 60)

    # 1. Test de base - Le serveur répond-il?
    print("\n1. Test de connexion au serveur...")
    ping_test = test_endpoint("GET", "/")
    if ping_test.get("error"):
        print(f"   ❌ ÉCHEC: {ping_test['error']}")
        return
    else:
        print(f"   ✅ Succès - Code: {ping_test['status_code']}")

    # 2. Récupérer les détails de la conversation
... (tronqué)

# ============================================================
# ORIGINE 28: diagnostic_gloria1.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC ET RÉPARATION - Problème GLORIA1
"""

import os
import sys
import django
import requests
import re

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group, Permission
from django.db import transaction

def diagnostic_complet():
    """Diagnostic complet de l'utilisateur GLORIA1"""
    print("🔍 DIAGNOSTIC COMPLET - UTILISATEUR GLORIA1")
    print("=" * 60)

    User = get_user_model()

    try:
        # 1. Récupère l'utilisateur
        user = User.objects.get(username='GLORIA1')

        print(f"📋 INFORMATIONS DE BASE:")
        print(f"   ID: {user.id}")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Prénom: {user.first_name}")
        print(f"   Nom: {user.last_name}")
        print(f"   Date joined: {user.date_joined}")
        print(f"   Dernière connexion: {user.last_login}")
        print(f"   Actif: {user.is_active}")
        print(f"   Staff: {user.is_staff}")
        print(f"   Superuser: {user.is_superuser}")

        # 2. Test d'authentification
        print(f"\n🔐 TEST D'AUTHENTIFICATION:")

        # Test avec le mot de passe actuel
        auth_user = authenticate(username='GLORIA1', password='Pharmacien123')
        if auth_user:
            print("   ✅ Authentification réussie avec 'Pharmacien123'")
        else:
... (tronqué)

# ============================================================
# ORIGINE 29: diagnostic_script.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE RÉPARATION AUTOMATIQUE
Corrige les problèmes courants détectés dans le diagnostic
"""

import os
import sys
from pathlib import Path
import re

class AutoFix:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.fixes_applied = []
        self.errors = []

    def fix_import_require_post(self):
        """Corrige l'importation de require_POST"""
        views_path = self.project_path / 'communication' / 'views.py'

        if not views_path.exists():
            self.errors.append("Fichier communication/views.py introuvable")
            return False

        try:
            with open(views_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Recherche et corrige l'import
            if 'from django.views.decorators.csrf import csrf_exempt, require_POST' in content:
                new_content = content.replace(
                    'from django.views.decorators.csrf import csrf_exempt, require_POST',
                    'from django.views.decorators.csrf import csrf_exempt\nfrom django.views.decorators.http import require_POST'
                )

                with open(views_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                self.fixes_applied.append("✅ Import require_POST corrigé")
                return True
            else:
                self.fixes_applied.append("⚠ Import require_POST déjà corrigé")
                return True

        except Exception as e:
            self.errors.append(f"Erreur correction import: {str(e)}")
            return False

    def add_communication_home_view(self):
... (tronqué)

# ============================================================
# ORIGINE 30: diagnostic_system.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
# diagnostic_system.py - Script complet de diagnostic du système

import os
import sys
import django
from pathlib import Path

# Ajouter le répertoire parent au chemin Python
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors du setup Django: {e}")
    sys.exit(1)

from django.core.management import execute_from_command_line
from django.conf import settings
from django.urls import reverse, resolve, Resolver404
from django.template.loader import get_template
from django.contrib.auth.models import User, Group
from django.apps import apps
from django.db import connection

def print_header(title):
    """Affiche un en-tête stylisé"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)

def check_django_setup():
    """Vérifie la configuration Django"""
    print_header("VÉRIFICATION DJANGO")

    try:
        # Vérifier les settings
        print(f"✅ Django version: {django.get_version()}")
        print(f"✅ BASE_DIR: {settings.BASE_DIR}")
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ Installed apps: {len(settings.INSTALLED_APPS)} apps")

        # Vérifier la base de données
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Connexion DB: OK")
... (tronqué)

# ============================================================
# ORIGINE 31: diagnostic_rapide_pharmacien.sh (2025-12-01)
# ============================================================

#!/bin/bash
# DIAGNOSTIC RAPIDE PHARMACIEN

echo "=== DIAGNOSTIC RAPIDE PHARMACIEN ==="
echo "Exécuté le: $(date)"
echo ""

# Vérifications rapides
check() {
    echo -n "Vérification de $1... "
    if $2; then
        echo "✓ OK"
    else
        echo "✗ ÉCHEC"
    fi
}

# 1. Environnement
check "Environnement virtuel" "[ -n \"$VIRTUAL_ENV\" ]"

# 2. Django
check "Django installé" "python -c 'import django' 2>/dev/null"

# 3. Application pharmacien
check "Application pharmacien" "python -c 'import pharmacien' 2>/dev/null"

# 4. Modèle OrdonnancePharmacien
check "Modèle OrdonnancePharmacien" "python -c 'from pharmacien.models import OrdonnancePharmacien' 2>/dev/null"

# 5. Vue historique_validation
check "Vue historique_validation" "python -c 'from pharmacien.views import historique_validation' 2>/dev/null"

# 6. Template historique
check "Template historique" "[ -f \"templates/pharmacien/historique_validation.html\" ]"

# 7. URLs
check "URLs pharmacien" "[ -f \"pharmacien/urls.py\" ]"

# 8. Décorateurs
check "Décorateur pharmacien_required" "[ -f \"pharmacien/decorators.py\" ]"

# Test rapide de la vue
echo ""
echo "=== TEST DE LA VUE historique_validation ==="
python << 'PYTHON_TEST'
import os
import sys
import django

sys.path.insert(0, os.getcwd())
... (tronqué)

# ============================================================
# ORIGINE 32: diagnostic_pharmacien.sh (2025-12-01)
# ============================================================

#!/bin/bash
# Script de diagnostic pour le projet Django - Pharmacien

echo "=================================================="
echo "DIAGNOSTIC DU PROJET DJANGO"
echo "Date: $(date)"
echo "Répertoire courant: $(pwd)"
echo "=================================================="

echo ""
echo "1. ENVIRONNEMENT VIRTUEL"
echo "--------------------------------------------------"
if [ -d "venv" ]; then
    echo "✓ Environnement virtuel trouvé"
    source venv/bin/activate
    echo "Environnement activé"
else
    echo "✗ Environnement virtuel non trouvé"
fi

echo ""
echo "2. VÉRIFICATION DES MODULES DJANGO"
echo "--------------------------------------------------"
python -c "
import sys
print('Python:', sys.version)
try:
    import django
    print('Django:', django.__version__)
    print('Chemin Django:', django.__path__[0])
except ImportError as e:
    print('✗ Django non installé:', e)
"

echo ""
echo "3. STRUCTURE DU PROJET"
echo "--------------------------------------------------"
echo "Arborescence:"
find . -type f -name "*.py" | grep -E "(models|views|urls)\.py$" | head -20

echo ""
echo "4. VÉRIFICATION DES MODÈLES PHARMACIEN"
echo "--------------------------------------------------"
python -c "
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
try:
    import django
    django.setup()
... (tronqué)

# ============================================================
# ORIGINE 33: diagnostic_rapport.json (2025-12-01)
# ============================================================

{
  "timestamp": "2025-12-01T12:12:05.144070+00:00",
  "total_users": 41,
  "conversations": 5,
  "messages": 15,
  "pharmaciens": 1,
  "issues": []
}

# ============================================================
# ORIGINE 34: diagnostic_pharmacien_communication.py (2025-12-01)
# ============================================================

#!/usr/bin/env python3
"""
SCRIPT DE DIAGNOSTIC PHARMACIEN & COMMUNICATION
Diagnostique les problèmes de communication et pharmacien
"""

import os
import sys
import django
import json
import traceback
from pathlib import Path

# Ajouter le chemin du projet
PROJECT_DIR = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_DIR))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors du setup Django: {e}")
    sys.exit(1)

print("=" * 80)
print("🔍 DIAGNOSTIC COMPLET PHARMACIEN & COMMUNICATION")
print("=" * 80)

# ============================================================================
# 1. VÉRIFICATION DES MODÈLES
# ============================================================================
print("\n1. 🔧 VÉRIFICATION DES MODÈLES")
print("-" * 40)

try:
    from communication.models import Conversation, Message, Notification, PieceJointe
    from pharmacien.models import Pharmacien, BonDeSoin, Ordonnance, MedicamentPrescrit

    print("✅ Modèles communication importés")
    print("✅ Modèles pharmacien importés")

except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print(traceback.format_exc())

# ============================================================================
# 2. VÉRIFICATION DES UTILISATEURS ET PERMISSIONS
# ============================================================================
... (tronqué)

# ============================================================
# ORIGINE 35: diagnostic_complet.py (2025-12-01)
# ============================================================


#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from communication.models import Conversation, Message
from django.contrib.auth import get_user_model

def diagnostic_complet():
    User = get_user_model()

    try:
        gloria = User.objects.get(username='GLORIA1')
        print(f"🔍 DIAGNOSTIC COMPLET pour: {gloria.username} (ID: {gloria.id})")
        print("=" * 60)

        # 1. Vérification de l'utilisateur
        print("1. ✅ UTILISATEUR TROUVÉ")
        print(f"   Username: {gloria.username}")
        print(f"   ID: {gloria.id}")
        print(f"   Email: {gloria.email}")
        print()

        # 2. Conversations via related_name (devrait maintenant fonctionner)
        print("2. RECHERCHE DES CONVERSATIONS:")
        try:
            convs_related = gloria.conversations.all()
            print(f"   ✅ gloria.conversations.all(): {convs_related.count()} conversations")
        except Exception as e:
            print(f"   ❌ Erreur related_name: {e}")

        # 3. Conversations via filter
        convs_filter = Conversation.objects.filter(participants=gloria)
        print(f"   ✅ Conversation.objects.filter(participants=gloria): {convs_filter.count()} conversations")
        print()

        # 4. Analyse détaillée de TOUTES les conversations
        print("3. ANALYSE DE TOUTES LES CONVERSATIONS:")
        all_conversations = Conversation.objects.all().prefetch_related('participants')
        print(f"   Total en base: {all_conversations.count()}")

        if all_conversations.count() == 0:
            print("   ⚠️  AUCUNE conversation en base de données!")
            return

        for i, conv in enumerate(all_conversations, 1):
            participants = list(conv.participants.all())
... (tronqué)

# ============================================================
# ORIGINE 36: diagnostic_conversations.py (2025-12-01)
# ============================================================


#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from communication.models import Conversation, Message
from django.contrib.auth import get_user_model

def diagnostic_complet():
    User = get_user_model()

    try:
        gloria = User.objects.get(username='GLORIA1')
        print(f"🔍 Diagnostic pour: {gloria.username} (ID: {gloria.id})")
        print("=" * 50)

        # 1. Conversations via différentes méthodes
        print("1. RECHERCHE DES CONVERSATIONS:")
        convs_method1 = Conversation.objects.filter(participants=gloria)
        print(f"   - filter(participants=user): {convs_method1.count()} conversations")

        convs_method2 = gloria.conversation_set.all()
        print(f"   - user.conversation_set.all(): {convs_method2.count()} conversations")

        # 2. Détail des conversations
        print("\n2. DÉTAIL DES CONVERSATIONS:")
        all_conversations = Conversation.objects.all()
        print(f"   Total en base: {all_conversations.count()} conversations")

        for i, conv in enumerate(all_conversations, 1):
            participants = list(conv.participants.all())
            participant_names = [p.username for p in participants]
            print(f"   {i}. Conversation {conv.id}:")
            print(f"      Participants: {participant_names}")
            print(f"      GLORIA1 dans participants: {gloria in participants}")
            print(f"      Date: {conv.date_creation}")

            # Messages dans cette conversation
            messages = Message.objects.filter(conversation=conv)
            print(f"      Messages: {messages.count()}")
            print()

        # 3. Vérification des relations
        print("3. VÉRIFICATION DES RELATIONS:")
        print(f"   GLORIA1 a {gloria.conversation_set.count()} conversations (relation inverse)")

    except User.DoesNotExist:
... (tronqué)

# ============================================================
# ORIGINE 37: diagnostic_final2.py (2025-12-01)
# ============================================================

#!/usr/bin/env python
"""
DIAGNOSTIC FINAL - POURQUOI LES ORDONNANCES N'APPARAISSENT PAS ?
"""
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_complet():
    """Diagnostic complet du problème"""
    print("🚀 DIAGNOSTIC FINAL - INTERFACE PHARMACIEN")
    print("=" * 60)

    # 1. Vérifier l'état des templates
    print("1. 📄 ÉTAT DES TEMPLATES:")
    templates = [
        'base_pharmacien.html',
        'liste_ordonnances.html',
        '_navbar_pharmacien.html',
        '_sidebar_pharmacien.html',
        '_sidebar_mobile.html'
    ]

    for template in templates:
        path = BASE_DIR / 'templates' / 'pharmacien' / template
        if path.exists():
            size = path.stat().st_size
            status = "✅" if size > 100 else "⚠️"
            print(f"   {status} {template} ({size} octets)")
        else:
            print(f"   ❌ {template} MANQUANT")

    # 2. Analyser le contenu de liste_ordonnances.html
    print("\n2. 🔍 ANALYSE liste_ordonnances.html:")
    liste_path = BASE_DIR / 'templates' / 'pharmacien' / 'liste_ordonnances.html'

    if liste_path.exists():
        with open(liste_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Vérifications critiques
        checks = [
            ('{% extends', 'Héritage base_pharmacien.html'),
            ('{% block content', 'Block content défini'),
... (tronqué)

# ============================================================
# ORIGINE 38: diagnostic_template_pharmacien.py (2025-12-01)
# ============================================================

#!/usr/bin/env python
"""
DIAGNOSTIC TEMPLATE PHARMACIEN - Pourquoi aucune ordonnance n'apparaît
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

def diagnostic_complet():
    """Diagnostic complet du template pharmacien"""
    print("🔍 DIAGNOSTIC TEMPLATE PHARMACIEN")
    print("=" * 60)

    # 1. Vérifier la vue Django
    diagnostic_vue()

    # 2. Vérifier le template
    diagnostic_template()

    # 3. Vérifier les données
    diagnostic_donnees()

    # 4. Vérifier les URLs
    diagnostic_urls()

def diagnostic_vue():
    """Diagnostic de la vue Django"""
    print("\n📋 1. DIAGNOSTIC VUE DJANGO")

    try:
        # Essayer d'importer la vue pharmacien
        from pharmacien import views

        # Vérifier si la vue ordonnances existe
        if hasattr(views, 'ordonnances_pharmacien'):
            print("✅ Vue 'ordonnances_pharmacien' trouvée")

            # Analyser ce que renvoie la vue
            from django.test import RequestFactory
            from django.contrib.auth.models import User

            # Créer une requête simulée
            factory = RequestFactory()
... (tronqué)

# ============================================================
# ORIGINE 39: diagnostic_projet_v2.py (2025-12-01)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET - MUTUELLE CORE V2
Version corrigée des erreurs
"""
import os
import sys
import django
import sqlite3
from pathlib import Path
from datetime import datetime

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Impossible de configurer Django: {e}")
    sys.exit(1)

def print_section(title):
    """Affiche une section du diagnostic"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def diagnostic_initial():
    """Diagnostic initial du projet"""
    print_section("DIAGNOSTIC INITIAL DU PROJET")

    # Vérification de l'environnement
    print(f"📁 Répertoire de base: {BASE_DIR}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"⚙️  Django: {django.get_version()}")

    from django.conf import settings
    print(f"🔧 Mode DEBUG: {settings.DEBUG}")

def diagnostic_settings():
    """Diagnostic des paramètres Django"""
    print_section("PARAMÈTRES DJANGO")

    from django.conf import settings

    # Applications installées
    print(f"📱 Applications installées: {len(settings.INSTALLED_APPS)}")

... (tronqué)

# ============================================================
# ORIGINE 40: diagnostic_projet.py (2025-12-01)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET - MUTUELLE CORE
Vérifie l'état de santé de tous les composants du projet
"""
import os
import sys
import django
import sqlite3
from pathlib import Path
from datetime import datetime

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Impossible de configurer Django: {e}")
    sys.exit(1)

def print_section(title):
    """Affiche une section du diagnostic"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def diagnostic_initial():
    """Diagnostic initial du projet"""
    print_section("DIAGNOSTIC INITIAL DU PROJET")

    # Vérification de l'environnement
    print(f"📁 Répertoire de base: {BASE_DIR}")
    print(f"🐍 Python: {sys.version}")
    print(f"⚙️  Django: {django.get_version()}")
    print(f"🔧 Mode DEBUG: {os.environ.get('DJANGO_DEBUG', 'Non défini')}")

def diagnostic_settings():
    """Diagnostic des paramètres Django"""
    print_section("PARAMÈTRES DJANGO")

    from django.conf import settings

    # Applications installées
    print(f"📱 Applications installées: {len(settings.INSTALLED_APPS)}")
    print("   - " + "\n   - ".join(settings.INSTALLED_APPS))

    # Base de données
... (tronqué)

# ============================================================
# ORIGINE 41: diagnostic_cotisations_final.py (2025-11-30)
# ============================================================

# diagnostic_cotisations_final.py
import os
import sys
import django
import json
from datetime import datetime, timedelta
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.db import connection
from django.db.models import Q, Count
from django.contrib.auth.models import User
from django.apps import apps

print("🔍 DIAGNOSTIC FINAL COTISATIONS ASSUREUR → AGENT")
print("=" * 60)

class DiagnosticCotisationsFinal:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'analyse': {},
            'problemes': [],
            'recommandations': [],
            'actions_immediates': []
        }

    def executer_diagnostic_complet(self):
        """Exécute le diagnostic complet avec corrections"""
        print("🎯 DIAGNOSTIC COMPLET AVEC CORRECTIONS...")

        try:
            # 1. Analyse de la structure actuelle
            self.analyser_structure_actuelle()

            # 2. Diagnostic des problèmes identifiés
            self.diagnostiquer_problemes_specifiques()

            # 3. Solutions immédiates
            self.proposer_solutions_immediates()

            # 4. Générer le rapport d'actions
            self.generer_rapport_actions()

            print("✅ DIAGNOSTIC TERMINÉ AVEC SOLUTIONS")
... (tronqué)

# ============================================================
# ORIGINE 42: diagnostic_cotisations_assureur.py (2025-11-28)
# ============================================================

# diagnostic_cotisations_assureur.py
import os
import django
import sys
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_cotisations_assureur():
    """Script complet de diagnostic du modèle Cotisation dans assureur"""

    print("🔍 DIAGNOSTIC COMPLET DU MODÈLE COTISATION - ASSUREUR")
    print("=" * 60)

    try:
        from assureur.models import Cotisation, Membre, Assureur
        from django.contrib.auth.models import User
        from django.db import models
        from django.utils import timezone
        print("✅ Modèles importés avec succès")
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        return

    # 1. DIAGNOSTIC STRUCTURE MODÈLE
    print("\n📊 STRUCTURE DU MODÈLE COTISATION")
    print("-" * 40)

    try:
        # Vérifier les champs du modèle Cotisation
        cotisation_fields = [f.name for f in Cotisation._meta.get_fields()]
        print(f"✅ Modèle Cotisation - {len(cotisation_fields)} champs:")

        champs_importants = [
            'membre', 'periode', 'type_cotisation', 'montant', 'statut',
            'date_emission', 'date_echeance', 'date_paiement', 'reference'
        ]

        for champ in champs_importants:
            try:
                field_obj = Cotisation._meta.get_field(champ)
                print(f"   ✅ {champ}: {field_obj.get_internal_type()}")
            except:
                print(f"   ❌ {champ}: CHAMP MANQUANT")

    except Exception as e:
        print(f"❌ Erreur analyse structure: {e}")

... (tronqué)

# ============================================================
# ORIGINE 43: diagnostic_permissions_acces.py (2025-11-28)
# ============================================================

# diagnostic_permissions_acces.py

import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.urls import reverse
from django.test import Client

def verifier_structure_base_donnees():
    """Vérifie la structure de la base de données"""
    print("🗃️ STRUCTURE DE LA BASE DE DONNÉES")
    print("=" * 50)

    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

    tables_importantes = [
        'membres_membre', 'soins_bondesoin', 'medecin_ordonnance',
        'pharmacien_ordonnancepharmacien', 'agents_agent', 'paiements_paiement'
    ]

    for table in tables_importantes:
        if table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"✅ {table}: {count} enregistrements")
        else:
            print(f"❌ {table}: TABLE MANQUANTE")

def verifier_groupes_utilisateurs():
    """Vérifie les groupes et leurs permissions"""
    print("\n👥 GROUPES ET UTILISATEURS")
    print("=" * 50)

    groupes_requis = ['Agents', 'Médecins', 'Pharmaciens', 'Membres']

    for nom_groupe in groupes_requis:
        try:
            groupe = Group.objects.get(name=nom_groupe)
... (tronqué)

# ============================================================
# ORIGINE 44: diagnostic_agents_complet.py (2025-11-28)
# ============================================================

# diagnostic_agents_complet.py

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import connection
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.urls import reverse, NoReverseMatch
from django.test import Client

# Import des modèles agents
try:
    from agents.models import Agent, PerformanceAgent
    MODELS_AGENTS_DISPONIBLES = True
except ImportError as e:
    MODELS_AGENTS_DISPONIBLES = False
    print(f"❌ Erreur import modèles agents: {e}")

# Import des autres modèles
try:
    from membres.models import Membre, DossierMedical
    from soins.models import BonDeSoin, Ordonnance
    from communication.models import Notification
    MODELS_AUTRES_DISPONIBLES = True
except ImportError as e:
    MODELS_AUTRES_DISPONIBLES = False
    print(f"⚠️  Erreur import autres modèles: {e}")

def verifier_structure_fichiers():
    """Vérifie la structure des fichiers de l'application agents"""
    print("=" * 80)
    print("🔍 DIAGNOSTIC COMPLET - APPLICATION AGENTS")
    print("=" * 80)

    repertoire_agents = BASE_DIR / "agents"
    templates_agents = BASE_DIR / "templates" / "agents"

    print("\n📁 STRUCTURE DES FICHIERS AGENTS")
    print("-" * 40)

... (tronqué)

# ============================================================
# ORIGINE 45: diagnostic_pharmacien.py (2025-11-28)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET - APPLICATION PHARMACIEN
Analyse la structure, les modèles, les vues et les templates pharmacien
"""

import os
import sys
import django
from pathlib import Path
import inspect

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

# Import des modules pharmacien
try:
    from pharmacien.models import Pharmacien, Medicament
    import pharmacien.views as pharmacien_views
    print("✅ Import des modèles pharmacien réussi")
except ImportError as e:
    print(f"❌ Erreur import pharmacien: {e}")
    pharmacien_views = None

def print_header(title):
    """Affiche un en-tête stylisé"""
    print("\n" + "="*80)
    print(f"🔍 {title}")
    print("="*80)

def analyse_structure_fichiers():
    """Analyse la structure des fichiers de l'application pharmacien"""
    print_header("STRUCTURE DES FICHIERS PHARMACIEN")

    pharmacien_dir = BASE_DIR / "pharmacien"
    templates_dir = BASE_DIR / "templates" / "pharmacien"

    print("📁 Répertoire pharmacien/ :")
    if pharmacien_dir.exists():
        for file in sorted(pharmacien_dir.rglob("*")):
            if file.is_file():
                rel_path = file.relative_to(BASE_DIR)
... (tronqué)

# ============================================================
# ORIGINE 46: diagnostic_assureur.py (2025-11-28)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET - APPLICATION ASSUREUR
Analyse la structure, les modèles, les vues et les templates assureur
"""

import os
import sys
import django
from pathlib import Path
import inspect

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

# Import des modules assureur - CORRECTION DES IMPORTS
try:
    from assureur.models import Assureur
    import assureur.views as assureur_views
    print("✅ Import des modèles assureur réussi")
except ImportError as e:
    print(f"❌ Erreur import assureur: {e}")
    # Continuer avec les imports disponibles
    assureur_views = None

def print_header(title):
    """Affiche un en-tête stylisé"""
    print("\n" + "="*80)
    print(f"🔍 {title}")
    print("="*80)

def analyse_structure_fichiers():
    """Analyse la structure des fichiers de l'application assureur"""
    print_header("STRUCTURE DES FICHIERS ASSUREUR")

    assureur_dir = BASE_DIR / "assureur"
    templates_dir = BASE_DIR / "templates" / "assureur"

    print("📁 Répertoire assureur/ :")
    if assureur_dir.exists():
        for file in sorted(assureur_dir.rglob("*")):
            if file.is_file():
... (tronqué)

# ============================================================
# ORIGINE 47: diagnostic_membres2.py (2025-11-28)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET - APPLICATION MEMBRES
Analyse la structure, les modèles, les vues et les templates
"""

import os
import sys
import django
from pathlib import Path
import inspect

# Configuration Django - CORRECTION DU CHEMIN
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

# CORRECTION : Import correct de l'application membres
from membres.models import Membre
import membres.views as membres_views
from membres.forms import InscriptionMembreForm

def print_header(title):
    """Affiche un en-tête stylisé"""
    print("\n" + "="*80)
    print(f"🔍 {title}")
    print("="*80)

def analyse_structure_fichiers():
    """Analyse la structure des fichiers de l'application"""
    print_header("STRUCTURE DES FICHIERS")

    membres_dir = BASE_DIR / "membres"
    templates_dir = BASE_DIR / "templates" / "membres"

    print("📁 Répertoire membres/ :")
    if membres_dir.exists():
        for file in sorted(membres_dir.rglob("*")):
            if file.is_file():
                rel_path = file.relative_to(BASE_DIR)
                size = file.stat().st_size
                print(f"   📄 {rel_path} ({size} octets)")
    else:
        print("   ❌ Répertoire membres/ non trouvé")
... (tronqué)

# ============================================================
# ORIGINE 48: diagnostic_assureur_boucle.py (2025-11-28)
# ============================================================

import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from assureur.models import Assureur
from django.urls import reverse, resolve, Resolver404
from django.utils import timezone
import logging

# Configuration logging
logging.basicConfig(level=logging.INFO, format='🔍 %(message)s')
logger = logging.getLogger(__name__)

def diagnostic_complet_assureur():
    print("🔍 DIAGNOSTIC COMPLET ERREUR BOUCLE ASSUREUR")
    print("=" * 60)

    # 1. Vérifier l'utilisateur DOUA
    print("\n1. 👤 DIAGNOSTIC UTILISATEUR DOUA")
    print("-" * 40)

    try:
        user_doua = User.objects.get(username='DOUA')
        print(f"✅ Utilisateur DOUA trouvé: ID {user_doua.id}")
        print(f"   📧 Email: {user_doua.email}")
        print(f"   👥 Groupes: {[g.name for g in user_doua.groups.all()]}")
        print(f"   🔐 Est actif: {user_doua.is_active}")
        print(f"   🏢 Est staff: {user_doua.is_staff}")
        print(f"   👑 Est superuser: {user_doua.is_superuser}")
    except User.DoesNotExist:
        print("❌ ERREUR CRITIQUE: Utilisateur DOUA non trouvé!")
        return False
    except Exception as e:
        print(f"❌ Erreur recherche DOUA: {e}")
        return False

    # 2. Vérifier le profil Assureur
    print("\n2. 🏥 DIAGNOSTIC PROFIL ASSUREUR")
    print("-" * 40)

    try:
        assureur = Assureur.objects.filter(user=user_doua).first()
        if assureur:
            print(f"✅ Profil Assureur trouvé: {assureur.numero_employe}")
... (tronqué)

# ============================================================
# ORIGINE 49: diagnostic_final.py (2025-11-28)
# ============================================================

import os
import django
import sys
import requests
from bs4 import BeautifulSoup

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from medecin.models import MaladieChronique

def diagnostic_final():
    print("🔍 DIAGNOSTIC FINAL DES FILTRES")
    print("=" * 60)

    # 1. Données disponibles
    print("1. 📊 DONNÉES DISPONIBLES:")
    patients_count = Membre.objects.count()
    maladies_count = MaladieChronique.objects.count()

    print(f"   👥 Patients dans la base: {patients_count}")
    if patients_count > 0:
        print("      ✅ Patients disponibles:")
        for p in Membre.objects.all()[:5]:  # Afficher les 5 premiers
            print(f"        - {p.prenom} {p.nom} (ID: {p.id})")
    else:
        print("      ❌ Aucun patient dans la base de données")

    print(f"   🩺 Maladies chroniques: {maladies_count}")
    if maladies_count > 0:
        print("      ✅ Maladies disponibles:")
        for m in MaladieChronique.objects.all()[:5]:  # Afficher les 5 premiers
            print(f"        - {m.nom} (Code: {m.code_cim})")
    else:
        print("      ❌ Aucune maladie chronique dans la base de données")

    # 2. Test de la page
    print("\n2. 🌐 TEST PAGE CRÉATION ACCOMPAGNEMENT...")
    try:
        # Simuler une requête à la page de création d'accompagnement
        # (Adapter l'URL selon votre configuration)
        BASE_URL = "http://localhost:8000"

        # Si vous voulez tester une vraie requête HTTP, décommentez :
        # response = requests.get(f"{BASE_URL}/votre-url-creation-accompagnement/")
        # print(f"   📊 Status: {response.status_code}")
        # print(f"   📏 Taille page: {len(response.text)} caractères")
... (tronqué)

# ============================================================
# ORIGINE 50: diagnostic_choix_membre.py (2025-11-28)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre

print("🔍 DIAGNOSTIC DES CHOIX DU MODÈLE MEMBRE")
print("==========================================")

# Analyser tous les champs avec choix
for field in Membre._meta.get_fields():
    if hasattr(field, 'choices') and field.choices:
        print(f"\n📋 Champ: {field.name}")
        print(f"   Type: {field.__class__.__name__}")
        print(f"   Choix disponibles:")
        for choice_value, choice_label in field.choices:
            print(f"     - '{choice_value}' : {choice_label}")

    # Afficher aussi les champs CharField pour voir les valeurs par défaut
    elif field.__class__.__name__ == 'CharField':
        print(f"\n📋 Champ: {field.name}")
        print(f"   Type: CharField")
        if field.default != django.db.models.NOT_PROVIDED:
            print(f"   Valeur par défaut: {field.default}")

# ============================================================
# ORIGINE 51: diagnostic_modeles1.py (2025-11-28)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

from django.apps import apps

def diagnostic_modeles():
    print("🔍 DIAGNOSTIC DES MODÈLES")
    print("=" * 50)

    # 1. Modèle Membre
    print("1. 📋 MODÈLE MEMBRE:")
    try:
        Membre = apps.get_model('membres', 'Membre')
        print("   ✅ Modèle Membre trouvé")
        print("   📝 Champs disponibles:")
        for field in Membre._meta.get_fields():
            print(f"      🎯 {field.name} ({field.__class__.__name__})")
    except LookupError:
        print("   ❌ Modèle Membre non trouvé")

    # 2. Modèle MaladieChronique
    print("\n2. 🩺 MODÈLE MALADIE CHRONIQUE:")
    try:
        MaladieChronique = apps.get_model('medecin', 'MaladieChronique')
        print("   ✅ Modèle MaladieChronique trouvé")
        print("   📝 Champs disponibles:")
        for field in MaladieChronique._meta.get_fields():
            print(f"      🎯 {field.name} ({field.__class__.__name__})")
    except LookupError:
        print("   ❌ Modèle MaladieChronique non trouvé")

    # 3. Vérifier la base de données
    print("\n3. 🗄️ ÉTAT DE LA BASE DE DONNÉES:")
    from django.db import connection

    with connection.cursor() as cursor:
        # Tables membres
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%membre%';")
        tables_membres = cursor.fetchall()
        print(f"   📊 Tables membres: {[t[0] for t in tables_membres]}")

        # Tables medecin
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%maladie%';")
        tables_maladies = cursor.fetchall()
... (tronqué)

# ============================================================
# ORIGINE 52: diagnostic_complet_filtres.py (2025-11-28)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    from django.test import Client
    from membres.models import Membre
    from medecin.models import MaladieChronique

    def diagnostic_complet_filtres():
        print("🔍 DIAGNOSTIC COMPLET DES FILTRES")
        print("=" * 60)

        # 1. Vérifier les données disponibles
        print("1. 📊 DONNÉES DISPONIBLES:")
        patients_count = Membre.objects.count()
        maladies_count = MaladieChronique.objects.count()

        print(f"   👥 Patients dans la base: {patients_count}")
        if patients_count > 0:
            patients = Membre.objects.all()[:3]
            for p in patients:
                print(f"      - {p.get_full_name()} (ID: {p.id})")

        print(f"   🩺 Maladies chroniques: {maladies_count}")
        if maladies_count > 0:
            maladies = MaladieChronique.objects.all()[:3]
            for m in maladies:
                print(f"      - {m.nom} (ID: {m.id})")

        # 2. Test de la page
        client = Client()

        print("\n2. 🔑 Connexion...")
        if not client.login(username='medecin_test', password='password123'):
            print("   ❌ Échec connexion")
            return

        print("   ✅ Connecté")

        # 3. Test de la page
        print("\n3. 🚀 Test page création accompagnement...")
        response = client.get('/medecin/suivi-chronique/accompagnements/creer/')

        print(f"   📊 Status: {response.status_code}")
... (tronqué)

# ============================================================
# ORIGINE 53: diagnostic_complet_template.py (2025-11-28)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

def diagnostic_complet_template():
    print("🔍 DIAGNOSTIC COMPLET DU TEMPLATE")
    print("=" * 50)

    # 1. Vérifier l'existence physique
    template_path = 'templates/medecin/suivi_chronique/tableau_bord.html'
    absolute_path = os.path.abspath(template_path)

    print(f"1. 📁 CHEMIN ABSOLU: {absolute_path}")
    print(f"   📍 Existe: {os.path.exists(absolute_path)}")

    if os.path.exists(absolute_path):
        print(f"   📏 Taille: {os.path.getsize(absolute_path)} octets")
        print(f"   🔐 Permissions: {oct(os.stat(absolute_path).st_mode)[-3:]}")

        # Lire le contenu
        with open(absolute_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"   📄 Lignes: {len(content.splitlines())}")
            print(f"   🔍 Début: {content[:100]}...")
    else:
        print("   ❌ FICHIER NON TROUVÉ - Création immédiate...")
        # Créer le fichier immédiatement
        os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
        with open(absolute_path, 'w', encoding='utf-8') as f:
            f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Suivi Chronique</title>
</head>
<body>
    <h1>Suivi des Maladies Chroniques</h1>
    <p>Module en développement</p>
</body>
</html>''')
        print("   ✅ Fichier créé!")

    # 2. Vérifier la structure des templates
    print("\n2. 📂 STRUCTURE TEMPLATES MEDECIN:")
    templates_dir = 'templates/medecin'
    if os.path.exists(templates_dir):
        for root, dirs, files in os.walk(templates_dir):
            level = root.replace(templates_dir, '').count(os.sep)
... (tronqué)

# ============================================================
# ORIGINE 54: diagnostic_templates1.py (2025-11-28)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    def diagnostic_templates():
        print("🔍 DIAGNOSTIC DES TEMPLATES MANQUANTS")
        print("=" * 50)

        # Vérifier la structure des templates medecin
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates', 'medecin')

        print("1. 📁 STRUCTURE DES TEMPLATES MEDECIN:")
        if os.path.exists(templates_dir):
            for root, dirs, files in os.walk(templates_dir):
                level = root.replace(templates_dir, '').count(os.sep)
                indent = ' ' * 2 * level
                print(f'{indent}📂 {os.path.basename(root)}/')
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    if file.endswith('.html'):
                        print(f'{subindent}📄 {file}')
        else:
            print("   ❌ Dossier templates/medecin non trouvé")

        # Vérifier le template manquant spécifiquement
        template_manquant = 'medecin/suivi_chronique/tableau_bord.html'
        print(f"\n2. 🔎 RECHERCHE DU TEMPLATE: {template_manquant}")

        from django.template.loader import get_template
        try:
            template = get_template(template_manquant)
            print("   ✅ Template trouvé!")
        except:
            print("   ❌ Template non trouvé")

        # Lister tous les templates medecin disponibles
        print("\n3. 📋 TEMPLATES MEDECIN DISPONIBLES:")
        templates_base = os.path.join(templates_dir)
        if os.path.exists(templates_base):
            for file in os.listdir(templates_base):
                if file.endswith('.html'):
                    print(f"   📄 {file}")

        # Vérifier le dossier suivi_chronique
... (tronqué)

# ============================================================
# ORIGINE 55: diagnostic_modele_medecin.py (2025-11-27)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    from django.apps import apps
    from medecin.models import Medecin

    def diagnostic_modele_medecin():
        print("🔍 DIAGNOSTIC DU MODÈLE MÉDECIN")
        print("=" * 50)

        # 1. Obtenir le modèle Medecin
        model = apps.get_model('medecin', 'Medecin')

        # 2. Afficher tous les champs du modèle
        print("📋 CHAMPS DU MODÈLE MÉDECIN:")
        for field in model._meta.get_fields():
            print(f"   🎯 {field.name} ({field.__class__.__name__})")
            if hasattr(field, 'related_model') and field.related_model:
                print(f"      → Related to: {field.related_model}")
            if hasattr(field, 'max_length'):
                print(f"      → Max length: {field.max_length}")

        # 3. Vérifier s'il y a des médecins existants
        print(f"\n📊 MÉDECINS EXISTANTS: {Medecin.objects.count()}")
        for medecin in Medecin.objects.all()[:5]:  # Premiers 5 seulement
            print(f"   👤 {medecin}")
            # Afficher les attributs disponibles
            attrs = [attr for attr in dir(medecin) if not attr.startswith('_') and not callable(getattr(medecin, attr))]
            print(f"      Attributs: {', '.join(attrs[:10])}...")

        # 4. Vérifier la structure via la base de données
        print("\n🗄️ STRUCTURE TABLE MÉDECIN:")
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(medecin_medecin);")
            columns = cursor.fetchall()
            for col in columns:
                print(f"   📝 {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULLABLE'}")

    diagnostic_modele_medecin()

except Exception as e:
    print(f"❌ ERREUR: {e}")
... (tronqué)

# ============================================================
# ORIGINE 56: diagnostic_modeles.py (2025-11-27)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    print("🔍 DIAGNOSTIC DES MODÈLES:")
    print("=" * 40)

    # Lister tous les modèles disponibles dans membres
    from django.apps import apps
    from membres import models as membres_models

    print("📦 Modèles dans membres.models:")
    for name in dir(membres_models):
        obj = getattr(membres_models, name)
        if hasattr(obj, '_meta') and hasattr(obj._meta, 'app_label'):
            if obj._meta.app_label == 'membres':
                print(f"   ✅ {name}")

    print("\n📋 Tous les modèles de l'application 'membres':")
    app_models = apps.get_app_config('membres').get_models()
    for model in app_models:
        print(f"   📝 {model.__name__}")

    # Vérifier les tables en base de données
    print("\n🗄️ Tables en base de données:")
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            if 'membres' in table[0] or 'medecin' in table[0]:
                print(f"   📊 {table[0]}")

except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()

# ============================================================
# ORIGINE 57: diagnostic_template.py (2025-11-27)
# ============================================================

#!/usr/bin/env python
"""
DIAGNOSTIC TEMPLATE MÉDECIN
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def diagnostic_template():
    client = Client()
    client.login(username='medecin_test', password='pass123')

    response = client.get('/medecin/ordonnances/')
    print("🔍 DIAGNOSTIC TEMPLATE:")
    print(f"Status: {response.status_code}")
    print(f"Template utilisé: {response.template_name}")
    print(f"Contenu (extrait): {response.content[:500]}...")

if __name__ == "__main__":
    diagnostic_template()

# ============================================================
# ORIGINE 58: diagnostic_interactions_acteurs.py (2025-11-27)
# ============================================================

#!/usr/bin/env python
"""
DIAGNOSTIC COMPLET DES INTERACTIONS ENTRE ACTEURS
Vérifie la visibilité et synchronisation des données entre tous les acteurs
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q

print("🔍 ===== DIAGNOSTIC DES INTERACTIONS ENTRE ACTEURS =====")
print()

# =============================================================================
# 1. VÉRIFICATION DES MODÈLES ET ACTEURS
# =============================================================================

print("1. 👥 VÉRIFICATION DES ACTEURS ET MODÈLES")

# Récupération des utilisateurs par rôle
try:
    # Agents
    agents = User.objects.filter(
        Q(groups__name='Agents') |
        Q(username__icontains='agent') |
        Q(email__icontains='agent')
    )
    print(f"   ✅ Agents trouvés: {agents.count()}")
    for agent in agents[:3]:
        print(f"      - {agent.username} ({agent.email})")

    # Assureurs
    assureurs = User.objects.filter(
        Q(groups__name='Assureurs') |
        Q(username__icontains='assureur') |
        Q(email__icontains='assureur')
    )
    print(f"   ✅ Assureurs trouvés: {assureurs.count()}")
    for assureur in assureurs[:3]:
... (tronqué)

# ============================================================
# ORIGINE 59: diagnostic_cotisations_final2.py (2025-11-27)
# ============================================================

# diagnostic_cotisations_final.py
import os
import sys
import django
import json
from datetime import datetime, timedelta
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.db import connection
from django.db.models import Q, Count
from django.contrib.auth.models import User
from django.apps import apps

print("🔍 DIAGNOSTIC FINAL COTISATIONS ASSUREUR → AGENT")
print("=" * 60)

class DiagnosticCotisationsFinal:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'analyse': {},
            'problemes': [],
            'recommandations': [],
            'actions_immediates': []
        }

    def executer_diagnostic_complet(self):
        """Exécute le diagnostic complet avec corrections"""
        print("🎯 DIAGNOSTIC COMPLET AVEC CORRECTIONS...")

        try:
            # 1. Analyse de la structure actuelle
            self.analyser_structure_actuelle()

            # 2. Diagnostic des problèmes identifiés
            self.diagnostiquer_problemes_specifiques()

            # 3. Solutions immédiates
            self.proposer_solutions_immediates()

            # 4. Générer le rapport d'actions
            self.generer_rapport_actions()

            print("✅ DIAGNOSTIC TERMINÉ AVEC SOLUTIONS")
... (tronqué)

# ============================================================
# ORIGINE 60: diagnostic_cotisations.py (2025-11-27)
# ============================================================

#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

import logging
from django.utils import timezone
from datetime import timedelta

# Configuration du logger
logger = logging.getLogger('diagnostic')

print("🔍 ===== DIAGNOSTIC SYSTÈME COTISATIONS =====")
print()

# 1. VÉRIFICATION DES MODÈLES
print("1. 📊 VÉRIFICATION DES MODÈLES DISPONIBLES")
try:
    from membres.models import Membre
    print("   ✅ Modèle Membre importé avec succès")

    # Test d'un membre spécifique
    try:
        membre_test = Membre.objects.get(id=6)
        print(f"   ✅ Membre trouvé: ID={membre_test.id}, {membre_test.prenom} {membre_test.nom}")
        print(f"   📅 Date inscription: {getattr(membre_test, 'date_inscription', 'Non définie')}")
        print(f"   💰 Est à jour: {getattr(membre_test, 'est_a_jour', 'Non défini')}")
    except Membre.DoesNotExist:
        print("   ❌ Membre ID=6 non trouvé")
    except Exception as e:
        print(f"   ❌ Erreur récupération membre: {e}")

except ImportError as e:
    print(f"   ❌ Modèle Membre non disponible: {e}")

print()

# 2. VÉRIFICATION DES FONCTIONS DANS LE FICHIER VIEWS
print("2. 🔧 VÉRIFICATION DES FONCTIONS DANS agents/views.py")

def test_fonctions_views():
    """Teste si les fonctions sont bien définies dans views.py"""
    try:
        # Essayer d'importer les fonctions
... (tronqué)

# ============================================================
# ORIGINE 61: diagnostic_formulaire_creation.py (2025-11-27)
# ============================================================

# diagnostic_formulaire_creation.py
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client, RequestFactory
from django.contrib.auth.models import User
from membres.models import Membre
from agents.views import creer_membre
from agents.models import Agent
import logging

# Configuration logging pour voir les erreurs
logging.basicConfig(level=logging.DEBUG)

def diagnostic_formulaire_creation():
    print("🔍 DIAGNOSTIC SPÉCIFIQUE - FORMULAIRE CRÉATION MEMBRE")
    print("=" * 70)

    # 1. TEST DIRECT DE LA VUE
    print("1. 🧪 TEST DIRECT DE LA VUE creer_membre:")

    factory = RequestFactory()

    # Créer une requête POST simulée
    request = factory.post('/agents/creer-membre/', {
        'nom': 'TestDirect',
        'prenom': 'VueDiagnostic',
        'telephone': '0100000001',
        'email': 'test.direct@example.com'
    })

    # Simuler un utilisateur connecté
    try:
        agent_user = User.objects.get(username='koffitanoh')
        request.user = agent_user

        # Appeler directement la vue
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        print("   ✅ Configuration requête simulée")

... (tronqué)

# ============================================================
# ORIGINE 62: diagnostic_creation_membre_amelioré.py (2025-11-27)
# ============================================================

# diagnostic_creation_membre_amelioré.py
import os
import django
import sys
from datetime import datetime
import getpass

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from membres.models import Membre
from agents.models import Agent, ActiviteAgent
import random
import string

def diagnostic_creation_membre_amelioré():
    print("🔍 DIAGNOSTIC CRÉATION MEMBRE PAR AGENT - VERSION AMÉLIORÉE")
    print("=" * 70)

    client = Client()

    # 1. VÉRIFICATION PRÉLIMINAIRE
    print("1. 📋 VÉRIFICATION PRÉLIMINAIRE:")

    total_membres_avant = Membre.objects.count()
    print(f"   ✅ Modèle Membre disponible - {total_membres_avant} membre(s) en base")

    agents = User.objects.filter(groups__name='Agents') | User.objects.filter(agent__isnull=False)
    if not agents.exists():
        print("   ❌ Aucun agent trouvé pour le test")
        return

    agent = agents.first()
    print(f"   ✅ Agent trouvé: {agent.username} ({agent.get_full_name()})")

    # 2. CONNEXION AVEC MOT DE PASSE MANUEL
    print("\n2. 🔐 CONNEXION MANUELLE:")

    print(f"   Agent: {agent.username}")
    print("   💡 Entrez le mot de passe manuellement (ne sera pas affiché):")

    try:
        # Essayer de récupérer le mot de passe de manière sécurisée
        password = getpass.getpass("   Mot de passe: ")

        if not password:
... (tronqué)

# ============================================================
# ORIGINE 63: diagnostic_creation_membre.py (2025-11-27)
# ============================================================

# diagnostic_creation_membre.py
import os
import django
import sys
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from membres.models import Membre
from agents.models import Agent, ActiviteAgent
import random
import string

def generer_donnees_test():
    """Génère des données de test uniques"""
    timestamp = str(random.randint(1000, 9999))
    return {
        'nom': f"Test{timestamp}",
        'prenom': f"Diagnostic{timestamp}",
        'telephone': f"01{random.randint(10000000, 99999999)}",
        'email': f"test.diagnostic{timestamp}@example.com",
        'numero_unique_attendu': f"MEM{''.join(random.choices(string.ascii_uppercase, k=3))}{timestamp[-4:]}"
    }

def diagnostic_creation_membre():
    print("🔍 DIAGNOSTIC CRÉATION MEMBRE PAR AGENT")
    print("=" * 60)

    client = Client()

    # 1. VÉRIFICATION PRÉLIMINAIRE
    print("1. 📋 VÉRIFICATION PRÉLIMINAIRE:")

    # Vérifier que le modèle Membre est disponible
    try:
        from membres.models import Membre
        total_membres_avant = Membre.objects.count()
        print(f"   ✅ Modèle Membre disponible - {total_membres_avant} membre(s) en base")
    except Exception as e:
        print(f"   ❌ Modèle Membre non disponible: {e}")
        return

    # Vérifier qu'il y a des agents
    agents = User.objects.filter(groups__name='Agents') | User.objects.filter(agent__isnull=False)
    if not agents.exists():
... (tronqué)

# ============================================================
# ORIGINE 64: diagnostic_implementation_affichage.py (2025-11-27)
# ============================================================

# diagnostic_implementation_affichage.py
import os
import sys
import django
from pathlib import Path
from datetime import datetime

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

print("🔍 DIAGNOSTIC IMPLÉMENTATION AFFICHAGE_UNIFIE")
print("=" * 60)

class DiagnosticImplementation:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'tests': [],
            'erreurs': [],
            'recommandations': []
        }

    def verifier_import_affichage_unifie(self):
        """Vérifie que le module affichage_unifie est importable"""
        print("\n1. 📦 VÉRIFICATION IMPORT AFFICHAGE_UNIFIE...")

        try:
            from affichage_unifie import afficher_fiche_cotisation_unifiee, determiner_statut_cotisation
            self.rapport['tests'].append({
                'test': 'Import affichage_unifie',
                'statut': '✅ SUCCÈS',
                'details': 'Module importé avec succès'
            })
            print("   ✅ Module affichage_unifie importé avec succès")
            return True
        except ImportError as e:
            self.rapport['erreurs'].append({
                'test': 'Import affichage_unifie',
                'erreur': f'Import impossible: {e}',
                'severite': 'CRITIQUE'
            })
            print(f"   ❌ ERREUR: Impossible d'importer affichage_unifie: {e}")
            return False

    def verifier_fonctions_disponibles(self):
        """Vérifie que les fonctions nécessaires sont disponibles"""
        print("\n2. 🔧 VÉRIFICATION FONCTIONS DISPONIBLES...")
... (tronqué)

# ============================================================
# ORIGINE 65: diagnostic_affichage_recherche_cotisations.py (2025-11-27)
# ============================================================

# diagnostic_affichage_recherche_cotisations.py
import os
import sys
import django
from pathlib import Path
from datetime import datetime, date

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from membres.models import Membre, Cotisation
from agents.models import VerificationCotisation
from django.db.models import Q

print("🔍 DIAGNOSTIC AFFICHAGE RECHERCHE COTISATIONS")
print("=" * 60)

class DiagnosticAffichageRecherche:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'problemes_affichage': [],
            'suggestions_amelioration': [],
            'exemples_corriges': []
        }

    def analyser_affichage_actuel(self):
        """Analyse l'affichage actuel des résultats de recherche"""
        print("🎯 ANALYSE DE L'AFFICHAGE ACTUEL...")

        # Simuler une recherche avec différents critères
        criteres_test = [
            {'telephone': '0710569896'},
            {'numero_unique': 'USER0014'},
            {'nom': 'Test'},
            {'statut': 'en_retard'}
        ]

        for critere in criteres_test:
            self.tester_recherche(critere)

    def tester_recherche(self, critere):
        """Teste une recherche avec un critère spécifique"""
        print(f"\n📋 TEST RECHERCHE: {critere}")

        queryset = Membre.objects.all()

... (tronqué)

# ============================================================
# ORIGINE 66: diagnostic_exactitude_cotisations.py (2025-11-27)
# ============================================================

# diagnostic_exactitude_cotisations.py - VERSION CORRIGÉE
import os
import sys
import django
from pathlib import Path
from datetime import datetime, date, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from membres.models import Membre, Cotisation
from agents.models import VerificationCotisation
from django.db.models import Q, Count, Sum, Avg  # AJOUT: Import Avg manquant
from decimal import Decimal

print("🔍 DIAGNOSTIC EXACTITUDE VÉRIFICATIONS COTISATIONS")
print("=" * 60)

class DiagnosticExactitudeCotisations:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'analyses': [],
            'anomalies': [],
            'recommandations': [],
            'statistiques': {}
        }

    def executer_diagnostic_complet(self):
        """Exécute le diagnostic complet d'exactitude"""
        print("🎯 LANCEMENT DIAGNOSTIC D'EXACTITUDE...")

        try:
            self.verifier_coherence_dates()
            self.verifier_montants_corrects()
            self.verifier_statuts_logiques()
            self.verifier_membres_sans_cotisations()
            self.verifier_doublons_verifications()
            self.generer_rapport_detaille()

            print("✅ DIAGNOSTIC D'EXACTITUDE TERMINÉ")

        except Exception as e:
            print(f"❌ Erreur lors du diagnostic: {str(e)}")
            self.rapport['erreur'] = str(e)

    def verifier_coherence_dates(self):
... (tronqué)

# ============================================================
# ORIGINE 67: diagnostic_cotisations_20251127_112202.json (2025-11-27)
# ============================================================

{
  "timestamp": "2025-11-27T11:22:02.126438",
  "analyse": {
    "modeles": {
      "membres.Membre": {
        "status": "✅ DISPONIBLE",
        "count": 23,
        "champs": [
          "historique_documents",
          "bon",
          "soins",
          "bondesoin",
          "consultations",
          "avis_medecins",
          "ordonnances_medecin",
          "bons_soin",
          "programmeaccompagnement",
          "bonsoin",
          "verificationcotisation",
          "id",
          "user",
          "agent_createur",
          "numero_unique",
          "nom",
          "prenom",
          "telephone",
          "numero_urgence",
          "date_inscription",
          "statut",
          "categorie",
          "cmu_option",
          "date_naissance",
          "adresse",
          "email",
          "profession",
          "date_derniere_cotisation",
          "prochain_paiement_le",
          "est_femme_enceinte",
          "date_debut_grossesse",
          "date_accouchement_prevue",
          "date_accouchement_reelle",
          "avance_payee",
          "carte_adhesion_payee",
          "taux_couverture",
          "type_piece_identite",
          "numero_piece_identite",
          "piece_identite_recto",
          "piece_identite_verso",
          "photo_identite",
          "date_expiration_piece",
... (tronqué)

# ============================================================
# ORIGINE 68: diagnostic_cotisations_20251127_111551.json (2025-11-27)
# ============================================================

{
  "timestamp": "2025-11-27T11:15:51.610788",
  "analyse": {
    "modeles": {
      "erreur": "cannot import name 'Cotisation' from 'membres.models' (/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/projet 21.49.30/membres/models.py)"
    },
    "statistiques": {
      "membres": 23,
      "cotisations": 0,
      "assureurs": 3,
      "verifications": 0
    }
  },
  "problemes": [
    {
      "type": "MODELE_MANQUANT",
      "description": "Modèles non trouvés: membres.Cotisation",
      "severite": "HAUTE"
    }
  ],
  "recommandations": [
    {
      "priorite": "HAUTE",
      "action": "Créer les modèles manquants",
      "description": "Développer les modèles Cotisation et VerificationCotisation si absents"
    }
  ],
  "trace_cotisations": [
    {
      "membre_id": 15,
      "membre_numero": "USER0014",
      "cotisations": "Erreur: cannot import name 'Cotisation' from 'membres.models' (/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/projet 21.49.30/membres/models.py)",
      "verifications": []
    },
    {
      "membre_id": 22,
      "membre_numero": "USER0023",
      "cotisations": "Erreur: cannot import name 'Cotisation' from 'membres.models' (/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/projet 21.49.30/membres/models.py)",
      "verifications": []
    },
    {
      "membre_id": 1,
      "membre_numero": "MEM20250001",
      "cotisations": "Erreur: cannot import name 'Cotisation' from 'membres.models' (/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/projet 21.49.30/membres/models.py)",
      "verifications": [
        {
          "id": 20,
          "statut": "N/A",
          "date":

# ============================================================
# ORIGINE 69: diagnostic_cotisations_assureur_agent1.py (2025-11-27)
# ============================================================

# diagnostic_cotisations_assureur_agent.py
import os
import sys
import django
import json
from datetime import datetime, timedelta
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.db import connection
from django.db.models import Q, Count, F
from django.contrib.auth.models import User

print("🔍 DIAGNOSTIC COTISATIONS ASSUREUR → AGENT")
print("=" * 60)

class DiagnosticCotisations:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'analyse': {},
            'problemes': [],
            'recommandations': [],
            'trace_cotisations': []
        }

    def executer_diagnostic_complet(self):
        """Exécute le diagnostic complet du flux cotisations"""
        print("🎯 DIAGNOSTIC FLUX COTISATIONS ASSUREUR-AGENT...")

        try:
            # 1. Analyse des modèles et relations
            self.analyser_structure_cotisations()

            # 2. Diagnostic du flux de données
            self.diagnostiquer_flux_cotisations()

            # 3. Vérification de la synchronisation
            self.verifier_synchronisation_assureur_agent()

            # 4. Analyse des problèmes courants
            self.analyser_problemes_courants()

            # 5. Générer le rapport
            self.generer_rapport_detaille()
... (tronqué)

# ============================================================
# ORIGINE 70: diagnostic_sync_final_20251127_093311.json (2025-11-27)
# ============================================================

{
  "timestamp": "2025-11-27T09:33:11.529162",
  "module_django": "mutuelle_core",
  "statistiques": {
    "utilisateurs": 38,
    "membres": 12,
    "agents": 7,
    "ordonnances": 3,
    "consultations": 0,
    "bons_de_soin": 0
  },
  "problemes": [
    {
      "type": "SYNCHRONISATION",
      "description": "Faible ratio membres/utilisateurs (31.6%) - synchronisation incomplète",
      "severite": "MOYENNE"
    },
    {
      "type": "SYNCHRONISATION",
      "description": "Seulement 58.3% des membres ont un user associé",
      "severite": "MOYENNE"
    },
    {
      "type": "RELATIONS BROYÉES",
      "description": "5 membres sans utilisateur associé",
      "severite": "HAUTE"
    }
  ],
  "recommandations": [
    {
      "priorite": "HAUTE",
      "action": "Corriger relations membres-user",
      "description": "Associer tous les membres à un utilisateur ou les archiver"
    },
    {
      "priorite": "MOYENNE",
      "action": "Améliorer synchronisation",
      "description": "Automatiser la création des membres pour les nouveaux utilisateurs"
    },
    {
      "priorite": "BASSE",
      "action": "Maintenance régulière",
      "description": "Exécuter ce diagnostic mensuellement pour surveiller la santé des données"
    }
  ],
  "performance": {
    "indexes": 204,
    "enregistrements_totaux": 1590
  },
  "synchronisation": {
... (tronqué)

# ============================================================
# ORIGINE 71: diagnostic_sync_final.py (2025-11-27)
# ============================================================

# diagnostic_sync_final.py
import os
import sys
import django
import json
from datetime import datetime
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.db import connection
from django.db.models import Count, Q
from django.contrib.auth.models import User

print("🔍 DIAGNOSTIC COMPLET DE SYNCHRONISATION - VERSION CORRIGÉE")
print("=" * 60)

# Import des modèles avec les noms corrects
try:
    from membres.models import Membre
    print("✅ Membre importé")
except ImportError as e:
    print(f"❌ Membre: {e}")
    sys.exit(1)

try:
    from medecin.models import Ordonnance, Consultation, BonDeSoin
    print("✅ Modèles medecin importés (BonDeSoin au lieu de BonSoin)")
except ImportError as e:
    print(f"❌ Modèles medecin: {e}")

try:
    from agents.models import Agent
    print("✅ Agent importé")
except ImportError as e:
    print(f"❌ Agent: {e}")

try:
    from communication.models import Notification
    print("✅ Notification importé")
except ImportError as e:
    print(f"❌ Notification: {e}")

class DiagnosticSynchronisationFinal:
    def __init__(self):
        self.resultats = {
... (tronqué)

# ============================================================
# ORIGINE 72: diagnostic_membres1.py (2025-11-27)
# ============================================================

# diagnostic_membres.py
import os
import sys
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.db import connection
from django.contrib.auth.models import User
from django.apps import apps

print("🔍 DIAGNOSTIC APPROFONDI - SYSTÈME MEMBRES")
print("=" * 60)

def investiguer_modele_membre():
    """Investigue pourquoi le modèle Membre n'est pas accessible"""
    print("1. 🔎 Investigation du modèle Membre...")

    # Vérifier si le modèle existe dans les apps
    try:
        modele_membre = apps.get_model('membres', 'Membre')
        print("   ✅ Modèle Membre trouvé dans les apps Django")

        # Compter les membres
        try:
            count = modele_membre.objects.count()
            print(f"   👤 Membres dans la base: {count}")

            if count == 0:
                print("   ⚠️  AUCUN MEMBRE - Base vide ou problème de création")
                return False, count
            else:
                print("   ✅ Membres présents - Problème d'import résolu")
                return True, count

        except Exception as e:
            print(f"   ❌ Erreur comptage membres: {e}")
            return False, 0

    except LookupError:
        print("   ❌ Modèle Membre non trouvé dans les apps")
        return False, 0

def verifier_structure_tables():
    """Vérifie la structure des tables en base"""
... (tronqué)

# ============================================================
# ORIGINE 73: diagnostic_mutuelle_core_20251127_090727.json (2025-11-27)
# ============================================================

{
  "timestamp": "2025-11-27T09:07:27.070279",
  "module_django": "mutuelle_core",
  "statistiques": {
    "utilisateurs": 38,
    "agents": 7
  },
  "problemes": [
    {
      "type": "DONNÉES MANQUANTES",
      "description": "Aucun membre dans la base de données",
      "severite": "MOYENNE"
    }
  ],
  "recommandations": [],
  "performance": {
    "indexes": 204
  },
  "modeles_disponibles": {
    "membres": false,
    "agents": true,
    "medecin": false,
    "communication": true
  },
  "resume_executif": {
    "date_execution": "2025-11-27T09:07:27.070279",
    "module_django": "mutuelle_core",
    "total_problemes": 1,
    "problemes_haute_priorite": 0,
    "problemes_moyenne_priorite": 1,
    "etat_general": "BON"
  }
}

# ============================================================
# ORIGINE 74: diagnostic_auto.py (2025-11-27)
# ============================================================

# diagnostic_auto.py
import os
import sys
import django
import json
from datetime import datetime
from pathlib import Path

def detecter_module_django():
    """Détecte le module Django automatiquement"""
    current_dir = Path(__file__).parent

    # Méthode 1: Via manage.py
    manage_py = current_dir / "manage.py"
    if manage_py.exists():
        with open(manage_py, 'r') as f:
            content = f.read()
            if 'os.environ.setdefault' in content:
                import re
                match = re.search(r"os\.environ\.setdefault\('DJANGO_SETTINGS_MODULE', '([^']+)'", content)
                if match:
                    full_module = match.group(1)
                    return full_module.split('.')[0]

    # Méthode 2: Recherche de settings.py
    for item in current_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            settings_file = item / "settings.py"
            if settings_file.exists():
                return item.name

    # Méthode 3: settings.py à la racine
    if (current_dir / "settings.py").exists():
        return current_dir.name

    return None

# Détection automatique
print("🔍 Détection du module Django...")
module_django = detecter_module_django()

if not module_django:
    print("❌ Impossible de détecter le module Django")
    print("📁 Contenu du dossier:")
    for item in Path('.').iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            print(f"   📂 {item.name}")
    sys.exit(1)

print(f"✅ Module détecté: {module_django}")
... (tronqué)

# ============================================================
# ORIGINE 75: diagnostic_sync.py (2025-11-27)
# ============================================================

# management/commands/diagnostic_sync.py
from django.core.management.base import BaseCommand
from diagnostics.sync_diagnostic import DiagnosticSynchronisation

class Command(BaseCommand):
    help = 'Exécute le diagnostic de synchronisation des données'

    def add_arguments(self, parser):
        parser.add_argument('--correct', action='store_true', help='Applique les corrections')

    def handle(self, *args, **options):
        diagnostic = DiagnosticSynchronisation()
        diagnostic.executer_diagnostic_complet()

        if options['correct']:
            from diagnostics.correcteur_sync import CorrecteurSynchronisation
            correcteur = CorrecteurSynchronisation(mode_test=False)
            correcteur.corriger_problemes(diagnostic.resultats)

# ============================================================
# ORIGINE 76: diagnostic_membres.py (2025-11-26)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC - MEMBRE INTROUVABLE
Version 1.0 - Diagnostic complet de la recherche membres
"""

import os
import sys
import django
from django.db.models import Q

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    django.setup()

    from membres.models import Membre
    from agents.models import Agent
    from django.contrib.auth import get_user_model
    from django.utils import timezone
    import logging

    # Configuration logging
    logging.basicConfig(level=logging.INFO, format='🔍 %(message)s')
    logger = logging.getLogger('diagnostic')

except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def diagnostic_complet():
    """Diagnostic complet du problème des membres introuvables"""

    print("=" * 80)
    print("🔍 DIAGNOSTIC COMPLET - MEMBRES INTROUVABLES")
    print("=" * 80)

    # 1. COMPTAGE DES MEMBRES
    print("\n1. 📊 ANALYSE DE LA BASE DE DONNÉES")
    print("-" * 40)

    try:
        total_membres = Membre.objects.count()
        print(f"✅ Total membres dans la base: {total_membres}")

        # Derniers membres créés
        derniers_membres = Membre.objects.all().order_by('-id')[:5]
        print(f"📋 5 derniers membres (ID décroissant):")
... (tronqué)

# ============================================================
# ORIGINE 77: diagnostic_final.py (2025-11-20)
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

def diagnostic_final():
    """Diagnostic final pour identifier le problème restant"""
    print("🐛 DIAGNOSTIC FINAL")
    print("==================")

    client = Client()
    user = authenticate(username='agent_operateur', password='agent123')

    if not user:
        print("❌ Authentification échouée")
        return

    client.force_login(user)
    print("✅ Authentification réussie")

    # Test de l'API
    print(f"\n🔍 Test API bon #17")
    response = client.get(f'/api/agents/bons/17/details/')

    print(f"📡 URL appelée: /api/agents/bons/17/details/")
    print(f"📊 Statut: {response.status_code}")
    print(f"📦 Réponse complète:")
    print(json.dumps(json.loads(response.content), indent=2, ensure_ascii=False))

    # Vérifier le JavaScript frontend
    print(f"\n🔍 VÉRIFICATION DU FRONTEND")
    print(f"💡 Le problème pourrait être dans le JavaScript qui parse la réponse")
    print(f"🌐 Ouvrez les outils de développement (F12) et vérifiez:")
    print(f"   - La requête réseau vers /api/agents/bons/17/details/")
    print(f"   - La réponse reçue par le navigateur")
    print(f"   - Les erreurs JavaScript dans la console")

if __name__ == "__main__":
    diagnostic_final()

# ============================================================
# ORIGINE 78: diagnostic_complet_frontend.py (2025-11-20)
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

def diagnostic_complet():
    """Diagnostic complet du problème frontend"""
    print("🐛 DIAGNOSTIC COMPLET FRONTEND")
    print("==============================")

    client = Client()
    user = authenticate(username='agent_operateur', password='agent123')

    if not user:
        print("❌ Authentification échouée")
        return

    client.force_login(user)
    print("✅ Authentification réussie")

    # 1. Test de l'API avec le dernier bon créé (ID: 17)
    bon = BonDeSoin.objects.get(id=17)
    print(f"\n1. 🔍 TEST API POUR LE BON #17")

    response = client.get(f'/api/agents/bons/17/details/')
    print(f"   📡 Statut: {response.status_code}")

    if response.status_code == 200:
        data = json.loads(response.content)
        print(f"   ✅ API répond correctement")

        if data.get('success'):
            bon_data = data['bon']
            print(f"   📦 DONNÉES RÉELLES RENVOYÉES PAR L'API:")
            for key, value in bon_data.items():
                print(f"      {key}: {value}")
        else:
            print(f"   ❌ Erreur API: {data.get('error')}")

    # 2. Vérifier la structure exacte attendue par le frontend
    print(f"\n2. 🎯 STRUCTURE ATTENDUE PAR LE FRONTEND")
... (tronqué)

# ============================================================
# ORIGINE 79: diagnostic_models.py (2025-11-20)
# ============================================================

# diagnostic_models.py
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')  # Remplacez par votre vrai nom de projet
django.setup()

def diagnostic_models():
    print("🔍 DIAGNOSTIC DES MODÈLES")
    print("=" * 50)

    # Vérifier Assureur
    try:
        from assureur.models import Assureur
        print("✅ Modèle Assureur importé")
        print(f"   Champs disponibles: {[f.name for f in Assureur._meta.get_fields()]}")
    except Exception as e:
        print(f"❌ Erreur Assureur: {e}")

    # Vérifier Agent
    try:
        from agents.models import Agent
        print("✅ Modèle Agent importé")
        print(f"   Champs disponibles: {[f.name for f in Agent._meta.get_fields()]}")
    except Exception as e:
        print(f"❌ Erreur Agent: {e}")

    # Vérifier Membre
    try:
        from membres.models import Membre
        print("✅ Modèle Membre importé")
        print(f"   Champs disponibles: {[f.name for f in Membre._meta.get_fields()]}")
    except Exception as e:
        print(f"❌ Erreur Membre: {e}")

    # Vérifier BonSoin
    try:
        from agents.models import BonSoin
        print("✅ Modèle BonSoin importé")
        print(f"   Champs disponibles: {[f.name for f in BonSoin._meta.get_fields()]}")
    except Exception as e:
        print(f"❌ Erreur BonSoin: {e}")

if __name__ == "__main__":
    diagnostic_models()

# ============================================================
# ORIGINE 80: diagnostic_rapide.py (2025-11-19)
# ============================================================

# diagnostic_rapide.py
import os
import django
from django.urls import reverse, NoReverseMatch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_rapide():
    print("🔍 DIAGNOSTIC RAPIDE - communication:liste_notifications")
    print("=" * 60)

    # Test direct
    try:
        url = reverse('communication:liste_notifications')
        print(f"✅ URL TROUVÉE: {url}")
        return True
    except NoReverseMatch as e:
        print(f"❌ ERREUR: {e}")
        print("\n🔧 SOLUTIONS IMMÉDIATES:")
        print("1. Vérifiez que communication/urls.py contient:")
        print('   path("notifications/", views.XXX, name="liste_notifications")')
        print("\n2. Vérifiez que l'app communication est dans INSTALLED_APPS")
        print("\n3. Vérifiez l'inclusion dans urls.py principal:")
        print('   path("communication/", include("communication.urls"))')
        return False

# Test alternatif
def tester_variantes():
    print("\n🔄 TEST DES VARIANTES:")
    variantes = [
        'communication:liste_notifications',
        'communication:notification_list',
        'liste_notifications',
    ]

    for var in variantes:
        try:
            url = reverse(var)
            print(f"✅ {var} -> {url}")
        except:
            print(f"❌ {var} -> NON TROUVÉE")

if __name__ == "__main__":
    if diagnostic_rapide():
        print("\n🎉 Le problème semble résolu!")
    else:
        print("\n🔴 Le problème persiste. Lancer le diagnostic complet.")
        tester_variantes()

# ============================================================
# ORIGINE 81: diagnostic_urls.py (2025-11-19)
# ============================================================

# diagnostic_urls.py
import os
import sys
import django
from django.urls import reverse, NoReverseMatch, get_resolver
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_complet():
    print("=" * 80)
    print("DIAGNOSTIC COMPLET DES URLS DJANGO")
    print("=" * 80)

    # 1. Vérifier l'URL problématique
    url_problematique = 'communication:liste_notifications'
    print(f"\n1. VÉRIFICATION DE L'URL: {url_problematique}")
    print("-" * 50)

    try:
        url = reverse(url_problematique)
        print(f"✅ SUCCÈS: URL trouvée -> {url}")
    except NoReverseMatch as e:
        print(f"❌ ERREUR: {e}")

    # 2. Lister toutes les URLs de l'app communication
    print(f"\n2. URLS DE L'APP 'communication'")
    print("-" * 50)

    resolver = get_resolver()
    urls_communication = []

    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'url_patterns'):  # Namespace ou include
            for sub_pattern in pattern.url_patterns:
                if hasattr(sub_pattern, 'app_name') and sub_pattern.app_name == 'communication':
                    for url_pattern in sub_pattern.url_patterns:
                        urls_communication.append({
                            'pattern': url_pattern.pattern,
                            'name': getattr(url_pattern, 'name', 'SANS_NOM'),
                            'callback': getattr(url_pattern, 'callback', None)
                        })

    if not urls_communication:
        print("❌ Aucune URL trouvée pour l'app 'communication'")
        # Essayer une autre méthode
        print("\n🔍 Recherche alternative des URLs...")
        all_urls = []
... (tronqué)

# ============================================================
# ORIGINE 82: diagnostic_templates.py (2025-11-19)
# ============================================================

#!/usr/bin/env python3
# diagnostic_templates.py

import os
import django
from pathlib import Path

# Configuration Django minimale
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.template.loader import get_template

def check_templates():
    print("🔍 DIAGNOSTIC DES TEMPLATES MEDECIN")
    print("=" * 50)

    templates_to_check = [
        'medecin/dashboard.html',
        'medecin/liste_bons.html',
        'medecin/mes_rendez_vous.html',
        'medecin/creer_ordonnance.html'
    ]

    for template_name in templates_to_check:
        try:
            template = get_template(template_name)
            print(f"✅ {template_name} - TROUVÉ")
        except Exception as e:
            print(f"❌ {template_name} - ERREUR: {e}")

if __name__ == "__main__":
    check_templates()

# ============================================================
# ORIGINE 83: diagnostic_final_complet.py (2025-11-19)
# ============================================================

# diagnostic_final_complet.py
import os
import django
import sys
from datetime import datetime, timedelta

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.db import transaction
from django.db.models import Q
from django.apps import apps
from django.utils import timezone

User = get_user_model()

class DiagnosticComplet:
    """
    Script de diagnostic COMPLET - version finalissime
    """

    def __init__(self):
        self.results = {
            'success': [],
            'warnings': [],
            'errors': []
        }
        self.models = {}
        self.test_data = {}

    def log_success(self, message):
        self.results['success'].append(message)
        print(f"✅ {message}")

    def log_warning(self, message):
        self.results['warnings'].append(message)
        print(f"⚠️ {message}")

    def log_error(self, message):
        self.results['errors'].append(message)
        print(f"❌ {message}")

    def detecter_modeles(self):
        """Détecter automatiquement tous les modèles disponibles"""
        print("🔍 Détection des modèles...")

        # Parcourir toutes les applications
... (tronqué)

# ============================================================
# ORIGINE 84: diagnostic_membre_erreur.py (2025-11-17)
# ============================================================

#!/usr/bin/env python3
"""
SCRIPT DE DIAGNOSTIC - Erreur "Cannot resolve keyword 'membre'"
Usage: python diagnostic_membre_erreur.py
"""

import os
import sys
import django
import re
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

from django.apps import apps
from django.db import models
from django.core.exceptions import FieldDoesNotExist

class DiagnosticMembreErreur:
    """Classe pour diagnostiquer l'erreur 'Cannot resolve keyword membre'"""

    def __init__(self):
        self.resultats = {
            'erreurs_trouvees': [],
            'modeles_avec_problemes': [],
            'fichiers_avec_erreurs': [],
            'suggestions_correction': []
        }

    def analyser_structure_modeles(self):
        """Analyse la structure des modèles et leurs relations"""
        print("\n" + "="*70)
        print("🔍 ANALYSE STRUCTURELLE DES MODÈLES")
        print("="*70)

        # Obtenir tous les modèles
        tous_les_modeles = apps.get_models()

        print(f"📊 Modèles trouvés: {len(tous_les_modeles)}")

        # Analyser chaque modèle
... (tronqué)

# ============================================================
# ORIGINE 85: diagnostic_final_vue.py (2025-11-17)
# ============================================================

# diagnostic_final_vue.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_final_vue():
    """Diagnostic final de la vue messagerie originale"""

    print("🔍 DIAGNOSTIC FINAL VUE MESSAGERIE ORIGINALE")
    print("=" * 60)

    # 1. Vérifier le type de réponse de la vue
    from communication.views import messagerie
    from django.test import RequestFactory
    from django.contrib.auth.models import User

    try:
        pharmacien = User.objects.get(username='test_pharmacien')
        factory = RequestFactory()
        request = factory.get('/communication/')
        request.user = pharmacien

        print("1. 🧪 TEST DU TYPE DE RÉPONSE:")
        response = messagerie(request)

        print(f"   - Type de réponse: {type(response)}")
        print(f"   - Statut: {response.status_code}")
        print(f"   - Content-Type: {response.get('Content-Type', 'Non défini')}")

        # Vérifier si c'est un TemplateResponse
        from django.template.response import TemplateResponse
        if isinstance(response, TemplateResponse):
            print("   ✅ C'est un TemplateResponse")
            print(f"   - Template: {response.template_name}")
            if hasattr(response, 'context_data'):
                print(f"   - Contexte: {len(response.context_data)} éléments")
            else:
                print("   ❌ Pas de context_data")
        else:
            print("   ❌ Ce n'est pas un TemplateResponse")
            print(f"   - C'est un: {response.__class__.__name__}")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

    # 2. Vérifier les logs Django en temps réel
... (tronqué)

# ============================================================
# ORIGINE 86: diagnostic_contexte_vue.py (2025-11-17)
# ============================================================

# diagnostic_contexte_vue.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostiquer_contexte_vue():
    """Diagnostiquer pourquoi les conversations ne sont pas dans le contexte"""

    print("🔍 DIAGNOSTIC DU CONTEXTE DE LA VUE")
    print("=" * 60)

    # 1. Vérifier la vue messagerie
    vue_path = 'communication/views.py'
    with open(vue_path, 'r') as f:
        vue_content = f.read()

    print("1. 📝 ANALYSE DE LA VUE MESSAGERIE:")
    print("-" * 40)

    # Extraire la fonction messagerie
    debut_vue = vue_content.find('def messagerie(request):')
    fin_vue = vue_content.find('def ', debut_vue + 1)
    if fin_vue == -1:
        fin_vue = len(vue_content)

    fonction_messagerie = vue_content[debut_vue:fin_vue]

    # Vérifier les éléments critiques
    elements_vue = {
        'conversations = ': 'conversations = ' in fonction_messagerie,
        'context = {': 'context = {' in fonction_messagerie,
        "'conversations'": "'conversations'" in fonction_messagerie,
        'return render': 'return render' in fonction_messagerie
    }

    for element, present in elements_vue.items():
        status = "✅" if present else "❌"
        print(f"   {status} {element}: {'PRÉSENT' if present else 'ABSENT'}")

    # 2. Tester la vue directement
    print(f"\n2. 🧪 TEST DIRECT DE LA VUE:")
    print("-" * 40)

    from communication.views import messagerie
    from django.test import RequestFactory
    from django.contrib.auth.models import User

    try:
... (tronqué)

# ============================================================
# ORIGINE 87: diagnostic_final_conversations.py (2025-11-17)
# ============================================================

# diagnostic_final_conversations.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_complet():
    print("🔍 DIAGNOSTIC FINAL DES CONVERSATIONS")
    print("=" * 60)

    from django.test import Client
    from django.contrib.auth.models import User
    from communication.models import Conversation

    try:
        # Se connecter
        pharmacien = User.objects.get(username='test_pharmacien')
        client = Client()
        client.force_login(pharmacien)

        # Faire une requête
        response = client.get('/communication/')
        content = response.content.decode('utf-8')

        print(f"📊 Statut: {response.status_code}")

        # Analyser le contenu HTML pour comprendre ce qui s'affiche
        print("\n📄 ANALYSE DU CONTENU HTML:")

        # Chercher où apparaissent test_agent et test_medecin
        for nom in ['test_agent', 'test_medecin']:
            index = content.find(nom)
            if index != -1:
                # Extraire le contexte autour du nom
                debut = max(0, index - 200)
                fin = min(len(content), index + 200)
                contexte = content[debut:fin]
                print(f"\n🔍 Contexte autour de '{nom}':")
                print("..." + contexte + "...")

        # Vérifier la présence de balises spécifiques
        balises_importantes = {
            'conversation-item': 'conversation-item' in content,
            'alert alert-success': 'alert alert-success' in content,
            'flex-grow-1': 'flex-grow-1' in content,
            'badge bg-secondary': 'badge bg-secondary' in content,
            'btn btn-primary': 'btn btn-primary' in content
        }

... (tronqué)

# ============================================================
# ORIGINE 88: diagnostic_contexte.py (2025-11-17)
# ============================================================

# diagnostic_contexte.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostiquer_contexte():
    print("🔍 DIAGNOSTIC DU CONTEXTE DE LA VUE MESSAGERIE")
    print("=" * 60)

    from communication.views import messagerie
    from django.test import RequestFactory
    from django.contrib.auth.models import User
    from django.template import Template, Context
    from django.template.loader import get_template

    try:
        # Récupérer l'utilisateur
        pharmacien = User.objects.get(username='test_pharmacien')

        # Créer une vraie requête (pas factory)
        from django.test import Client
        client = Client()
        client.force_login(pharmacien)

        # Faire une vraie requête HTTP
        response = client.get('/communication/')

        print(f"📊 Statut HTTP: {response.status_code}")
        print(f"📝 Content-Type: {response.get('Content-Type', 'Non défini')}")

        # Vérifier si c'est un TemplateResponse
        if hasattr(response, 'template_name'):
            print(f"✅ Template utilisé: {response.template_name}")

        # Vérifier le contexte
        if hasattr(response, 'context_data'):
            print(f"✅ Contexte disponible: {len(response.context_data)} éléments")
            for key, value in response.context_data.items():
                print(f"   - {key}: {type(value)}")
        else:
            print("❌ Aucun contexte_data (normal pour HttpResponse)")

        # Vérifier le contenu
        content = response.content.decode('utf-8')

        # Vérifier si les données sont dans le HTML
        checks = {
            'conversations dans HTML': 'conversation' in content.lower(),
... (tronqué)

# ============================================================
# ORIGINE 89: diagnostic_vue_messagerie_detail.py (2025-11-17)
# ============================================================

# diagnostic_vue_messagerie_detail.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyser_vue_messagerie():
    """Analyser en détail la vue messagerie"""

    print("🔍 ANALYSE DÉTAILLÉE DE LA VUE MESSAGERIE")
    print("=" * 60)

    # Lire le fichier views.py
    with open('communication/views.py', 'r') as f:
        contenu = f.read()

    # Extraire la fonction messagerie
    debut = contenu.find('def messagerie(request):')
    if debut == -1:
        print("❌ Fonction messagerie non trouvée dans views.py")
        return

    fin = contenu.find('def ', debut + 1)
    if fin == -1:
        fin = len(contenu)

    fonction_messagerie = contenu[debut:fin]
    print("📝 CODE DE LA VUE MESSAGERIE:")
    print("-" * 40)
    print(fonction_messagerie)
    print("-" * 40)

    # Vérifications
    verifications = {
        "return render avec context": "return render(request, 'communication/messagerie.html', context)" in fonction_messagerie,
        "context défini": "context = {" in fonction_messagerie,
        "conversations dans context": "'conversations'" in fonction_messagerie,
        "form dans context": "'form'" in fonction_messagerie,
        "gestion des erreurs": "except Exception as e:" in fonction_messagerie
    }

    print("\n✅ VÉRIFICATIONS:")
    for check, result in verifications.items():
        status = "✅" if result else "❌"
        print(f"   {status} {check}")

    return fonction_messagerie

def tester_vue_messagerie_direct():
... (tronqué)

# ============================================================
# ORIGINE 90: diagnostic_messagerie_communication1.py (2025-11-17)
# ============================================================

# diagnostic_messagerie_communication.py
import os
import django
import sys

# Ajouter le chemin du projet
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

# Configuration Django AVANT tout import
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré avec succès")
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def diagnostiquer_vue_messagerie():
    print("🔍 DIAGNOSTIC VUE MESSAGERIE (/communication/)")
    print("=" * 60)

    from communication.views import messagerie
    from django.contrib.auth.models import User
    from django.test import RequestFactory

    try:
        # Récupérer un utilisateur pharmacien pour tester
        pharmacien = User.objects.filter(username='test_pharmacien').first()
        if not pharmacien:
            print("❌ Utilisateur test_pharmacien non trouvé, création d'un utilisateur de test...")
            # Créer un utilisateur de test si nécessaire
            pharmacien = User.objects.create_user(
                username='test_pharmacien',
                password='test123',
                email='pharmacien@test.com'
            )

        # Créer une requête simulée
        factory = RequestFactory()
        request = factory.get('/communication/')
        request.user = pharmacien

        # Appeler la vue
        response = messagerie(request)

        print(f"✅ Vue messagerie exécutée avec succès")
        print(f"📊 Statut HTTP: {response.status_code}")

... (tronqué)

# ============================================================
# ORIGINE 91: diagnostic_messagerie_communication.py (2025-11-17)
# ============================================================

# diagnostic_messagerie_communication.py
import os
import django
from django.test import RequestFactory
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostiquer_vue_messagerie():
    print("🔍 DIAGNOSTIC VUE MESSAGERIE (/communication/)")
    print("=" * 60)

    from communication.views import messagerie
    from django.contrib.auth.models import User

    # Créer une requête simulée
    factory = RequestFactory()

    try:
        # Récupérer un utilisateur pharmacien pour tester
        pharmacien = User.objects.get(username='test_pharmacien')

        # Créer une requête simulée
        request = factory.get('/communication/')
        request.user = pharmacien

        # Appeler la vue
        response = messagerie(request)

        print(f"✅ Vue messagerie exécutée avec succès")
        print(f"📊 Statut HTTP: {response.status_code}")
        print(f"📝 Template utilisé: {response.template_name}")

        # Vérifier le contexte
        if hasattr(response, 'context_data'):
            context = response.context_data
            print(f"📦 Données du contexte:")
            print(f"   - Conversations: {len(context.get('conversations', []))}")
            print(f"   - Formulaire présent: {'form' in context}")
            print(f"   - Erreur: {context.get('error', 'Aucune')}")
        else:
            print("❌ Aucun contexte de données")

    except User.DoesNotExist:
        print("❌ Utilisateur test_pharmacien non trouvé")
    except Exception as e:
        print(f"❌ Erreur lors du diagnostic: {e}")

def verifier_messages_utilisateur():
... (tronqué)

# ============================================================
# ORIGINE 92: diagnostic_rendez_vous.html (2025-11-17)
# ============================================================

<!-- templates/medecin/diagnostic_rendez_vous.html -->
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diagnostic - Bouton Sélection Patient</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .diagnostic-section {
            border: 2px solid #dee2e6;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .success { border-color: #28a745; background: #f8fff9; }
        .warning { border-color: #ffc107; background: #fffef0; }
        .danger { border-color: #dc3545; background: #fff5f5; }
        .test-btn { margin: 5px; }
        .log-container {
            background: #1e1e1e;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            padding: 15px;
            border-radius: 5px;
            max-height: 300px;
            overflow-y: auto;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container-fluid py-4">
        <div class="row">
            <div class="col-12">
                <h1 class="text-center mb-4">🔍 Diagnostic - Bouton Sélection Patient</h1>

                <!-- Section 1: Test Bootstrap -->
                <div class="diagnostic-section" id="bootstrap-test">
                    <h3>1. Test Bootstrap</h3>
                    <div class="row">
                        <div class="col-md-6">
                            <h5>Tests Automatiques</h5>
                            <div id="bootstrap-results"></div>
                        </div>
                        <div class="col-md-6">
                            <h5>Tests Manuel</h5>
                            <button class="btn btn-primary test-btn" onclick="testBootstrapModal()">
                                Test Modal Bootstrap
... (tronqué)

# ============================================================
# ORIGINE 93: diagnostic_messagerie.py (2025-11-17)
# ============================================================

# diagnostic_messagerie.py
import os
import sys
import django
from django.urls import reverse, resolve, NoReverseMatch
from django.core.management import execute_from_command_line

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostiquer_erreur_liste_messages():
    """
    Script complet de diagnostic pour l'erreur 'liste_messages' not found
    """
    print("=" * 80)
    print("DIAGNOSTIC ERREUR 'liste_messages' NOT FOUND")
    print("=" * 80)

    # 1. Vérifier les URLs de l'application communication
    print("\n1. VÉRIFICATION DES URLs COMMUNICATION")
    print("-" * 40)

    try:
        from django.conf import settings
        from importlib import import_module

        # Vérifier si l'application communication est installée
        if 'communication' in settings.INSTALLED_APPS:
            print("✓ Application 'communication' trouvée dans INSTALLED_APPS")

            # Essayer d'importer les URLs de communication
            try:
                communication_urls = import_module('communication.urls')
                print("✓ Module communication.urls importé avec succès")

                # Vérifier les patterns d'URL
                if hasattr(communication_urls, 'urlpatterns'):
                    url_count = len(communication_urls.urlpatterns)
                    print(f"✓ {url_count} pattern(s) URL trouvé(s) dans communication.urls")

                    # Lister tous les noms d'URL
                    url_names = []
                    for pattern in communication_urls.urlpatterns:
                        if hasattr(pattern, 'name') and pattern.name:
                            url_names.append(pattern.name)
                        elif hasattr(pattern, 'url_patterns'):
                            for subpattern in pattern.url_patterns:
                                if hasattr(subpattern, 'name') and subpattern.name:
                                    url_names.append(subpattern.name)
... (tronqué)

# ============================================================
# ORIGINE 94: diagnostic_vue_message.py (2025-11-16)
# ============================================================

# diagnostic_vue_message.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_vue_message():
    print("=== DIAGNOSTIC VUE MESSAGE ===")

    try:
        # Vérifier la vue qui envoie les messages
        from assureur import views as assureur_views
        print("✅ Module assureur.views importé")

        # Vérifier si la vue envoyer_message existe
        if hasattr(assureur_views, 'envoyer_message'):
            print("✅ Vue envoyer_message trouvée dans assureur.views")
        else:
            print("❌ Vue envoyer_message NON trouvée dans assureur.views")

    except ImportError as e:
        print(f"❌ Erreur import assureur.views: {e}")

    # Vérifier les URLs
    try:
        from django.urls import get_resolver
        resolver = get_resolver()

        print("\n📋 URLs de message trouvées:")
        url_patterns = []

        def list_urls(patterns, base=''):
            for pattern in patterns:
                if hasattr(pattern, 'pattern'):
                    if hasattr(pattern, 'url_patterns'):
                        list_urls(pattern.url_patterns, base + str(pattern.pattern))
                    else:
                        url_name = getattr(pattern, 'name', 'Sans nom')
                        if 'message' in str(pattern.pattern).lower() or 'message' in str(url_name).lower():
                            url_patterns.append({
                                'pattern': base + str(pattern.pattern),
                                'name': url_name
                            })

        list_urls(resolver.url_patterns)

        for url in url_patterns:
            print(f"   - {url['pattern']} (name: {url['name']})")
... (tronqué)

# ============================================================
# ORIGINE 95: diagnostic_message.py (2025-11-16)
# ============================================================

# diagnostic_message.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_message():
    print("=== DIAGNOSTIC MODÈLE MESSAGE ===")

    try:
        from communication.models import Message

        # Vérifier si le modèle existe
        messages = Message.objects.all()
        print(f"Nombre de messages: {messages.count()}")

        if messages.exists():
            first_msg = messages.first()
            print(f"\nStructure du premier message (ID: {first_msg.id}):")

            # Lister tous les champs disponibles
            fields = [f.name for f in first_msg._meta.fields]
            print(f"Champs disponibles: {fields}")

            # Afficher les valeurs de chaque champ
            for field in first_msg._meta.fields:
                try:
                    value = getattr(first_msg, field.name)
                    print(f"  - {field.name}: {value}")
                except Exception as e:
                    print(f"  - {field.name}: ERREUR - {e}")

        else:
            print("Aucun message dans la base de données")

    except Exception as e:
        print(f"❌ Erreur avec le modèle Message: {e}")

        # Essayer d'importer quand même pour voir la structure
        try:
            from communication.models import Message
            print("✓ Modèle Message importé avec succès")
            print(f"Champs définis: {[f.name for f in Message._meta.fields]}")
        except Exception as import_error:
            print(f"❌ Impossible d'importer le modèle Message: {import_error}")

if __name__ == "__main__":
    diagnostic_message()

# ============================================================
# ORIGINE 96: diagnostic_communication.py (2025-11-16)
# ============================================================

# diagnostic_communication.py
import os
import django
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from communication.models import Message, Notification
from django.utils import timezone

def diagnostic_communication():
    User = get_user_model()

    print("=== DIAGNOSTIC SYSTÈME DE COMMUNICATION ===")

    # 1. Vérification des sessions
    print("\n1. SESSIONS ACTIVES:")
    sessions = Session.objects.filter(expire_date__gt=timezone.now())
    print(f"   {sessions.count()} session(s) active(s)")

    for session in sessions:
        session_data = session.get_decoded()
        print(f"   - Session {session.session_key}: {session_data}")

    # 2. Vérification des utilisateurs
    print("\n2. UTILISATEURS:")
    assureurs = User.objects.filter(groups__name='ASSUREUR')
    print(f"   {assureurs.count()} assureur(s) trouvé(s)")

    # 3. Vérification des messages
    print("\n3. MESSAGES:")
    messages = Message.objects.all()
    print(f"   {messages.count()} message(s) dans la base")

    for msg in messages[:5]:  # 5 premiers messages
        print(f"   - Message {msg.id}: {msg.type_message} - {msg.sujet}")

    # 4. Vérification des notifications
    print("\n4. NOTIFICATIONS:")
    notifications = Notification.objects.all()
    print(f"   {notifications.count()} notification(s)")

    # 5. Vérification configuration
    print("\n5. CONFIGURATION:")
    print(f"   TIME_ZONE: {settings.TIME_ZONE}")
    print(f"   USE_TZ: {settings.USE_TZ}")
... (tronqué)

# ============================================================
# ORIGINE 97: diagnostic_complet.py (2025-11-16)
# ============================================================

# assureur/diagnostic_complet.py
import os
import django
import sys

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.template.loader import get_template
from django.urls import resolve, Resolver404
from django.conf import settings

def diagnostic_complet():
    print("=" * 60)
    print("🔍 DIAGNOSTIC COMPLET DU DASHBOARD ASSUREUR")
    print("=" * 60)

    # 1. Vérifier le template
    print("\n1. 📄 TEMPLATE DASHBOARD:")
    try:
        template = get_template('assureur/dashboard.html')
        print(f"   ✅ Template trouvé: {template.origin.name}")
        print(f"   📍 Chemin physique: {template.origin.loadname}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

    # 2. Vérifier les URLs
    print("\n2. 🌐 URLs ASSUREUR:")
    urls_assureur = [
        '/assureur/dashboard/',
        '/assureur-dashboard/',
        '/assureur/',
    ]

    for url in urls_assureur:
        try:
            match = resolve(url)
            print(f"   {url} → {match.view_name} ({match.func.__module__}.{match.func.__name__})")
        except Resolver404:
            print(f"   {url} → ❌ NON TROUVÉ")

    # 3. Vérifier la structure des templates
    print("\n3. 📁 STRUCTURE DES TEMPLATES:")
    template_dirs = settings.TEMPLATES[0]['DIRS']
    for dir in template_dirs:
        if os.path.exists(dir):
            print(f"   📂 {dir}")
            assureur_path = os.path.join(dir, 'assureur')
            if os.path.exists(assureur_path):
... (tronqué)

# ============================================================
# ORIGINE 98: diagnostic.py (2025-11-16)
# ============================================================

# assureur/diagnostic.py
import os
import django
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.template.loader import get_template

def find_dashboard_template():
    """Trouve quel template est utilisé pour le dashboard assureur"""
    try:
        # Essayer de trouver le template
        template = get_template('assureur/dashboard.html')
        print(f"✅ Template trouvé: {template.origin.name}")
        print(f"📁 Chemin complet: {template.origin.loadname}")
        return True
    except Exception as e:
        print(f"❌ Template non trouvé: {e}")
        return False

def list_assureur_templates():
    """Lister tous les templates de l'app assureur"""
    template_dirs = settings.TEMPLATES[0]['DIRS']
    print("📂 Dossiers de templates configurés:")
    for dir in template_dirs:
        print(f"  - {dir}")

    # Chercher dans les apps installed
    from django.apps import apps
    assureur_config = apps.get_app_config('assureur')
    if assureur_config:
        print(f"📦 App assureur trouvée: {assureur_config.path}")
        templates_path = os.path.join(assureur_config.path, 'templates')
        if os.path.exists(templates_path):
            print(f"📁 Templates de l'app: {templates_path}")

if __name__ == "__main__":
    print("🔍 Diagnostic du dashboard assureur...")
    list_assureur_templates()
    find_dashboard_template()

