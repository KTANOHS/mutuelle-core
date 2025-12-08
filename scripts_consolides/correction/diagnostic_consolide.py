"""
FICHIER CONSOLIDÉ: diagnostic
Catégorie: correction
Fusion de 13 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: diagnostic_assureur_corrige2.py (2025-12-06)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET - SYSTÈME ASSUREUR
Vérifie tous les aspects du système Assureur et corrige les problèmes.
Version corrigée pour les imports.
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
        print(f"  - {groupe.name}: {users_count} utilisateur(s)")
... (tronqué)

# ============================================================
# ORIGINE 2: diagnostic_assureur_corrige1.py (2025-12-03)
# ============================================================

#!/usr/bin/env python3
"""
Script de diagnostic corrigé pour l'application assureur
Utilise mutuelle_core.settings au lieu de core.settings
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
    print("✅ Django chargé avec mutuelle_core.settings")
except Exception as e:
    print(f"⚠️  Django non chargé: {e}")
    print("🔄 Tentative avec core.settings...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        django.setup()
        DJANGO_LOADED = True
        print("✅ Django chargé avec core.settings")
    except Exception as e2:
        print(f"❌ Django non chargé: {e2}")
        DJANGO_LOADED = False

BASE_DIR = Path(__file__).resolve().parent.parent

def verifier_installation_assureur():
    """Vérifie si l'app assureur est bien installée"""
    print("\n" + "="*80)
    print("VÉRIFICATION INSTALLATION ASSUREUR")
    print("="*80)

    if not DJANGO_LOADED:
        print("❌ Django non chargé - vérification impossible")
        return

    try:
        from django.apps import apps

        # Vérifier si l'app assureur est dans INSTALLED_APPS
        assureur_installe = apps.is_installed('assureur')

        if assureur_installe:
... (tronqué)

# ============================================================
# ORIGINE 3: diagnostic_assureur_corrige.py (2025-12-03)
# ============================================================

#!/usr/bin/env python3
"""
SCRIPT DE DIAGNOSTIC COMPLET POUR L'APPLICATION ASSUREUR - VERSION CORRIGÉE

Ce script vérifie tous les composants de l'application assureur avec les chemins corrects.
"""
import os
import sys
import django
from pathlib import Path

# Configuration de Django
BASE_DIR = Path(__file__).resolve().parent  # Le répertoire où se trouve ce script
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django initialisé avec succès")
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation de Django: {e}")
    sys.exit(1)

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def print_header(title):
    """Affiche un en-tête de section"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def print_success(message):
    """Affiche un message de succès"""
    print(f"✅ {message}")

def print_warning(message):
    """Affiche un message d'avertissement"""
    print(f"⚠️  {message}")

def print_error(message):
    """Affiche un message d'erreur"""
    print(f"❌ {message}")

def print_info(message):
    """Affiche un message informatif"""
    print(f"📋 {message}")

# ============================================================================
... (tronqué)

# ============================================================
# ORIGINE 4: diagnostic_communication_corrige2.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
# diagnostic_communication_corrige.py - Diagnostic complet sans erreur
import os
import sys
import django
from pathlib import Path

# Ajouter le chemin du projet
project_path = Path(__file__).parent
sys.path.append(str(project_path))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation de Django: {e}")
    sys.exit(1)

def diagnostic_communication():
    print("🔍 DIAGNOSTIC COMPLET - MODULE COMMUNICATION")
    print("=" * 60)

    try:
        from communication.models import Conversation, Message
        from django.contrib.auth.models import User
        from django.contrib.sessions.models import Session
        from django.utils import timezone

        # =============================================================
        # 1. SESSIONS ACTIVES
        # =============================================================
        print("\n1. SESSIONS ACTIVES:")
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        print(f"   {active_sessions.count()} session(s) active(s)")

        # =============================================================
        # 2. UTILISATEURS
        # =============================================================
        print("\n2. UTILISATEURS:")
        total_users = User.objects.count()
        print(f"   {total_users} utilisateur(s) au total")

        # Afficher les 10 premiers utilisateurs
        for user in User.objects.all()[:10]:
            print(f"   - {user.username} ({user.get_full_name()}) - {user.email}")

        # =============================================================
        # 3. MESSAGES
... (tronqué)

# ============================================================
# ORIGINE 5: diagnostic_rapide_corrige.sh (2025-12-01)
# ============================================================

#!/bin/bash
# DIAGNOSTIC RAPIDE PHARMACIEN - VERSION CORRIGÉE

echo "=== DIAGNOSTIC RAPIDE PHARMACIEN ==="
echo "Exécuté le: $(date)"
echo ""

# Fonction de vérification corrigée
check() {
    echo -n "Vérification de $1... "
    if eval "$2" 2>/dev/null; then
        echo "✓ OK"
        return 0
    else
        echo "✗ ÉCHEC"
        return 1
    fi
}

# 1. Environnement
check "Environnement virtuel" '[ -n "$VIRTUAL_ENV" ]'

# 2. Django
check "Django installé" 'python -c "import django"'

# 3. Application pharmacien
check "Application pharmacien" 'python -c "import pharmacien"'

# 4. Modèle OrdonnancePharmacien
check "Modèle OrdonnancePharmacien" 'python -c "from pharmacien.models import OrdonnancePharmacien"'

# 5. Vue historique_validation
check "Vue historique_validation" 'python -c "from pharmacien.views import historique_validation"'

# 6. Template historique
check "Template historique" '[ -f "templates/pharmacien/historique_validation.html" ]'

# 7. URLs
check "URLs pharmacien" '[ -f "pharmacien/urls.py" ]'

# 8. Décorateurs
check "Décorateur pharmacien_required" '[ -f "pharmacien/decorators.py" ]'

# Test rapide de la vue
echo ""
echo "=== TEST DE LA VUE historique_validation ==="
python << 'PYTHON_TEST'
import os
import sys
import django
... (tronqué)

# ============================================================
# ORIGINE 6: diagnostic_cotisations_corrige.py (2025-11-30)
# ============================================================

# diagnostic_cotisations_final.py - VERSION CORRIGÉE
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
            self.analyser_structure_actuelle()
            self.diagnostiquer_problemes_specifiques()
            self.proposer_solutions_immediates()
            self.generer_rapport_actions()
            print("✅ DIAGNOSTIC TERMINÉ AVEC SOLUTIONS")
        except Exception as e:
            print(f"❌ Erreur lors du diagnostic: {str(e)}")
            self.rapport['erreur'] = str(e)

    def analyser_structure_actuelle(self):
        """Analyse la structure actuelle du système"""
        print("\n1. 📊 ANALYSE STRUCTURE ACTUELLE...")

... (tronqué)

# ============================================================
# ORIGINE 7: diagnostic_permissions_acces_corrige.py (2025-11-28)
# ============================================================

# diagnostic_permissions_acces_corrige.py

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
    """Vérifie la structure de la base de données - VERSION CORRIGÉE"""
    print("🗃️ STRUCTURE DE LA BASE DE DONNÉES")
    print("=" * 50)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

        tables_importantes = [
            'membres_membre', 'soins_bondesoin', 'medecin_ordonnance',
            'pharmacien_ordonnancepharmacien', 'agents_agent', 'paiements_paiement'
        ]

        for table in tables_importantes:
            if table in tables:
                # CORRECTION: Créer un nouveau curseur pour chaque requête
                with connection.cursor() as cursor_count:
                    cursor_count.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor_count.fetchone()[0]
                print(f"✅ {table}: {count} enregistrements")
            else:
                print(f"❌ {table}: TABLE MANQUANTE")

    except Exception as e:
        print(f"❌ Erreur vérification base de données: {e}")

def verifier_groupes_utilisateurs():
    """Vérifie les groupes et leurs permissions"""
    print("\n👥 GROUPES ET UTILISATEURS")
    print("=" * 50)
... (tronqué)

# ============================================================
# ORIGINE 8: diagnostic_complet_filtres_corrige.py (2025-11-28)
# ============================================================

# diagnostic_complet_filtres_corrige.py
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
        else:
            print("      ❌ Aucun patient dans la base de données")

        print(f"   🩺 Maladies chroniques: {maladies_count}")
        if maladies_count > 0:
            maladies = MaladieChronique.objects.all()[:3]
            for m in maladies:
                print(f"      - {m.nom} (ID: {m.id})")
        else:
            print("      ❌ Aucune maladie chronique dans la base de données")

        # 2. Test de la page
        client = Client()

        print("\n2. 🔑 Connexion...")
        if not client.login(username='medecin_test', password='password123'):
            print("   ❌ Échec connexion")
            return

        print("   ✅ Connecté")

... (tronqué)

# ============================================================
# ORIGINE 9: diagnostic_corrige.py (2025-11-27)
# ============================================================

import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    from django.test import RequestFactory
    from django.contrib.sessions.middleware import SessionMiddleware
    from django.contrib.auth.models import User
    from membres.models import Medecin
    from medecin.views import tableau_de_bord_medecin

    def diagnostic_corrige():
        print("🔍 DIAGNOSTIC TEMPLATE CORRIGÉ:")
        print("=" * 50)

        # Créer une requête simulée
        factory = RequestFactory()
        request = factory.get('/medecin/tableau-de-bord/')

        # Ajouter la session
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()

        # Créer et connecter un médecin de test
        try:
            user = User.objects.get(username='medecin_test')
        except User.DoesNotExist:
            user = User.objects.create_user('medecin_test', 'medecin@test.com', 'password123')
            user.save()

        try:
            medecin = Medecin.objects.get(user=user)
        except Medecin.DoesNotExist:
            medecin = Medecin.objects.create(
                user=user,
                nom="Docteur Test",
                prenom="Jean",
                specialite="Generaliste"
            )

        request.user = user

        # Appeler la vue
... (tronqué)

# ============================================================
# ORIGINE 10: diagnostic_affichage_corrige.py (2025-11-27)
# ============================================================

# diagnostic_affichage_corrige.py
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

from membres.models import Membre, Cotisation
from agents.models import VerificationCotisation
from django.db.models import Q

# Import de notre fonction unifiée
from affichage_unifie import afficher_fiche_cotisation_unifiee

print("🔍 DIAGNOSTIC AFFICHAGE CORRIGÉ")
print("=" * 50)

class DiagnosticAffichageCorrige:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'tests_realises': [],
            'resultats': []
        }

    def tester_affichage_unifie(self):
        """Teste l'affichage unifié avec différents scénarios"""
        print("🎯 TEST AFFICHAGE UNIFIÉ...")

        # Scénario 1: Membre avec téléphone spécifique
        print("\n1. 📞 TEST AVEC TÉLÉPHONE: 0710569896")
        try:
            membre = Membre.objects.get(telephone="0710569896")
            verification = VerificationCotisation.objects.filter(membre=membre).first()
            cotisation = Cotisation.objects.filter(membre=membre).first()

            fiche = afficher_fiche_cotisation_unifiee(membre, verification, cotisation)
            print(fiche)

            self.rapport['tests_realises'].append({
                'scenario': 'telephone_0710569896',
                'membre': membre.numero_unique,
                'statut_reel': verification.statut_cotisation if verification else 'N/A',
                'success': True
... (tronqué)

# ============================================================
# ORIGINE 11: diagnostic_sync_corrige.py (2025-11-27)
# ============================================================

# diagnostic_sync_corrige.py
import os
import sys
import django
import json
from datetime import datetime
from pathlib import Path

# 🔧 CORRECTION : Configuration Django correcte
try:
    # Votre projet utilise probablement 'core' comme module principal
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    print("✅ Configuration Django: core.settings")

    # Ajouter le chemin du projet
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))

    django.setup()
    print("✅ Django configuré avec succès")

