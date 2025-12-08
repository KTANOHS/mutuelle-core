#!/usr/bin/env python3
"""
SCRIPT DE BACKUP SIMPLE - Mutuelle Core
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
BACKUP_DIR = BASE_DIR / 'backups'

def backup_database():
    """Créer un backup de la base de données"""
    # Créer le dossier backup
    BACKUP_DIR.mkdir(exist_ok=True)
    
    # Nom du fichier
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    db_path = BASE_DIR / 'db.sqlite3'
    
    if db_path.exists():
        backup_file = BACKUP_DIR / f'db_backup_{timestamp}.sqlite3'
        
        try:
            # Copier la base de données
            shutil.copy2(db_path, backup_file)
            
            # Taille en MB
            file_size = backup_file.stat().st_size / 1024 / 1024
            
            print(f"✅ Backup créé: {backup_file.name}")
            print(f"📊 Taille: {file_size:.2f} MB")
            
            # Garder seulement les 5 derniers backups
            backups = sorted(BACKUP_DIR.glob('db_backup_*.sqlite3'))
            if len(backups) > 5:
                for old_backup in backups[:-5]:
                    old_backup.unlink()
                    print(f"🗑️  Supprimé: {old_backup.name}")
                    
        except Exception as e:
            print(f"❌ Erreur: {e}")
    else:
        print("❌ Base de données non trouvée")

if __name__ == "__main__":
    print("🔍 Début du backup...")
    backup_database()
    print("✅ Backup terminé !")
