"""
FICHIER CONSOLIDÉ: analyser
Catégorie: diagnostic
Fusion de 4 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: analyser_structure_agent.py (2025-11-30)
# ============================================================

# analyser_structure_agent.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Agent

def analyser_structure_agent():
    print("🔍 ANALYSE DE LA STRUCTURE DU MODÈLE AGENT...")

    # 1. Vérifier les champs disponibles
    print("\n📋 CHAMPS DU MODÈLE AGENT:")
    for field in Agent._meta.get_fields():
        print(f"  - {field.name} ({field.get_internal_type()})")

    # 2. Vérifier s'il y a des agents existants
    print(f"\n👨‍💼 AGENTS EXISTANTS: {Agent.objects.count()}")

    # 3. Analyser VerificationCotisation
    from agents.models import VerificationCotisation
    print("\n📋 CHAMPS DU MODÈLE VERIFICATIONCOTISATION:")
    for field in VerificationCotisation._meta.get_fields():
        print(f"  - {field.name} ({field.get_internal_type()})")

    # 4. Vérifier la relation entre Agent et User
    try:
        from django.contrib.auth.models import User
        print("\n🔗 RELATION AVEC USER:")
        # Vérifier si Agent a un champ user
        for field in Agent._meta.get_fields():
            if hasattr(field, 'related_model') and field.related_model == User:
                print(f"  - Relation User trouvée: {field.name}")
    except:
        pass

if __name__ == "__main__":
    analyser_structure_agent()

# ============================================================
# ORIGINE 2: analyser_mutuelle_core2.py (2025-11-19)
# ============================================================

import os
import importlib
import django
import subprocess
from datetime import datetime
from pathlib import Path

# 🔧 Configuration de base
BASE_DIR = Path(__file__).resolve().parent
SETTINGS_PATH = BASE_DIR / "mutuelle_core" / "settings.py"
RAPPORT_PATH = BASE_DIR / "rapport_analyse.html"

def print_header():
    print("\n🔍 ANALYSE COMPLÈTE DU PROJET DJANGO MUTUELLE")
    print("=" * 70)

def check_django_settings():
    print(f"\n➡️ Vérification du fichier settings.py : {SETTINGS_PATH}")
    if SETTINGS_PATH.exists():
        print("✅ settings.py trouvé")
    else:
        print("❌ settings.py manquant")

def get_installed_apps():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()
    from django.conf import settings
from django.utils import timezone
    return settings.INSTALLED_APPS

def check_apps(apps):
    print("\n➡️ Vérification des applications locales...")
    results = []
    for app in apps:
        if app.startswith("django.") or app.startswith("rest_framework") or "corsheaders" in app:
            continue
        app_path = BASE_DIR / app.replace(".", "/")
        if app_path.exists():
            results.append((app, "✅ OK"))
        else:
            results.append((app, "❌ Dossier manquant"))
    return results

def check_files(app_name):
    required_files = ["models.py", "views.py", "urls.py"]
    app_path = BASE_DIR / app_name.replace(".", "/")
    missing = [f for f in required_files if not (app_path / f).exists()]
    return missing

def check_imports(app_name):
... (tronqué)

# ============================================================
# ORIGINE 3: analyser_mutuelle_core3.py (2025-11-19)
# ============================================================

#!/usr/bin/env python3
"""
analyser_mutuelle_core3.py
Analyse avancée des modèles Django + détection relations + rapport HTML + Dot (Graphviz).

Place ce fichier à la racine du projet (même dossier que manage.py) et exécute :
    source venv/bin/activate
    python analyser_mutuelle_core3.py
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import importlib
import textwrap
import html
from collections import defaultdict

# --- Configuration ---
BASE_DIR = Path(__file__).resolve().parent
REPORT_HTML = BASE_DIR / "rapport_analyse3.html"
DOT_FILE = BASE_DIR / "mutuelle_models.dot"
SVG_FILE = BASE_DIR / "mutuelle_models.svg"
DJANGO_SETTINGS_MODULE = "mutuelle_core.settings"

# --- Setup Django environment ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
try:
    import django
from django.utils import timezone
    django.setup()
    from django.apps import apps as django_apps
    from django.db import models as dj_models
    from django.conf import settings
except Exception as e:
    print("❌ Impossible d'initialiser Django. Vérifie DJANGO_SETTINGS_MODULE et l'environnement virtuel.")
    print("Erreur:", e)
    sys.exit(1)


def safe_str(s):
    return html.escape(str(s))


def collect_models_info():
    """Collecte des informations sur tous les modèles installés."""
    model_infos = []
    relations = []  # tuples (from_model, to_model, relation_type, field_name)
... (tronqué)

# ============================================================
# ORIGINE 4: analyser_section_conformite.py (2025-11-12)
# ============================================================

#!/usr/bin/env python3
"""
ANALYSE SPÉCIFIQUE - Trouver la section exacte du taux de conformité
"""

import os
import re

def trouver_section_conformite():
    """Trouve exactement où se trouve la section problématique"""

    template_path = 'templates/agents/dashboard.html'

    print("🔍 RECHERCHE DE LA SECTION 'TAUX CONFORMITÉ'")
    print("=" * 50)

    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Rechercher toutes les occurrences de "Taux conformité" ou similaires
    patterns = [
        r'Taux conformité',
        r'Taux.*conformité',
        r'conformité',
        r'pourcentage',
        r'%',
        r'stats\.membres_a_jour.*stats\.membres_actifs'
    ]

    for pattern in patterns:
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        if matches:
            print(f"\n📌 Pattern: '{pattern}' - {len(matches)} occurrence(s)")
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1

                # Afficher le contexte (5 lignes avant/après)
                lines = content.split('\n')
                start_line = max(0, line_num - 6)  # -1 car index 0-based
                end_line = min(len(lines), line_num + 4)

                print(f"   Ligne {line_num}:")
                for i in range(start_line, end_line):
                    marker = ">>>" if i == line_num - 1 else "   "
                    print(f"   {marker} {i+1}: {lines[i]}")

    # Recherche spécifique de la section carte
    print("\n🎯 RECHERCHE DES CARTES DE STATISTIQUES:")
    carte_sections = re.finditer(r'<div class="card[^>]*>.*?</div>\s*</div>\s*</div>', content, re.DOTALL)

... (tronqué)

