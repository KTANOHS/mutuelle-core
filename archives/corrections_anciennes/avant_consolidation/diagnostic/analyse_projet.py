#!/usr/bin/env python3
"""
Script d'analyse complète du projet Django Mutuelle
Analyse la structure, les dépendances, la configuration et les éventuels problèmes
"""

import os
import sys
import ast
import importlib
from pathlib import Path
from django.conf import settings
from django.core.management import execute_from_command_line
import django
from datetime import datetime

class ProjectAnalyzer:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.analysis_results = {
            'errors': [],
            'warnings': [],
            'info': [],
            'recommendations': []
        }
        
    def setup_django(self):
        """Configure Django pour l'analyse"""
        try:
            sys.path.insert(0, str(self.project_path))
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
            django.setup()
            return True
        except Exception as e:
            self.analysis_results['errors'].append(f"Erreur configuration Django: {e}")
            return False
    
    def analyze_project_structure(self):
        """Analyse la structure du projet"""
        print("🔍 Analyse de la structure du projet...")
        
        required_dirs = [
            'templates',
            'static',
            'media',
            'logs',
            'agents/templates',
            'agents/static'
        ]
        
        for dir_path in required_dirs:
            full_path = self.project_path / dir_path
            if full_path.exists():
                self.analysis_results['info'].append(f"✅ Répertoire trouvé: {dir_path}")
            else:
                self.analysis_results['warnings'].append(f"⚠️ Répertoire manquant: {dir_path}")
    
    def analyze_settings(self):
        """Analyse la configuration Django"""
        print("🔍 Analyse des paramètres Django...")
        
        # Vérification des paramètres critiques
        critical_settings = [
            ('SECRET_KEY', bool(settings.SECRET_KEY)),
            ('DEBUG', True),  # Juste pour info
            ('ALLOWED_HOSTS', len(settings.ALLOWED_HOSTS) > 0),
            ('DATABASES', bool(settings.DATABASES.get('default'))),
            ('INSTALLED_APPS', len(settings.INSTALLED_APPS) > 0),
        ]
        
        for setting, condition in critical_settings:
            if condition:
                self.analysis_results['info'].append(f"✅ {setting} configuré")
            else:
                self.analysis_results['errors'].append(f"❌ {setting} non configuré")
        
        # Vérification des applications installées
        required_apps = [
            'membres', 'inscription', 'paiements', 'soins', 'notifications',
            'api', 'assureur', 'medecin', 'pharmacien', 'core', 'mutuelle_core',
            'pharmacie_public', 'agents', 'communication'
        ]
        
        for app in required_apps:
            if app in settings.INSTALLED_APPS:
                self.analysis_results['info'].append(f"✅ Application installée: {app}")
            else:
                self.analysis_results['warnings'].append(f"⚠️ Application manquante: {app}")
    
    def analyze_urls(self):
        """Analyse la configuration des URLs"""
        print("🔍 Analyse des URLs...")
        
        try:
            from mutuelle_core import urls as root_urls
            url_patterns = len(root_urls.urlpatterns)
            self.analysis_results['info'].append(f"✅ {url_patterns} patterns d'URL trouvés")
        except Exception as e:
            self.analysis_results['errors'].append(f"❌ Erreur analyse URLs: {e}")
    
    def analyze_models(self):
        """Analyse les modèles Django"""
        print("🔍 Analyse des modèles...")
        
        try:
            from django.apps import apps
