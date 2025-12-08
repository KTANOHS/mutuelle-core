#!/usr/bin/env python3
"""
SOLUTION ULTIME - TOUTES LES APPLICATIONS INCLUSES
"""

import os
import django
from pathlib import Path
import subprocess
import sys
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

BASE_DIR = Path(__file__).parent

def ultimate_migration_fix():
    """Solution ultime incluant toutes les applications"""
    
    print("🔄 SOLUTION ULTIME DES MIGRATIONS")
    print("=" * 50)
    
    # 1. Identifier toutes les applications
    all_apps = find_all_apps()
    print(f"📋 Applications trouvées: {', '.join(all_apps)}")
    
    # 2. Supprimer toutes les migrations
    delete_all_migrations_complete(all_apps)
    
    # 3. Supprimer la base de données
    delete_database()
    
    # 4. Recréer les migrations dans le bon ordre
    recreate_migrations_ordered(all_apps)
    
    # 5. Appliquer les migrations
    apply_migrations()
    
    print("\n✅ RÉINITIALISATION COMPLÈTE TERMINÉE!")

def find_all_apps():
    """Trouve toutes les applications Django dans le projet"""
    
    print("\n🔍 RECHERCHE DES APPLICATIONS...")
    
    apps = []
    # Applications standard Django
    django_apps = ['admin', 'auth', 'contenttypes', 'sessions', 'staticfiles']
    
    # Recherche des applications personnalisées
    for item in BASE_DIR.iterdir():
        if item.is_dir() and not item.name.startswith(('.', '__', 'venv')):
            # Vérifier si c'est une app Django (a un models.py ou un dossier migrations)
            if (item / 'models.py').exists() or (item / 'migrations').exists():
                apps.append(item.name)
    
    # Retirer les doublons et trier
    all_apps = list(set(apps + django_apps))
    return sorted(all_apps)

def delete_all_migrations_complete(apps):
    """Supprime toutes les migrations de toutes les applications"""
    
    print("\n🗑️ SUPPRESSION COMPLÈTE DES MIGRATIONS...")
    
    for app in apps:
        migrations_dir = BASE_DIR / app / 'migrations'
        if migrations_dir.exists():
            print(f"   📁 Traitement de: {app}/migrations")
            
            # Supprimer tous les fichiers .py sauf __init__.py
            py_files_deleted = 0
            for file in migrations_dir.glob('*.py'):
                if file.name != '__init__.py':
                    file.unlink()
                    py_files_deleted += 1
            
            # Supprimer le cache
            pycache_dir = migrations_dir / '__pycache__'
            if pycache_dir.exists():
                shutil.rmtree(pycache_dir)
                print(f"     🗑️  Cache supprimé")
            
            if py_files_deleted > 0:
                print(f"     ✅ {py_files_deleted} fichiers supprimés")

def delete_database():
    """Supprime la base de données SQLite"""
    
    print("\n🗄️ SUPPRESSION DE LA BASE DE DONNÉES...")
    
    db_path = BASE_DIR / 'db.sqlite3'
    if db_path.exists():
        db_path.unlink()
        print("   ✅ Base de données supprimée")
    else:
        print("   ℹ️  Base de données non trouvée")

def recreate_migrations_ordered(apps):
    """Recrée les migrations dans l'ordre correct"""
    
    print("\n🔄 CRÉATION DES MIGRATIONS DANS L'ORDRE...")
    
    # Ordre recommandé pour les migrations
    ordered_apps = [
        'contenttypes',
        'auth',
        'admin',
        'sessions',
        'membres',  # Vos apps de base en premier
        'agents',
        'assureur',  # L'app qui causait le problème
        'soins',
        'mutuelle_core',
    ]
    
    # Ajouter les apps manquantes
    for app in apps:
        if app not in ordered_apps:
            ordered_apps.append(app)
    
    # Créer les migrations pour chaque app
    for app in ordered_apps:
        app_path = BASE_DIR / app
        if app_path.exists():
            print(f"   📦 Création des migrations pour {app}...")
            
            try:
                result = subprocess.run([
                    sys.executable, 'manage.py', 'makemigrations', app
                ], capture_output=True, text=True, cwd=BASE_DIR, timeout=30)
                
                if result.returncode == 0:
                    if "No changes detected" not in result.stdout:
                        print(f"     ✅ Migrations créées pour {app}")
                        if result.stdout.strip():
                            print(f"       📝 {result.stdout.strip()}")
                    else:
                        print(f"     ℹ️  Aucun changement pour {app}")
                else:
                    print(f"     ⚠️  Avertissement pour {app}: {result.stderr[:200]}...")
                    
            except subprocess.TimeoutExpired:
                print(f"     ⏰ Timeout pour {app}, continuation...")
            except Exception as e:
                print(f"     ❌ Erreur pour {app}: {e}")
    
    # Création finale de toutes les migrations
    print("   🔄 Création finale de toutes les migrations...")
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'makemigrations'
        ], capture_output=True, text=True, cwd=BASE_DIR, timeout=30)
        
        if result.returncode == 0:
            print("     ✅ Toutes les migrations créées avec succès")
        else:
            print(f"     ⚠️  Avertissement final: {result.stderr[:200]}...")
    except Exception as e:
        print(f"     ❌ Erreur finale: {e}")

def apply_migrations():
    """Applique toutes les migrations"""
    
    print("\n🚀 APPLICATION DES MIGRATIONS...")
    
    try:
        # Désactiver temporairement le check staticfiles
        env = os.environ.copy()
        env['DJANGO_SETTINGS_MODULE'] = 'mutuelle_core.settings'
        
        result = subprocess.run([
            sys.executable, 'manage.py', 'migrate', '--run-syncdb'
        ], capture_output=True, text=True, cwd=BASE_DIR, env=env, timeout=60)
        
        if result.returncode == 0:
            print("   ✅ Toutes les migrations appliquées avec succès!")
            if result.stdout:
                print(f"   📋 Output: {result.stdout}")
        else:
            print(f"   ❌ Erreur lors de la migration: {result.stderr}")
            # Essayer sans --run-syncdb
            print("   🔄 Nouvelle tentative sans --run-syncdb...")
            result2 = subprocess.run([
                sys.executable, 'manage.py', 'migrate'
            ], capture_output=True, text=True, cwd=BASE_DIR, env=env, timeout=60)
            
            if result2.returncode == 0:
                print("   ✅ Migrations appliquées avec succès (2ème tentative)")
            else:
                print(f"   ❌ Échec de la 2ème tentative: {result2.stderr}")
                
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

if __name__ == "__main__":
    ultimate_migration_fix()