"""
FICHIER CONSOLIDÉ: verification
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
# ORIGINE 1: verification_post_corrections.py (2025-12-06)
# ============================================================

#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.test import Client

print("🔍 VÉRIFICATION APRÈS CORRECTIONS")
print("=" * 40)

client = Client()

# Vérifier les assureurs
assureurs = User.objects.filter(groups__name='Assureur')
print("\n👥 ASSUREURS CORRIGÉS:")
for assureur in assureurs:
    print(f"\n• {assureur.username}:")
    print(f"  is_staff: {assureur.is_staff}")
    print(f"  is_superuser: {assureur.is_superuser}")
    print(f"  Groupes: {[g.name for g in assureur.groups.all()]}")

    # Tester la connexion
    if client.login(username=assureur.username, password=assureur.username):
        print(f"  ✅ Connexion réussie")

        # Tester la redirection
        response = client.get('/redirect-after-login/', follow=True)
        if response.redirect_chain:
            print(f"  🔗 Redirections:")
            for i, (url, status) in enumerate(response.redirect_chain):
                print(f"    {i+1}. {status} -> {url}")

        client.logout()
    else:
        print(f"  ❌ Échec connexion")

# Vérifier ORNELLA
print("\n👤 ORNELLA (Agent):")
ornella = User.objects.get(username='ORNELLA')
try:
    from agents.models import Agent
    agent = Agent.objects.filter(user=ornella).first()
    if agent:
        print(f"  ✅ Profil Agent trouvé: {agent}")
    else:
        print(f"  ❌ Profil Agent non trouvé")
... (tronqué)

# ============================================================
# ORIGINE 2: verification_complete_corrigee1.py (2025-12-04)
# ============================================================

# verification_complete_corrigee.py
import os
import sys
import django
import traceback
from pathlib import Path

# Ajouter le chemin du projet
project_path = str(Path(__file__).resolve().parent)
sys.path.append(project_path)

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Impossible de configurer Django: {e}")
    sys.exit(1)

print("="*80)
print("🔍 VÉRIFICATION COMPLÈTE DU SYSTÈME ASSUREUR")
print("="*80)

# ============================================================================
# 1. VÉRIFICATION DES IMPORTS
# ============================================================================
print("\n📦 1. VÉRIFICATION DES IMPORTS")
print("-"*50)

try:
    # Lire le fichier views.py pour vérifier les imports
    with open('assureur/views.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Vérifier l'import de Membre
    import_lines = [line.strip() for line in content.split('\n') if 'import Membre' in line]

    print(f"Imports 'Membre' trouvés: {len(import_lines)}")

    if len(import_lines) == 1 and 'from agents.models import Membre' in import_lines[0]:
        print("✅ Import CORRECT: from agents.models import Membre")
    elif len(import_lines) > 1:
        print("⚠️  MULTIPLES IMPORTS détectés:")
        for line in import_lines:
            print(f"   → {line}")
    else:
        print("❌ MAUVAIS IMPORT: Ce n'est pas 'from agents.models import Membre'")

except Exception as e:
... (tronqué)

# ============================================================
# ORIGINE 3: verification_complete_corrigee.py (2025-12-04)
# ============================================================

# verification_complete_corrigee.py
import os
import sys
import django
import traceback
from pathlib import Path

# Ajouter le chemin du projet
project_path = str(Path(__file__).resolve().parent)
sys.path.append(project_path)

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votre_projet.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Impossible de configurer Django: {e}")
    sys.exit(1)

print("="*80)
print("🔍 VÉRIFICATION COMPLÈTE DU SYSTÈME ASSUREUR")
print("="*80)

# ============================================================================
# 1. VÉRIFICATION DES IMPORTS
# ============================================================================
print("\n📦 1. VÉRIFICATION DES IMPORTS")
print("-"*50)

try:
    # Lire le fichier views.py pour vérifier les imports
    with open('assureur/views.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Vérifier l'import de Membre
    import_lines = [line.strip() for line in content.split('\n') if 'import Membre' in line]

    print(f"Imports 'Membre' trouvés: {len(import_lines)}")

    if len(import_lines) == 1 and 'from agents.models import Membre' in import_lines[0]:
        print("✅ Import CORRECT: from agents.models import Membre")
    elif len(import_lines) > 1:
        print("⚠️  MULTIPLES IMPORTS détectés:")
        for line in import_lines:
            print(f"   → {line}")
    else:
        print("❌ MAUVAIS IMPORT: Ce n'est pas 'from agents.models import Membre'")

except Exception as e:
... (tronqué)

# ============================================================
# ORIGINE 4: verification_corrections1.py (2025-12-03)
# ============================================================

#!/usr/bin/env python
"""
VÉRIFICATION RAPIDE DES CORRECTIONS
"""

import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur Django: {e}")
    sys.exit(1)

from django.urls import reverse, NoReverseMatch

print("🔍 VÉRIFICATION DES URLS CORRIGÉES")
print("=" * 60)

urls_a_verifier = [
    'assureur:liste_messages',
    'assureur:envoyer_message',
    'assureur:export_bons_pdf',
    'assureur:creer_cotisation',
    'assureur:preview_generation',
]

for url_name in urls_a_verifier:
    try:
        url = reverse(url_name)
        print(f"✅ {url_name:30} -> {url}")
    except NoReverseMatch as e:
        print(f"❌ {url_name:30} -> ERREUR: {str(e)[:50]}...")

print("\n📋 VÉRIFICATION DES FICHIERS CRÉÉS")
print("=" * 60)

fichiers_a_verifier = [
    'assureur/views.py',
    'assureur/urls.py',
    'templates/assureur/communication/liste_messages.html',
    'templates/assureur/communication/envoyer_message.html',
    'templates/assureur/cotisations/creer_cotisation.html',
]

... (tronqué)

# ============================================================
# ORIGINE 5: verification_corrigee1.py (2025-11-30)
# ============================================================

# verification_corrigee.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps

print("🔍 VÉRIFICATION CORRIGÉE DES APPLICATIONS")
print("=" * 50)

def verifier_apps_corrige():
    """Vérification corrigée des applications"""
    apps_a_verifier = ['ia_detection', 'scoring', 'relances', 'dashboard']

    for app in apps_a_verifier:
        try:
            app_config = apps.get_app_config(app)
            modeles = list(app_config.get_models())  # Convertir en liste
            print(f"✅ {app}: CHARGÉE - {len(modeles)} modèles")
            for modele in modeles:
                print(f"     📄 {modele.__name__}")
        except Exception as e:
            print(f"❌ {app}: NON CHARGÉE - {e}")

def test_fonctionnalites_sans_erreur():
    """Test des fonctionnalités sans erreur de champ manquant"""
    print("\\n🎯 TEST DES FONCTIONNALITÉS SANS ERREUR:")

    try:
        from membres.models import Membre
        from scoring.models import HistoriqueScore
        from scoring.calculators import CalculateurScoreMembre

        # Utiliser une approche qui ne dépend pas des champs manquants
        membre = Membre.objects.raw('SELECT * FROM membres_membre LIMIT 1')[0]
        print(f"✅ Membre trouvé: {membre.nom}")

        # Calculer un score
        calculateur = CalculateurScoreMembre()
        resultat = calculateur.calculer_score_complet(membre)
        print(f"✅ Score calculé: {resultat['score_final']}")
        print(f"✅ Niveau risque: {resultat['niveau_risque']}")

        # Vérifier l'historique
        scores_count = HistoriqueScore.objects.count()
        print(f"✅ Historique scores: {scores_count}")

    except Exception as e:
        print(f"⚠️  Note: {e}")
... (tronqué)

# ============================================================
# ORIGINE 6: verification_correction_finale.py (2025-11-28)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

def verification_correction_finale():
    print("🔍 VÉRIFICATION CORRECTION FINALE")
    print("=" * 50)

    # Vérifier le template corrigé
    template_path = 'templates/medecin/suivi_chronique/tableau_bord.html'

    if not os.path.exists(template_path):
        print("❌ Template non trouvé")
        return False

    # Lire le contenu
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print("📄 Vérification extension:")
    if "{% extends 'medecin/base.html' %}" in content:
        print("✅ Utilise medecin/base.html")
    elif "{% extends 'medecin/base_medecin.html' %}" in content:
        print("❌ Utilise encore base_medecin.html")
        return False
    else:
        print("⚠️  Extension non standard")

    # Test Django
    try:
        django.setup()
        from django.template.loader import get_template

        print("\n🐍 TEST DJANGO:")
        try:
            template = get_template('medecin/suivi_chronique/tableau_bord.html')
            print("✅ Template chargé avec succès")

            # Test de rendu
            from django.contrib.auth.models import User
            user = User.objects.get(username='medecin_test')

            context = {
                'request': type('Request', (), {'user': user, 'path': '/medecin/suivi-chronique/'})(),
                'patients_suivis': 5,
                'accompagnements_actifs': 3,
                'alertes_en_cours': 2,
... (tronqué)

# ============================================================
# ORIGINE 7: verification_post_correction1.py (2025-11-27)
# ============================================================

# verification_post_correction.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_workflow_complet():
    """Teste le workflow complet après corrections"""
    print("🔄 TEST DU WORKFLOW COMPLET")

    client = Client()

    # Test avec les nouveaux mots de passe
    test_users = [
        ('test_agent', 'test123', 'Agent'),
        ('assureur_test', 'test123', 'Assureur'),
        ('medecin_test', 'test123', 'Médecin'),
        ('test_pharmacien', 'test123', 'Pharmacien')
    ]

    for username, password, role in test_users:
        print(f"\n👤 Test {role} ({username})")

        # Test connexion
        if client.login(username=username, password=password):
            print(f"   ✅ Connexion réussie")

            # Test accès dashboard
            if role == 'Agent':
                urls = ['/agents/tableau-de-bord/', '/agents/creer-membre/']
            elif role == 'Assureur':
                urls = ['/assureur/dashboard/', '/assureur/cotisations/']
            elif role == 'Médecin':
                urls = ['/medecin/dashboard/', '/medecin/ordonnances/']
            elif role == 'Pharmacien':
                urls = ['/pharmacien/dashboard/', '/pharmacien/ordonnances/']

            for url in urls:
                response = client.get(url)
                if response.status_code == 200:
                    print(f"   ✅ Accès {url}")
                else:
                    print(f"   ❌ Accès refusé {url} (Status: {response.status_code})")
... (tronqué)

# ============================================================
# ORIGINE 8: verification_post_correction.py (2025-11-27)
# ============================================================

# verification_post_correction.py
import os
import sys
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.contrib.auth.models import User
from membres.models import Membre
from django.db.models import Count, Q

print("✅ VÉRIFICATION POST-CORRECTION")
print("=" * 50)

# Statistiques après correction
total_users = User.objects.count()
total_membres = Membre.objects.count()
membres_avec_user = Membre.objects.filter(user__isnull=False).count()
membres_sans_user = Membre.objects.filter(user__isnull=True).count()

print(f"📊 STATISTIQUES:")
print(f"   👥 Utilisateurs: {total_users}")
print(f"   👤 Membres: {total_membres}")
print(f"   🔗 Membres avec user: {membres_avec_user}")
print(f"   ❌ Membres sans user: {membres_sans_user}")

if total_membres > 0:
    ratio = (membres_avec_user / total_membres) * 100
    print(f"   📈 Taux de synchronisation: {ratio:.1f}%")

    if ratio == 100:
        print("🎉 SYNCHRONISATION COMPLÈTE!")
    elif ratio >= 90:
        print("✅ SYNCHRONISATION EXCELLENTE")
    elif ratio >= 75:
        print("⚠️  SYNCHRONISATION BONNE")
    else:
        print("🚨 SYNCHRONISATION INSUFFISANTE")

# Vérifier l'intégrité des numéros uniques
try:
    doublons = Membre.objects.values('numero_unique').annotate(
        count=Count('id')
    ).filter(count__gt=1, numero_unique__isnull=False)

    if doublons.exists():
... (tronqué)

# ============================================================
# ORIGINE 9: verification_permissions_corrige.py (2025-11-20)
# ============================================================

import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Agent
from django.contrib.auth.models import User

def verifier_permissions_utilisateur():
    """Vérifier et corriger les permissions de l'utilisateur - VERSION CORRIGÉE"""
    print("🔐 VÉRIFICATION DES PERMISSIONS - CORRIGÉ")
    print("=========================================")

    username = "koffitanoh"

    try:
        user = User.objects.get(username=username)
        print(f"👤 Utilisateur trouvé: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Superutilisateur: {user.is_superuser}")
        print(f"   Staff: {user.is_staff}")
        print(f"   Actif: {user.is_active}")

        # Vérifier les groupes
        groups = user.groups.all()
        print(f"   Groupes: {[g.name for g in groups]}")

        # Vérifier les permissions
        permissions = user.get_all_permissions()
        print(f"   Permissions: {len(permissions)}")

        # Vérifier si c'est un agent - VERSION CORRIGÉE
        try:
            agent = Agent.objects.get(user=user)
            print(f"✅ AGENT TROUVÉ: {agent}")
            print(f"   Matricule: {agent.matricule}")  # CORRIGÉ: matricule au lieu de code_agent
            print(f"   Poste: {agent.poste}")
            print(f"   Est actif: {agent.est_actif}")
            print(f"   Limite quotidienne: {agent.limite_bons_quotidienne}")

        except Agent.DoesNotExist:
            print("❌ L'utilisateur n'est pas associé à un agent")

    except User.DoesNotExist:
        print(f"❌ Utilisateur '{username}' non trouvé")

