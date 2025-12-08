"""
FICHIER CONSOLIDÉ: analyse
Catégorie: diagnostic
Fusion de 36 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: analyse_avancee.py (2025-12-03)
# ============================================================

# analyse_avancee.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Cotisation, Membre
from django.db.models import Count, Sum, Avg, Min, Max
from datetime import datetime

print("="*70)
print("📈 ANALYSE AVANCÉE DU SYSTÈME")
print("="*70)

# 1. Analyse des membres
membres = Membre.objects.all()
print("\n1. 📊 ANALYSE DES MEMBRES")
print("   " + "-"*40)

types_membres = membres.values('type_contrat').annotate(
    count=Count('id'),
    pourcentage=Count('id') * 100.0 / membres.count()
)

for type_m in types_membres:
    type_label = dict(Membre.TYPE_CONTRAT_CHOICES).get(type_m['type_contrat'], type_m['type_contrat'])
    print(f"   {type_label}: {type_m['count']} membres ({type_m['pourcentage']:.1f}%)")

# 2. Analyse des cotisations
cotisations = Cotisation.objects.all()
print("\n2. 💰 ANALYSE DES COTISATIONS")
print("   " + "-"*40)

# Statistiques générales
stats = cotisations.aggregate(
    total=Count('id'),
    somme=Sum('montant'),
    moyenne=Avg('montant'),
    min=Min('montant'),
    max=Max('montant')
)

print(f"   Nombre total: {stats['total']}")
print(f"   Montant total: {stats['somme']:,.0f} FCFA")
print(f"   Moyenne par cotisation: {stats['moyenne']:,.0f} FCFA")
... (tronqué)

# ============================================================
# ORIGINE 2: analyse_existant1.py (2025-12-01)
# ============================================================

#!/usr/bin/env python
"""
ANALYSE DU TEMPLATE ET VUE EXISTANTS
"""
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyser_template_existant():
    """Analyse le template liste_ordonnances.html existant"""
    print("🔍 ANALYSE DU TEMPLATE EXISTANT")
    print("=" * 50)

    template_path = BASE_DIR / 'templates' / 'pharmacien' / 'liste_ordonnances.html'

    if template_path.exists():
        print(f"✅ Template trouvé: {template_path}")

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()

            print("\n📝 CONTENU DU TEMPLATE (premières 50 lignes):")
            print("=" * 40)

            lines = content.split('\n')
            for i, line in enumerate(lines[:50]):
                print(f"{i+1:3d}: {line}")

            # Analyse critique
            print("\n🔍 ANALYSE CRITIQUE:")

            # Vérifier l'extension
            if '{% extends' in content:
                print("✅ Template étend un base")
            else:
                print("❌ Template n'étend pas de base")

            # Vérifier la variable ordonnances
            if 'ordonnances' in content:
                print("✅ Variable 'ordonnances' trouvée")
            else:
                print("❌ Variable 'ordonnances' NON trouvée")

... (tronqué)

# ============================================================
# ORIGINE 3: analyse_template_pharmacien.py (2025-12-01)
# ============================================================

#!/usr/bin/env python
"""
ANALYSE DU TEMPLATE PHARMACIEN EXISTANT
"""
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyser_template_liste_ordonnances():
    """Analyse le template liste_ordonnances.html"""
    print("🔍 ANALYSE TEMPLATE liste_ordonnances.html")
    print("=" * 60)

    template_path = BASE_DIR / 'templates' / 'pharmacien' / 'liste_ordonnances.html'

    if template_path.exists():
        print(f"✅ Template trouvé: {template_path}")

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()

            print("\n📝 CONTENU DU TEMPLATE:")
            print("=" * 40)

            # Afficher les premières lignes
            lines = content.split('\n')
            for i, line in enumerate(lines[:50]):  # Premières 50 lignes
                print(f"{i+1:3d}: {line}")

            # Analyse spécifique
            print("\n🔍 ANALYSE CRITIQUE:")

            # Vérifier la variable de contexte
            if 'ordonnances' in content:
                print("✅ Variable 'ordonnances' trouvée")
            else:
                print("❌ Variable 'ordonnances' NON trouvée")

            # Vérifier la boucle
            if '{% for' in content and 'ordonnance' in content:
                print("✅ Boucle for avec variable 'ordonnance' trouvée")
            else:
                print("❌ Boucle for NON trouvée")
... (tronqué)

# ============================================================
# ORIGINE 4: analyse_templates_pharmacien.py (2025-11-28)
# ============================================================

#!/usr/bin/env python
"""
ANALYSE DES TEMPLATES PHARMACIEN
Vérifie la cohérence entre les modèles et les templates pharmacien
"""

import os
import re
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates" / "pharmacien"

def analyser_template(file_path):
    """Analyse un template HTML pharmacien"""
    print(f"\n📄 Analyse de : {file_path.name}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Recherche des variables Django
        variables = re.findall(r'\{\{\s*([^\s\}]+)\s*\}\}', content)
        urls = re.findall(r'\{\%\s*url\s+[\'\"]([^\'\"]+)[\'\"]', content)

        variables_filtrees = []
        for var in set(variables):
            # Filtrer les variables intéressantes
            if '|' not in var and any(keyword in var for keyword in
                                    ['membre', 'numero', 'date', 'medicament', 'ordonnance', 'stock']):
                variables_filtrees.append(var)

        if variables_filtrees:
            print("   📊 Variables importantes trouvées:")
            for var in sorted(variables_filtrees):
                print(f"      • {var}")

        if urls:
            print("   🌐 URLs trouvées:")
            for url in sorted(set(urls)):
                print(f"      • {url}")

        # Vérification des champs problématiques
        champs_problematiques = {
            'numero_membre': 'Devrait être numero_unique',
            'date_adhesion': 'Devrait être date_inscription',
            'membre.numero_membre': 'Devrait être membre.numero_unique',
            'membre.date_adhesion': 'Devrait être membre.date_inscription'
        }
... (tronqué)

# ============================================================
# ORIGINE 5: analyse_templates_assureur1.py (2025-11-28)
# ============================================================

#!/usr/bin/env python
"""
ANALYSE DES TEMPLATES ASSUREUR
Vérifie la cohérence entre les modèles et les templates assureur
"""

import os
import re
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates" / "assureur"

def analyser_template(file_path):
    """Analyse un template HTML assureur"""
    print(f"\n📄 Analyse de : {file_path.name}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Recherche des variables Django
        variables = re.findall(r'\{\{\s*([^\s\}]+)\s*\}\}', content)
        urls = re.findall(r'\{\%\s*url\s+[\'\"]([^\'\"]+)[\'\"]', content)

        variables_filtrees = []
        for var in set(variables):
            # Filtrer les variables simples (sans filtres) et liées aux membres
            if '|' not in var and ('membre' in var or 'numero' in var or 'date' in var):
                variables_filtrees.append(var)

        if variables_filtrees:
            print("   📊 Variables membres trouvées:")
            for var in sorted(variables_filtrees):
                print(f"      • {var}")

        if urls:
            print("   🌐 URLs trouvées:")
            for url in sorted(set(urls)):
                print(f"      • {url}")

        # Vérification des champs problématiques
        champs_problematiques = {
            'numero_membre': 'Devrait être numero_unique',
            'date_adhesion': 'Devrait être date_inscription',
            'membre.numero_membre': 'Devrait être membre.numero_unique',
            'membre.date_adhesion': 'Devrait être membre.date_inscription'
        }

... (tronqué)

# ============================================================
# ORIGINE 6: analyse_templates.py (2025-11-28)
# ============================================================

#!/usr/bin/env python
"""
ANALYSE DES TEMPLATES MEMBRES
Vérifie la cohérence entre les modèles et les templates
"""

import os
import re
from pathlib import Path

# Configuration - CORRECTION DU CHEMIN
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates" / "membres"

def analyser_template(file_path):
    """Analyse un template HTML"""
    print(f"\n📄 Analyse de : {file_path.name}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Recherche des variables Django
        variables = re.findall(r'\{\{\s*([^\s\}]+)\s*\}\}', content)
        urls = re.findall(r'\{\%\s*url\s+[\'\"]([^\'\"]+)[\'\"]', content)

        if variables:
            print("   📊 Variables trouvées:")
            for var in sorted(set(variables)):
                # Filtrer les variables simples (sans filtres)
                if '|' not in var:
                    print(f"      • {var}")

        if urls:
            print("   🌐 URLs trouvées:")
            for url in sorted(set(urls)):
                print(f"      • {url}")

        # Vérification des champs problématiques
        champs_problematiques = {
            'numero_membre': 'Devrait être numero_unique',
            'date_adhesion': 'Devrait être date_inscription',
            'membre.numero_membre': 'Devrait être membre.numero_unique',
            'membre.date_adhesion': 'Devrait être membre.date_inscription'
        }

        problemes_trouves = False
        for champ, correction in champs_problematiques.items():
            if champ in content:
                if not problemes_trouves:
... (tronqué)

# ============================================================
# ORIGINE 7: analyse_medecin_rapide.py (2025-11-19)
# ============================================================

#!/usr/bin/env python3
import os, sys, re
from pathlib import Path

def quick_analyze():
    project = Path("/Users/koffitanohsoualiho/Documents/sup/projet 21.49.30")
    medecin = project / "medecin"

    print("⚡ ANALYSE RAPIDE MEDECIN")
    print("=" * 40)

    # Structure
    print("📁 Structure:")
    for f in medecin.glob("*.py"):
        print(f"  📄 {f.name}")

    # URLs critiques
    urls_file = medecin / "urls.py"
    if urls_file.exists():
        content = urls_file.read_text()
        print(f"\n🔗 URLs: {len(re.findall(r'path\(', content))}")
        if "views_suivi_chronique" in content:
            print("🚨 URGENT: 'views_suivi_chronique' trouvé dans urls.py")

    # Vues principales
    views_file = medecin / "views.py"
    if views_file.exists():
        content = views_file.read_text()
        views = re.findall(r"def (\w+)\(", content)
        print(f"👁️  Vues: {len(views)}")
        for v in ['dashboard', 'liste_bons', 'mes_rendez_vous']:
            if any(v in view for view in views):
                print(f"  ✅ {v}")
            else:
                print(f"  ❌ {v}")

    # Test final
    try:
        sys.path.insert(0, str(project))
        from medecin import urls, views
        print("✅ Import réussi")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    quick_analyze()

# ============================================================
# ORIGINE 8: analyse_medecin.py (2025-11-19)
# ============================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT D'ANALYSE COMPLÈTE - MODULE MEDECIN
Version Python compatible avec tous les environnements
"""

