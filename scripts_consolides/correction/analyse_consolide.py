"""
FICHIER CONSOLIDÉ: analyse
Catégorie: correction
Fusion de 5 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: analyse_projet_corrige.py (2025-11-19)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT D'ANALYSE CORRIGÉ - DÉTECTION AMÉLIORÉE DE LA STRUCTURE DJANGO
"""

import os
import sys
import ast
import json
import datetime
from pathlib import Path
import django
from django.conf import settings

# Configuration Django minimale pour l'analyse
def setup_django(project_path):
    """Configure Django pour l'analyse"""
    project_dir = project_path
    sys.path.insert(0, str(project_dir))

    # Trouve le module settings
    settings_module = None
    for file in project_dir.glob('*settings*.py'):
        settings_module = file.stem
        break

    if not settings_module:
        # Cherche dans les sous-dossiers
        for file in project_dir.rglob('*settings*.py'):
            relative_path = file.relative_to(project_dir)
            settings_module = str(relative_path).replace('/', '.').replace('.py', '')
            break

    if settings_module:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
        try:
            django.setup()
            return True
        except Exception as e:
            print(f"⚠️  Impossible de charger Django: {e}")

    return False

class DjangoProjectAnalyzerCorrige:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.analysis_results = {
            'timestamp': datetime.datetime.now().isoformat(),
            'project_info': {},
            'apps_detected': [],
... (tronqué)

# ============================================================
# ORIGINE 2: analyse_assureur_corrige.py (2025-11-18)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT D'ANALYSE CORRIGÉ - APPLICATION ASSUREUR
Version corrigée pour la détection des templates
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
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def analyse_templates_assureur_corrige():
    """Analyse corrigée des templates"""
    print("\n" + "="*80)
    print("🎨 ANALYSE DES TEMPLATES ASSUREUR (CORRIGÉE)")
    print("="*80)

    try:
        # Chemin absolu vers templates/assureur
        templates_dir = BASE_DIR / 'templates' / 'assureur'

        print(f"🔍 Recherche dans: {templates_dir}")

        if not templates_dir.exists():
            print(f"❌ Dossier introuvable: {templates_dir}")
            # Vérifier les dossiers templates existants
            templates_parent = BASE_DIR / 'templates'
            if templates_parent.exists():
                print(f"📁 Dossiers templates trouvés:")
                for item in templates_parent.iterdir():
                    if item.is_dir():
                        print(f"   - {item.name}")
            return False

        # Compter les templates
        categories = {
            'cotisations': 0,
            'configuration': 0,
            'communication': 0,
... (tronqué)

# ============================================================
# ORIGINE 3: analyse_existant_corrige.py (2025-11-18)
# ============================================================

# analyse_existant_corrige.py
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre, Cotisation
from django.db import models

def analyser_modeles_corrige():
    """Analyse corrigée des modèles"""
    print("=== ANALYSE CORRIGÉE DES MODÈLES ===")

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

def analyser_relations_corrigee():
    """Analyse corrigée des relations"""
    print("\n=== ANALYSE DES RELATIONS CORRIGÉE ===")

    try:
        # Relation Cotisation -> Membre
        champ_membre = Cotisation._meta.get_field('membre')
        print(f"Relation Cotisation -> Membre: {champ_membre.related_model.__name__}")
        print(f"Related name: {champ_membre.related_query_name()}")

        # Vérifier si le related_name existe
        membre = Membre.objects.first()
        if membre:
            cotisations = membre.cotisations_assureur.all()
            print(f"Related name fonctionnel: {cotisations.count()} cotisations pour le premier membre")

    except Exception as e:
        print(f"Erreur relation: {e}")
... (tronqué)

# ============================================================
# ORIGINE 4: analyse_post_implementation_corrige.py (2025-11-14)
# ============================================================

# analyse_post_implementation_corrige.py

import os
import sys
import django

# Configuration Django CORRECTE
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')  # Corrigez avec le bon nom
django.setup()

from django.apps import apps
from django.db import models
from django.contrib.auth.models import User, Group
from django.template.loader import get_template
from django.urls import reverse, NoReverseMatch

class AnalysePostImplementation:
    def __init__(self):
        self.resultats = {}
        self.erreurs = []

    def executer_analyse_complete(self):
        print("🚀 ANALYSE POST-IMPLÉMENTATION - CRÉATION MEMBRES PAR AGENTS")
        print("=" * 70)
        print()

        self.verifier_fonction_generer_numero()
        self.verifier_formulaires()
        self.verifier_vues()
        self.verifier_urls()
        self.verifier_templates()
        self.verifier_permissions()
        self.tester_fonctionnalites()
        self.analyser_donnees_test()
        self.generer_rapport_final()

    def verifier_fonction_generer_numero(self):
        print("🔢 1. VÉRIFICATION FONCTION GÉNÉRATION NUMÉRO")
        print("-" * 45)

        try:
            from core.utils import generer_numero_unique
            numero_test = generer_numero_unique()
            print(f"   ✅ generer_numero_unique() fonctionne")
            print(f"   📝 Numéro test généré: {numero_test}")

        except ImportError as e:
            print(f"   ❌ Fonction manquante: {e}")
            print("   🔧 Solution: Ajouter la fonction dans core/utils.py")
... (tronqué)

# ============================================================
# ORIGINE 5: analyse_creation_membres_corrige.py (2025-11-14)
# ============================================================

# analyse_creation_membres_corrige.py

import os
import sys
import django
from django.apps import apps
from django.conf import settings

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.template.loader import get_template
from django.urls import get_resolver

class AnalyseCreationMembres:
    def __init__(self):
        self.analyse_resultats = {
            'membre_champs': [],
            'agent_champs': [],
            'relations': [],
            'permissions': [],
            'templates': [],
            'urls': [],
            'donnees_test': {}
        }

    def analyser_structure_actuelle(self):
        print("🔍 ANALYSE DE LA STRUCTURE ACTUELLE")
        print("=" * 60)
        print()

        self.analyser_modele_membre()
        self.analyser_modele_agent()
        self.analyser_relations()
        self.analyser_permissions()
        self.analyser_templates()
        self.analyser_urls_vues()
        self.analyser_donnees_test()

    def analyser_modele_membre(self):
        print("📋 1. ANALYSE DU MODÈLE MEMBRE")
        print("-" * 40)

        try:
            Membre = apps.get_model('membres', 'Membre')
            fields = Membre._meta.get_fields()
... (tronqué)