... (tronqué)

# ============================================================
# ORIGINE 10: verification_apres_correction.py (2025-11-17)
# ============================================================

# verification_apres_correction.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_apres_correction():
    """Vérification après application de la correction finale"""

    print("🎯 VÉRIFICATION APRÈS CORRECTION FINALE")
    print("=" * 50)

    from django.test import Client
    from django.contrib.auth.models import User

    try:
        # Tester avec assureur_test
        user = User.objects.get(username='assureur_test')
        client = Client()
        client.force_login(user)

        # Faire une requête
        response = client.get('/communication/')
        content = response.content.decode('utf-8')

        print(f"📊 Statut: {response.status_code}")

        # Vérifications COMPLÈTES du nouveau template
        verifications = {
            'Structure conversation-item': 'conversation-item' in content,
            'Badges colorés': 'badge bg-' in content,
            'Modal nouveau message': 'nouveauMessageModal' in content,
            'Date activité affichée': 'Dernière activité' in content,
            'Statistiques détaillées': 'Statistiques:' in content,
            'Bouton nouveau message': 'Nouveau Message' in content,
            'Participants avec badges': 'Participants:' in content and 'badge' in content,
            'Conversation avec': 'Conversation avec:' in content,
            'Messages comptés': 'message(s)' in content,
            'Interface complète': 'container-fluid' in content
        }

        print(f"\n✅ VÉRIFICATION DU TEMPLATE COMPLET:")
        score = 0
        for element, present in verifications.items():
            status = "✅" if present else "❌"
            if present: score += 1
            print(f"   {status} {element}: {'PRÉSENT' if present else 'ABSENT'}")

        pourcentage = (score / len(verifications)) * 100