import os
import sys
import re
import subprocess
from pathlib import Path

class MedecinAnalyzer:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.medecin_dir = self.project_dir / "medecin"
        self.templates_dir = self.medecin_dir / "templates" / "medecin"

    def print_header(self, title):
        print(f"\n{'='*50}")
        print(f"🔍 {title}")
        print(f"{'='*50}")

    def analyze_structure(self):
        """Analyse la structure du module medecin"""
        self.print_header("STRUCTURE DU MODULE MEDECIN")

        if not self.medecin_dir.exists():
            print("❌ Dossier medecin introuvable")
            return False

        print("✅ Dossier medecin trouvé")
        print("\n📁 Structure:")
        for item in self.medecin_dir.rglob("*"):
            if "__pycache__" not in str(item) and not item.name.endswith(".pyc"):
                rel_path = item.relative_to(self.medecin_dir)
                prefix = "  " * (len(rel_path.parents) - 1)
                if item.is_dir():
                    print(f"{prefix}📁 {rel_path}/")
                else:
                    print(f"{prefix}📄 {rel_path}")
        return True

    def analyze_models(self):
        """Analyse le fichier models.py"""
        self.print_header("ANALYSE DES MODÈLES")

        models_file = self.medecin_dir / "models.py"
        if not models_file.exists():
... (tronqué)

# ============================================================
# ORIGINE 9: analyse_projet2.py (2025-11-19)
# ============================================================

