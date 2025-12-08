#!/usr/bin/env python
"""
DIAGNOSTIC RAPIDE - TOUTES LES APPLICATIONS
Version rapide en ligne de commande.
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.conf import settings
from django.apps import apps
from django.db import connection

def diagnostic_rapide_applications():
    """Diagnostic rapide de toutes les applications"""
    print("🔧 DIAGNOSTIC RAPIDE - TOUTES LES APPLICATIONS")
    print("="*60)
    
    # 1. Lister toutes les applications
    print(f"\n📊 APPLICATIONS INSTALLÉES ({len(settings.INSTALLED_APPS)}):")
    
    custom_apps = []
    django_apps = []
    third_party_apps = []
    
    third_party_prefixes = [
        'rest_framework', 'corsheaders', 'crispy_forms', 'channels',
        'django_extensions', 'rest_framework_simplejwt'
    ]
    
    for app_name in settings.INSTALLED_APPS:
        if app_name.startswith('django.'):
            django_apps.append(app_name)
        elif any(app_name.startswith(prefix) for prefix in third_party_prefixes):
            third_party_apps.append(app_name)
        else:
            custom_apps.append(app_name)
    
    print(f"  • Applications Django: {len(django_apps)}")
    print(f"  • Applications tierces: {len(third_party_apps)}")
    print(f"  • Applications personnalisées: {len(custom_apps)}")
    
    # 2. Analyser les applications personnalisées
    print(f"\n🎯 APPLICATIONS PERSONNALISÉES:")
    
    app_stats = []
    
    for app_name in custom_apps:
        try:
            # Obtenir la configuration de l'application
            app_label = app_name.split('.')[-1]
            try:
                app_config = apps.get_app_config(app_label)
                models_count = len(list(app_config.get_models()))
            except:
                models_count = 0
            
            # Vérifier les fichiers
            app_path = None
            try:
                module = __import__(app_name)
                if hasattr(module, '__file__'):
                    app_path = Path(module.__file__).parent
            except:
                pass
            
            # Vérifier les tables en base
            table_count = 0
            if app_path and models_count > 0:
                with connection.cursor() as cursor:
                    if connection.vendor == 'sqlite':
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                        all_tables = [row[0] for row in cursor.fetchall()]
                        app_prefix = app_label + '_'
                        table_count = len([t for t in all_tables if t.startswith(app_prefix)])
            
            app_stats.append({
                'name': app_name,
                'models': models_count,
                'tables': table_count,
                'has_models_missing_tables': models_count > 0 and table_count == 0
            })
            
        except Exception as e:
            app_stats.append({
                'name': app_name,
                'error': str(e)
            })
    
    # Afficher les statistiques
    for stat in app_stats:
        if 'error' in stat:
            print(f"  ❌ {stat['name']}: Erreur - {stat['error']}")
        else:
            models_str = f"{stat['models']} modèle(s)"
            tables_str = f"{stat['tables']} table(s)"
            
            if stat['has_models_missing_tables']:
                print(f"  ⚠️  {stat['name']}: {models_str}, {tables_str} (TABLES MANQUANTES!)")
            elif stat['models'] > 0:
                print(f"  ✅ {stat['name']}: {models_str}, {tables_str}")
            else:
                print(f"  🔍 {stat['name']}: {models_str}")
    
    # 3. Identifier les problèmes
    print(f"\n🔍 PROBLÈMES IDENTIFIÉS:")
    
    problems_found = False
    
    for stat in app_stats:
        if 'error' not in stat and stat.get('has_models_missing_tables'):
            print(f"  ❌ {stat['name']}: {stat['models']} modèles mais {stat['tables']} tables en BDD")
            problems_found = True
    
    # Vérifier les migrations
    try:
        from django.db.migrations.recorder import MigrationRecorder
        migration_count = MigrationRecorder.Migration.objects.count()
        print(f"\n📦 Migrations appliquées: {migration_count}")
    except:
        print(f"\n📦 Migrations: Impossible de vérifier")
    
    # 4. Recommandations
    print(f"\n🎯 RECOMMANDATIONS:")
    
    if problems_found:
        print("  • Exécuter 'python manage.py makemigrations'")
        print("  • Exécuter 'python manage.py migrate'")
        print("  • Vérifier les applications avec modèles mais sans tables")
    else:
        print("  ✅ Aucun problème critique détecté")
    
    print("\n  • Tester le serveur: python manage.py runserver")
    print("  • Vérifier les URLs: python manage.py show_urls")
    print("  • Vérifier les modèles: python manage.py shell")
    
    print("\n" + "="*60)
    print("✅ DIAGNOSTIC RAPIDE TERMINÉ")

if __name__ == "__main__":
    diagnostic_rapide_applications()