"""
CORRECTEUR AUTOMATIQUE - Mutuelle Core
Ce script corrige automatiquement les problèmes identifiés
"""

import os
import sys
import django
import shutil
from pathlib import Path
from datetime import datetime

# Ajouter le chemin du projet Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def setup_django():
    """Configurer l'environnement Django"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        django.setup()
        return True
    except Exception as e:
        print(f"❌ Erreur Django: {e}")
        return False

def corriger_import_bonsoin():
    """Corriger l'import du modèle BonSoin -> BonDeSoin"""
    print("🔄 Correction de l'import BonSoin...")
    
    # Liste des fichiers à vérifier
    fichiers_a_corriger = []
    
    # Chercher tous les fichiers Python
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                fichiers_a_corriger.append(file_path)
    
    corrections = 0
    for fichier in fichiers_a_corriger:
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Rechercher les imports incorrects
            if 'BonSoin' in contenu and 'BonDeSoin' not in contenu:
                nouveau_contenu = contenu.replace(
                    'from soins.models import BonSoin',
                    'from soins.models import BonDeSoin'
                ).replace(
                    'import BonSoin',
                    'import BonDeSoin'
                ).replace(
                    'BonSoin.objects',
                    'BonDeSoin.objects'
                ).replace(
                    'BonSoin.DoesNotExist',
                    'BonDeSoin.DoesNotExist'
                )
                
                if nouveau_contenu != contenu:
                    with open(fichier, 'w', encoding='utf-8') as f:
                        f.write(nouveau_contenu)
                    print(f"✅ Corrigé: {fichier.relative_to(BASE_DIR)}")
                    corrections += 1
                    
        except Exception as e:
            continue
    
    return corrections

def creer_repertoires_manquants():
    """Créer les répertoires manquants"""
    print("📁 Création des répertoires manquants...")
    
    repertoires = [
        BASE_DIR / 'media',
        BASE_DIR / 'staticfiles',
        BASE_DIR / 'logs',
        BASE_DIR / 'media/uploads',
        BASE_DIR / 'media/profile_pics',
        BASE_DIR / 'media/documents',
    ]
    
    crees = 0
    for rep in repertoires:
        if not rep.exists():
            rep.mkdir(parents=True, exist_ok=True)
            print(f"✅ Créé: {rep.relative_to(BASE_DIR)}")
            crees += 1
    
    return crees

def verifier_modeles():
    """Vérifier et corriger les modèles"""
    print("🧪 Vérification des modèles...")
    
    if not setup_django():
        return False
    
    try:
        # Importer les modèles corrects
        from soins.models import BonDeSoin
        print("✅ Modèle BonDeSoin importé")
        
        # Vérifier s'il y a des données
        count = BonDeSoin.objects.count()
        print(f"✅ {count} bons de soin en base")
        
        return True
    except Exception as e:
        print(f"❌ Erreur avec BonDeSoin: {e}")
        return False

def generer_rapport_securite():
    """Générer un rapport de sécurité"""
    print("🔒 Rapport de sécurité...")
    
    rapport = []
    
    # Vérifier le .env
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        rapport.append("✅ Fichier .env présent")
        
        with open(env_file, 'r') as f:
            content = f.read()
            
        if 'SECRET_KEY' in content:
            rapport.append("✅ SECRET_KEY configurée")
        else:
            rapport.append("❌ SECRET_KEY manquante dans .env")
    else:
        rapport.append("⚠️  Fichier .env manquant")
    
    # Vérifier les permissions
    from django.conf import settings
    if settings.DEBUG:
        rapport.append("🚨 DEBUG activé (désactiver en production)")
    
    # Afficher le rapport
    for ligne in rapport:
        print(f"  {ligne}")
    
    return rapport

def creer_script_backup():
    """Créer un script de backup automatique"""
    print("💾 Création script de backup...")
    
    script_backup = BASE_DIR / 'backup_database.py'
    
    script_content = '''#!/usr/bin/env python3
"""
SCRIPT DE BACKUP - Mutuelle Core
Backup automatique de la base de données
"""

import os
import sys
import django
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).resolve().parent
BACKUP_DIR = BASE_DIR / 'backups'

def setup_django():
    """Configurer Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    sys.path.insert(0, str(BASE_DIR))
    django.setup()

def backup_database():
    """Créer un backup de la base de données"""
    from django.conf import settings
    
    # Créer le dossier backup s'il n'existe pas
    BACKUP_DIR.mkdir(exist_ok=True)
    
    # Nom du fichier avec timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    db_path = Path(settings.DATABASES['default']['NAME'])
    backup_file = BACKUP_DIR / f'db_backup_{timestamp}.sqlite3'
    
    try:
        # Copier la base de données
        shutil.copy2(db_path, backup_file)
        
        # Créer un fichier info
        info_file = BACKUP_DIR / f'info_{timestamp}.txt'
        file_size = backup_file.stat().st_size / 1024 / 1024
        with open(info_file, 'w') as f:
            f.write(f'''Backup Mutuelle Core
Date: {datetime.now()}
Fichier: {backup_file.name}
Taille: {file_size:.2f} MB
Répertoire: {BACKUP_DIR}
''')
        
        print(f"✅ Backup créé: {backup_file}")
        print(f"📊 Taille: {file_size:.2f} MB")
        
        # Nettoyer les anciens backups (garder les 10 derniers)
        backups = sorted(BACKUP_DIR.glob('db_backup_*.sqlite3'))
        if len(backups) > 10:
            for old_backup in backups[:-10]:
                old_backup.unlink()
                print(f"🗑️  Supprimé: {old_backup.name}")
        
    except Exception as e:
        print(f"❌ Erreur backup: {e}")

def backup_media():
    """Backup des fichiers média"""
    from django.conf import settings
    
    media_dir = Path(settings.MEDIA_ROOT)
    if media_dir.exists():
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        media_backup = BACKUP_DIR / f'media_backup_{timestamp}.zip'
        
        try:
            shutil.make_archive(
                str(media_backup).replace('.zip', ''),
                'zip',
                media_dir
            )
            print(f"✅ Media backup: {media_backup}")
        except Exception as e:
            print(f"⚠️  Erreur media backup: {e}")

if __name__ == "__main__":
    print("🔍 Début du backup...")
    setup_django()
    backup_database()
    backup_media()
    print("✅ Backup terminé !")
'''

    with open(script_backup, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # Rendre le script exécutable
    os.chmod(script_backup, 0o755)
    
    print(f"✅ Script créé: {script_backup}")
    return script_backup

def creer_guide_production():
    """Créer un guide pour la mise en production"""
    print("🚀 Création guide production...")
    
    guide_file = BASE_DIR / 'GUIDE_PRODUCTION.md'
    
    guide_content = '''# 🚀 GUIDE DE MISE EN PRODUCTION - Mutuelle Core

## 1. CONFIGURATION DE SÉCURITÉ

### 1.1 Désactiver le mode DEBUG
Dans `settings.py` ou `.env` :
```python
DEBUG = False