#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE DU PROJET MUTUELLE_CORE
Analyse complète de la configuration et de l'architecture du projet
"""

import os
import sys
from pathlib import Path

def analyse_architecture():
    """Analyse l'architecture globale du projet"""
    print("=" * 80)
    print("ANALYSE ARCHITECTURALE DU PROJET MUTUELLE_CORE")
    print("=" * 80)

    architecture = {
        "Type": "Application Django de gestion de mutuelle santé",
        "Architecture": "MVC (Model-View-Controller) avec API REST",
        "Base de données": "SQLite (développement) - à migrer en production",
        "Authentification": "JWT + Sessions Django",
        "Interface": "Templates Django + API REST",
        "Communication temps réel": "WebSocket avec Django Channels"
    }

    for key, value in architecture.items():
        print(f"• {key}: {value}")

def analyse_applications():
    """Analyse des applications Django installées"""
    print("\n" + "=" * 80)
    print("ANALYSE DES APPLICATIONS")
    print("=" * 80)

    applications = {
        "Applications coeur": ["core", "mutuelle_core", "api"],
        "Gestion des membres": ["membres", "inscription"],
        "Gestion financière": ["paiements"],
        "Gestion des soins": ["soins"],
        "Acteurs métier": ["assureur", "medecin", "pharmacien", "agents"],
        "Communication": ["notifications", "communication"],
        "Services publics": ["pharmacie_public"],
        "Applications tierces": [
            "rest_framework", "rest_framework_simplejwt", "corsheaders",
            "crispy_forms", "channels", "django_extensions"
        ]
    }

    for categorie, apps in applications.items():
        print(f"\n📁 {categorie.upper()}:")
... (tronqué)

# ============================================================
# ORIGINE 10: analyse_dependances.py (2025-11-19)
# ============================================================

#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE DES DÉPENDANCES
Analyse les dépendances et packages requis
"""

def analyse_dependances():
    """Analyse des dépendances du projet"""
    print("=" * 80)
    print("ANALYSE DES DÉPENDANCES")
    print("=" * 80)

    dependances_principales = {
        "Django": "Framework web principal",
        "Django REST Framework": "API REST",
        "djangorestframework-simplejwt": "Authentification JWT",
        "django-cors-headers": "Gestion CORS",
        "django-crispy-forms": "Formulaires Bootstrap",
        "crispy-bootstrap5": "Template Bootstrap 5",
        "django-channels": "WebSockets",
        "python-dotenv": "Variables d'environnement",
        "django-extensions": "Outils de développement"
    }

    print("\n📦 DÉPENDANCES PRINCIPALES:")
    for package, description in dependances_principales.items():
        print(f"   • {package}: {description}")

    print("\n🔧 CONFIGURATION REQUISE:")
    configurations = [
        "Python 3.8+",
        "Django 4.x+",
        "Base de données SQLite/PostgreSQL",
        "Serveur ASGI pour WebSockets",
        "Redis (recommandé en production)"
    ]

    for config in configurations:
        print(f"   ✓ {config}")

if __name__ == "__main__":
    analyse_dependances()

# ============================================================
# ORIGINE 11: analyse_projet1.py (2025-11-19)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT D'ANALYSE COMPLÈTE DU PROJET DJANGO
Analyse la structure, les dépendances, les performances et la qualité du code
"""

import os
import sys
import ast
import glob
import json
import datetime
from pathlib import Path
from collections import defaultdict, Counter
import subprocess
import platform

class DjangoProjectAnalyzer:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.analysis_results = {
            'timestamp': datetime.datetime.now().isoformat(),
            'project_info': {},
            'apps_analysis': {},
            'models_analysis': {},
            'views_analysis': {},
            'urls_analysis': {},
            'templates_analysis': {},
            'static_analysis': {},
            'security_analysis': {},
            'performance_analysis': {},
            'agents_module_analysis': {},
            'issues': [],
            'recommendations': []
        }

    def analyze_project_structure(self):
        """Analyse la structure globale du projet"""
        print("🔍 Analyse de la structure du projet...")

        project_info = {
            'project_name': self.project_path.name,
            'total_size': self.get_directory_size(self.project_path),
            'python_files': 0,
            'template_files': 0,
            'static_files': 0,
            'database_files': 0,
            'migration_files': 0
        }

... (tronqué)

# ============================================================
# ORIGINE 12: analyse_configuration_communication1.py (2025-11-19)
# ============================================================

# analyse_configuration_communication.py
import os
import django
import sys

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.conf import settings
import os

class AnalyseurConfigurationCommunication:
    """
    Script pour analyser et corriger la configuration de la communication
    dans les applications agents et assureur
    """

    def __init__(self):
        self.results = {
            'success': [],
            'warnings': [],
            'errors': []
        }

    def log_success(self, message):
        self.results['success'].append(message)
        print(f"✅ {message}")

    def log_warning(self, message):
        self.results['warnings'].append(message)
        print(f"⚠️ {message}")

    def log_error(self, message):
        self.results['errors'].append(message)
        print(f"❌ {message}")

    def analyser_installation_apps(self):
        """Analyser l'installation des applications dans settings.py"""
        print("🔍 ANALYSE DE LA CONFIGURATION DJANGO")
        print("="*50)

        # Vérifier si communication est dans INSTALLED_APPS
        installed_apps = getattr(settings, 'INSTALLED_APPS', [])

        apps_requises = ['communication', 'agents', 'assureur']

        for app in apps_requises:
            if app in installed_apps:
... (tronqué)

# ============================================================
# ORIGINE 13: analyse_probleme.py (2025-11-19)
# ============================================================

