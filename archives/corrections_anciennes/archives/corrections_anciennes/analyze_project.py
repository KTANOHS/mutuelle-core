# analyze_project.py
import os
import sys
import ast
import inspect
from pathlib import Path
import django
from django.apps import apps
from django.conf import settings
from django.core.checks import run_checks
from django.core.management import execute_from_command_line

class DjangoProjectAnalyzer:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.issues = []
        self.stats = {
            'models': 0,
            'views': 0,
            'urls': 0,
            'templates': 0,
            'static_files': 0,
            'migrations': 0
        }
    
    def setup_django(self):
        """Configure l'environnement Django"""
        try:
            # Trouver le répertoire contenant manage.py
            manage_py = self.project_path / 'manage.py'
            if not manage_py.exists():
                raise FileNotFoundError("manage.py non trouvé")
            
            # Ajouter le chemin du projet au Python path
            sys.path.insert(0, str(self.project_path))
            
            # Trouver le nom du module settings
            settings_module = None
            for item in self.project_path.iterdir():
                if item.is_dir() and (item / 'settings.py').exists():
                    settings_module = f"{item.name}.settings"
                    break
            
            if not settings_module:
                raise ImportError("Impossible de trouver le module settings")
            
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
            django.setup()
            
            print(f"✅ Django configuré avec le module: {settings_module}")
            return True
        except Exception as e:
            self.issues.append(f"❌ Erreur configuration Django: {e}")
            return False
    
    def analyze_settings(self):
        """Analyse la configuration Django"""
        print("\n🔧 ANALYSE DES SETTINGS")
        
        checks = [
            ('DEBUG', settings.DEBUG, not settings.DEBUG, "DEBUG devrait être False en production"),
            ('SECRET_KEY', bool(settings.SECRET_KEY), True, "SECRET_KEY est configuré"),
            ('ALLOWED_HOSTS', len(settings.ALLOWED_HOSTS) > 0, True, "ALLOWED_HOSTS est configuré"),
            ('DATABASES', 'default' in settings.DATABASES, True, "Base de données configurée"),
            ('INSTALLED_APPS', len(settings.INSTALLED_APPS) > 0, True, "Applications installées"),
            ('MIDDLEWARE', len(settings.MIDDLEWARE) > 0, True, "Middleware configuré"),
        ]
        
        for setting, value, expected, message in checks:
            status = "✅" if value == expected else "❌"
            print(f"  {status} {setting}: {message}")
            
            if value != expected:
                self.issues.append(f"Setting {setting}: {message}")
    
    def analyze_models(self):
        """Analyse tous les modèles Django"""
        print("\n🗄️ ANALYSE DES MODÈLES")
        
        try:
            for app_config in apps.get_app_configs():
                print(f"\n  📱 Application: {app_config.verbose_name}")
                
                for model in app_config.get_models():
                    self.stats['models'] += 1
                    print(f"    📊 Modèle: {model.__name__}")
                    
                    # Analyser les champs du modèle
                    fields = model._meta.get_fields()
                    print(f"      📋 Champs: {len(fields)}")
                    
                    # Vérifier les éventuels problèmes
                    for field in fields:
                        if hasattr(field, 'related_model') and field.related_model:
                            print(f"      🔗 Relation: {field.name} -> {field.related_model.__name__}")
                    
                    # Vérifier la méthode __str__
                    if '__str__' in model.__dict__:
                        print("      ✅ Méthode __str__ définie")
                    else:
                        print("      ⚠️ Méthode __str__ manquante")
                        self.issues.append(f"Modèle {model.__name__}: méthode __str__ manquante")
        
        except Exception as e:
            self.issues.append(f"Erreur analyse modèles: {e}")
    
    def analyze_views(self):
        """Analyse les vues Django"""
        print("\n👁️ ANALYSE DES VUES")
        
        views_count = 0
        for app_config in apps.get_app_configs():
            app_path = Path(app_config.path)
            views_file = app_path / 'views.py'
            
            if views_file.exists():
                try:
                    with open(views_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Compter les fonctions de vue
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            # Vérifier si c'est une vue (contient request en paramètre)
                            for arg in node.args.args:
                                if arg.arg == 'request':
                                    views_count += 1
                                    print(f"  👁️ Vue: {node.name} dans {app_config.name}")
                                    break
                
                except Exception as e:
                    self.issues.append(f"Erreur analyse vues {app_config.name}: {e}")
        
        self.stats['views'] = views_count
        print(f"  📊 Total vues trouvées: {views_count}")
    
    def analyze_urls(self):
        """Analyse les configurations d'URLs"""
        print("\n🔗 ANALYSE DES URLs")
        
        try:
            from django.urls import get_resolver
            resolver = get_resolver()
            
            def count_urls(patterns, prefix=''):
                count = 0
                for pattern in patterns:
                    if hasattr(pattern, 'pattern'):
                        count += 1
                        url_name = getattr(pattern, 'name', 'sans-nom')
                        print(f"  🌐 URL: {prefix}{pattern.pattern} -> {url_name}")
                    
                    if hasattr(pattern, 'url_patterns'):
                        count += count_urls(pattern.url_patterns, prefix + str(pattern.pattern))
                
                return count
            
            total_urls = count_urls(resolver.url_patterns)
            self.stats['urls'] = total_urls
            print(f"  📊 Total URLs configurées: {total_urls}")
            
        except Exception as e:
            self.issues.append(f"Erreur analyse URLs: {e}")
    
    def analyze_templates(self):
        """Analyse les templates"""
        print("\n🎨 ANALYSE DES TEMPLATES")
        
        template_dirs = getattr(settings, 'TEMPLATES', [{}])[0].get('DIRS', [])
        template_dirs.extend([app.path for app in apps.get_app_configs()])
        
        template_count = 0
        for template_dir in template_dirs:
            template_path = Path(template_dir)
            if template_path.exists():
                for ext in ['*.html', '*.htm']:
                    for template_file in template_path.rglob(ext):
                        template_count += 1
                        print(f"  📄 Template: {template_file.relative_to(self.project_path)}")
        
        self.stats['templates'] = template_count
        print(f"  📊 Total templates trouvés: {template_count}")
    
    def analyze_static_files(self):
        """Analyse les fichiers statiques"""
        print("\n📁 ANALYSE DES FICHIERS STATIQUES")
        
        static_dirs = getattr(settings, 'STATICFILES_DIRS', [])
        static_count = 0
        
        for static_dir in static_dirs:
            static_path = Path(static_dir)
            if static_path.exists():
                for ext in ['*.css', '*.js', '*.png', '*.jpg', '*.jpeg', '*.gif', '*.svg']:
                    for static_file in static_path.rglob(ext):
                        static_count += 1
                        if static_count <= 10:  # Limiter l'affichage
                            print(f"  🖼️ Static: {static_file.relative_to(self.project_path)}")
        
        self.stats['static_files'] = static_count
        print(f"  📊 Total fichiers statiques: {static_count}")
    
    def analyze_migrations(self):
        """Analyse les migrations"""
        print("\n🔄 ANALYSE DES MIGRATIONS")
        
        migration_count = 0
        for app_config in apps.get_app_configs():
            migrations_path = Path(app_config.path) / 'migrations'
            if migrations_path.exists():
                for migration_file in migrations_path.glob('*.py'):
                    if migration_file.name != '__init__.py':
                        migration_count += 1
                        print(f"  📦 Migration: {migration_file.relative_to(self.project_path)}")
        
        self.stats['migrations'] = migration_count
        print(f"  📊 Total fichiers de migration: {migration_count}")
    
    def run_django_checks(self):
        """Exécute les vérifications Django intégrées"""
        print("\n🔍 VÉRIFICATIONS DJANGO AUTOMATIQUES")
        
        try:
            errors = run_checks()
            if errors:
                for error in errors:
                    print(f"  ❌ {error}")
                    self.issues.append(f"Check Django: {error}")
            else:
                print("  ✅ Aucune erreur détectée par les vérifications Django")
        except Exception as e:
            self.issues.append(f"Erreur vérifications Django: {e}")
    
    def check_database(self):
        """Vérifie la configuration de la base de données"""
        print("\n🗃️ VÉRIFICATION BASE DE DONNÉES")
        
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            print("  ✅ Connexion BD fonctionnelle")
        except Exception as e:
            print(f"  ❌ Erreur connexion BD: {e}")
            self.issues.append(f"Base de données: {e}")
    
    def generate_report(self):
        """Génère un rapport complet"""
        print("\n" + "="*60)
        print("📊 RAPPORT D'ANALYSE COMPLET")
        print("="*60)
        
        print(f"\n📈 STATISTIQUES:")
        print(f"  📊 Modèles: {self.stats['models']}")
        print(f"  👁️ Vues: {self.stats['views']}")
        print(f"  🔗 URLs: {self.stats['urls']}")
        print(f"  🎨 Templates: {self.stats['templates']}")
        print(f"  📁 Fichiers statiques: {self.stats['static_files']}")
        print(f"  🔄 Migrations: {self.stats['migrations']}")
        
        if self.issues:
            print(f"\n🚨 PROBLÈMES IDENTIFIÉS ({len(self.issues)}):")
            for issue in self.issues:
                print(f"  ❌ {issue}")
        else:
            print(f"\n✅ Aucun problème identifié!")
        
        print(f"\n💡 RECOMMANDATIONS:")
        if settings.DEBUG:
            print("  ⚠️ DEBUG est True - désactiver en production")
        if not settings.ALLOWED_HOSTS:
            print("  ⚠️ ALLOWED_HOSTS est vide - configurer pour la production")
        if self.stats['models'] == 0:
            print("  ⚠️ Aucun modèle détecté - vérifier les applications")
        
        print(f"\n🎯 PROCHAINES ÉTAPES:")
        print("  1. Résoudre les problèmes identifiés ci-dessus")
        print("  2. Exécuter les migrations: python manage.py migrate")
        print("  3. Créer un superutilisateur: python manage.py createsuperuser")
        print("  4. Tester l'application: python manage.py runserver")
    
    def analyze(self):
        """Exécute l'analyse complète"""
        print("🚀 DÉMARRAGE DE L'ANALYSE DU PROJET DJANGO")
        print("="*60)
        
        if not self.setup_django():
            print("❌ Impossible de configurer Django - arrêt de l'analyse")
            return
        
        # Exécuter toutes les analyses
        self.analyze_settings()
        self.analyze_models()
        self.analyze_views()
        self.analyze_urls()
        self.analyze_templates()
        self.analyze_static_files()
        self.analyze_migrations()
        self.run_django_checks()
        self.check_database()
        
        # Générer le rapport final
        self.generate_report()

def main():
    """Fonction principale"""
    # Déterminer automatiquement le chemin du projet
    current_dir = Path(__file__).parent
    project_path = current_dir
    
    # Vérifier si nous sommes dans le bon répertoire
    if not (project_path / 'manage.py').exists():
        print("❌ manage.py non trouvé dans le répertoire courant")
        print("💡 Exécutez ce script depuis la racine de votre projet Django")
        return
    
    print(f"📁 Analyse du projet: {project_path}")
    
    # Créer et exécuter l'analyseur
    analyzer = DjangoProjectAnalyzer(project_path)
    analyzer.analyze()

if __name__ == "__main__":
    main()