from django.utils import timezone
            models = apps.get_models()
            
            self.analysis_results['info'].append(f"✅ {len(models)} modèles trouvés")
            
            # Analyse des modèles par application
            app_models = {}
            for model in models:
                app_label = model._meta.app_label
                if app_label not in app_models:
                    app_models[app_label] = []
                app_models[app_label].append(model.__name__)
            
            for app, models_list in app_models.items():
                self.analysis_results['info'].append(f"  📱 {app}: {len(models_list)} modèles")
                
        except Exception as e:
            self.analysis_results['errors'].append(f"❌ Erreur analyse modèles: {e}")
    
    def analyze_static_files(self):
        """Analyse les fichiers statiques"""
        print("🔍 Analyse des fichiers statiques...")
        
        static_dirs = getattr(settings, 'STATICFILES_DIRS', [])
        static_root = getattr(settings, 'STATIC_ROOT', '')
        static_url = getattr(settings, 'STATIC_URL', '')
        
        self.analysis_results['info'].append(f"✅ URL statique: {static_url}")
        self.analysis_results['info'].append(f"✅ Racine statique: {static_root}")
        self.analysis_results['info'].append(f"✅ {len(static_dirs)} répertoire(s) statique(s)")
    
    def analyze_database(self):
        """Analyse la configuration de la base de données"""
        print("🔍 Analyse de la base de données...")
        
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT sqlite_version()")
                version = cursor.fetchone()[0]
                self.analysis_results['info'].append(f"✅ SQLite version: {version}")
        except Exception as e:
            self.analysis_results['warnings'].append(f"⚠️ Impossible de vérifier la base: {e}")
    
    def analyze_security(self):
        """Analyse la sécurité"""
        print("🔍 Analyse de sécurité...")
        
        if settings.DEBUG:
            self.analysis_results['warnings'].append("⚠️ DEBUG est activé - désactiver en production")
        
        if not settings.SECRET_KEY or settings.SECRET_KEY == 'django-insecure-':
            self.analysis_results['errors'].append("❌ SECRET_KEY non sécurisé")
        
        if not settings.ALLOWED_HOSTS:
            self.analysis_results['errors'].append("❌ ALLOWED_HOSTS vide")
    
    def analyze_agents_config(self):
        """Analyse spécifique à l'application agents"""
        print("🔍 Analyse configuration agents...")
        
        # Vérification de la configuration agents
        agents_config = getattr(settings, 'MUTUELLE_CONFIG', {})
        
        required_configs = [
            'LIMITE_BONS_QUOTIDIENNE',
            'DUREE_VALIDITE_BON'
        ]
        
        for config in required_configs:
            if config in agents_config:
                self.analysis_results['info'].append(f"✅ Configuration agent: {config} = {agents_config[config]}")
            else:
                self.analysis_results['warnings'].append(f"⚠️ Configuration agent manquante: {config}")
    
    def check_file_structure(self):
        """Vérifie la structure des fichiers importants"""
        print("🔍 Vérification des fichiers...")
        
        required_files = [
            'manage.py',
            'mutuelle_core/__init__.py',
            'mutuelle_core/settings.py',
            'mutuelle_core/urls.py',
            'mutuelle_core/wsgi.py',
            'agents/__init__.py',
            'agents/models.py',
            'agents/views.py',
            'agents/urls.py',
        ]
        
        for file_path in required_files:
            full_path = self.project_path / file_path
            if full_path.exists():
                self.analysis_results['info'].append(f"✅ Fichier trouvé: {file_path}")
            else:
                self.analysis_results['errors'].append(f"❌ Fichier manquant: {file_path}")
    
    def analyze_dependencies(self):
        """Analyse les dépendances du projet"""
        print("🔍 Analyse des dépendances...")
        
        requirements_file = self.project_path / 'requirements.txt'
        if requirements_file.exists():
            self.analysis_results['info'].append("✅ Fichier requirements.txt trouvé")
        else:
            self.analysis_results['warnings'].append("⚠️ Fichier requirements.txt manquant")
        
        # Vérification des packages critiques
        critical_packages = [
            'Django',
            'django-rest-framework',
            'django-cors-headers',
            'django-crispy-forms',
            'channels',
            'python-dotenv'
        ]
        
        for package in critical_packages:
            try:
                importlib.import_module(package.replace('-', '_'))
                self.analysis_results['info'].append(f"✅ Package installé: {package}")
            except ImportError:
                self.analysis_results['warnings'].append(f"⚠️ Package manquant: {package}")
    
    def run_migrations_check(self):
        """Vérifie l'état des migrations"""
        print("🔍 Vérification des migrations...")
        
        try:
            from django.core.management import call_command
            from io import StringIO
            
            output = StringIO()
            call_command('showmigrations', '--list', stdout=output)
            output.seek(0)
            migrations_output = output.read()
            
            # Compter les migrations appliquées et en attente
            applied = migrations_output.count('[X]')
            pending = migrations_output.count('[ ]')
            
            self.analysis_results['info'].append(f"✅ Migrations appliquées: {applied}")
            if pending > 0:
                self.analysis_results['warnings'].append(f"⚠️ Migrations en attente: {pending}")
            else:
                self.analysis_results['info'].append("✅ Toutes les migrations sont appliquées")
                
        except Exception as e:
            self.analysis_results['errors'].append(f"❌ Erreur vérification migrations: {e}")
    
    def generate_report(self):
        """Génère un rapport complet"""
        print("\n" + "="*80)
        print("📊 RAPPORT D'ANALYSE DU PROJET MUTUELLE")
        print("="*80)
        
        # Résumé
        total_errors = len(self.analysis_results['errors'])
        total_warnings = len(self.analysis_results['warnings'])
        total_info = len(self.analysis_results['info'])
        
        print(f"\n📈 RÉSUMÉ:")
        print(f"   ❌ Erreurs: {total_errors}")
        print(f"   ⚠️  Avertissements: {total_warnings}")
        print(f"   ✅ Informations: {total_info}")
        
        # Affichage des erreurs
        if self.analysis_results['errors']:
            print(f"\n❌ ERREURS CRITIQUES ({total_errors}):")
            for error in self.analysis_results['errors']:
                print(f"   • {error}")
        
        # Affichage des avertissements
        if self.analysis_results['warnings']:
            print(f"\n⚠️  AVERTISSEMENTS ({total_warnings}):")
            for warning in self.analysis_results['warnings']:
                print(f"   • {warning}")
        
        # Affichage des informations
        if self.analysis_results['info']:
            print(f"\n✅ INFORMATIONS ({total_info}):")
            for info in self.analysis_results['info'][:20]:  # Limite pour éviter overflow
                print(f"   • {info}")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        if settings.DEBUG:
            print("   • Désactiver DEBUG en production")
        if not settings.ALLOWED_HOSTS:
            print("   • Configurer ALLOWED_HOSTS")
        if total_errors == 0 and total_warnings == 0:
            print("   • ✅ Projet bien configuré!")
        else:
            print("   • Corriger les erreurs avant le déploiement")
        
        print("\n" + "="*80)
        
        # Sauvegarde du rapport
        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.project_path / f"analyse_rapport_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("RAPPORT D'ANALYSE - PROJET MUTUELLE\n")
            f.write("="*50 + "\n\n")
            
            f.write(f"Erreurs: {total_errors}\n")
            f.write(f"Avertissements: {total_warnings}\n")
            f.write(f"Informations: {total_info}\n\n")
            
            for category, items in self.analysis_results.items():
                f.write(f"\n{category.upper()}:\n")
                for item in items:
                    f.write(f"  • {item}\n")
        
        print(f"📄 Rapport sauvegardé: {report_file}")
        
        return total_errors == 0

def main():
    """Fonction principale"""
    project_path = Path(__file__).resolve().parent
    
    print("🚀 Démarrage de l'analyse du projet Mutuelle...")
    print(f"📁 Répertoire du projet: {project_path}")
    
    analyzer = ProjectAnalyzer(project_path)
    
    # Exécution des analyses
    if analyzer.setup_django():
        analyzer.analyze_project_structure()
        analyzer.check_file_structure()
        analyzer.analyze_settings()
        analyzer.analyze_urls()
        analyzer.analyze_models()
        analyzer.analyze_static_files()
        analyzer.analyze_database()
        analyzer.analyze_security()
        analyzer.analyze_agents_config()
        analyzer.analyze_dependencies()
        analyzer.run_migrations_check()
        
        # Génération du rapport
        success = analyzer.generate_report()
        
        if success:
            print("\n🎉 Analyse terminée avec succès!")
            sys.exit(0)
        else:
            print("\n❌ Des problèmes ont été détectés. Veuillez les corriger.")
            sys.exit(1)
    else:
        print("❌ Impossible de configurer Django. Vérifiez la structure du projet.")
        sys.exit(1)

if __name__ == "__main__":
    main()