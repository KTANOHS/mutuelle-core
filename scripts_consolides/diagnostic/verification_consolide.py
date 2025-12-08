"""
FICHIER CONSOLIDÉ: verification
Catégorie: diagnostic
Fusion de 37 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: verification_final.py (2025-12-04)
# ============================================================

# verification_finale.py
import os
import sys
import django
import sqlite3

sys.path.append('/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import connection

print("🔍 VÉRIFICATION FINALE DU SYSTÈME DE COTISATION")
print("="*60)

# 1. Vérifier la structure de la table
print("\n1. Structure de la table assureur_cotisation :")
with connection.cursor() as cursor:
    cursor.execute("PRAGMA table_info(assureur_cotisation)")
    columns = cursor.fetchall()

    problem_fields = ['montant_clinique', 'montant_pharmacie', 'montant_charges_mutuelle']
    found_problems = []

    for col in columns:
        col_name = col[1]
        col_type = col[2]

        if col_name in problem_fields:
            found_problems.append(col_name)
            print(f"   ❌ {col_name:30} ({col_type}) - CHAMP PROBLÉMATIQUE TROUVÉ")
        else:
            print(f"   ✅ {col_name:30} ({col_type})")

    if not found_problems:
        print("\n   🎉 AUCUN CHAMP PROBLÉMATIQUE TROUVÉ !")
    else:
        print(f"\n   ⚠️  {len(found_problems)} champ(s) problématique(s) : {', '.join(found_problems)}")

# 2. Vérifier les données existantes
print("\n2. Données existantes :")
with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM assureur_cotisation")
    total = cursor.fetchone()[0]
    print(f"   📊 Total cotisations : {total}")

    cursor.execute("SELECT statut, COUNT(*) FROM assureur_cotisation GROUP BY statut ORDER BY statut")
    statuts = cursor.fetchall()
    for statut, count in statuts:
        print(f"   📊 Statut '{statut}': {count}")
... (tronqué)

# ============================================================
# ORIGINE 2: verification_cotisations.html (2025-12-04)
# ============================================================

<!-- templates/agents/verification_cotisations.html - VERSION COMPLÈTEMENT CORRIGÉE -->
{% extends 'agents/base_agent.html' %}
{% load static %}

{% block title %}Vérification cotisations - Agent{% endblock %}
{% block page_title %}Vérification des cotisations{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row">
        <div class="col-lg-8">
            <!-- Carte principale de vérification -->
            <div class="card shadow-sm mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-check-circle me-2"></i>Vérification en temps réel
                    </h5>
                </div>
                <div class="card-body">
                    <!-- Recherche rapide -->
                    <div class="mb-4">
                        <label class="form-label fw-bold">Rechercher un membre</label>
                        <div class="input-group input-group-lg">
                            <span class="input-group-text bg-light">
                                <i class="fas fa-search text-muted"></i>
                            </span>
                            <input type="text" class="form-control" id="rechercheMembreRapide"
                                   placeholder="Nom, prénom, numéro de membre ou téléphone...">
                            <button class="btn btn-primary" type="button" id="btnRechercheRapide">
                                <i class="fas fa-search me-1"></i>Rechercher
                            </button>
                        </div>
                        <div class="form-text">
                            <i class="fas fa-info-circle me-1"></i>
                            Saisissez au moins 2 caractères pour lancer la recherche
                        </div>
                        <div id="resultatsRechercheRapide" class="mt-3"></div>
                    </div>

                    <!-- Résultats de vérification -->
                    <div id="resultatsVerification" class="mt-4">
                        <div class="alert alert-info border-start border-info border-4">
                            <div class="d-flex align-items-center">
                                <i class="fas fa-info-circle fa-2x me-3 text-info"></i>
                                <div>
                                    <h5 class="alert-heading mb-2">Bienvenue dans le module de vérification</h5>
                                    <p class="mb-0">
                                        Utilisez la recherche ci-dessus pour vérifier les cotisations des membres.<br>
                                        Le système affichera le statut de cotisation en temps réel.
                                    </p>
... (tronqué)

# ============================================================
# ORIGINE 3: verification_complete2.py (2025-12-04)
# ============================================================

# verification_complete.py
import os
import sys
import django
import inspect
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
# 1. VÉRIFICATION DES IMPORTS ET MODÈLES
# ============================================================================
print("\n📦 1. VÉRIFICATION DES IMPORTS ET MODÈLES")
print("-"*50)

try:
    from assureur import views
    print("✅ Module assureur.views importé")

    # Vérifier les imports dans le code source
    with open('assureur/views.py', 'r', encoding='utf-8') as f:
        view_content = f.read()

    # Compter les imports Membre
    membre_imports = [line for line in view_content.split('\n') if 'import Membre' in line]

    print(f"   Nombre d'imports 'Membre': {len(membre_imports)}")

    if len(membre_imports) > 1:
        print("   ⚠️  ATTENTION: Plusieurs imports Membre détectés")
        for imp in membre_imports:
            print(f"     → {imp.strip()}")
    else:
        print("   ✅ Un seul import Membre (bon)")
... (tronqué)

# ============================================================
# ORIGINE 4: verification_rapide2.py (2025-12-04)
# ============================================================

# verification_rapide.py
import os
import sys
import django

# Configuration Django
projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("="*70)
print("🔍 VÉRIFICATION RAPIDE - LISTE DES MEMBRES")
print("="*70)

# 1. Vérifier l'import
print("\n1. IMPORT DE MEMBRE DANS assureur/views.py:")
try:
    with open('assureur/views.py', 'r') as f:
        content = f.read()

    found = False
    for line in content.split('\n'):
        if 'Membre' in line and 'import' in line:
            print(f"   ✅ Trouvé: {line.strip()}")
            found = True
            if 'agents.models' in line:
                print("      → Utilise agents.models.Membre (20 membres)")
            elif 'assureur.models' in line:
                print("      → Utilise assureur.models.Membre (3 membres)")

    if not found:
        print("   ❌ Aucun import de Membre trouvé")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# 2. Vérifier la vue
print("\n2. VUE liste_membres:")
try:
    from django.test import RequestFactory
    from assureur.views import liste_membres
    print("   ✅ Vue importable")

    # Vérifier la source
    import inspect
    source = inspect.getsource(liste_membres)

    checks = [
        ("order_by", "date_inscription" in source or "date_adhesion" in source),
        ("search", "Q(" in source and "icontains" in source),
... (tronqué)

# ============================================================
# ORIGINE 5: verification_complete.py (2025-12-04)
# ============================================================

# verification_complete.py
import os
import sys
import django
from django.db.models import Q

# Configuration Django
projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("="*80)
print("🔍 VERIFICATION COMPLÈTE DU SYSTÈME MEMBRES")
print("="*80)

def verifier_imports():
    """Vérifie les imports dans assureur/views.py"""
    print("\n📋 1. VÉRIFICATION DES IMPORTS DANS assureur/views.py")
    print("-"*50)

    try:
        with open('assureur/views.py', 'r') as f:
            content = f.read()

        # Chercher les imports de Membre
        import_lines = []
        for line in content.split('\n'):
            if 'Membre' in line and ('import' in line or 'from' in line):
                import_lines.append(line.strip())

        if import_lines:
            for line in import_lines:
                print(f"  ✅ Trouvé: {line}")

                # Extraire le module source
                if 'from' in line:
                    module = line.split('from')[1].split('import')[0].strip()
                    print(f"     → Module: {module}")
        else:
            print("  ❌ Aucun import de 'Membre' trouvé dans assureur/views.py")

    except Exception as e:
        print(f"  ❌ Erreur: {e}")

def verifier_modeles():
    """Compare les deux modèles Membre"""
    print("\n📋 2. COMPARAISON DES MODÈLES MEMBRE")
    print("-"*50)

... (tronqué)

# ============================================================
# ORIGINE 6: verification_finale_agents.py (2025-12-03)
# ============================================================

# verification_finale_agents.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User, Group
from agents.models import Agent
from assureur.models import Cotisation, Membre

print("="*70)
print("🎯 VÉRIFICATION FINALE - SYSTÈME AGENTS")
print("="*70)

# Configuration
client = Client()

# 1. Tester avec l'utilisateur existant
print("1. 🔐 TEST AVEC UTILISATEUR EXISTANT:")
print("   " + "-"*30)

for username in ['agent_test', 'agent_complet_test', 'admin']:
    try:
        user = User.objects.get(username=username)
        login = client.login(username=username, password='agent123' if 'agent' in username else 'admin123')
        if login:
            # Test d'accès simple
            response = client.get('/agents/tableau-de-bord/')
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {username}: Tableau de bord - {response.status_code}")
        else:
            print(f"   ❌ {username}: Échec connexion")
    except User.DoesNotExist:
        print(f"   ❌ {username}: Non trouvé")

# 2. Statistiques du système
print(f"\n2. 📊 STATISTIQUES DU SYSTÈME:")
print("   " + "-"*30)

cotisations = Cotisation.objects.all()
membres = Membre.objects.filter(statut='actif')
agents = Agent.objects.filter(statut='actif')

print(f"   Cotisations totales: {cotisations.count()}")
... (tronqué)

# ============================================================
# ORIGINE 7: verification_finale9.py (2025-12-03)
# ============================================================

#!/usr/bin/env python3
"""
VÉRIFICATION FINALE - Mutuelle Core
"""

import os
import sys
import django
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.conf import settings

print("=" * 60)
print("✅ VÉRIFICATION FINALE DU SYSTÈME")
print("=" * 60)
print(f"Date: {datetime.now()}")
print(f"Répertoire: {BASE_DIR}")
print()

# 1. Vérifier les modèles principaux
print("1. MODÈLES PRINCIPAUX:")
print("-" * 30)

try:
    from soins.models import BonDeSoin
    print(f"   ✅ BonDeSoin: {BonDeSoin.objects.count()} enregistrement(s)")
except Exception as e:
    print(f"   ❌ BonDeSoin: {e}")

try:
    from membres.models import Membre
    print(f"   ✅ Membre: {Membre.objects.count()} enregistrement(s)")
except Exception as e:
    print(f"   ❌ Membre: {e}")

try:
    from agents.models import Agent
    print(f"   ✅ Agent: {Agent.objects.count()} enregistrement(s)")
except Exception as e:
    print(f"   ❌ Agent: {e}")

try:
... (tronqué)

# ============================================================
# ORIGINE 8: verification_finale8.py (2025-12-02)
# ============================================================

# verification_finale.py
import requests

print("🎯 Vérification finale du système assureur")
print("="*50)

# Vérification que toutes les URLs de base existent
print("1. Vérification des URLs (sans authentification):")
urls = {
    'Dashboard racine': '/assureur/',
    'Dashboard alternatif': '/assureur/dashboard/',
    'Liste membres': '/assureur/membres/',
    'Liste bons': '/assureur/bons/',
    'Statistiques': '/assureur/statistiques/',
    'Configuration': '/assureur/configuration/',
}

for name, url in urls.items():
    response = requests.get(f'http://localhost:8000{url}', allow_redirects=False)

    if response.status_code == 302:
        print(f"   ✅ {name}: Protégé (redirection login)")
    elif response.status_code == 200:
        print(f"   ⚠️  {name}: Accessible sans auth (problème sécurité)")
    elif response.status_code == 404:
        print(f"   ❌ {name}: Non trouvé")
    else:
        print(f"   ❓ {name}: Code {response.status_code}")

print("\n2. Vérification des templates existants:")
import os
templates_dir = 'templates/assureur'
if os.path.exists(templates_dir):
    templates = os.listdir(templates_dir)
    print(f"   ✅ {len(templates)} templates trouvés")

    templates_importants = [
        'dashboard.html',
        'liste_membres.html',
        'liste_bons.html',
        'statistiques.html',
    ]

    for template in templates_importants:
        if template in templates:
            print(f"      ✅ {template}: Présent")
        else:
            print(f"      ❌ {template}: Absent")
else:
    print(f"   ❌ Répertoire templates/assureur non trouvé")
... (tronqué)

# ============================================================
# ORIGINE 9: verification_complete_messages.py (2025-12-02)
# ============================================================

# verification_complete_messages.py
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def verifier_tous_les_messages():
    """Vérifie que tous les messages spécifiques sont présents"""

    print("=" * 60)
    print("VÉRIFICATION COMPLÈTE DES MESSAGES")
    print("=" * 60)

    # Récupérer tous les messages
    url = f"{BASE_URL}/communication/api/public/conversations/5/messages/"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            messages = data.get('messages', [])

            print(f"📊 Total de messages dans la réponse: {len(messages)}")

            # Liste des messages à vérifier
            messages_a_verifier = [
                {"recherche": "Test diagnostique", "trouve": False, "ids": []},
                {"recherche": "Test API diagnostique", "trouve": False, "ids": []},
                {"recherche": "Test API", "trouve": False, "ids": []},
                {"recherche": "Shell Test", "trouve": False, "ids": []},
                {"recherche": "Test Diagnostic", "trouve": False, "ids": []},
                {"recherche": "CAPTURE", "trouve": False, "ids": []},
                {"recherche": "Message via API", "trouve": False, "ids": []},
            ]

            print("\n🔍 Recherche dans tous les messages...")

            for msg in messages:
                titre = msg.get('titre', '')
                contenu = msg.get('contenu', '')

                for recherche in messages_a_verifier:
                    if (recherche['recherche'] in titre or
                        recherche['recherche'] in contenu):
                        recherche['trouve'] = True
                        recherche['ids'].append(msg['id'])

            # Afficher les résultats
            print("\n" + "=" * 60)
... (tronqué)

# ============================================================
# ORIGINE 10: verification_finale_systeme.py (2025-12-01)
# ============================================================

#!/usr/bin/env python3
import os
import sys
import django

sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    print("=== VÉRIFICATION FINALE DU SYSTÈME ===")

    # 1. Vérifier le modèle Pharmacien
    from pharmacien.models import Pharmacien
    pharmaciens_count = Pharmacien.objects.count()
    print(f"1. ✅ Pharmaciens dans la base: {pharmaciens_count}")

    # 2. Vérifier OrdonnancePharmacien
    from pharmacien.models import OrdonnancePharmacien
    ord_pharma_count = OrdonnancePharmacien.objects.count()
    print(f"2. ✅ OrdonnancePharmacien dans la base: {ord_pharma_count}")

    # 3. Vérifier un utilisateur pharmacien
    from django.contrib.auth.models import User
    pharmacien_users = User.objects.filter(groups__name='Pharmacien')
    print(f"3. ✅ Utilisateurs dans groupe Pharmacien: {pharmacien_users.count()}")

    # 4. Tester la vue historique_validation
    from pharmacien.views import historique_validation
    print(f"4. ✅ Vue historique_validation importée avec succès")

    # 5. Vérifier les templates
    import os
    templates = [
        'templates/pharmacien/historique.html',
        'templates/pharmacien/base_pharmacien.html',
        'templates/medecin/base_medecin.html',
    ]

    print("5. ✅ Vérification des templates:")
    for template in templates:
        if os.path.exists(template):
            size = os.path.getsize(template)
            print(f"   - {template}: {size} octets ✓")
        else:
            print(f"   - {template}: MANQUANT ✗")

    # 6. Tester une requête simple
    if pharmacien_users.exists():
... (tronqué)

# ============================================================
# ORIGINE 11: verification_sans_erreur.py (2025-11-30)
# ============================================================

# verification_sans_erreur.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("🔍 VÉRIFICATION SANS ERREUR DE CHAMP")
print("=" * 50)

def verifier_apps_sans_erreur():
    """Vérification des apps sans erreur"""
    from django.apps import apps

    apps_a_verifier = ['ia_detection', 'scoring', 'relances']

    for app in apps_a_verifier:
        try:
            app_config = apps.get_app_config(app)
            modeles = list(app_config.get_models())
            print(f"✅ {app}: CHARGÉE - {len(modeles)} modèles")
        except Exception as e:
            print(f"❌ {app}: ERREUR - {e}")

def verifier_donnees_sans_champ():
    """Vérifie les données sans accéder aux champs manquants"""
    print("\\n📊 VÉRIFICATION DES DONNÉES:")

    try:
        from scoring.models import HistoriqueScore, RegleScoring
        from relances.models import TemplateRelance

        print(f"   📈 Règles scoring: {RegleScoring.objects.count()}")
        print(f"   📧 Templates relance: {TemplateRelance.objects.count()}")
        print(f"   📋 Scores historiques: {HistoriqueScore.objects.count()}")

    except Exception as e:
        print(f"   ❌ Erreur données: {e}")

def calculer_scores_sans_erreur():
    """Calcule les scores sans erreur de champ"""
    print("\\n🎯 CALCUL DES SCORES SANS ERREUR:")

    try:
        from membres.models import Membre
        from scoring.models import HistoriqueScore
        from scoring.calculators import CalculateurScoreMembre

        # Compter les membres avec une requête simple
        total_membres = Membre.objects.count()
        total_scores = HistoriqueScore.objects.count()
... (tronqué)

# ============================================================
# ORIGINE 12: verification_post_deploiement.py (2025-11-30)
# ============================================================

# verification_post_deploiement.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_deploiement():
    print("🔍 VÉRIFICATION POST-DÉPLOIEMENT")

    # Vérifier les modèles
    from django.apps import apps
    apps_attendues = ['ia_detection', 'scoring', 'relances']

    for app in apps_attendues:
        try:
            app_config = apps.get_app_config(app)
            print(f"✅ App {app} chargée - {len(app_config.get_models())} modèles")
        except:
            print(f"❌ App {app} NON trouvée")

    # Vérifier les données initialisées
    from ia_detection.models import ModeleIA
    from scoring.models import RegleScoring
    from relances.models import TemplateRelance

    print(f"📊 Modèles IA: {ModeleIA.objects.count()}")
    print(f"📊 Règles scoring: {RegleScoring.objects.count()}")
    print(f"📊 Templates relance: {TemplateRelance.objects.count()}")

    # Tester une fonctionnalité
    from membres.models import Membre
    from scoring.calculators import CalculateurScoreMembre

    membre = Membre.objects.first()
    if membre:
        calculateur = CalculateurScoreMembre()
        score = calculateur.calculer_score_complet(membre)
        print(f"🎯 Test scoring: {membre.nom} → {score['score_final']} ({score['niveau_risque']})")

    print("✅ Vérification terminée")

if __name__ == "__main__":
    verifier_deploiement()

# ============================================================
# ORIGINE 13: verification_rapide1.py (2025-11-28)
# ============================================================

# verification_rapide.py

import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_rapide():
    """Vérification rapide de l'état de l'application agents"""

    print("🔍 VÉRIFICATION RAPIDE AGENTS")
    print("=" * 50)

    # Vérifier l'accès aux URLs principales
    from django.urls import reverse
    from django.test import Client

    urls_test = [
        'agents:tableau_de_bord',
        'agents:creer_membre',
        'agents:liste_membres',
        'agents:creer_bon_soin',
    ]

    client = Client()

    print("\n🌐 Test des URLs:")
    for url_name in urls_test:
        try:
            url = reverse(url_name)
            print(f"   ✅ {url_name} -> {url}")
        except Exception as e:
            print(f"   ❌ {url_name} -> ERREUR: {e}")

    # Vérifier les modèles
    print("\n📊 Données existantes:")
    try:
        from agents.models import Agent
        from membres.models import Membre
        from soins.models import BonDeSoin

        print(f"   • Agents: {Agent.objects.count()}")
        print(f"   • Membres: {Membre.objects.count()}")
        print(f"   • Bons de soin: {BonDeSoin.objects.count()}")

... (tronqué)

# ============================================================
# ORIGINE 14: verification_template_complet.py (2025-11-28)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

def verification_template_complet():
    print("🔍 VÉRIFICATION DU TEMPLATE COMPLET")
    print("=" * 50)

    # Vérifier le template
    template_path = 'templates/medecin/suivi_chronique/tableau_bord.html'

    if not os.path.exists(template_path):
        print("❌ Template non trouvé")
        return False

    print("✅ Template trouvé")

    # Analyser le contenu
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"📏 Taille: {len(content)} caractères")
    print(f"📄 Lignes: {len(content.splitlines())}")

    # Vérifier les éléments clés
    elements = [
        ("Extension base", "{% extends 'medecin/base_medecin.html' %}" in content),
        ("Titre", "Suivi des Maladies Chroniques" in content),
        ("Cartes statistiques", "card border-left-primary" in content),
        ("Tableau accompagnements", "table table-hover" in content),
        ("Bouton création", "Créer un Accompagnement" in content)
    ]

    print("\n🔍 Éléments détectés:")
    for element, present in elements:
        status = "✅" if present else "❌"
        print(f"   {status} {element}")

    # Test Django
    try:
        django.setup()
        from django.template.loader import get_template

        template = get_template('medecin/suivi_chronique/tableau_bord.html')
        print("\n✅ Django peut charger le template complet")

        # Test de rendu avec contexte
... (tronqué)

# ============================================================
# ORIGINE 15: verification_finale_suivi.py (2025-11-28)
# ============================================================

import os
import django
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    from django.test import Client
    from medecin.models import Medecin

    def verification_finale_suivi():
        print("🎯 VÉRIFICATION FINALE - SUIVI CHRONIQUE")
        print("=" * 50)

        client = Client()

        # 1. Vérifier médecin
        try:
            medecin = Medecin.objects.get(user__username='medecin_test')
            print(f"✅ Médecin: Dr {medecin.user.first_name} {medecin.user.last_name}")
        except Medecin.DoesNotExist:
            print("❌ Médecin non trouvé")
            return False

        # 2. Connexion
        print("🔑 Connexion...")
        if not client.login(username='medecin_test', password='password123'):
            print("❌ Échec connexion")
            return False
        print("✅ Connecté")

        # 3. Test de la page suivi chronique
        print("\n🚀 Test page suivi chronique...")
        start_time = time.time()
        response = client.get('/medecin/suivi-chronique/')
        end_time = time.time()

        print(f"⏱️  Temps de réponse: {end_time - start_time:.2f}s")
        print(f"📊 Status: {response.status_code}")

        if response.status_code == 200:
            print("🎉 SUCCÈS - Page accessible sans erreur!")

            # Analyse du contenu
            content = response.content.decode('utf-8')
            print(f"📏 Taille page: {len(content)} caractères")
... (tronqué)

# ============================================================
# ORIGINE 16: verification_donnees_exacte.py (2025-11-28)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    from django.contrib.auth.models import User
    from medecin.models import Medecin, SpecialiteMedicale, EtablissementMedical

    def verification_donnees_exacte():
        print("📊 VÉRIFICATION DES DONNÉES EXACTES")
        print("=" * 50)

        # 1. Vérifier le médecin de test
        print("1. 🧪 MÉDECIN DE TEST:")
        try:
            medecin_test = Medecin.objects.get(user__username='medecin_test')
            print(f"   ✅ Trouvé: {medecin_test}")
            print(f"   👤 User: {medecin_test.user.username}")
            print(f"   📧 Email pro: {medecin_test.email_pro}")
            print(f"   📞 Téléphone: {medecin_test.telephone_pro}")
            print(f"   🎯 Spécialité: {medecin_test.specialite.nom}")
            print(f"   🏥 Établissement: {medecin_test.etablissement.nom}")
            print(f"   ✅ Actif: {medecin_test.actif}")
            print(f"   🟢 Disponible: {medecin_test.disponible}")

        except Medecin.DoesNotExist:
            print("   ❌ Médecin test non trouvé")
            return False

        # 2. Vérifier les spécialités
        print("\n2. 📚 SPÉCIALITÉS MÉDICALES:")
        specialites = SpecialiteMedicale.objects.all()
        for spec in specialites:
            count = Medecin.objects.filter(specialite=spec).count()
            print(f"   🎯 {spec.nom}: {count} médecin(s)")

        # 3. Vérifier les établissements
        print("\n3. 🏥 ÉTABLISSEMENTS MÉDICAUX:")
        etablissements = EtablissementMedical.objects.all()
        for etab in etablissements:
            count = Medecin.objects.filter(etablissement=etab).count()
            print(f"   🏥 {etab.nom} ({etab.type_etablissement}): {count} médecin(s)")

        # 4. Statistiques générales
        print("\n4. 📈 STATISTIQUES:")
... (tronqué)

# ============================================================
# ORIGINE 17: verification_donnees.py (2025-11-27)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    from django.contrib.auth.models import User
    from medecin.models import Medecin, SpecialiteMedicale, BonSoin

    def verification_donnees():
        print("📊 VÉRIFICATION DES DONNÉES")
        print("=" * 40)

        # 1. Médecins
        print("1. 🩺 Médecins dans le système:")
        medecins = Medecin.objects.all()
        for medecin in medecins:
            print(f"   👤 {medecin} (User: {medecin.user.username})")

        # 2. Spécialités
        print("\n2. 📚 Spécialités médicales:")
        specialites = SpecialiteMedicale.objects.all()
        for spec in specialites:
            print(f"   🎯 {spec.nom} - {spec.description}")

        # 3. Bons de soin
        print("\n3. 📋 Bons de soin:")
        bons = BonSoin.objects.all()[:5]  # Premiers 5 seulement
        for bon in bons:
            print(f"   📄 {bon.numero_bon} - {bon.membre} - Statut: {bon.statut}")

        print(f"\n📈 Total bons dans le système: {BonSoin.objects.count()}")

        # 4. Vérifier les bons assignés au médecin de test
        try:
            medecin_test = Medecin.objects.get(user__username='medecin_test')
            bons_medecin = BonSoin.objects.filter(medecin_destinataire=medecin_test)
            print(f"\n4. 🎯 Bons assignés au médecin test: {bons_medecin.count()}")

            for bon in bons_medecin:
                print(f"   📋 {bon.numero_bon} - {bon.membre} - {bon.statut}")

        except Medecin.DoesNotExist:
            print("\n4. ❌ Médecin test non trouvé")

    verification_donnees()
... (tronqué)

# ============================================================
# ORIGINE 18: verification_urls_medecin.py (2025-11-27)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

def verifier_urls_medecin():
    print("🔗 VÉRIFICATION DES URLS MÉDECIN")
    print("=" * 40)

    # Vérifier le fichier urls.py de l'application medecin
    urls_path = os.path.join(os.path.dirname(__file__), 'medecin', 'urls.py')

    if os.path.exists(urls_path):
        print("✅ Fichier medecin/urls.py existe")
        with open(urls_path, 'r') as f:
            content = f.read()
            print("📄 Contenu de medecin/urls.py:")
            print("-" * 30)
            for line in content.split('\n'):
                if line.strip() and not line.strip().startswith('#'):
                    print(f"  {line}")
            print("-" * 30)
    else:
        print("❌ Fichier medecin/urls.py n'existe pas")

    # Vérifier les URLs dans le projet principal
    projet_urls_path = os.path.join(os.path.dirname(__file__), 'votre_projet', 'urls.py')
    if os.path.exists(projet_urls_path):
        print("\n📋 URLs dans le projet principal:")
        with open(projet_urls_path, 'r') as f:
            content = f.read()
            if 'medecin' in content:
                print("✅ Application medecin incluse dans les URLs principales")
            else:
                print("❌ Application medecin NON incluse dans les URLs principales")

    # Tester l'accès via le resolver Django
    print("\n🌐 URLs disponibles via Django:")
    from django.urls import get_resolver
    resolver = get_resolver()

    def extract_urls(patterns, prefix=''):
        urls = []
        for pattern in patterns:
            if hasattr(pattern, 'pattern'):
                current_pattern = str(pattern.pattern)
... (tronqué)

# ============================================================
# ORIGINE 19: verification_medecin.py (2025-11-27)
# ============================================================

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    from django.contrib.auth.models import User
    from membres.models import Medecin

    def verifier_medecin():
        print("🔍 VÉRIFICATION MÉDECIN:")
        print("=" * 40)

        # Vérifier si l'utilisateur médecin existe
        try:
            user = User.objects.get(username='medecin_test')
            print(f"✅ Utilisateur trouvé: {user.username}")

            # Vérifier si c'est un médecin
            try:
                medecin = Medecin.objects.get(user=user)
                print(f"✅ Médecin trouvé: {medecin.prenom} {medecin.nom}")
                print(f"   Specialité: {medecin.specialite}")
                print(f"   ID: {medecin.id}")

                # Vérifier les permissions
                print(f"   User is_active: {user.is_active}")
                print(f"   User is_staff: {user.is_staff}")
                print(f"   User is_superuser: {user.is_superuser}")

            except Medecin.DoesNotExist:
                print("❌ L'utilisateur n'est pas associé à un médecin")
                # Créer le médecin
                medecin = Medecin.objects.create(
                    user=user,
                    nom="Docteur",
                    prenom="Test",
                    specialite="Generaliste"
                )
                print("✅ Médecin créé automatiquement")

        except User.DoesNotExist:
            print("❌ Utilisateur médecin_test non trouvé")
            # Créer l'utilisateur et le médecin
            user = User.objects.create_user(
                username='medecin_test',
... (tronqué)

# ============================================================
# ORIGINE 20: verification_interface_medecin.py (2025-11-27)
# ============================================================

#!/usr/bin/env python
"""
VÉRIFICATION INTERFACE MÉDECIN - CORRIGÉ
"""

import os
import sys
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Bon
from django.contrib.auth import get_user_model

User = get_user_model()

def verification_interface_medecin():
    print("🔍 VÉRIFICATION INTERFACE MÉDECIN")
    print("=" * 40)

    client = Client()

    # 1. Connexion médecin
    print("1. 🔐 Connexion médecin...")
    login_success = client.login(username='medecin_test', password='pass123')
    if not login_success:
        print("   ❌ Échec connexion")
        return False
    print("   ✅ Connecté")

    # 2. Test dashboard médecin
    print("2. 📊 Test dashboard...")
    response = client.get('/medecin/dashboard/')
    if response.status_code == 200:
        print("   ✅ Dashboard accessible")
    else:
        print(f"   ❌ Dashboard: {response.status_code}")

    # 3. Test page ordonnances
    print("3. 📋 Test ordonnances...")
    response = client.get('/medecin/ordonnances/')
    if response.status_code == 200:
        print("   ✅ Page ordonnances accessible")

        # Vérifier si les bons apparaissent dans le contexte (méthode sécurisée)
        if hasattr(response, 'context') and response.context is not None:
            context_keys = list(response.context.keys()) if response.context else []
            print(f"   📋 Clés du contexte: {context_keys}")
... (tronqué)

# ============================================================
# ORIGINE 21: verification_finale_systeme1.py (2025-11-27)
# ============================================================

# verification_finale_systeme.py
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from membres.models import Membre

def verification_systeme_complet():
    print("🔍 VÉRIFICATION SYSTÈME COMPLET")
    print("=" * 60)

    client = Client()

    # Test 1: Vérification que le serveur répond
    try:
        response = client.get('/')
        print(f"✅ Serveur Django - Statut: {response.status_code}")
    except Exception as e:
        print(f"❌ Serveur Django - Erreur: {e}")

    # Test 2: Vérification module affichage unifié
    try:
        from affichage_unifie import afficher_fiche_cotisation_unifiee, determiner_statut_cotisation
        print("✅ Module affichage_unifie - Import réussi")
    except Exception as e:
        print(f"❌ Module affichage_unifie - Erreur: {e}")

    # Test 3: Vérification des modèles
    try:
        membres_count = Membre.objects.count()
        print(f"✅ Modèle Membre - {membres_count} membre(s) trouvé(s)")
    except Exception as e:
        print(f"❌ Modèle Membre - Erreur: {e}")

    # Test 4: Vérification des URLs agents
    urls_a_verifier = [
        '/agents/tableau-de-bord/',
        '/agents/liste-membres/',
        '/agents/verification-cotisations/',
    ]

    for url in urls_a_verifier:
        try:
... (tronqué)

# ============================================================
# ORIGINE 22: verification_installation_complete.py (2025-11-27)
# ============================================================

# verification_installation_complete.py
import os
import sys
import json
from pathlib import Path
from datetime import datetime

print("🎯 VÉRIFICATION INSTALLATION COMPLÈTE")
print("=" * 60)

class VerificateurInstallation:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'composants': {},
            'statut': 'EN_COURS'
        }

    def verifier_composants(self):
        """Vérifie tous les composants installés"""
        print("🔍 Vérification des composants...")

        composants = {
            'scripts_surveillance': self._verifier_scripts_surveillance(),
            'planification_cron': self._verifier_planification_cron(),
            'dossiers_donnees': self._verifier_dossiers_donnees(),
            'donnees_historiques': self._verifier_donnees_historiques(),
            'compatibilite_scripts': self._verifier_compatibilite_scripts()
        }

        self.rapport['composants'] = composants
        self.rapport['statut'] = 'COMPLET' if all(composants.values()) else 'PARTIEL'

        return composants

    def _verifier_scripts_surveillance(self):
        """Vérifie que tous les scripts de surveillance sont présents"""
        scripts_requis = [
            'surveillance_simple.py',
            'surveillance_hebdomadaire.py',
            'diagnostic_sync_final.py',
            'correcteur_sync_urgence.py',
            'rapport_performance_mensuel.py',
            'monitoring_long_terme.py',
            'adaptateur_evolution.py'
        ]

        presents = []
        manquants = []

... (tronqué)

# ============================================================
# ORIGINE 23: verification_permissions.py (2025-11-20)
# ============================================================

import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from agents.models import Agent

def verifier_permissions_utilisateur():
    """Vérifier et corriger les permissions de l'utilisateur"""
    print("🔐 VÉRIFICATION DES PERMISSIONS")
    print("==============================")

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

        # Vérifier si c'est un agent
        try:
            agent = Agent.objects.get(user=user)
            print(f"✅ AGENT TROUVÉ: {agent.nom_complet}")
            print(f"   Code agent: {agent.code_agent}")
            print(f"   Poste: {agent.poste}")
        except Agent.DoesNotExist:
            print("❌ L'utilisateur n'est pas associé à un agent")
            print("🔄 Création de l'agent...")

            # Créer l'agent
            agent = Agent.objects.create(
                user=user,
                nom_complet=user.get_full_name() or username,
                code_agent=f"AGENT-{user.id:03d}",
... (tronqué)

# ============================================================
# ORIGINE 24: verification_finale7.py (2025-11-19)
# ============================================================

# verification_finale.py
import os
import django
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_finale():
    print("🎯 VÉRIFICATION FINALE - TOUTES LES URLS")
    print("=" * 60)

    urls_a_verifier = [
        # Communication
        'communication:liste_notifications',
        'communication:messagerie',

        # Médecin
        'medecin:dashboard',           # Nom principal
        'medecin:dashboard_medecin',   # Alias de compatibilité
        'medecin:liste_bons',
        'medecin:mes_ordonnances',

        # URLs de base
        'medecin:dashboard_root',
    ]

    for url_name in urls_a_verifier:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name:35} -> {url}")
        except Exception as e:
            print(f"❌ {url_name:35} -> ERREUR: {e}")

