"""
FICHIER CONSOLIDÉ: check
Catégorie: correction
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
# ORIGINE 1: check_system_corrige1.py (2025-12-03)
# ============================================================

# check_system_corrige.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Cotisation, Membre
from django.db.models import Count, Sum

print("="*60)
print("ÉTAT DU SYSTÈME DE COTISATIONS")
print("="*60)

# Compter les membres
membres = Membre.objects.all()
membres_actifs = Membre.objects.filter(statut='actif')
print(f"📊 MEMBRES:")
print(f"   Total: {membres.count()}")
print(f"   Actifs: {membres_actifs.count()}")
print(f"   Inactifs: {membres.filter(statut='inactif').count()}")

# Afficher les membres actifs
print(f"\n👥 LISTE DES MEMBRES ACTIFS:")
for m in membres_actifs:
    # Utiliser le champ 'nom_complet' s'il existe, sinon combiner nom et prénom
    if hasattr(m, 'nom_complet'):
        nom_affichage = m.nom_complet
    else:
        nom_affichage = f"{getattr(m, 'nom', '')} {getattr(m, 'prenom', '')}".strip()

    # Utiliser le bon attribut pour le type (type_membre ou type_contrat)
    if hasattr(m, 'get_type_membre_display'):
        type_membre = m.get_type_membre_display()
    elif hasattr(m, 'get_type_contrat_display'):
        type_membre = m.get_type_contrat_display()
    else:
        type_membre = "Non spécifié"

    print(f"   - {m.numero_membre}: {nom_affichage} ({type_membre})")

# Compter les cotisations
cotisations = Cotisation.objects.all()
print(f"\n💰 COTISATIONS:")
print(f"   Total: {cotisations.count()}")

... (tronqué)

# ============================================================
# ORIGINE 2: check_system_corrige.py (2025-12-03)
# ============================================================

# check_system_corrige.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Cotisation, Membre

print("="*60)
print("ÉTAT DU SYSTÈME DE COTISATIONS")
print("="*60)

# Compter les membres
membres = Membre.objects.all()
membres_actifs = Membre.objects.filter(statut='actif')
print(f"📊 MEMBRES:")
print(f"   Total: {membres.count()}")
print(f"   Actifs: {membres_actifs.count()}")
print(f"   Inactifs: {membres.filter(statut='inactif').count()}")

# Afficher les membres actifs
print(f"\n👥 LISTE DES MEMBRES ACTIFS:")
for m in membres_actifs:
    # Utiliser les champs disponibles (nom et prénom séparés)
    nom_affichage = f"{m.nom} {m.prenom}" if hasattr(m, 'nom') and hasattr(m, 'prenom') else str(m)
    print(f"   - {m.numero_membre}: {nom_affichage} ({m.get_type_membre_display()})")

# Compter les cotisations
cotisations = Cotisation.objects.all()
print(f"\n💰 COTISATIONS:")
print(f"   Total: {cotisations.count()}")

# Par période
periodes = cotisations.values_list('periode', flat=True).distinct()
print(f"   Périodes: {list(sorted(periodes))}")

# Détail par période
print(f"\n📅 DÉTAIL PAR PÉRIODE:")
for periode in sorted(periodes):
    nb = cotisations.filter(periode=periode).count()
    cotis_periode = cotisations.filter(periode=periode)
    montant_total = sum(c.montant for c in cotis_periode if c.montant)
    print(f"   {periode}: {nb} cotisations, {montant_total} FCFA")

# Statistiques par statut
... (tronqué)

# ============================================================
# ORIGINE 3: check_member_sync_fixed.py (2025-11-30)
# ============================================================

# check_member_sync_fixed.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyze_member_sync():
    """Analyser la synchronisation des membres entre tous les acteurs - VERSION CORRIGÉE"""
    print("🔍 ANALYSE COMPLÈTE SYNCHRONISATION MEMBRES")
    print("=" * 60)

    from django.db import connection

    # 1. Vérifier tous les modèles Membre dans le système
    print("\n📦 MODÈLES MEMBRE DANS LE SYSTÈME")
    print("-" * 40)

    from django.apps import apps
    membre_models = []
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            if 'membre' in model.__name__.lower():
                membre_models.append(f"{app_config.name}.{model.__name__}")

    print("Modèles trouvés:")
    for model in membre_models:
        print(f"   📋 {model}")

    # 2. Analyser les tables de membres
    print("\n🗃️  TABLES MEMBRE DANS LA BASE")
    print("-" * 40)

    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%membre%'")
        tables = [row[0] for row in cursor.fetchall()]

        for table in tables:
            print(f"\n📊 Table: {table}")
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   👥 Nombre d'enregistrements: {count}")

    # 3. Vérifier la cohérence des données - VERSION CORRIGÉE
    print("\n🔗 COHÉRENCE DES DONNÉES")
    print("-" * 40)

    with connection.cursor() as cursor:
        # Compter les membres uniques dans membres_membre
        cursor.execute("SELECT COUNT(DISTINCT id) FROM membres_membre")
        membres_uniques = cursor.fetchone()[0]
... (tronqué)

# ============================================================
# ORIGINE 4: check_imports_fixed.py (2025-11-30)
# ============================================================

#!/usr/bin/env python
"""
SCRIPT D'ANALYSE CORRIGÉ - CONTOURNE L'ERREUR D'ENREGISTREMENT
Exécutez: python check_imports_fixed.py
"""

import os
import sys
import importlib
import inspect
from pathlib import Path

def safe_django_setup():
    """Configurer Django de manière sécurisée"""
    try:
        # Ajouter le répertoire du projet au path
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

        # Importer et configurer Django sans déclencher les erreurs d'admin
        import django
        from django.conf import settings

        # Configurer Django sans initialiser complètement les apps
        if not settings.configured:
            settings.configure(
                INSTALLED_APPS=[
                    'django.contrib.admin',
                    'django.contrib.auth',
                    'django.contrib.contenttypes',
                    'scoring',
                    'ia_detection',
                    'relances',
                    'dashboard',
                ],
                DATABASES={
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': project_root / 'db.sqlite3',
                    }
                },
                SECRET_KEY='temp-key-for-analysis'
            )

        django.setup()
        return True

    except Exception as e:
... (tronqué)