#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE - Diagnostic complet de l'erreur Django Template
Analyse : Could not parse some characters: |((stats.membres_a_jour / stats.membres_actifs) * 100)||floatformat:0
"""

import os
import re
import sys
from pathlib import Path

class TemplateAnalyzer:
    def __init__(self):
        self.problems = []
        self.template_files = []

    def analyze_project_structure(self):
        """Analyse la structure du projet"""
        print("📁 ANALYSE DE LA STRUCTURE DU PROJET")
        print("=" * 50)

        # Vérifier la structure des dossiers
        required_dirs = [
            'agents',
            'agents/templates',
            'agents/templates/agents',
            'templates'
        ]

        for dir_path in required_dirs:
            if os.path.exists(dir_path):
                print(f"✅ {dir_path}/")
            else:
                print(f"❌ {dir_path}/ - MANQUANT")
                self.problems.append(f"Dossier manquant: {dir_path}")

    def find_template_files(self):
        """Trouve tous les fichiers templates"""
        print("\n🔍 RECHERCHE DES FICHIERS TEMPLATES")
        print("=" * 50)

        patterns = [
            '**/*.html',
            '**/templates/**/*.html',
            'agents/**/*.html'
        ]

        for pattern in patterns:
            for file_path in Path('.').glob(pattern):
                if file_path.is_file():
... (tronqué)

# ============================================================
# ORIGINE 14: analyse_projet.py (2025-11-19)
# ============================================================

#!/usr/bin/env python3
"""
Script d'analyse complète du projet Django Mutuelle
Analyse la structure, les dépendances, la configuration et les éventuels problèmes
"""

import os
import sys
import ast
import importlib
from pathlib import Path
from django.conf import settings
from django.core.management import execute_from_command_line
import django
from datetime import datetime

class ProjectAnalyzer:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.analysis_results = {
            'errors': [],
            'warnings': [],
            'info': [],
            'recommendations': []
        }

    def setup_django(self):
        """Configure Django pour l'analyse"""
        try:
            sys.path.insert(0, str(self.project_path))
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
            django.setup()
            return True
        except Exception as e:
            self.analysis_results['errors'].append(f"Erreur configuration Django: {e}")
            return False

    def analyze_project_structure(self):
        """Analyse la structure du projet"""
        print("🔍 Analyse de la structure du projet...")

        required_dirs = [
            'templates',
            'static',
            'media',
            'logs',
            'agents/templates',
            'agents/static'
        ]

... (tronqué)

# ============================================================
# ORIGINE 15: analyse_configuration_communication.py (2025-11-19)
# ============================================================

# analyse_configuration_communication.py
import os
import django
import sys

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.conf import settings
import os

class AnalyseurConfigurationCommunication:
    """
    Script pour analyser et corriger la configuration de la communication
    dans les applications agents et assureur
    """

    def __init__(self):
        self.results = {
            'success': [],
            'warnings': [],
            'errors': []
        }

    def log_success(self, message):
        self.results['success'].append(message)
        print(f"✅ {message}")

    def log_warning(self, message):
        self.results['warnings'].append(message)
        print(f"⚠️ {message}")

    def log_error(self, message):
        self.results['errors'].append(message)
        print(f"❌ {message}")

    def analyser_installation_apps(self):
        """Analyser l'installation des applications dans settings.py"""
        print("🔍 ANALYSE DE LA CONFIGURATION DJANGO")
        print("=" * 50)

        # Vérifier si communication est dans INSTALLED_APPS
        installed_apps = getattr(settings, 'INSTALLED_APPS', [])

        apps_requises = ['communication', 'agents', 'assureur']

        for app in apps_requises:
            if app in installed_apps:
... (tronqué)

# ============================================================
# ORIGINE 16: analyse_assureur_final.py (2025-11-18)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT D'ANALYSE FINAL - APPLICATION ASSUREUR
Version finale avec toutes les corrections
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré avec succès")
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def verification_globale():
    """Vérification globale et finale"""
    print("\n" + "="*80)
    print("🎯 VÉRIFICATION GLOBALE ASSUREUR - RAPPORT FINAL")
    print("="*80)

    # 1. Vérification des modèles
    print("\n📊 1. MODÈLES:")
    try:
        from assureur.models import Membre, Bon, Paiement, Cotisation, Assureur, ConfigurationAssurance
        modeles = [Membre, Bon, Paiement, Cotisation, Assureur, ConfigurationAssurance]
        print(f"   ✅ {len(modeles)} modèles importés avec succès")

        # Compter les instances
        for modele in modeles:
            count = modele.objects.count()
            print(f"      - {modele.__name__}: {count} instances")

    except Exception as e:
        print(f"   ❌ Erreur modèles: {e}")

    # 2. Vérification des vues
    print("\n👁️ 2. VUES:")
    try:
        from assureur.views import dashboard_assureur, liste_cotisations, liste_membres, liste_bons
        vues_importees = [dashboard_assureur, liste_cotisations, liste_membres, liste_bons]
        print(f"   ✅ {len(vues_importees)} vues principales importées")
... (tronqué)

# ============================================================
# ORIGINE 17: analyse_assureur3.py (2025-11-18)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT D'ANALYSE COMPLÈTE - APPLICATION ASSUREUR
Vérifie les modèles, vues, formulaires, templates et URLs
"""

import os
import sys
import django
from pathlib import Path
from django.apps import apps
from django.conf import settings
from django.core.checks import run_checks
from django.core.management import execute_from_command_line
from django.db import connection
from django.test import TestCase
import ast
import inspect

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def analyse_modeles_assureur():
    """Analyse complète des modèles de l'application assureur"""
    print("\n" + "="*80)
    print("📊 ANALYSE DES MODÈLES ASSUREUR")
    print("="*80)

    try:
        from assureur.models import (
            Membre, Bon, Soin, Paiement, Assureur,
            Cotisation, ConfigurationAssurance, StatistiquesAssurance
        )

        modeles = [Membre, Bon, Soin, Paiement, Assureur, Cotisation, ConfigurationAssurance]

        for modele in modeles:
            print(f"\n🔍 Analyse du modèle: {modele.__name__}")
            print(f"   - Table: {modele._meta.db_table}")
            print(f"   - Champs: {len(modele._meta.fields)}")
            print(f"   - Relations: {len(modele._meta.related_objects)}")

... (tronqué)

# ============================================================
# ORIGINE 18: analyse_existant_complet.py (2025-11-18)
# ============================================================

# analyse_existant_complet.py
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre, Cotisation
from django.db import models

def analyser_modeles_complet():
    """Analyse complète des modèles"""
    print("=== ANALYSE COMPLÈTE DES MODÈLES ===")

    # Modèle Membre
    print("\n📊 MODÈLE MEMBRE:")
    for field in Membre._meta.get_fields():
        if field.is_relation:
            print(f"  - {field.name}: {field.get_internal_type()} -> {field.related_model.__name__}")
        else:
            print(f"  - {field.name}: {field.get_internal_type()}")

    # Modèle Cotisation
    print("\n📊 MODÈLE COTISATION:")
    for field in Cotisation._meta.get_fields():
        if field.is_relation:
            print(f"  - {field.name}: {field.get_internal_type()} -> {field.related_model.__name__}")
        else:
            print(f"  - {field.name}: {field.get_internal_type()}")

