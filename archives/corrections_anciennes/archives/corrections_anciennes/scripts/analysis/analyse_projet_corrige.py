#!/usr/bin/env python3
"""
Script d'analyse complète d'un projet Django - VERSION CORRIGÉE
"""

import os
import ast
import sys
from pathlib import Path
import django
from django.conf import settings

# Configuration Django minimale pour pouvoir importer les modules
if not settings.configured:
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'api',
            'assureur',
            'core',
            'medecin',
            'membres',
            'mutuelle_core',
            'paiements',
            'pharmacien',
            'soins',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        },
        SECRET_KEY='temp-key-for-analysis',
    )

django.setup()

class ProjectAnalyzer:
    def __init__(self, project_root='.'):
        self.project_root = Path(project_root)
        self.results = {
            'apps': {},
            'models': {},
            'views': {},
            'urls': {},
            'templates': {},
            'static': {},
            'issues': []
        }
    
    def analyze_project_structure(self):
        """Analyse la structure du projet"""
        print("🔍 Analyse de la structure du projet...")
        
        # Applications Django
        apps = ['api', 'assureur', 'core', 'medecin', 'membres', 'mutuelle_core', 'paiements', 'pharmacien', 'soins']
        
        for app in apps:
            app_path = self.project_root / app
            if app_path.exists():
                self.results['apps'][app] = {
                    'models': 1 if (app_path / 'models.py').exists() else 0,
                    'views': 1 if (app_path / 'views.py').exists() else 0,
                    'urls': 1 if (app_path / 'urls.py').exists() else 0,
                    'migrations': len(list(app_path.glob('migrations/*.py'))),
                    'templates': len(list(app_path.glob('templates/**/*.html'))),
                }
    
    def analyze_python_files(self):
        """Analyse les fichiers Python pour détecter les problèmes"""
        print("📊 Analyse des fichiers Python...")
        
        python_files = list(self.project_root.rglob('*.py'))
        
        for py_file in python_files:
            if 'venv' in str(py_file) or 'migrations' in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Analyse syntaxique basique
                try:
                    tree = ast.parse(content)
                    self.results['issues'].extend(self._check_python_issues(py_file, content, tree))
                    
                except SyntaxError as e:
                    self.results['issues'].append({
                        'type': 'Syntax Error',
                        'file': str(py_file.relative_to(self.project_root)),
                        'line': e.lineno,
                        'message': str(e)
                    })
                    
            except Exception as e:
                self.results['issues'].append({
                    'type': 'File Error',
                    'file': str(py_file.relative_to(self.project_root)),
                    'message': f"Impossible de lire le fichier: {e}"
                })
    
    def _check_python_issues(self, file_path, content, tree):
        """Détecte les problèmes spécifiques dans le code Python"""
        issues = []
        relative_path = file_path.relative_to(self.project_root)
        
        # Vérification des imports Django courants
        if 'urls.py' in str(file_path) or 'views.py' in str(file_path):
            if 'from django.conf import settings' not in content and 'settings' in content:
                issues.append({
                    'type': 'Import Manquant',
                    'file': str(relative_path),
                    'message': 'Import manquant: from django.conf import settings'
                })
        
        return issues
    
    def analyze_urls(self):
        """Analyse la configuration des URLs"""
        print("🌐 Analyse des configurations d'URLs...")
        
        try:
            # Analyser le fichier urls.py principal
            main_urls = self.project_root / 'mutuelle_core' / 'urls.py'
            if main_urls.exists():
                with open(main_urls, 'r') as f:
                    content = f.read()
                
                # Vérifier les inclusions d'URLs
                if 'include(' in content:
                    include_count = content.count('include(')
                    self.results['urls']['main_includes'] = include_count
                
                # Vérifier les patterns d'URL
                if 'urlpatterns' in content:
                    self.results['urls']['has_urlpatterns'] = True
        
        except Exception as e:
            self.results['issues'].append({
                'type': 'URLs Analysis',
                'message': f"Erreur lors de l'analyse des URLs: {e}"
            })
    
    def analyze_templates(self):
        """Analyse les templates HTML"""
        print("📄 Analyse des templates...")
        
        template_dirs = [
            self.project_root / 'templates',
            *[self.project_root / app / 'templates' for app in self.results['apps'].keys()]
        ]
        
        for template_dir in template_dirs:
            if template_dir.exists():
                html_files = list(template_dir.rglob('*.html'))
                self.results['templates'][str(template_dir.relative_to(self.project_root))] = len(html_files)
    
    def analyze_database(self):
        """Analyse la base de données"""
        print("💾 Analyse de la base de données...")
        
        db_file = self.project_root / 'db.sqlite3'
        if db_file.exists():
            db_size = db_file.stat().st_size
            self.results['database'] = {
                'size_mb': round(db_size / (1024 * 1024), 2),
                'exists': True
            }
        else:
            self.results['database'] = {'exists': False}
    
    def generate_report(self):
        """Génère un rapport détaillé"""
        print("\n" + "="*80)
        print("📋 RAPPORT D'ANALYSE DU PROJET DJANGO")
        print("="*80)
        
        # Structure du projet
        print(f"\n🏗️  STRUCTURE DU PROJET:")
        print(f"Applications détectées: {len(self.results['apps'])}")
        for app, details in self.results['apps'].items():
            print(f"  📁 {app}:")
            print(f"    - Modèles: {'✅' if details['models'] else '❌'}")
            print(f"    - Vues: {'✅' if details['views'] else '❌'}")
            print(f"    - URLs: {'✅' if details['urls'] else '❌'}")
            print(f"    - Migrations: {details['migrations']}")
            print(f"    - Templates: {details['templates']}")
        
        # Base de données
        if 'database' in self.results:
            db_info = self.results['database']
            if db_info.get('exists'):
                print(f"\n💾 BASE DE DONNÉES:")
                print(f"  Taille: {db_info['size_mb']} MB")
            else:
                print(f"\n❌ Base de données non trouvée")
        
        # Templates
        if self.results['templates']:
            print(f"\n📄 TEMPLATES:")
            total_templates = sum(self.results['templates'].values())
            print(f"  Total: {total_templates} templates")
            for dir_path, count in self.results['templates'].items():
                print(f"  {dir_path}: {count} templates")
        
        # Problèmes détectés
        if self.results['issues']:
            print(f"\n⚠️  PROBLÈMES DÉTECTÉS ({len(self.results['issues'])}):")
            for issue in self.results['issues'][:10]:
                print(f"  🔸 {issue['type']} - {issue.get('file', 'N/A')}")
                print(f"     {issue['message']}")
            
            if len(self.results['issues']) > 10:
                print(f"  ... et {len(self.results['issues']) - 10} autres problèmes")
        else:
            print(f"\n✅ Aucun problème détecté!")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        self._generate_recommendations()
    
    def _generate_recommendations(self):
        """Génère des recommandations basées sur l'analyse"""
        recommendations = []
        
        # Vérifier la présence de requirements.txt
        requirements_file = self.project_root / 'requirements.txt'
        if not requirements_file.exists():
            recommendations.append("Créer un fichier requirements.txt pour les dépendances")
        
        # Vérifier les applications sans migrations
        for app, details in self.results['apps'].items():
            if details['migrations'] == 0 and details['models']:
                recommendations.append(f"Appliquer les migrations pour l'application {app}")
        
        # Vérifier les applications sans urls.py
        for app, details in self.results['apps'].items():
            if not details['urls']:
                recommendations.append(f"Créer un fichier urls.py pour l'application {app}")
        
        # Afficher les recommandations
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        
        if not recommendations:
            print("  ✅ Aucune recommandation spécifique pour le moment")

    def run_full_analysis(self):
        """Exécute l'analyse complète"""
        print("🚀 Démarrage de l'analyse complète du projet...\n")
        
        self.analyze_project_structure()
        self.analyze_python_files()
        self.analyze_urls()
        self.analyze_templates()
        self.analyze_database()
        
        self.generate_report()