except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    print("🔍 Tentative avec mutuelle_core...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        django.setup()
        print("✅ Django configuré avec mutuelle_core.settings")
    except Exception as e2:
        print(f"❌ Échec configuration: {e2}")
        sys.exit(1)

# Maintenant importer les modèles Django
from django.db import connection
from django.db.models import Count, Q
from django.contrib.auth.models import User

# Importer vos modèles avec gestion d'erreur
try:
    from membres.models import Membre, Paiement, Cotisation
    print("✅ Modèles membres importés")
except ImportError as e:
    print(f"⚠️  Impossible d'importer membres: {e}")
    # Créer des placeholders pour le diagnostic
    class Membre:
        objects = None
    class Paiement:
        objects = None
    class Cotisation:
        objects = None
... (tronqué)

# ============================================================
# ORIGINE 12: diagnostic_communication_corrige1.py (2025-11-16)
# ============================================================

# diagnostic_communication_corrige.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from communication.models import Message, Notification
from django.utils import timezone

def diagnostic_communication():
    User = get_user_model()

    print("=== DIAGNOSTIC SYSTÈME DE COMMUNICATION CORRIGÉ ===")

    # 1. Vérification des sessions
    print("\n1. SESSIONS ACTIVES:")
    sessions = Session.objects.filter(expire_date__gt=timezone.now())
    print(f"   {sessions.count()} session(s) active(s)")

    # 2. Vérification des utilisateurs et groupes
    print("\n2. UTILISATEURS ET GROUPES:")
    try:
        assureurs_group = Group.objects.filter(name='ASSUREUR').first()
        if assureurs_group:
            assureurs = assureurs_group.user_set.all()
            print(f"   {assureurs.count()} assureur(s) trouvé(s) dans le groupe ASSUREUR")
            for user in assureurs:
                print(f"   - {user.username} | {user.email}")
        else:
            print("   ❌ Groupe ASSUREUR non trouvé")

        # Vérifier tous les utilisateurs
        all_users = User.objects.all()
        print(f"   Total utilisateurs: {all_users.count()}")
        for user in all_users:
            groups = [g.name for g in user.groups.all()]
            print(f"   - {user.username} | Groupes: {groups}")

    except Exception as e:
        print(f"   ❌ Erreur utilisateurs: {e}")

    # 3. Vérification des messages (CORRIGÉ - utiliser 'titre' au lieu de 'sujet')
    print("\n3. MESSAGES:")
    messages = Message.objects.all()
    print(f"   {messages.count()} message(s) dans la base")
... (tronqué)

# ============================================================
# ORIGINE 13: diagnostic_communication_corrige.py (2025-11-16)
# ============================================================

# diagnostic_communication_corrige.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votre_projet.settings')
django.setup()

from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.utils import timezone

def diagnostic_complet():
    User = get_user_model()

    print("=== DIAGNOSTIC COMPLET SYSTÈME ===")

    # 1. Nettoyage des sessions corrompues
    print("\n1. NETTOYAGE DES SESSIONS:")
    sessions_count_before = Session.objects.count()
    print(f"   Sessions avant nettoyage: {sessions_count_before}")

    # Commande pour nettoyer les sessions
    os.system('python manage.py clearsessions')

    sessions_count_after = Session.objects.count()
    print(f"   Sessions après nettoyage: {sessions_count_after}")

    # 2. Diagnostic utilisateurs et groupes
    print("\n2. DIAGNOSTIC UTILISATEURS:")
    try:
        from django.contrib.auth.models import Group
        assureurs_group = Group.objects.filter(name='ASSUREUR').first()

        if assureurs_group:
            assureurs = assureurs_group.user_set.all()
            print(f"   Groupe ASSUREUR trouvé: {assureurs.count()} utilisateur(s)")

            for user in assureurs:
                print(f"   - {user.username} ({user.email})")
        else:
            print("   ❌ Groupe ASSUREUR non trouvé")

    except Exception as e:
        print(f"   ❌ Erreur groupes: {e}")

    # 3. Vérification de tous les utilisateurs
    all_users = User.objects.all()
    print(f"   Total utilisateurs: {all_users.count()}")

... (tronqué)