def analyser_donnees_complet():
    """Analyse complète des données existantes"""
    print("\n=== ANALYSE DES DONNÉES EXISTANTES ===")

    total_membres = Membre.objects.count()
    total_cotisations = Cotisation.objects.count()

    print(f"Nombre total de membres: {total_membres}")
    print(f"Nombre total de cotisations: {total_cotisations}")

    # Statistiques détaillées sur les membres
    if total_membres > 0:
        membres_avec_avance = Membre.objects.filter(avance_payee__gt=0).count()
        membres_avec_carte = Membre.objects.filter(carte_adhesion_payee__gt=0).count()
        femmes_enceintes = Membre.objects.filter(est_femme_enceinte=True).count()

        print(f"\n📈 Statistiques détaillées:")
        print(f"  - Membres avec avance payée: {membres_avec_avance}")
... (tronqué)

# ============================================================
# ORIGINE 19: analyse_existant.py (2025-11-18)
# ============================================================

# analyse_existant.py
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre, Cotisation
from django.db import models

def analyser_modeles():
    """Analyse les modèles existants"""
    print("=== ANALYSE DES MODÈLES ===")

    # Analyse du modèle Membre
    membre_fields = Membre._meta.get_fields()
    print("\n📊 Champs du modèle Membre:")
    for field in membre_fields:
        print(f"  - {field.name}: {field.get_internal_type()}")

    # Analyse du modèle Cotisation
    cotisation_fields = Cotisation._meta.get_fields()
    print("\n📊 Champs du modèle Cotisation:")
    for field in cotisation_fields:
        print(f"  - {field.name}: {field.get_internal_type()}")

def analyser_donnees():
    """Analyse les données existantes"""
    print("\n=== ANALYSE DES DONNÉES ===")

    total_membres = Membre.objects.count()
    total_cotisations = Cotisation.objects.count()

    print(f"Nombre total de membres: {total_membres}")
    print(f"Nombre total de cotisations: {total_cotisations}")

    # Statistiques sur les membres
    if total_membres > 0:
        membres_avec_avance = Membre.objects.filter(avance_payee__gt=0).count()
        membres_avec_carte = Membre.objects.filter(carte_adhesion_payee__gt=0).count()

        print(f"Membres avec avance payée: {membres_avec_avance}")
        print(f"Membres avec carte payée: {membres_avec_carte}")

        # Aperçu des 5 premiers membres
        print("\n👥 Aperçu des membres:")
        for membre in Membre.objects.all()[:5]:
... (tronqué)

# ============================================================
# ORIGINE 20: analyse_rapide1.py (2025-11-17)
# ============================================================

# analyse_rapide.py
import os
import django
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyse_rapide():
    print("🔍 ANALYSE RAPIDE DE L'EXISTANT")
    print("=" * 50)

    # Vérification des modèles clés
    modeles = ['Membre', 'Cotisation', 'Paiement', 'Bon', 'Soin']

    for modele in modeles:
        try:
            obj = apps.get_model('assureur', modele)
            count = obj.objects.count()
            print(f"✅ {modele}: {count} enregistrements")
        except:
            print(f"❌ {modele}: Modèle non trouvé")

    # Vérification Membre détaillée
    try:
        Membre = apps.get_model('assureur', 'Membre')
        if Membre.objects.exists():
            membre = Membre.objects.first()
            print(f"\n📋 EXEMPLE MEMBRE:")
            print(f"   • Nom: {membre.nom} {membre.prenom}")
            print(f"   • Contrat: {membre.type_contrat}")
            print(f"   • Couverture: {membre.taux_couverture}%")
            print(f"   • Statut: {membre.statut}")
    except:
        pass

if __name__ == "__main__":
    analyse_rapide()

# ============================================================
# ORIGINE 21: analyse_cotisations_existant.py (2025-11-17)
# ============================================================

# analyse_cotisations_existant.py
import os
import sys
import django
from django.db import models
from django.apps import apps
from datetime import datetime, timedelta
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyser_modeles_existants():
    """Analyse les modèles existants dans la base de données"""
    print("=" * 80)
    print("🔍 ANALYSE DES MODÈLES EXISTANTS")
    print("=" * 80)

    modeles_pertinents = [
        'Membre', 'Cotisation', 'Paiement', 'Bon', 'Soin',
        'Assureur', 'Agent', 'VerificationCotisation'
    ]

    for modele_name in modeles_pertinents:
        try:
            modele = apps.get_model('assureur', modele_name)
            print(f"\n📊 MODÈLE: {modele_name}")
            print(f"   📍 Application: {modele._meta.app_label}")
            print(f"   📋 Champs:")

            for champ in modele._meta.get_fields():
                if hasattr(champ, 'name'):
                    type_champ = champ.get_internal_type()
                    print(f"      • {champ.name} ({type_champ})")

        except LookupError:
            print(f"\n❌ MODÈLE: {modele_name} - NON TROUVÉ")

def analyser_membres_existants():
    """Analyse les membres existants et leurs données"""
    print("\n" + "=" * 80)
    print("👥 ANALYSE DES MEMBRES EXISTANTS")
    print("=" * 80)

    try:
        Membre = apps.get_model('assureur', 'Membre')
        total_membres = Membre.objects.count()

        print(f"📈 Total membres: {total_membres}")
... (tronqué)

# ============================================================
# ORIGINE 22: analyse_assureur1.py (2025-11-17)
# ============================================================