... (tronqué)

# ============================================================
# ORIGINE 11: verification_structure_corrigee.py (2025-11-17)
# ============================================================

# verification_structure_corrigee.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_structure_corrigee():
    """Vérifier que la structure corrigée fonctionne"""

    print("🔍 VÉRIFICATION DE LA STRUCTURE CORRIGÉE")
    print("=" * 50)

    from django.test import Client
    from django.contrib.auth.models import User

    try:
        # Se connecter
        pharmacien = User.objects.get(username='test_pharmacien')
        client = Client()
        client.force_login(pharmacien)

        # Faire une requête
        response = client.get('/communication/')
        content = response.content.decode('utf-8')

        print(f"📊 Statut: {response.status_code}")

        # Vérifications CRITIQUES
        checks = {
            'Template Corrigé - Mode Debug': 'Template Corrigé' in content,
            'Conversations dans base': 'conversation(s) trouvée(s)' in content,
            'test_agent visible': 'test_agent' in content,
            'test_medecin visible': 'test_medecin' in content,
            'Conversation #7': 'Conversation #7' in content,
            'Conversation #6': 'Conversation #6' in content,
            'Statistiques affichées': 'Statistiques:' in content,
            'Bouton Nouveau Message': 'Nouveau Message' in content
        }

        print("\n✅ VÉRIFICATIONS CRITIQUES:")
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"   {status} {check}: {'TROUVÉ' if result else 'NON TROUVÉ'}")

        # Compter les occurrences
        count_agent = content.count('test_agent')
        count_medecin = content.count('test_medecin')
        count_conversations = content.count('Conversation #')

