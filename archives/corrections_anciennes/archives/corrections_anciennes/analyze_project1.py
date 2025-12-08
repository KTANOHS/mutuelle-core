#!/usr/bin/env python
"""
SCRIPT D'ANALYSE COMPLÈTE DU PROJET DJANGO
Analyse la structure, les modèles, les vues, les URLs et les problèmes potentiels
"""

import os
import sys
import django
import importlib
import ast
from pathlib import Path
from django.conf import settings
from django.core.management import execute_from_command_line
from django.apps import apps

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Impossible de configurer Django: {e}")
    sys.exit(1)

class ProjectAnalyzer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.issues = []
        self.stats = {
            'models': 0,
            'views': 0,
            'urls': 0,
            'templates': 0,
            'static_files': 0,
            'migrations': 0
        }

    def analyze_project_structure(self):
        """Analyse la structure du projet"""
        print("\n" + "="*80)
        print("📁 ANALYSE DE LA STRUCTURE DU PROJET")
        print("="*80)
        
        required_dirs = [
            'membres', 'paiements', 'soins', 'api', 'inscription',
            'assureur', 'medecin', 'pharmacien', 'core', 'mutuelle_core'
        ]
        
        for app in required_dirs:
            app_path = self.base_dir / app
            if app_path.exists():
                print(f"✅ {app}: Présent")
                # Compter les fichiers
                models_count = len(list(app_path.glob('models.py')))
                views_count = len(list(app_path.glob('views*.py')))
                migrations_count = len(list((app_path / 'migrations').glob('*.py'))) if (app_path / 'migrations').exists() else 0
                
                self.stats['models'] += models_count
                self.stats['views'] += views_count
                self.stats['migrations'] += migrations_count
            else:
                print(f"❌ {app}: MANQUANT")
                self.issues.append(f"Application manquante: {app}")

    def analyze_models(self):
        """Analyse les modèles Django"""
        print("\n" + "="*80)
        print("🗄️ ANALYSE DES MODÈLES")
        print("="*80)
        
        try:
            for app_config in apps.get_app_configs():
                print(f"\n📦 Application: {app_config.verbose_name}")
                models = app_config.get_models()
                
                for model in models:
                    self.stats['models'] += 1
                    print(f"   ├── Modèle: {model.__name__}")
                    print(f"   │   ├── Table: {model._meta.db_table}")
                    print(f"   │   ├── Champs: {len(model._meta.fields)}")
                    
                    # Vérifier les relations
                    relations = []
                    for field in model._meta.fields:
                        if field.is_relation:
                            relations.append(field.name)
                    
                    if relations:
                        print(f"   │   ├── Relations: {', '.join(relations)}")
                    
                    # Vérifier les index
                    indexes = model._meta.indexes
                    if indexes:
                        print(f"   │   └── Indexes: {len(indexes)}")
                    
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse des modèles: {e}")
            self.issues.append(f"Erreur modèles: {e}")

    def analyze_urls(self):
        """Analyse la configuration des URLs"""
        print("\n" + "="*80)
        print("🌐 ANALYSE DES URLS")
        print("="*80)
        
        try:
            from django.urls import get_resolver
            resolver = get_resolver()
            
            def print_urls(url_patterns, prefix='', depth=0):
                for pattern in url_patterns:
                    if hasattr(pattern, 'url_patterns'):
                        # C'est un include
                        print(f"{'   ' * depth}📁 {pattern.pattern}")
                        print_urls(pattern.url_patterns, prefix, depth + 1)
                    else:
                        # C'est une route simple
                        callback = getattr(pattern, 'callback', None)
                        if callback:
                            name = getattr(pattern, 'name', 'Sans nom')
                            print(f"{'   ' * depth}├── {pattern.pattern}")
                            print(f"{'   ' * depth}│   └── {callback.__module__}.{callback.__name__} (name: {name})")
                            self.stats['urls'] += 1
            
            print_urls(resolver.url_patterns)
            
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse des URLs: {e}")
            self.issues.append(f"Erreur URLs: {e}")

    def analyze_settings(self):
        """Analyse la configuration Django"""
        print("\n" + "="*80)
        print("⚙️ ANALYSE DES SETTINGS")
        print("="*80)
        
        critical_settings = [
            'SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS', 'DATABASES',
            'INSTALLED_APPS', 'MIDDLEWARE', 'ROOT_URLCONF'
        ]
        
        for setting in critical_settings:
            try:
                value = getattr(settings, setting, None)
                if value:
                    if setting == 'SECRET_KEY':
                        # Ne pas afficher la clé secrète en clair
                        print(f"✅ {setting}: {'***' + value[-4:] if value else 'Non défini'}")
                    elif setting == 'DATABASES':
                        db_engine = value['default']['ENGINE']
                        print(f"✅ {setting}: {db_engine}")
                    else:
                        truncated = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                        print(f"✅ {setting}: {truncated}")
                else:
                    print(f"⚠️  {setting}: Non défini")
                    self.issues.append(f"Setting manquant: {setting}")
            except Exception as e:
                print(f"❌ {setting}: Erreur - {e}")
                self.issues.append(f"Erreur setting {setting}: {e}")

    def analyze_templates_static(self):
        """Analyse les templates et fichiers statiques"""
        print("\n" + "="*80)
        print("🎨 ANALYSE DES TEMPLATES ET FICHIERS STATIQUES")
        print("="*80)
        
        # Templates
        templates_dirs = getattr(settings, 'TEMPLATES', [{}])[0].get('DIRS', [])
        print("📝 Templates directories:")
        for template_dir in templates_dirs:
            if os.path.exists(template_dir):
                template_files = list(Path(template_dir).rglob('*.html'))
                self.stats['templates'] += len(template_files)
                print(f"   ✅ {template_dir} ({len(template_files)} templates)")
            else:
                print(f"   ❌ {template_dir} (N'existe pas)")
                self.issues.append(f"Template dir manquant: {template_dir}")
        
        # Static files
        static_dirs = getattr(settings, 'STATICFILES_DIRS', [])
        print("\n📁 Static files directories:")
        for static_dir in static_dirs:
            if os.path.exists(static_dir):
                static_files = list(Path(static_dir).rglob('*.*'))
                self.stats['static_files'] += len(static_files)
                print(f"   ✅ {static_dir} ({len(static_files)} fichiers)")
            else:
                print(f"   ❌ {static_dir} (N'existe pas)")
                self.issues.append(f"Static dir manquant: {static_dir}")

    def analyze_database(self):
        """Analyse l'état de la base de données"""
        print("\n" + "="*80)
        print("🗃️ ANALYSE DE LA BASE DE DONNÉES")
        print("="*80)
        
        try:
            from django.db import connection
            from django.core.management.color import no_style
            from django.db.backends.utils import CursorWrapper
            
            with connection.cursor() as cursor:
                # Liste des tables
                if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = [row[0] for row in cursor.fetchall()]
                else:
                    # Pour PostgreSQL/MySQL
                    cursor.execute("SHOW TABLES;")
                    tables = [row[0] for row in cursor.fetchall()]
                
                print(f"📊 Tables dans la base de données: {len(tables)}")
                for table in tables:
                    cursor.execute(f"PRAGMA table_info({table});")
                    columns = cursor.fetchall()
                    print(f"   ├── {table} ({len(columns)} colonnes)")
        
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse de la base de données: {e}")
            self.issues.append(f"Erreur DB: {e}")

    def check_potential_issues(self):
        """Vérifie les problèmes potentiels"""
        print("\n" + "="*80)
        print("🔍 VÉRIFICATION DES PROBLÈMES POTENTIELS")
        print("="*80)
        
        # Vérifier les apps installées
        installed_apps = getattr(settings, 'INSTALLED_APPS', [])
        required_apps = ['membres', 'paiements', 'soins', 'inscription']
        
        for app in required_apps:
            if app not in installed_apps:
                print(f"❌ Application manquante dans INSTALLED_APPS: {app}")
                self.issues.append(f"App manquante: {app}")
            else:
                print(f"✅ Application présente: {app}")
        
        # Vérifier la configuration des médias
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        media_url = getattr(settings, 'MEDIA_URL', None)
        
        if not media_root:
            print("❌ MEDIA_ROOT non configuré")
            self.issues.append("MEDIA_ROOT non configuré")
        else:
            print(f"✅ MEDIA_ROOT: {media_root}")
            
        if not media_url:
            print("❌ MEDIA_URL non configuré")
            self.issues.append("MEDIA_URL non configuré")
        else:
            print(f"✅ MEDIA_URL: {media_url}")

    def generate_report(self):
        """Génère un rapport complet"""
        print("\n" + "="*80)
        print("📊 RAPPORT FINAL")
        print("="*80)
        
        print(f"\n📈 STATISTIQUES:")
        print(f"   ├── Modèles: {self.stats['models']}")
        print(f"   ├── Vues: {self.stats['views']}")
        print(f"   ├── URLs: {self.stats['urls']}")
        print(f"   ├── Templates: {self.stats['templates']}")
        print(f"   ├── Fichiers statiques: {self.stats['static_files']}")
        print(f"   └── Migrations: {self.stats['migrations']}")
        
        if self.issues:
            print(f"\n🚨 PROBLÈMES IDENTIFIÉS ({len(self.issues)}):")
            for i, issue in enumerate(self.issues, 1):
                print(f"   {i}. {issue}")
        else:
            print(f"\n✅ Aucun problème critique identifié!")
        
        print(f"\n💡 RECOMMANDATIONS:")
        print("   1. Vérifiez que toutes les migrations sont appliquées")
        print("   2. Testez les fonctionnalités principales")
        print("   3. Vérifiez les permissions des utilisateurs")
        print("   4. Testez les APIs REST si présentes")
        print("   5. Vérifiez la configuration en production")

    def run_full_analysis(self):
        """Exécute l'analyse complète"""
        print("🔬 LANCEMENT DE L'ANALYSE COMPLÈTE DU PROJET")
        print(f"📂 Répertoire du projet: {self.base_dir}")
        
        self.analyze_project_structure()
        self.analyze_settings()
        self.analyze_models()
        self.analyze_urls()
        self.analyze_templates_static()
        self.analyze_database()
        self.check_potential_issues()
        self.generate_report()

def main():
    """Fonction principale"""
    try:
        analyzer = ProjectAnalyzer(BASE_DIR)
        analyzer.run_full_analysis()
        
        # Vérification supplémentaire: tester les imports critiques
        print("\n" + "="*80)
        print("🧪 TEST DES IMPORTS CRITIQUES")
        print("="*80)
        
        critical_imports = [
            'membres.models.Membre',
            'django.contrib.auth.models.User',
            'rest_framework',
            'corsheaders'
        ]
        
        for import_path in critical_imports:
            try:
                module_path, class_name = import_path.rsplit('.', 1)
                module = __import__(module_path, fromlist=[class_name])
                getattr(module, class_name)
                print(f"✅ Import réussi: {import_path}")
            except ImportError as e:
                print(f"❌ Échec import: {import_path} - {e}")
        
    except Exception as e:
        print(f"💥 Erreur critique lors de l'analyse: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()