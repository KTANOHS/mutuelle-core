#!/usr/bin/env python
"""
DIAGNOSTIC DES CHEMINS DU PROJET
"""

import os
import sys
from pathlib import Path

def diagnose_paths():
    print("🔍 DIAGNOSTIC DES CHEMINS DU PROJET")
    print("=" * 50)
    
    # Chemin actuel
    current_dir = Path.cwd()
    print(f"📂 Répertoire courant: {current_dir}")
    
    # Chemin du script
    script_dir = Path(__file__).resolve().parent
    print(f"📂 Répertoire du script: {script_dir}")
    
    # Vérifier la structure
    print(f"\n📁 STRUCTURE DU PROJET:")
    
    # Dossiers à vérifier
    directories = [
        'agents',
        'templates/agents',
        'projet',  # settings Django
        'manage.py'
    ]
    
    for dir_path in directories:
        full_path = script_dir / dir_path
        if full_path.exists():
            if full_path.is_dir():
                items = list(full_path.glob('*'))
                print(f"   ✅ {dir_path:25} - DOSSIER ({len(items)} éléments)")
            else:
                size_kb = full_path.stat().st_size / 1024
                print(f"   ✅ {dir_path:25} - FICHIER ({size_kb:.1f} KB)")
        else:
            print(f"   ❌ {dir_path:25} - MANQUANT")
    
    # Vérifier les fichiers agents essentiels
    print(f"\n📄 FICHIERS AGENTS:")
    agents_files = [
        '__init__.py',
        'admin.py', 
        'urls.py',
        'views.py',
        'models.py'
    ]
    
    for file_name in agents_files:
        file_path = script_dir / 'agents' / file_name
        if file_path.exists():
            size_kb = file_path.stat().st_size / 1024
            print(f"   ✅ {file_name:20} - PRÉSENT ({size_kb:.1f} KB)")
        else:
            print(f"   ❌ {file_name:20} - MANQUANT")
    
    # Vérifier les templates agents
    templates_dir = script_dir / 'templates' / 'agents'
    if templates_dir.exists():
        templates = list(templates_dir.glob('*.html'))
        print(f"\n📄 TEMPLATES AGENTS: {len(templates)} fichiers")
        for template in templates:
            size_kb = template.stat().st_size / 1024
            print(f"   📋 {template.name:25} - {size_kb:.1f} KB")
    else:
        print(f"\n📄 TEMPLATES AGENTS: ❌ Dossier manquant")

if __name__ == '__main__':
    diagnose_paths()