if __name__ == "__main__":
    verification_finale()
    print("\n🎉 VÉRIFICATION TERMINÉE !")

# ============================================================
# ORIGINE 25: verification_config.py (2025-11-19)
# ============================================================

#!/usr/bin/env python3
"""
SCRIPT DE VÉRIFICATION DE CONFIGURATION
Vérifie la configuration actuelle du projet
"""

import os
from pathlib import Path

def verifier_configuration():
    """Vérifie la configuration du projet"""
    print("=" * 80)
    print("VÉRIFICATION DE CONFIGURATION")
    print("=" * 80)

    # Vérification des dossiers
    dossiers_requis = [
        "templates",
        "static",
        "media",
        "logs",
        "agents/templates",
        "agents/static"
    ]

    print("\n📁 VÉRIFICATION DES DOSSIERS:")
    for dossier in dossiers_requis:
        if os.path.exists(dossier):
            print(f"   ✅ {dossier} - Présent")
        else:
            print(f"   ❌ {dossier} - Manquant")

    # Vérification des configurations critiques
    print("\n⚙️  CONFIGURATIONS CRITIQUES:")
    configurations = {
        "SECRET_KEY": "Définie via variable d'environnement",
        "DEBUG": "True en développement uniquement",
        "ALLOWED_HOSTS": "Configurés pour l'environnement",
        "DATABASES": "SQLite configuré",
        "EMAIL_BACKEND": "Console en développement"
    }

    for config, statut in configurations.items():
        print(f"   • {config}: {statut}")