#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE ASSUREUR - VERSION FINALE CORRIGÉE
"""

import os
import sys
import django
from pathlib import Path

# Configuration CORRIGÉE
BASE_DIR = Path(__file__).resolve().parent  # Maintenant correct pour votre structure
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()

    from django.urls import reverse, NoReverseMatch
    from django.apps import apps

    print("🔍 ANALYSE COMPLÈTE ASSUREUR - TOUT EST FONCTIONNEL!")
    print("=" * 55)

    # Vérification URLs critiques
    urls_critiques = [
        ('assureur:liste_messages', {}),
        ('assureur:envoyer_message', {}),
        ('assureur:repondre_message', {'message_id': 1}),
        ('assureur:liste_notifications', {}),
        ('assureur:dashboard', {}),
        ('assureur:liste_bons', {}),
        ('assureur:liste_membres', {}),
        ('assureur:liste_paiements', {})
    ]

    print("\n🔗 URLs CRITIQUES:")
    urls_ok = 0
    for url_name, kwargs in urls_critiques:
        try:
            url = reverse(url_name, kwargs=kwargs)
            print(f"   ✅ {url_name} -> {url}")
            urls_ok += 1
        except NoReverseMatch as e:
            print(f"   ❌ {url_name} - ERREUR: {e}")

    # Vérification modèles
    print("\n🗄️ MODÈLES ASSUREUR:")
    try:
        modeles = [model for model in apps.get_models()
... (tronqué)

# ============================================================
# ORIGINE 23: analyse_assureur.py (2025-11-17)
# ============================================================

#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE ASSUREUR - Diagnostic complet de l'application
Usage: python analyse_assureur.py
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
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

# =============================================================================
# IMPORTS APRÈS CONFIGURATION DJANGO
# =============================================================================
from django.urls import reverse, NoReverseMatch, get_resolver
from django.apps import apps
from django.db import connection
from django.core.checks import run_checks
import inspect
from collections import defaultdict

class AnalyseurAssureur:
    """Classe pour analyser l'application assureur"""

    def __init__(self):
        self.resultats = {
            'erreurs': [],
            'avertissements': [],
            'succes': [],
            'statistiques': defaultdict(int)
        }
        self.app_config = apps.get_app_config('assureur')

    def analyser_structure(self):
        """Analyse la structure de l'application"""
        print("\n" + "="*60)
        print("📁 ANALYSE STRUCTURELLE")
        print("="*60)

... (tronqué)

# ============================================================
# ORIGINE 24: analyse_configuration_communication2.py (2025-11-15)
# ============================================================

# analyse_configuration_communication.py
import os
import django
import sys

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.conf import settings
import os

class AnalyseurConfigurationCommunication:
    """
    Script pour analyser et corriger la configuration de la communication
    dans les applications agents et assureur
    """

    def __init__(self):
        self.results = {
            'success': [],
            'warnings': [],
            'errors': []
        }

    def log_success(self, message):
        self.results['success'].append(message)
        print(f"✅ {message}")

    def log_warning(self, message):
        self.results['warnings'].append(message)
        print(f"⚠️ {message}")

    def log_error(self, message):
        self.results['errors'].append(message)
        print(f"❌ {message}")

    def analyser_installation_apps(self):
        """Analyser l'installation des applications dans settings.py"""
        print("🔍 ANALYSE DE LA CONFIGURATION DJANGO")
        print("=" * 50)  # CORRECTION: Parenthèse fermante correcte

        # Vérifier si communication est dans INSTALLED_APPS
        installed_apps = getattr(settings, 'INSTALLED_APPS', [])

        apps_requises = ['communication', 'agents', 'assureur']

        for app in apps_requises:
            if app in installed_apps:
... (tronqué)

# ============================================================
# ORIGINE 25: analyse_communication_finale.py (2025-11-15)
# ============================================================

# analyse_communication_corrigee.py
import os
import django
import sys
from datetime import datetime, timedelta

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction
from django.apps import apps

User = get_user_model()

class AnalyseurCommunicationCorrige:
    """
    Script d'analyse du système de communication - Version corrigée
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

    def detecter_modeles_communication(self):
        """Détecter les modèles liés à la communication"""
        print("🔍 Détection des modèles de communication...")

        modeles_communication = [
            'Notification', 'Message', 'Conversation', 'MessageGroupe',
            'GroupeCommunication', 'PieceJointe', 'PreferenceNotification'
        ]
... (tronqué)

# ============================================================
# ORIGINE 26: analyse_communication.py (2025-11-15)
# ============================================================

# analyse_communication.py
import os
import django
import sys
from datetime import datetime, timedelta

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction
from django.apps import apps

User = get_user_model()

class AnalyseurCommunication:
    """
    Script d'analyse du système de communication entre les acteurs
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

    def detecter_modeles_communication(self):
        """Détecter les modèles liés à la communication"""
        print("🔍 Détection des modèles de communication...")

        modeles_communication = [
            'Notification', 'Message', 'Conversation', 'MessageGroupe',
            'GroupeCommunication', 'PieceJointe', 'PreferenceNotification'
        ]
... (tronqué)

# ============================================================
# ORIGINE 27: analyse_complete_projet.py (2025-11-14)
# ============================================================

# analyse_complete_projet.py

import os
import sys
import django
import subprocess
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.core.management import call_command
from django.urls import get_resolver, reverse, NoReverseMatch
from django.template.loader import get_template
import importlib
import inspect

class AnalyseCompleteProjet:
    def __init__(self):
        self.resultats = {
            'applications': {},
            'modeles': {},
            'vues': {},
            'urls': {},
            'templates': {},
            'permissions': {},
            'donnees': {},
            'problemes': [],
            'recommandations': []
        }

    def executer_analyse_complete(self):
        """Exécute l'analyse complète du projet"""
        print("🚀 ANALYSE COMPLÈTE DU PROJET DJANGO")
        print("=" * 70)
        print()

        self.analyser_structure_projet()
        self.analyser_applications()
        self.analyser_modeles()
        self.analyser_vues()
        self.analyser_urls()
        self.analyser_templates()
        self.analyser_permissions()
... (tronqué)

# ============================================================
# ORIGINE 28: analyse_post_implementation.py (2025-11-14)
# ============================================================

# analyse_post_implementation.py

import os
import sys
import django
from django.apps import apps
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, Group
from django.core.management import call_command

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

