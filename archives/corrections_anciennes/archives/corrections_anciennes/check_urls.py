#!/usr/bin/env python
"""
Script d'analyse des URLs Django
Vérifie tous les problèmes liés aux URLs, vues et templates
"""

import os
import sys
import django
from pathlib import Path
import re
from django.urls import get_resolver, URLResolver, URLPattern
from django.apps import apps
from django.core.management import execute_from_command_line

# Configuration Django
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

class URLAnalyzer:
    def __init__(self):
        self.problems = []
        self.all_urls = []
        self.template_refs = []

    def analyze_all(self):
        """Lance toutes les analyses"""
        print("🔍 ANALYSE COMPLÈTE DES URLs DJANGO")
        print("=" * 80)
        
        self.analyze_url_patterns()
        self.analyze_view_imports()
        self.analyze_template_urls()
        self.analyze_urls_in_code()
        self.check_missing_urls()
        
        self.report_problems()

    def analyze_url_patterns(self):
        """Analyse les patterns d'URLs définis"""
        print("\n📋 1. ANALYSE DES PATTERNS D'URLS")
        print("-" * 40)
        
        resolver = get_resolver()
        self.extract_all_urls(resolver)
        
        for url_pattern in self.all_urls:
            print(f"✅ {url_pattern['pattern']} -> {url_pattern['view']} (app: {url_pattern['app_name']})")

    def extract_all_urls(self, resolver, namespace=None, prefix=''):
        """Extrait récursivement toutes les URLs"""
        for pattern in resolver.url_patterns:
            if isinstance(pattern, URLResolver):
                # C'est un include, on descend récursivement
                new_namespace = namespace
                if pattern.namespace:
                    new_namespace = f"{namespace}:{pattern.namespace}" if namespace else pattern.namespace
                
                self.extract_all_urls(pattern, new_namespace, prefix + str(pattern.pattern))
            elif isinstance(pattern, URLPattern):
                # C'est un pattern d'URL simple
                view_name = self.get_view_name(pattern)
                app_name = namespace or 'root'
                
                self.all_urls.append({
                    'pattern': prefix + str(pattern.pattern),
                    'view': view_name,
                    'app_name': app_name,
                    'namespace': namespace,
                    'callback': pattern.callback
                })

    def get_view_name(self, pattern):
        """Récupère le nom de la vue"""
        if hasattr(pattern, 'name') and pattern.name:
            return pattern.name
        elif hasattr(pattern.callback, '__name__'):
            return pattern.callback.__name__
        else:
            return str(pattern.callback)

    def analyze_view_imports(self):
        """Vérifie que toutes les vues référencées existent"""
        print("\n👁️ 2. VÉRIFICATION DES IMPORTS DE VUES")
        print("-" * 40)
        
        for url_info in self.all_urls:
            callback = url_info['callback']
            
            if not callable(callback):
                self.problems.append({
                    'type': 'VIEW_IMPORT',
                    'message': f"Vue non callable: {url_info['pattern']} -> {callback}",
                    'severity': 'ERROR'
                })
                print(f"❌ {url_info['pattern']} -> Vue non importable")

    def analyze_template_urls(self):
        """Analyse les références aux URLs dans les templates"""
        print("\n📄 3. ANALYSE DES RÉFÉRENCES D'URLS DANS LES TEMPLATES")
        print("-" * 40)
        
        template_dirs = [
            project_dir / 'templates',
        ]
        
        url_pattern = re.compile(r'{%\s*url\s+[\'"]([^\'"]+)[\'"]\s*%}')
        url_with_var_pattern = re.compile(r'{%\s*url\s+[\'"]([^\'"]+)[\'"](?:\s+[^%]+)?\s*%}')
        
        for template_dir in template_dirs:
            if template_dir.exists():
                for template_file in template_dir.rglob('*.html'):
                    try:
                        with open(template_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Recherche toutes les références {% url %}
                        for match in url_pattern.findall(content):
                            url_name = match.strip()
                            self.template_refs.append({
                                'template': str(template_file.relative_to(project_dir)),
                                'url_name': url_name
                            })
                            
                            # Vérifie si l'URL existe
                            if not self.url_exists(url_name):
                                self.problems.append({
                                    'type': 'TEMPLATE_URL',
                                    'message': f"URL non trouvée: '{url_name}' dans {template_file.name}",
                                    'severity': 'ERROR',
                                    'file': str(template_file)
                                })
                                print(f"❌ {template_file.name}: URL '{url_name}' non trouvée")
                            else:
                                print(f"✅ {template_file.name}: URL '{url_name}' trouvée")
                                
                    except Exception as e:
                        print(f"⚠️ Erreur lecture {template_file}: {e}")

    def url_exists(self, url_name):
        """Vérifie si une URL existe dans la configuration"""
        try:
            # Séparer le namespace et le nom
            if ':' in url_name:
                namespace, name = url_name.split(':', 1)
            else:
                namespace, name = None, url_name
            
            # Vérifier dans toutes les URLs
            for url_info in self.all_urls:
                if namespace and url_info['namespace']:
                    if url_info['namespace'] == namespace and url_info['view'] == name:
                        return True
                elif url_info['view'] == name:
                    return True
            return False
        except:
            return False

    def analyze_urls_in_code(self):
        """Analyse les références aux URLs dans le code Python"""
        print("\n🐍 4. ANALYSE DES RÉFÉRENCES D'URLS DANS LE CODE")
        print("-" * 40)
        
        python_files = list(project_dir.rglob('*.py'))
        
        reverse_pattern = re.compile(r'reverse\([\'"]([^\'"]+)[\'"]')
        redirect_pattern = re.compile(r'redirect\([\'"]([^\'"]+)[\'"]')
        url_pattern = re.compile(r'url\([\'"]([^\'"]+)[\'"]')
        
        for py_file in python_files:
            if 'migrations' in str(py_file) or 'venv' in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Recherche reverse()
                for match in reverse_pattern.findall(content):
                    self.check_code_url_reference(py_file, match, 'reverse()')
                
                # Recherche redirect()
                for match in redirect_pattern.findall(content):
                    self.check_code_url_reference(py_file, match, 'redirect()')
                    
                # Recherche url()
                for match in url_pattern.findall(content):
                    self.check_code_url_reference(py_file, match, 'url()')
                    
            except Exception as e:
                print(f"⚠️ Erreur lecture {py_file}: {e}")

    def check_code_url_reference(self, file_path, url_name, context):
        """Vérifie une référence d'URL dans le code"""
        if not self.url_exists(url_name):
            self.problems.append({
                'type': 'CODE_URL',
                'message': f"URL non trouvée: '{url_name}' dans {file_path.name} ({context})",
                'severity': 'ERROR',
                'file': str(file_path)
            })
            print(f"❌ {file_path.name}: URL '{url_name}' non trouvée ({context})")
        else:
            print(f"✅ {file_path.name}: URL '{url_name}' trouvée ({context})")

    def check_missing_urls(self):
        """Vérifie les URLs manquantes pour les applications existantes"""
        print("\n🔎 5. RECHERCHE D'URLS MANQUANTES")
        print("-" * 40)
        
        apps_without_urls = []
        
        for app_config in apps.get_app_configs():
            app_name = app_config.name
            app_path = Path(app_config.path)
            
            # Vérifier si l'app a un fichier urls.py
            urls_file = app_path / 'urls.py'
            if not urls_file.exists():
                apps_without_urls.append(app_name)
                print(f"⚠️ Application '{app_name}' n'a pas de urls.py")
            else:
                print(f"✅ Application '{app_name}' a un urls.py")
                
                # Vérifier si l'app est incluse dans les URLs principales
                if not self.is_app_included(app_name):
                    self.problems.append({
                        'type': 'APP_NOT_INCLUDED',
                        'message': f"Application '{app_name}' a un urls.py mais n'est pas incluse dans les URLs principales",
                        'severity': 'WARNING'
                    })

    def is_app_included(self, app_name):
        """Vérifie si une application est incluse dans les URLs principales"""
        main_urls_file = project_dir / 'mutuelle_core' / 'urls.py'
        if main_urls_file.exists():
            with open(main_urls_file, 'r', encoding='utf-8') as f:
                content = f.read()
                return app_name in content
        return False

    def report_problems(self):
        """Génère un rapport des problèmes trouvés"""
        print("\n" + "=" * 80)
        print("📊 RAPPORT D'ANALYSE")
        print("=" * 80)
        
        if not self.problems:
            print("🎉 Aucun problème détecté !")
            return
        
        # Grouper par sévérité
        errors = [p for p in self.problems if p['severity'] == 'ERROR']
        warnings = [p for p in self.problems if p['severity'] == 'WARNING']
        
        if errors:
            print("\n❌ ERREURS CRITIQUES:")
            for error in errors:
                print(f"  • {error['message']}")
                if 'file' in error:
                    print(f"    Fichier: {error['file']}")
        
        if warnings:
            print("\n⚠️  AVERTISSEMENTS:")
            for warning in warnings:
                print(f"  • {warning['message']}")
        
        print(f"\n📈 STATISTIQUES:")
        print(f"  URLs définies: {len(self.all_urls)}")
        print(f"  Références dans templates: {len(self.template_refs)}")
        print(f"  Erreurs: {len(errors)}")
        print(f"  Avertissements: {len(warnings)}")
        
        # Suggestions de correctifs
        if errors:
            print(f"\n💡 SUGGESTIONS DE CORRECTIFS:")
            self.suggest_fixes()

    def suggest_fixes(self):
        """Suggère des correctifs pour les problèmes trouvés"""
        assureur_problems = [p for p in self.problems if 'assureur' in p['message'].lower()]
        
        if assureur_problems:
            print("\n  Pour les problèmes 'assureur':")
            print("  1. Créez le fichier assureur/urls.py")
            print("  2. Ajoutez 'assureur' dans INSTALLED_APPS")
            print("  3. Incluez les URLs dans mutuelle_core/urls.py")
            print("  4. Vérifiez que les vues existent dans assureur/views.py")

def run_django_checks():
    """Exécute les vérifications Django intégrées"""
    print("\n🔧 6. VÉRIFICATIONS DJANGO")
    print("-" * 40)
    
    try:
        # Exécute la commande check de Django
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'check'])
    except SystemExit:
        pass  # La commande check sort avec un code d'erreur

if __name__ == '__main__':
    analyzer = URLAnalyzer()
    analyzer.analyze_all()
    run_django_checks()