def main():
    """Fonction principale"""
    analyzer = ProjectAnalyzer()
    analyzer.run_full_analysis()

if __name__ == "__main__":
    main()#!/usr/bin/env python3
"""
Script d'analyse complète d'un projet Django - VERSION CORRIGÉE
"""

import os
import ast
import sys
from pathlib import Path
import django
from django.conf import settings

# Configuration Django minimale pour pouvoir importer les modules
if not settings.configured:
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'api',
            'assureur',
            'core',
            'medecin',
            'membres',
            'mutuelle_core',
            'paiements',
            'pharmacien',
            'soins',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        },
        SECRET_KEY='temp-key-for-analysis',
    )

django.setup()

class ProjectAnalyzer:
    def __init__(self, project_root='.'):
        self.project_root = Path(project_root)
        self.results = {
            'apps': {},
            'models': {},
            'views': {},
            'urls': {},
            'templates': {},
            'static': {},
            'issues': []
        }
    
    def analyze_project_structure(self):
        """Analyse la structure du projet"""
        print("🔍 Analyse de la structure du projet...")
        
        # Applications Django
        apps = ['api', 'assureur', 'core', 'medecin', 'membres', 'mutuelle_core', 'paiements', 'pharmacien', 'soins']
        
        for app in apps:
            app_path = self.project_root / app
            if app_path.exists():
                self.results['apps'][app] = {
                    'models': 1 if (app_path / 'models.py').exists() else 0,
                    'views': 1 if (app_path / 'views.py').exists() else 0,
                    'urls': 1 if (app_path / 'urls.py').exists() else 0,
                    'migrations': len(list(app_path.glob('migrations/*.py'))),
                    'templates': len(list(app_path.glob('templates/**/*.html'))),
                }
    
    def analyze_python_files(self):
        """Analyse les fichiers Python pour détecter les problèmes"""
        print("📊 Analyse des fichiers Python...")
        
        python_files = list(self.project_root.rglob('*.py'))
        
        for py_file in python_files:
            if 'venv' in str(py_file) or 'migrations' in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Analyse syntaxique basique
                try:
                    tree = ast.parse(content)
                    self.results['issues'].extend(self._check_python_issues(py_file, content, tree))
                    
                except SyntaxError as e:
                    self.results['issues'].append({
                        'type': 'Syntax Error',
                        'file': str(py_file.relative_to(self.project_root)),
                        'line': e.lineno,
                        'message': str(e)
                    })
                    
            except Exception as e:
                self.results['issues'].append({
                    'type': 'File Error',
                    'file': str(py_file.relative_to(self.project_root)),
                    'message': f"Impossible de lire le fichier: {e}"
                })
    
    def _check_python_issues(self, file_path, content, tree):
        """Détecte les problèmes spécifiques dans le code Python"""
        issues = []
        relative_path = file_path.relative_to(self.project_root)
        
        # Vérification des imports Django courants
        if 'urls.py' in str(file_path) or 'views.py' in str(file_path):
            if 'from django.conf import settings' not in content and 'settings' in content:
                issues.append({
                    'type': 'Import Manquant',
                    'file': str(relative_path),
                    'message': 'Import manquant: from django.conf import settings'
                })
        
        return issues
    
    def analyze_urls(self):
        """Analyse la configuration des URLs"""
        print("🌐 Analyse des configurations d'URLs...")
        
        try:
            # Analyser le fichier urls.py principal
            main_urls = self.project_root / 'mutuelle_core' / 'urls.py'
            if main_urls.exists():
                with open(main_urls, 'r') as f:
                    content = f.read()
                
                # Vérifier les inclusions d'URLs
                if 'include(' in content:
                    include_count = content.count('include(')
                    self.results['urls']['main_includes'] = include_count
                
                # Vérifier les patterns d'URL
                if 'urlpatterns' in content:
                    self.results['urls']['has_urlpatterns'] = True
        
        except Exception as e:
            self.results['issues'].append({
                'type': 'URLs Analysis',
                'message': f"Erreur lors de l'analyse des URLs: {e}"
            })
    
    def analyze_templates(self):
        """Analyse les templates HTML"""
        print("📄 Analyse des templates...")
        
        template_dirs = [
            self.project_root / 'templates',
            *[self.project_root / app / 'templates' for app in self.results['apps'].keys()]
        ]
        
        for template_dir in template_dirs:
            if template_dir.exists():
                html_files = list(template_dir.rglob('*.html'))
                self.results['templates'][str(template_dir.relative_to(self.project_root))] = len(html_files)
    
    def analyze_database(self):
        """Analyse la base de données"""
        print("💾 Analyse de la base de données...")
        
        db_file = self.project_root / 'db.sqlite3'
        if db_file.exists():
            db_size = db_file.stat().st_size
            self.results['database'] = {
                'size_mb': round(db_size / (1024 * 1024), 2),
                'exists': True
            }
        else:
            self.results['database'] = {'exists': False}
    
    def generate_report(self):
        """Génère un rapport détaillé"""
        print("\n" + "="*80)
        print("📋 RAPPORT D'ANALYSE DU PROJET DJANGO")
        print("="*80)
        
        # Structure du projet
        print(f"\n🏗️  STRUCTURE DU PROJET:")
        print(f"Applications détectées: {len(self.results['apps'])}")
        for app, details in self.results['apps'].items():
            print(f"  📁 {app}:")
            print(f"    - Modèles: {'✅' if details['models'] else '❌'}")
            print(f"    - Vues: {'✅' if details['views'] else '❌'}")
            print(f"    - URLs: {'✅' if details['urls'] else '❌'}")
            print(f"    - Migrations: {details['migrations']}")
            print(f"    - Templates: {details['templates']}")
        
        # Base de données
        if 'database' in self.results:
            db_info = self.results['database']
            if db_info.get('exists'):
                print(f"\n💾 BASE DE DONNÉES:")
                print(f"  Taille: {db_info['size_mb']} MB")
            else:
                print(f"\n❌ Base de données non trouvée")
        
        # Templates
        if self.results['templates']:
            print(f"\n📄 TEMPLATES:")
            total_templates = sum(self.results['templates'].values())
            print(f"  Total: {total_templates} templates")
            for dir_path, count in self.results['templates'].items():
                print(f"  {dir_path}: {count} templates")
        
        # Problèmes détectés
        if self.results['issues']:
            print(f"\n⚠️  PROBLÈMES DÉTECTÉS ({len(self.results['issues'])}):")
            for issue in self.results['issues'][:10]:
                print(f"  🔸 {issue['type']} - {issue.get('file', 'N/A')}")
                print(f"     {issue['message']}")
            
            if len(self.results['issues']) > 10:
                print(f"  ... et {len(self.results['issues']) - 10} autres problèmes")
        else:
            print(f"\n✅ Aucun problème détecté!")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        self._generate_recommendations()
    
    def _generate_recommendations(self):
        """Génère des recommandations basées sur l'analyse"""
        recommendations = []
        
        # Vérifier la présence de requirements.txt
        requirements_file = self.project_root / 'requirements.txt'
        if not requirements_file.exists():
            recommendations.append("Créer un fichier requirements.txt pour les dépendances")
        
        # Vérifier les applications sans migrations
        for app, details in self.results['apps'].items():
            if details['migrations'] == 0 and details['models']:
                recommendations.append(f"Appliquer les migrations pour l'application {app}")
        
        # Vérifier les applications sans urls.py
        for app, details in self.results['apps'].items():
            if not details['urls']:
                recommendations.append(f"Créer un fichier urls.py pour l'application {app}")
        
        # Afficher les recommandations
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        
        if not recommendations:
            print("  ✅ Aucune recommandation spécifique pour le moment")

    def run_full_analysis(self):
        """Exécute l'analyse complète"""
        print("🚀 Démarrage de l'analyse complète du projet...\n")
        
        self.analyze_project_structure()
        self.analyze_python_files()
        self.analyze_urls()
        self.analyze_templates()
        self.analyze_database()
        
        self.generate_report()

def main():
    """Fonction principale"""
    analyzer = ProjectAnalyzer()
    analyzer.run_full_analysis()

if __name__ == "__main__":
    main()