class AnalysePostImplementation:
    def __init__(self):
        self.resultats = {}
        self.erreurs = []

    def executer_analyse_complete(self):
        print("🚀 ANALYSE POST-IMPLÉMENTATION - CRÉATION MEMBRES PAR AGENTS")
        print("=" * 70)
        print()

        self.verifier_formulaires()
        self.verifier_vues()
        self.verifier_urls()
        self.verifier_templates()
        self.verifier_permissions()
        self.tester_fonctionnalites()
        self.analyser_donnees_test()
        self.generer_rapport_final()

    def verifier_formulaires(self):
        print("📝 1. VÉRIFICATION DES FORMULAIRES")
        print("-" * 40)

        try:
            from membres.forms import MembreCreationForm, MembreDocumentForm

            # Test MembreCreationForm
            form_creation = MembreCreationForm()
            champs_attendus = ['username', 'password', 'email', 'nom', 'prenom', 'telephone']
            champs_trouves = [field.name for field in form_creation]

            print("   ✅ MembreCreationForm importé avec succès")
            print(f"   📋 Champs trouvés: {len(champs_trouves)}")

... (tronqué)

# ============================================================
# ORIGINE 29: analyse_creation_membres1.py (2025-11-14)
# ============================================================

#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE DE L'EXISTANT - Création de membres par les agents
Version corrigée
"""

import os
import sys
import django
from pathlib import Path
import logging

# Configuration Django
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.db import models
from django.contrib.auth.models import User, Group
from membres.models import Membre, Profile
from agents.models import Agent
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class AnalyseMembreCreation:
    """Classe d'analyse complète pour la création de membres par les agents"""

    def __init__(self):
        self.analyse_resultats = {}
        self.problemes = []
        self.recommandations = []

    def analyser_structure_actuelle(self):
        """Analyse la structure actuelle des modèles"""
        print("🔍 ANALYSE DE LA STRUCTURE ACTUELLE")
        print("=" * 60)

        # 1. Analyse du modèle Membre
        self.analyser_modele_membre()

        # 2. Analyse du modèle Agent
        self.analyser_modele_agent()

        # 3. Analyse des relations
        self.analyser_relations()

... (tronqué)

# ============================================================
# ORIGINE 30: analyse_creation_membres.py (2025-11-14)
# ============================================================

#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE DE L'EXISTANT - Création de membres par les agents
Analyse complète de la structure actuelle et plan d'implémentation
"""

import os
import sys
import django
from pathlib import Path
import inspect

# Configuration Django
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.db import models
from django.contrib.auth.models import User, Group
from membres.models import Membre, Profile
from agents.models import Agent
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class AnalyseMembreCreation:
    """Classe d'analyse complète pour la création de membres par les agents"""

    def __init__(self):
        self.analyse_resultats = {}
        self.problemes = []
        self.recommandations = []

    def analyser_structure_actuelle(self):
        """Analyse la structure actuelle des modèles"""
        print("🔍 ANALYSE DE LA STRUCTURE ACTUELLE")
        print("=" * 60)

        # 1. Analyse du modèle Membre
        self.analyser_modele_membre()

        # 2. Analyse du modèle Agent
        self.analyser_modele_agent()

        # 3. Analyse des relations
        self.analyser_relations()

... (tronqué)

# ============================================================
# ORIGINE 31: analyse_templates_assureur.py (2025-11-14)
# ============================================================