if __name__ == "__main__":
    verifier_configuration()

# ============================================================
# ORIGINE 26: verification_rapide3.py (2025-11-18)
# ============================================================

#!/usr/bin/env python
"""
VÉRIFICATION RAPIDE ASSUREUR
Vérifications essentielles en 30 secondes
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

def verification_rapide():
    """Vérification rapide des éléments critiques"""
    print("🔍 VÉRIFICATION RAPIDE ASSUREUR")
    print("="*50)

    checks = []

    # 1. Vérifier l'application dans INSTALLED_APPS
    from django.conf import settings
    if 'assureur' in settings.INSTALLED_APPS:
        checks.append(("✅ Application dans INSTALLED_APPS", True))
    else:
        checks.append(("❌ Application absente de INSTALLED_APPS", False))

    # 2. Vérifier les modèles
    try:
        from assureur.models import Membre, Bon, Cotisation
        checks.append(("✅ Modèles principaux importables", True))
    except ImportError as e:
        checks.append((f"❌ Erreur import modèles: {e}", False))

    # 3. Vérifier les vues
    try:
        from assureur.views import dashboard_assureur, liste_cotisations
        checks.append(("✅ Vues principales importables", True))
    except ImportError as e:
        checks.append((f"❌ Erreur import vues: {e}", False))

    # 4. Vérifier les URLs
    try:
        from assureur.urls import urlpatterns
        checks.append((f"✅ {len(urlpatterns)} patterns d'URL configurés", True))
    except Exception as e:
... (tronqué)

# ============================================================
# ORIGINE 27: verification_settings1.py (2025-11-17)
# ============================================================

# verification_settings.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_configuration_agents():
    """Vérifie la configuration pour les agents"""
    print("🔧 VÉRIFICATION DE LA CONFIGURATION")
    print("=" * 50)

    # 1. Vérifier les applications installées
    apps_requises = ['assureur', 'agents', 'communication']
    apps_manquantes = [app for app in apps_requises if app not in settings.INSTALLED_APPS]

    if apps_manquantes:
        print("❌ APPLICATIONS MANQUANTES:", apps_manquantes)
    else:
        print("✅ Toutes les applications requises sont installées")

    # 2. Vérifier les context processors
    context_processors = getattr(settings, 'TEMPLATES', [{}])[0].get('OPTIONS', {}).get('context_processors', [])
    if 'agents.context_processors.agent_context' in context_processors:
        print("✅ Context processor agents configuré")
    else:
        print("❌ Context processor agents non configuré")

    # 3. Vérifier les dossiers templates
    templates_dirs = getattr(settings, 'TEMPLATES', [{}])[0].get('DIRS', [])
    agents_templates = any('agents/templates' in str(dir) for dir in templates_dirs)
    if agents_templates:
        print("✅ Dossier templates agents configuré")
    else:
        print("❌ Dossier templates agents non configuré")

    # 4. Vérifier la configuration métier
    mutuelle_config = getattr(settings, 'MUTUELLE_CONFIG', {})
    config_requise = ['COTISATION_STANDARD', 'COTISATION_FEMME_ENCEINTE', 'AVANCE', 'FRAIS_CARTE']
    config_manquante = [key for key in config_requise if key not in mutuelle_config]

    if config_manquante:
        print("❌ CONFIGURATION MANQUANTE:", config_manquante)
    else:
        print("✅ Configuration métier complète")
        print(f"   • Cotisation standard: {mutuelle_config['COTISATION_STANDARD']} FCFA")
        print(f"   • Cotisation femme enceinte: {mutuelle_config['COTISATION_FEMME_ENCEINTE']} FCFA")
        print(f"   • Avance: {mutuelle_config['AVANCE']} FCFA")
        print(f"   • Frais carte: {mutuelle_config['FRAIS_CARTE']} FCFA")
... (tronqué)

# ============================================================
# ORIGINE 28: verification_immediate.py (2025-11-17)
# ============================================================

# verification_immediate.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_immediate():
    """Vérification immédiate après correction du template"""

    print("🔍 VÉRIFICATION IMMÉDIATE APRÈS CORRECTION")
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

        # Vérifications CRITIQUES du nouveau template
        verifications_critiques = {
            'Template complet chargé': 'container-fluid' in content,
            'Structure conversation-item': 'conversation-item' in content,
            'Badges Bootstrap': 'badge bg-' in content,
            'Modal nouveau message': 'nouveauMessageModal' in content,
            'Date activité': 'Dernière activité' in content,
            'Statistiques section': 'Statistiques:' in content,
            'Bouton action présent': 'btn btn-primary' in content,
            'En-tête messagerie': 'Messagerie' in content and 'fa-comments' in content
        }

        print(f"\n✅ ÉLÉMENTS CRITIQUES:")
        score = 0
        for element, present in verifications_critiques.items():
            status = "✅" if present else "❌"
            if present: score += 1
            print(f"   {status} {element}: {'PRÉSENT' if present else 'ABSENT'}")

        pourcentage = (score / len(verifications_critiques)) * 100
        print(f"\n📈 SCORE: {score}/{len(verifications_critiques)} ({pourcentage:.0f}%)")

... (tronqué)

# ============================================================
# ORIGINE 29: verification_affichage_final.py (2025-11-17)
# ============================================================

# verification_affichage_final.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_affichage_final():
    """Vérifier exactement ce qui s'affiche dans la messagerie"""

    print("🔍 VÉRIFICATION AFFICHAGE FINAL")
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

        # Chercher la section des conversations
        if 'conversation-item' in content:
            print("✅ Section conversations trouvée")

            # Extraire la partie HTML des conversations
            debut = content.find('conversation-item')
            fin = content.find('</div>', debut) + 1000  # Prendre un extrait
            extrait_conversation = content[debut:fin] if debut != -1 else "Non trouvé"

            print(f"\n📄 EXTRAT DE LA CONVERSATION:")
            print(extrait_conversation[:500] + "..." if len(extrait_conversation) > 500 else extrait_conversation)

        # Vérifications détaillées
        verifications = {
            'Conversation #4': 'Conversation #4' in content,
            'koffitanoh': 'koffitanoh' in content,
            'assureur_test': 'assureur_test' in content,
            'Messages non lus': 'Messages non lus' in content or 'non lu' in content,
            'Total messages': 'Total messages' in content or 'message(s)' in content,
            'Dernière activité': 'Dernière activité' in content or 'activité' in content,
            'Badge messages': 'badge bg-info' in content or 'badge bg-danger' in content
        }
