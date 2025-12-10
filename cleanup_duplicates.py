# cleanup_duplicates.py
#!/usr/bin/env python3
"""
Script pour nettoyer les doublons et réorganiser le projet
"""

import os
import shutil
from pathlib import Path

def clean_project():
    """Nettoie la structure du projet"""
    base_dir = Path.cwd()
    
    print("🧹 NETTOYAGE DU PROJET")
    print("=" * 80)
    
    # 1. Supprimer les applications en double
    duplicates_to_remove = [
        'apps/core',  # Doublon de core/
        'apps/soins',
        'apps/medecin', 
        'apps/membres',
        'apps/assureur',
        'apps/inscription',
        'apps/api',
        'apps/paiements',
        'apps/pharmacien'
    ]
    
    for duplicate in duplicates_to_remove:
        dup_path = base_dir / duplicate
        if dup_path.exists():
            print(f"🗑️  Suppression du doublon: {duplicate}")
            shutil.rmtree(dup_path)
    
    # 2. Supprimer les fichiers backup inutiles
    backup_patterns = [
        '*.backup*',
        '*.save',
        '*.old',
        '*_backup_*',
        '*.final_backup',
        '*.backup2',
        '*.backup_existing',
        '*.backup_pre_simple',
        '*.backup_structure_cassee',
        '*.final',
        '*.1764855030',
        '*.1764855031',
        '*.1764855032',
        '*.20251022_*'
    ]
    
    for pattern in backup_patterns:
        for file in base_dir.rglob(pattern):
            if file.is_file():
                print(f"🗑️  Suppression backup: {file.relative_to(base_dir)}")
                file.unlink()
    
    # 3. Organiser les scripts consolidés
    scripts_dir = base_dir / 'scripts_consolides'
    if scripts_dir.exists():
        print(f"📦 Réorganisation de: {scripts_dir.name}")
        # Garder seulement les fichiers utiles
        keep_folders = ['utilitaires', 'rapports']
        for item in scripts_dir.iterdir():
            if item.is_dir() and item.name not in keep_folders:
                shutil.rmtree(item)
    
    # 4. Créer structure organisée
    organized_dirs = [
        'backups/old',
        'logs/archives',
        'media/archives',
        'templates/backups',
        'static/backups'
    ]
    
    for dir_path in organized_dirs:
        (base_dir / dir_path).mkdir(parents=True, exist_ok=True)
    
    print(f"\n✅ Nettoyage terminé!")
    print(f"📁 Structure actuelle:")
    
    # Afficher la nouvelle structure
    for item in sorted(base_dir.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
            print(f"  • {item.name}/ ({size/1024/1024:.1f} MB)")
    
    return True

if __name__ == "__main__":
    clean_project()