# analyse_templates_assureur.py
import os
import sys
import re
from pathlib import Path
import django
from django.conf import settings

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyser_templates_assureur():
    """
    Script d'analyse complet des templates de l'application assureur
    """
    print("🔍 ANALYSE DES TEMPLATES ASSUREUR")
    print("=" * 80)

    # 1. LOCALISATION DES TEMPLATES
    print("\n1. 📁 LOCALISATION DES TEMPLATES ASSUREUR")

    templates_dirs = []
    for template_config in settings.TEMPLATES:
        if 'DIRS' in template_config:
            templates_dirs.extend(template_config['DIRS'])

    # Dossiers spécifiques à vérifier
    dossiers_assureur = [
        BASE_DIR / 'assureur' / 'templates' / 'assureur',
        BASE_DIR / 'templates' / 'assureur',
    ]

    templates_trouves = []
    for dossier in dossiers_assureur:
        if dossier.exists():
            print(f"✅ Dossier trouvé: {dossier}")
            for file_path in dossier.rglob("*.html"):
                templates_trouves.append(file_path)
        else:
            print(f"❌ Dossier non trouvé: {dossier}")

    print(f"\n📊 {len(templates_trouves)} templates assureur trouvés")

    # 2. ANALYSE DÉTAILLÉE DE CHAQUE TEMPLATE
    print("\n2. 📋 ANALYSE DÉTAILLÉE DES TEMPLATES")

    stats = {
... (tronqué)

# ============================================================
# ORIGINE 32: analyse_urgence.py (2025-11-12)
# ============================================================

#!/usr/bin/env python3
"""
ANALYSE URGENTE - Problème de chemin et vérification complète
"""

import os
import re
import sys

def analyse_urgence():
    print("🔍 ANALYSE URGENTE - Problème de chemin détecté")
    print("=" * 60)

    # 1. Vérifier la structure exacte
    print("📁 STRUCTURE DES DOSSIERS:")
    for root, dirs, files in os.walk('.'):
        if 'dashboard.html' in files:
            print(f"✅ dashboard.html trouvé dans: {root}/")
        if 'agents' in dirs:
            print(f"✅ Dossier agents trouvé dans: {root}/")

    # 2. Vérifier le template spécifique
    template_path = 'templates/agents/dashboard.html'
    print(f"\n🎯 ANALYSE DU TEMPLATE: {template_path}")

    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print("✅ Template existe - Analyse du contenu...")

        # Rechercher TOUTES les occurrences du calcul de pourcentage
        patterns = [
            (r'stats\.membres_a_jour', "Référence à membres_a_jour"),
            (r'stats\.membres_actifs', "Référence à membres_actifs"),
            (r'pourcentage_conformite', "Référence à pourcentage_conformite"),
            (r'\|\s*\(\(.*\*.*100\)', "Calcul avec multiplication"),
            (r'\|\|', "Double pipe"),
            (r'\{\{\s*\|', "Pipe au début d'expression"),
        ]

        print("\n🔎 PATTERNS TROUVÉS DANS LE TEMPLATE:")
        for pattern, description in patterns:
            matches = list(re.finditer(pattern, content))
            if matches:
                print(f"📌 {description}: {len(matches)} occurrence(s)")
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    context_start = max(0, match.start() - 30)
                    context_end = min(len(content), match.end() + 30)
... (tronqué)

# ============================================================
# ORIGINE 33: analyse_agents_rapide.py (2025-11-12)
# ============================================================

#!/usr/bin/env python3
"""
Analyse rapide de l'application Agents
"""

import os
import sys
from pathlib import Path

def quick_agents_analysis():
    project_path = Path(__file__).resolve().parent
    agents_path = project_path / 'agents'

    print("🔍 ANALYSE RAPIDE - APPLICATION AGENTS")
    print("=" * 50)

    # Structure de base
    print("\n📁 STRUCTURE:")
    files = ['models.py', 'views.py', 'urls.py', 'admin.py', 'apps.py']
    for file in files:
        if (agents_path / file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")

    # Templates
    print("\n🎨 TEMPLATES:")
    templates_path = project_path / 'templates' / 'agents'
    if templates_path.exists():
        templates = list(templates_path.glob('*.html'))
        print(f"  ✅ {len(templates)} templates trouvés")

        critical_templates = ['base_agent.html', 'dashboard.html']
        for template in critical_templates:
            if (templates_path / template).exists():
                print(f"    ✅ {template}")
            else:
                print(f"    ❌ {template}")
    else:
        print("  ❌ Dossier templates/agents introuvable")

    # URLs
    print("\n🔗 URLs:")
    main_urls = project_path / 'mutuelle_core' / 'urls.py'
    if main_urls.exists():
        with open(main_urls, 'r') as f:
            content = f.read()
        if 'agents.urls' in content:
            print("  ✅ Inclus dans URLs principales")
        else:
... (tronqué)

# ============================================================
# ORIGINE 34: analyse_agents.py (2025-11-12)
# ============================================================

#!/usr/bin/env python3
"""
Script d'analyse approfondie de l'application Agents
"""

import os
import sys
import ast
import inspect
from pathlib import Path
from datetime import datetime
import django
from django.conf import settings

# Configuration Django
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

# Import des modèles après configuration Django
from django.apps import apps
from django.db import models
from django.core.management import call_command
from io import StringIO

class AgentsAnalyzer:
    def __init__(self):
        self.project_path = Path(__file__).resolve().parent
        self.agents_path = self.project_path / 'agents'
        self.results = {
            'critical': [],
            'errors': [],
            'warnings': [],
            'info': [],
            'success': []
        }

    def log(self, level, message):
        """Journalise un message avec niveau"""
        self.results[level].append(message)
        print(f"{self.get_emoji(level)} {message}")

    def get_emoji(self, level):
        """Retourne l'emoji correspondant au niveau"""
        emojis = {
            'critical': '🚨',
            'errors': '❌',
            'warnings': '⚠️',
            'info': 'ℹ️',
            'success': '✅'
... (tronqué)

# ============================================================
# ORIGINE 35: analyse_rapport_20251112_083706.txt (2025-11-12)
# ============================================================

RAPPORT D'ANALYSE - PROJET MUTUELLE
==================================================

Erreurs: 0
Avertissements: 7
Informations: 61


ERRORS:

WARNINGS:
  • ⚠️ Répertoire manquant: agents/templates
  • ⚠️ DEBUG est activé - désactiver en production
  • ⚠️ Package manquant: Django
  • ⚠️ Package manquant: django-rest-framework
  • ⚠️ Package manquant: django-cors-headers
  • ⚠️ Package manquant: django-crispy-forms
  • ⚠️ Package manquant: python-dotenv

INFO:
  • ✅ Répertoire trouvé: templates
  • ✅ Répertoire trouvé: static
  • ✅ Répertoire trouvé: media
  • ✅ Répertoire trouvé: logs
  • ✅ Répertoire trouvé: agents/static
  • ✅ Fichier trouvé: manage.py
  • ✅ Fichier trouvé: mutuelle_core/__init__.py
  • ✅ Fichier trouvé: mutuelle_core/settings.py
  • ✅ Fichier trouvé: mutuelle_core/urls.py
  • ✅ Fichier trouvé: mutuelle_core/wsgi.py
  • ✅ Fichier trouvé: agents/__init__.py
  • ✅ Fichier trouvé: agents/models.py
  • ✅ Fichier trouvé: agents/views.py
  • ✅ Fichier trouvé: agents/urls.py
  • ✅ SECRET_KEY configuré
  • ✅ DEBUG configuré
  • ✅ ALLOWED_HOSTS configuré
  • ✅ DATABASES configuré
  • ✅ INSTALLED_APPS configuré
  • ✅ Application installée: membres
  • ✅ Application installée: inscription
  • ✅ Application installée: paiements
  • ✅ Application installée: soins
  • ✅ Application installée: notifications
  • ✅ Application installée: api
  • ✅ Application installée: assureur
  • ✅ Application installée: medecin
  • ✅ Application installée: pharmacien
  • ✅ Application installée: core
  • ✅ Application installée: mutuelle_core
... (tronqué)

# ============================================================
# ORIGINE 36: analyse_rapide.py (2025-11-12)
# ============================================================

#!/usr/bin/env python3
"""
Script d'analyse rapide du projet
"""

import os
import sys
from pathlib import Path

def quick_analysis():
    project_path = Path(__file__).resolve().parent

    print("🔍 Analyse rapide du projet...")

    # Vérifications basiques
    checks = [
        ("manage.py", "Fichier manage.py"),
        ("mutuelle_core/settings.py", "Fichier settings.py"),
        ("agents/models.py", "Modèles agents"),
        ("requirements.txt", "Dépendances"),
        (".env", "Variables d'environnement"),
    ]

    for file_path, description in checks:
        if (project_path / file_path).exists():
            print(f"✅ {description} - OK")
        else:
            print(f"❌ {description} - MANQUANT")

    # Vérification structure dossiers
    folders = ['static', 'media', 'templates', 'logs']
    for folder in folders:
        folder_path = project_path / folder
        if folder_path.exists():
            print(f"✅ Dossier {folder} - OK")
        else:
            print(f"⚠️  Dossier {folder} - MANQUANT")

if __name__ == "__main__":
    quick_analysis()

