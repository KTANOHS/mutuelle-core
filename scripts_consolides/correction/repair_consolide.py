"""
FICHIER CONSOLIDÉ: repair
Catégorie: correction
Fusion de 3 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: repair.py (2025-12-05)
# ============================================================

import os
import sys
import subprocess

def run_command(cmd):
    """Exécute une commande et retourne le résultat"""
    print(f"➤ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"✗ Erreur: {result.stderr}")
    else:
        print(f"✓ Succès: {result.stdout}")
    return result.returncode

def main():
    print("="*60)
    print("RÉPARATION COMPLÈTE DU PROJET DJANGO")
    print("="*60)

    # 1. Nettoyer les fichiers de cache
    print("\n1. Nettoyage des fichiers de cache...")
    os.system('find . -name "__pycache__" -type d -exec rm -rf {} +')
    os.system('find . -name "*.pyc" -delete')
    os.system('find . -name ".pytest_cache" -type d -exec rm -rf {} +')
    os.system('find . -name ".coverage" -delete')

    # 2. Corriger le fichier forms.py problématique
    print("\n2. Correction du fichier forms.py...")
    forms_content = '''class FiltreBonsForm(forms.Form):
    STATUT_CHOICES = [
        ('', 'Tous les statuts'),
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
        ('paye', 'Payé'),
    ]

    TYPE_SOIN_CHOICES = [
        ('', 'Tous les types'),
        ('consultation', 'Consultation'),
        ('hospitalisation', 'Hospitalisation'),
        ('pharmacie', 'Pharmacie'),
        ('radiologie', 'Radiologie'),
        ('laboratoire', 'Laboratoire'),
        ('dentaire', 'Dentaire'),
        ('optique', 'Optique'),
    ]

    numero = forms.CharField(required=False, label="Numéro de bon")
    membre = forms.CharField(required=False, label="Nom du membre")
... (tronqué)

# ============================================================
# ORIGINE 2: repair_ultimate.py (2025-12-04)
# ============================================================

# repair_ultimate.py
import os
import shutil
import sys
import subprocess

def clean_project():
    """Nettoie complètement le projet"""
    print("=== NETTOYAGE COMPLET DU PROJET ===")

    # 1. Arrêter le serveur
    subprocess.run("pkill -f 'python manage.py runserver'", shell=True, capture_output=True)

    # 2. Supprimer les migrations
    print("\n1. Nettoyage des migrations...")
    migrations_dirs = [
        "membres/migrations/",
        "agents/migrations/",
        "assureur/migrations/",
        "medecin/migrations/",
    ]

    for dir_path in migrations_dirs:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"  Supprimé: {dir_path}")
        os.makedirs(dir_path, exist_ok=True)
        with open(os.path.join(dir_path, "__init__.py"), "w") as f:
            f.write("")

    # 3. Supprimer la base de données
    print("\n2. Nettoyage de la base de données...")
    db_files = ["db.sqlite3", "db.sqlite3-journal"]
    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"  Supprimé: {db_file}")

    # 4. Nettoyer les caches Python
    print("\n3. Nettoyage des caches...")
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                dir_path = os.path.join(root, dir_name)
                shutil.rmtree(dir_path, ignore_errors=True)
                print(f"  Supprimé: {dir_path}")
        for file_name in files:
            if file_name.endswith(".pyc"):
                file_path = os.path.join(root, file_name)
                os.remove(file_path)
... (tronqué)

# ============================================================
# ORIGINE 3: repair_migrations.py (2025-12-04)
# ============================================================

# repair_migrations_v2.py - SCRIPT AMÉLIORÉ
import os
import shutil
import sys
import subprocess

def run_command(cmd, description):
    """Exécute une commande avec gestion d'erreur"""
    print(f"\n{description}...")
    print(f"Commande: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERREUR: {result.stderr}")
        return False
    print(f"  SUCCÈS: {result.stdout[:200]}...")
    return True

def fix_forms_file():
    """Corrige le fichier forms.py problématique"""
    forms_path = "assureur/forms.py"
    if not os.path.exists(forms_path):
        return True

    print("\nCorrection du fichier forms.py...")

    # Faire une sauvegarde
    shutil.copy2(forms_path, f"{forms_path}.backup")

    # Lire le contenu
    with open(forms_path, 'r') as f:
        content = f.read()

    # Remplacer la ligne problématique
    old_line = "choices=[('', 'Tous les statuts')] + [(s, s) for s in Membre.objects.values_list('statut', flat=True).distinct()],"
    new_line = "choices=[('', 'Tous les statuts'), ('actif', 'Actif'), ('en_retard', 'En retard de paiement'), ('inactif', 'Inactif')],"

    if old_line in content:
        content = content.replace(old_line, new_line)
        with open(forms_path, 'w') as f:
            f.write(content)
        print("  Ligne corrigée dans forms.py")
        return True
    else:
        print("  La ligne problématique n'a pas été trouvée")
        return True

def repair_migrations():
    print("=== DÉBUT DE LA RÉPARATION DES MIGRATIONS V2 ===")

    # 1. Corriger le fichier forms.py
... (tronqué)