... (tronqué)

# ============================================================
# ORIGINE 30: verification_finale6.py (2025-11-17)
# ============================================================

# verification_finale.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_finale():
    """Vérification finale que la messagerie fonctionne"""

    print("🎯 VÉRIFICATION FINALE")
    print("=" * 50)

    from django.test import Client
    from django.contrib.auth.models import User

    try:
        # Tester avec assureur_test qui a des conversations
        user = User.objects.get(username='assureur_test')
        client = Client()
        client.force_login(user)

        # Tester la messagerie principale
        response = client.get('/communication/')
        content = response.content.decode('utf-8')

        print(f"📊 Statut: {response.status_code}")

        # Vérifications critiques
        checks = {
            'Conversation 4': 'Conversation #4' in content,
            'koffitanoh': 'koffitanoh' in content,
            'assureur_test': 'assureur_test' in content,
            'Messages: 2': 'Messages: 2' in content,
            'Dernière activité': 'Dernière activité' in content
        }

        print("\n✅ VÉRIFICATIONS:")
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"   {status} {check}: {'TROUVÉ' if result else 'NON TROUVÉ'}")

        if all(checks.values()):
            print("\n🎉 SUCCÈS TOTAL ! La messagerie fonctionne parfaitement.")
            print("🌐 L'URL http://127.0.0.1:8000/communication/ affiche maintenant les conversations")
        else:
            print("\n⚠️  Il reste des problèmes d'affichage")

    except Exception as e:
        print(f"❌ Erreur: {e}")
