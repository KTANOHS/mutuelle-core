#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE COMPLÈTE DU PROJET DJANGO
Analyse la structure, les dépendances, la configuration et les problèmes potentiels
"""

import os
import sys
import ast
import importlib
import inspect
from pathlib import Path
from django.conf import settings
from django.core.management import execute_from_command_line
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

class ProjectAnalyzer:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.issues = []
        self.warnings = []
        self.recommendations = []
        
    def analyze_project_structure(self):
        """Analyse la structure du projet"""
        print("=" * 60)
        print("📁 ANALYSE DE LA STRUCTURE DU PROJET")
        print("=" * 60)
        
        required_dirs = [
            'templates',
            'static',
            'media',
            'logs',
            'locale'
        ]
        
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                print(f"✅ Dossier {dir_name}: {dir_path}")
            else:
                print(f"❌ Dossier manquant: {dir_name}")
                self.issues.append(f"Dossier manquant: {dir_name}")
    
    def analyze_settings(self):
        """Analyse la configuration Django"""
        print("\n" + "=" * 60)
        print("⚙️ ANALYSE DE LA CONFIGURATION DJANGO")
        print("=" * 60)
        
        # Vérification des settings critiques
        critical_settings = {
            'SECRET_KEY': settings.SECRET_KEY,
            'DEBUG': settings.DEBUG,
            'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
            'DATABASES': settings.DATABASES,
            'INSTALLED_APPS': settings.INSTALLED_APPS,
        }
        
        for setting, value in critical_settings.items():
            print(f"🔧 {setting}: {value}")
            
        # Vérification sécurité en production
        if not settings.DEBUG:
            security_checks = [
                ('SESSION_COOKIE_SECURE', settings.SESSION_COOKIE_SECURE),
                ('CSRF_COOKIE_SECURE', settings.CSRF_COOKIE_SECURE),
                ('SECURE_SSL_REDIRECT', getattr(settings, 'SECURE_SSL_REDIRECT', False)),
            ]
            
            for check_name, check_value in security_checks:
                if not check_value:
                    self.warnings.append(f"Setting de sécurité manquant: {check_name}")
    
    def analyze_apps(self):
        """Analyse toutes les applications Django"""
        print("\n" + "=" * 60)
        print("📱 ANALYSE DES APPLICATIONS")
        print("=" * 60)
        
        for app in settings.INSTALLED_APPS:
            if not app.startswith('django.'):
                print(f"\n🔍 Application: {app}")
                self.analyze_single_app(app)
    
    def analyze_single_app(self, app_name):
        """Analyse une application spécifique"""
        try:
            app_module = importlib.import_module(app_name)
            app_path = Path(app_module.__file__).parent
            
            # Vérification des fichiers essentiels
            essential_files = ['models.py', 'views.py', 'urls.py', 'admin.py']
            for file in essential_files:
                file_path = app_path / file
                if file_path.exists():
                    print(f"   ✅ {file}: Présent")
                    
                    # Analyse spécifique pour models.py
                    if file == 'models.py':
                        self.analyze_models(app_name)
                else:
                    print(f"   ⚠️ {file}: Absent")
                    
            # Vérification des dossiers templates et static
            templates_dir = app_path / 'templates'
            static_dir = app_path / 'static'
            
            if templates_dir.exists():
                print(f"   ✅ templates/: Présent ({len(list(templates_dir.rglob('*.html')))} fichiers)")
            if static_dir.exists():
                print(f"   ✅ static/: Présent")
                
        except ImportError as e:
            print(f"   ❌ Impossible d'importer l'application {app_name}: {e}")
            self.issues.append(f"Application inaccessible: {app_name}")
    
    def analyze_models(self, app_name):
        """Analyse les modèles d'une application"""
        try:
            models_module = importlib.import_module(f'{app_name}.models')
            
            # Récupération de tous les modèles
            models = []
            for name, obj in inspect.getmembers(models_module):
                if inspect.isclass(obj) and hasattr(obj, '_meta'):
                    models.append(name)
                    
            if models:
                print(f"   📊 Modèles: {', '.join(models)}")
            else:
                print(f"   ℹ️ Aucun modèle défini")
                
        except Exception as e:
            print(f"   ❌ Erreur analyse modèles: {e}")
    
    def analyze_urls(self):
        """Analyse la configuration des URLs"""
        print("\n" + "=" * 60)
        print("🌐 ANALYSE DES URLS")
        print("=" * 60)
        
        try:
            from django.urls import get_resolver
            resolver = get_resolver()
            url_patterns = self.extract_url_patterns(resolver)
            
            print(f"Nombre total d'URLs: {len(url_patterns)}")
            
            # URLs par application
            app_urls = {}
            for pattern in url_patterns:
                app_name = pattern.get('app_name', 'core')
                if app_name not in app_urls:
                    app_urls[app_name] = []
                app_urls[app_name].append(pattern)
            
            for app, patterns in app_urls.items():
                print(f"📱 {app}: {len(patterns)} URLs")
                
        except Exception as e:
            print(f"❌ Erreur analyse URLs: {e}")
    
    def extract_url_patterns(self, resolver, namespace='', prefix=''):
        """Extrait récursivement tous les patterns d'URL"""
        patterns = []
        
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):
                # C'est un include
                new_namespace = namespace
                if pattern.namespace:
                    new_namespace = f"{namespace}:{pattern.namespace}" if namespace else pattern.namespace
                
                patterns.extend(self.extract_url_patterns(
                    pattern, 
                    new_namespace, 
                    prefix + str(pattern.pattern)
                ))
            else:
                # C'est un pattern simple
                pattern_info = {
                    'pattern': prefix + str(pattern.pattern),
                    'name': pattern.name,
                    'app_name': getattr(pattern, 'app_name', 'core'),
                    'namespace': namespace
                }
                patterns.append(pattern_info)
                
        return patterns
    
    def analyze_database(self):
        """Analyse la configuration et l'état de la base de données"""
        print("\n" + "=" * 60)
        print("🗄️ ANALYSE DE LA BASE DE DONNÉES")
        print("=" * 60)
        
        db_config = settings.DATABASES['default']
        print(f"Moteur: {db_config['ENGINE']}")
        print(f"Base: {db_config['NAME']}")
        
        # Vérification des migrations en attente
        try:
            from django.core.management import call_command
            from io import StringIO
            
            output = StringIO()
            call_command('showmigrations', '--list', stdout=output)
            output.seek(0)
            migrations = output.read()
            
            if '[ ]' in migrations:
                self.warnings.append("Migrations en attente détectées")
                print("⚠️ Migrations en attente détectées")
            else:
                print("✅ Toutes les migrations sont appliquées")
                
        except Exception as e:
            print(f"❌ Erreur vérification migrations: {e}")
    
    def analyze_dependencies(self):
        """Analyse les dépendances du projet"""
        print("\n" + "=" * 60)
        print("📦 ANALYSE DES DÉPENDANCES")
        print("=" * 60)
        
        requirements_file = self.project_root / 'requirements.txt'
        if requirements_file.exists():
            print("📋 requirements.txt trouvé")
            with open(requirements_file, 'r') as f:
                dependencies = f.readlines()
                print(f"Nombre de dépendances: {len(dependencies)}")
        else:
            self.warnings.append("Fichier requirements.txt manquant")
    
    def analyze_security(self):
        """Analyse les aspects sécurité"""
        print("\n" + "=" * 60)
        print("🔒 ANALYSE DE SÉCURITÉ")
        print("=" * 60)
        
        # Vérifications de sécurité
        security_checks = [
            ('DEBUG mode', settings.DEBUG, False, "DEBUG devrait être False en production"),
            ('Secret Key par défaut', 'django-insecure' in settings.SECRET_KEY, False, "Secret Key ne devrait pas être la valeur par défaut"),
            ('Allowed Hosts vide', not settings.ALLOWED_HOSTS, False, "ALLOWED_HOSTS devrait être configuré"),
        ]
        
        for check_name, current, expected, message in security_checks:
            if current != expected:
                print(f"✅ {check_name}: Correct")
            else:
                print(f"❌ {check_name}: {message}")
                self.issues.append(message)
    
    def generate_report(self):
        """Génère un rapport complet"""
        print("\n" + "=" * 60)
        print("📊 RAPPORT D'ANALYSE COMPLET")
        print("=" * 60)
        
        print(f"\n📈 STATISTIQUES:")
        print(f"   • Problèmes critiques: {len(self.issues)}")
        print(f"   • Avertissements: {len(self.warnings)}")
        print(f"   • Recommandations: {len(self.recommendations)}")
        
        if self.issues:
            print(f"\n🚨 PROBLÈMES CRITIQUES:")
            for issue in self.issues:
                print(f"   • {issue}")
        
        if self.warnings:
            print(f"\n⚠️ AVERTISSEMENTS:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if self.recommendations:
            print(f"\n💡 RECOMMANDATIONS:")
            for rec in self.recommendations:
                print(f"   • {rec}")
        
        # Recommandations générales
        print(f"\n🎯 ACTIONS RECOMMANDÉES:")
        print("   1. Vérifier que toutes les migrations sont appliquées")
        print("   2. Tester les fonctionnalités principales")
        print("   3. Vérifier la configuration de production")
        print("   4. Tester les APIs et WebSockets")
        print("   5. Vérifier les permissions des agents")
    
    def run_full_analysis(self):
        """Exécute l'analyse complète"""
        print("🚀 LANCEMENT DE L'ANALYSE COMPLÈTE DU PROJET")
        print(f"📁 Répertoire du projet: {self.project_root}")
        
        self.analyze_project_structure()
        self.analyze_settings()
        self.analyze_apps()
        self.analyze_urls()
        self.analyze_database()
        self.analyze_dependencies()
        self.analyze_security()
        self.generate_report()

def main():
    """Fonction principale"""
    project_root = Path(__file__).parent
    
    analyzer = ProjectAnalyzer(project_root)
    analyzer.run_full_analysis()
    
    # Retour code d'erreur
    return 1 if analyzer.issues else 0

if __name__ == "__main__":
    sys.exit(main())