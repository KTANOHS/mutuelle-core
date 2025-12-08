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