... (tronqué)

# ============================================================
# ORIGINE 12: verification_formulaire_corrige.py (2025-11-16)
# ============================================================

# verification_formulaire_corrige.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_formulaire_corrige():
    print("=== VÉRIFICATION FORMULAIRE CORRIGÉ ===")

    try:
        from communication.forms import MessageForm
        form = MessageForm()

        # Vérifier si la méthode save est celle de la classe parente ou notre surcharge
        import inspect
        save_method = inspect.getsource(form.save)
        if 'get_or_create_conversation' in save_method:
            print("✅ Formulaire utilise la méthode save() corrigée avec gestion de conversation")
        else:
            print("❌ Formulaire n'utilise PAS la méthode save() corrigée")

    except Exception as e:
        print(f"❌ Erreur: {e}")

def corriger_formulaire_manuellement():
    """Correction manuelle du formulaire si nécessaire"""
    print("\n=== CORRECTION MANUELLE FORMULAIRE ===")

    forms_path = 'communication/forms.py'

    # Lire le fichier
    with open(forms_path, 'r') as f:
        content = f.read()

    # Vérifier si la méthode save corrigée existe
    if 'def save(self, commit=True):' in content and 'get_or_create_conversation' in content:
        print("✅ Méthode save() corrigée déjà présente")
        return

    # Ajouter la méthode save manuellement
    save_method = '''
    def save(self, commit=True):
        """Surcharge de la méthode save pour gérer automatiquement la conversation et l'expéditeur"""
        from .utils import get_or_create_conversation

        message = super().save(commit=False)

        # Assigner l'expéditeur
... (tronqué)

# ============================================================
# ORIGINE 13: verification_corrections.py (2025-11-14)
# ============================================================

#!/usr/bin/env python3
"""
Script de vérification après correction des templates assureur
"""

import os
import re
from pathlib import Path

def verify_corrections():
    """Vérifie que toutes les corrections ont été appliquées"""
    print("🔍 VÉRIFICATION POST-CORRECTION")
    print("=" * 50)

    project_root = Path(__file__).parent
    issues_found = 0

    # URLs qui ne devraient plus exister
    forbidden_urls = ['assureur:rapports']

    # Templates problématiques identifiés
    problematic_templates = [
        project_root / "templates/assureur/dashboard.html",
        project_root / "templates/assureur/partials/_sidebar.html"
    ]

    for template_path in problematic_templates:
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()

            for url in forbidden_urls:
                if url in content:
                    print(f"❌ URL problématique trouvée: {url} dans {template_path}")
                    issues_found += 1
                else:
                    print(f"✅ URL corrigée: {url} dans {template_path}")

    # Vérifier les doublons
    duplicates = {
        'base_assureur.html': [
            project_root / "assureur/templates/assureur/base_assureur.html",
            project_root / "templates/assureur/base_assureur.html"
        ],
        'dashboard.html': [
            project_root / "assureur/templates/assureur/dashboard.html",
            project_root / "templates/assureur/dashboard.html"
        ]
    }

... (tronqué)

