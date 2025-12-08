#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analyse complète d’un projet Django :
 - Affiche l’arborescence du projet
 - Identifie les applications installées
 - Vérifie la présence de fichiers clés (models.py, views.py, urls.py, etc.)
 - Vérifie le fichier settings.py
 - Affiche les dépendances (requirements.txt)
"""

import os
from pathlib import Path
import json
import sys
import importlib.util

BASE_DIR = Path(__file__).resolve().parent

# ============================================================
# 1️⃣ AFFICHAGE DE L’ARBORESCENCE DU PROJET
# ============================================================

def afficher_arborescence(path: Path, prefix: str = ""):
    """Affiche l’arborescence du dossier sous forme d’arborescence hiérarchique."""
    fichiers = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    for fichier in fichiers:
        if fichier.name.startswith('.') or fichier.name == '__pycache__':
            continue
        print(prefix + ("📁 " if fichier.is_dir() else "📄 ") + fichier.name)
        if fichier.is_dir():
            afficher_arborescence(fichier, prefix + "   ")

# ============================================================
# 2️⃣ ANALYSE DES APPLICATIONS DJANGO
# ============================================================

def extraire_apps(settings_path: Path):
    """Extrait les applications installées depuis settings.py."""
    apps = []
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            contenu = f.read()
        start = contenu.find("INSTALLED_APPS")
        if start != -1:
            bloc = contenu[start:contenu.find("]", start)]
            for ligne in bloc.splitlines():
                if "'" in ligne or '"' in ligne:
                    app = ligne.strip().strip(",").strip("'\"")
                    if app and not app.startswith("#"):
                        apps.append(app)
    except Exception as e:
        print(f"⚠️ Erreur lecture settings.py : {e}")
    return apps

# ============================================================
# 3️⃣ VÉRIFICATION DES FICHIERS CLÉS PAR APP
# ============================================================

def verifier_app_structure(app_name):
    """Vérifie les fichiers principaux d'une app Django."""
    app_path = BASE_DIR / app_name
    if not app_path.exists():
        return None

    fichiers = ['models.py', 'views.py', 'urls.py', 'admin.py', 'forms.py']
    manquants = [f for f in fichiers if not (app_path / f).exists()]
    return {
        "app": app_name,
        "path": str(app_path),
        "manquants": manquants
    }

# ============================================================
# 4️⃣ ANALYSE DU FICHIER requirements.txt
# ============================================================

def analyser_requirements():
    """Liste les dépendances installées dans requirements.txt."""
    req_file = BASE_DIR / "requirements.txt"
    if not req_file.exists():
        return []
    deps = []
    with open(req_file, "r", encoding="utf-8") as f:
        for ligne in f:
            if ligne.strip() and not ligne.startswith("#"):
                deps.append(ligne.strip())
    return deps

# ============================================================
# 5️⃣ SYNTHÈSE
# ============================================================

def analyse_complete():
    print("🔍 ANALYSE DU PROJET DJANGO")
    print("=" * 60)
    print(f"📂 Répertoire racine : {BASE_DIR}")
    print()

    # Arborescence
    print("📁 Arborescence du projet :")
    print("-" * 60)
    afficher_arborescence(BASE_DIR)
    print()

    # Settings
    settings_path = None
    for root, dirs, files in os.walk(BASE_DIR):
        if "settings.py" in files:
            settings_path = Path(root) / "settings.py"
            break

    if not settings_path:
        print("❌ settings.py introuvable.")
        return

    print(f"⚙️  Fichier settings.py trouvé : {settings_path}")
    print()

    # Apps
    apps = extraire_apps(settings_path)
    print("📦 Applications installées :")
    for app in apps:
        print(f"   - {app}")
    print()

    # Structure des apps locales
    print("🔧 Vérification des structures d'apps locales :")
    for app in apps:
        if app not in [
            'django.contrib.admin', 'django.contrib.auth', 'django.contrib.sessions',
            'django.contrib.contenttypes', 'django.contrib.messages', 'django.contrib.staticfiles',
            'rest_framework', 'corsheaders', 'channels', 'rest_framework_simplejwt'
        ]:
            result = verifier_app_structure(app)
            if result:
                print(f"📂 {app} → OK" if not result['manquants'] else f"⚠️ {app} → Fichiers manquants : {', '.join(result['manquants'])}")
    print()

    # Requirements
    deps = analyser_requirements()
    if deps:
        print("📜 Dépendances (requirements.txt) :")
        for d in deps:
            print(f"   - {d}")
    else:
        print("⚠️ Aucun fichier requirements.txt trouvé ou vide.")
    print()

    print("✅ Analyse terminée.")

# ============================================================
# 6️⃣ POINT D’ENTRÉE
# ============================================================

if __name__ == "__main__":
    try:
        analyse_complete()
    except KeyboardInterrupt:
        print("\n❌ Analyse interrompue par l'utilisateur.")