... (tronqué)

# ============================================================
# ORIGINE 31: verification_cotisation.html (2025-11-17)
# ============================================================

{% extends 'agents/base_agent.html' %}
{% load static %}

{% block title %}Vérification cotisations - Agent{% endblock %}
{% block page_title %}Vérification des cotisations{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-check-circle me-2"></i>Vérification en temps réel
                </h5>
            </div>
            <div class="card-body">
                <!-- Recherche rapide -->
                <div class="mb-4">
                    <label class="form-label">Rechercher un membre</label>
                    <div class="input-group">
                        <input type="text" class="form-control" id="rechercheMembreRapide"
                               placeholder="Nom, prénom ou numéro de membre...">
                        <button class="btn btn-outline-primary" type="button" id="btnRechercheRapide">
                            <i class="fas fa-search"></i>
                        </button>
                    </div>
                    <div id="resultatsRechercheRapide" class="mt-2"></div>
                </div>

                <!-- Formulaire de vérification manuelle -->
                <form id="formVerificationManuelle" class="mb-4 p-3 border rounded">
                    <h6 class="mb-3">Vérification manuelle</h6>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Numéro de membre</label>
                            <input type="text" class="form-control" id="numeroMembre"
                                   placeholder="Entrez le numéro de membre">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Nom complet</label>
                            <input type="text" class="form-control" id="nomMembre"
                                   placeholder="Nom et prénom">
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-check me-1"></i>Vérifier la cotisation
                    </button>
                </form>

                <!-- Résultats -->
... (tronqué)

# ============================================================
# ORIGINE 32: verification_urls_vues.py (2025-11-16)
# ============================================================

# verification_urls_vues.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_urls_vues():
    print("=== VÉRIFICATION URLS ET VUES ===")

    # Vérifier que la vue existe maintenant
    try:
        from assureur import views
        if hasattr(views, 'envoyer_message_assureur'):
            print("✅ Vue envoyer_message_assureur trouvée dans assureur.views")
        else:
            print("❌ Vue envoyer_message_assureur toujours manquante")

        # Vérifier les autres vues nécessaires
        vues_necessaires = ['liste_messages', 'detail_message', 'repondre_message']
        for vue in vues_necessaires:
            if hasattr(views, vue):
                print(f"✅ Vue {vue} trouvée")
            else:
                print(f"⚠️  Vue {vue} manquante")

    except Exception as e:
        print(f"❌ Erreur import assureur.views: {e}")

    # Vérifier les URLs
    print("\n📋 VÉRIFICATION URLs ASSUREUR:")
    try:
        from django.urls import reverse, NoReverseMatch

        urls_assureur = [
            'assureur:liste_messages',
            'assureur:envoyer_message',
            'assureur:detail_message',
            'assureur:repondre_message',
        ]

        for url_name in urls_assureur:
            try:
                url = reverse(url_name)
                print(f"✅ {url_name} → {url}")
            except NoReverseMatch:
                print(f"❌ {url_name} non trouvée")

    except Exception as e:
... (tronqué)

# ============================================================
# ORIGINE 33: verification_formulaire.py (2025-11-16)
# ============================================================

# verification_formulaire.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_formulaire():
    print("=== VÉRIFICATION FORMULAIRE MESSAGE ===")

    try:
        from communication.forms import MessageForm
        print("✅ MessageForm existe dans communication.forms")

        # Tester l'import du modèle
        from communication.models import Message
        print("✅ Modèle Message importé avec succès")

        # Vérifier les champs du formulaire
        form = MessageForm()
        print("✅ Formulaire instancié")
        print(f"Champs du formulaire: {list(form.fields.keys())}")

    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("Création du formulaire MessageForm...")
        creer_formulaire()
    except Exception as e:
        print(f"❌ Autre erreur: {e}")

def creer_formulaire():
    """Crée le fichier forms.py s'il n'existe pas"""
    forms_content = '''# communication/forms.py
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['type_message', 'destinataire', 'titre', 'contenu']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre le champ type_message obligatoire avec une valeur par défaut
        self.fields['type_message'].required = True
        self.fields['type_message'].initial = 'MESSAGE'  # Valeur par défaut
        self.fields['type_message'].widget.attrs.update({
            'class': 'form-control',
            'required': 'required'
... (tronqué)

# ============================================================
# ORIGINE 34: verification_base_donnees.py (2025-11-14)
# ============================================================

#!/usr/bin/env python3
"""
SCRIPT DE VÉRIFICATION BASE DE DONNÉES
Vérifie l'état actuel de la base pour l'implémentation
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import connection
from membres.models import Membre
from django.contrib.auth.models import User, Group, Permission
from django.core.management import call_command

def verifier_base_donnees():
    """Vérifie l'état de la base de données"""
    print("🔍 VÉRIFICATION BASE DE DONNÉES")
    print("=" * 50)

    # 1. Vérifier les migrations
    print("\n1. 📦 ÉTAT DES MIGRATIONS")
    print("-" * 25)
    try:
        call_command('showmigrations', '--list')
        print("   ✅ Migrations vérifiées")
    except Exception as e:
        print(f"   ❌ Erreur migrations: {e}")

    # 2. Vérifier la connexion DB
    print("\n2. 🗄️ CONNEXION BASE DE DONNÉES")
    print("-" * 30)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"   ✅ Connecté à: {version[0]}")
    except Exception as e:
        print(f"   ❌ Erreur connexion DB: {e}")

    # 3. Compter les enregistrements
    print("\n3. 📊 STATISTIQUES DONNÉES")
    print("-" * 25)
... (tronqué)

# ============================================================
# ORIGINE 35: verification_detaillee.py (2025-11-14)
# ============================================================

#!/usr/bin/env python3
"""
Vérification détaillée après correction
"""

import re
from pathlib import Path

def detailed_verification():
    """Vérification détaillée des corrections"""
    print("🔍 VÉRIFICATION DÉTAILLÉE POST-CORRECTION")
    print("=" * 60)

    project_root = Path(__file__).parent
    issues = []

    # Fichiers spécifiques à vérifier
    critical_files = [
        "templates/assureur/dashboard.html",
        "templates/assureur/partials/_sidebar.html",
        "assureur/templates/assureur/dashboard.html",
        "templates/assureur/base_assureur.html",
        "assureur/templates/assureur/base_assureur.html"
    ]

    print("\n📋 VÉRIFICATION DES URLs PROBLÉMATIQUES")
    print("-" * 40)

    for file_path in critical_files:
        full_path = project_root / file_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Vérifier les URLs problématiques
            problematic_patterns = [
                r'assureur:rapports',
                r"{%\s*url\s+['\"]assureur:rapports['\"]\s*%}"
            ]

            file_issues = []
            for pattern in problematic_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    file_issues.extend(matches)

            if file_issues:
                print(f"❌ {file_path}")
                for issue in set(file_issues):
                    print(f"   → {issue}")
... (tronqué)

# ============================================================
# ORIGINE 36: verification_finale5.py (2025-11-12)
# ============================================================

#!/usr/bin/env python3
"""
VÉRIFICATION FINALE - Test complet après correction
"""

import requests
import time
import sys

def test_dashboard_access():
    """Test l'accès au dashboard après correction"""

    print("🧪 TEST DU DASHBOARD APRÈS CORRECTION")
    print("=" * 50)

    base_url = "http://localhost:8000"
    dashboard_url = f"{base_url}/agents/tableau-de-bord/"

    try:
        print(f"🔗 Test de l'URL: {dashboard_url}")

        # Faire une requête GET
        response = requests.get(dashboard_url, timeout=10)

        print(f"📊 Statut HTTP: {response.status_code}")

        if response.status_code == 200:
            print("✅ SUCCÈS: La page charge correctement !")

            # Vérifier le contenu de la réponse
            if "Taux conformité" in response.text:
                print("✅ Le contenu 'Taux conformité' est présent")

            if "stats.pourcentage_conformite" in response.text:
                print("❌ ATTENTION: La variable template est visible dans le HTML")
            else:
                print("✅ La variable template est correctement rendue")

            # Vérifier l'absence d'erreurs
            if "TemplateSyntaxError" in response.text:
                print("🚨 ERREUR: TemplateSyntaxError toujours présente !")
                return False
            else:
                print("✅ Aucune TemplateSyntaxError détectée")
                return True

        elif response.status_code == 302:
            print("⚠️  Redirection détectée - Vérifiez la connexion")
            return False
        else:
... (tronqué)

# ============================================================
# ORIGINE 37: verification_agents.py (2025-11-12)
# ============================================================

#!/usr/bin/env python3
"""
Vérification finale de l'application Agents
"""

import os
import sys
from pathlib import Path

def final_check():
    print("🔍 VÉRIFICATION FINALE - APPLICATION AGENTS")
    print("=" * 50)

    project_path = Path(__file__).resolve().parent
    agents_path = project_path / 'agents'

    # Vérification des fichiers modifiés
    print("\n📁 FICHIERS MODIFIÉS:")

    files_to_check = [
        ('views.py', 'Vues agents'),
        ('urls.py', 'URLs agents'),
        ('admin.py', 'Configuration admin')
    ]

    for filename, description in files_to_check:
        file_path = agents_path / filename
        if file_path.exists():
            with open(file_path, 'r') as f:
                content = f.read()
                lines = content.count('\n') + 1
            print(f"  ✅ {description}: {lines} lignes")
        else:
            print(f"  ❌ {description}: Fichier manquant")

    # Vérification des URLs
    print("\n🔗 URLs CONFIGURÉES:")
    urls_file = agents_path / 'urls.py'
    if urls_file.exists():
        with open(urls_file, 'r') as f:
            content = f.read()

        urls = [
            ('dashboard', 'Tableau de bord'),
            ('creer_membre', 'Création membre'),
            ('liste_membres', 'Liste membres'),
            ('creer_bon_soin', 'Création bon soin'),
            ('historique_bons', 'Historique bons')
        ]

... (tronqué)

