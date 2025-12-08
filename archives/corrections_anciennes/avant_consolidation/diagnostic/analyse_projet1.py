#!/usr/bin/env python
"""
SCRIPT D'ANALYSE COMPLÈTE DU PROJET DJANGO
Analyse la structure, les dépendances, les performances et la qualité du code
"""

import os
import sys
import ast
import glob
import json
import datetime
from pathlib import Path
from collections import defaultdict, Counter
import subprocess
import platform

class DjangoProjectAnalyzer:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.analysis_results = {
            'timestamp': datetime.datetime.now().isoformat(),
            'project_info': {},
            'apps_analysis': {},
            'models_analysis': {},
            'views_analysis': {},
            'urls_analysis': {},
            'templates_analysis': {},
            'static_analysis': {},
            'security_analysis': {},
            'performance_analysis': {},
            'agents_module_analysis': {},
            'issues': [],
            'recommendations': []
        }
    
    def analyze_project_structure(self):
        """Analyse la structure globale du projet"""
        print("🔍 Analyse de la structure du projet...")
        
        project_info = {
            'project_name': self.project_path.name,
            'total_size': self.get_directory_size(self.project_path),
            'python_files': 0,
            'template_files': 0,
            'static_files': 0,
            'database_files': 0,
            'migration_files': 0
        }
        
        # Parcours de l'arborescence
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                file_path = Path(root) / file
                if file.endswith('.py'):
                    project_info['python_files'] += 1
                elif file.endswith('.html'):
                    project_info['template_files'] += 1
                elif file.endswith(('.css', '.js', '.png', '.jpg', '.jpeg')):
                    project_info['static_files'] += 1
                elif file.endswith('.sqlite3'):
                    project_info['database_files'] += 1
                elif 'migrations' in str(file_path) and file.endswith('.py'):
                    project_info['migration_files'] += 1
        
        self.analysis_results['project_info'] = project_info
    
    def analyze_django_apps(self):
        """Analyse toutes les applications Django"""
        print("📱 Analyse des applications Django...")
        
        apps_path = self.project_path
        apps = []
        
        # Recherche des applications Django
        for item in apps_path.iterdir():
            if item.is_dir() and not item.name.startswith('.') and not item.name.startswith('__'):
                # Vérifie si c'est une app Django (présence de models.py ou views.py)
                if (item / 'models.py').exists() or (item / 'views.py').exists():
                    apps.append(item.name)
        
        for app_name in apps:
            app_analysis = self.analyze_single_app(app_name)
            self.analysis_results['apps_analysis'][app_name] = app_analysis
    
    def analyze_single_app(self, app_name):
        """Analyse une application spécifique"""
        app_path = self.project_path / app_name
        analysis = {
            'name': app_name,
            'models_count': 0,
            'views_count': 0,
            'urls_count': 0,
            'templates_count': 0,
            'static_files_count': 0,
            'models_list': [],
            'views_list': [],
            'url_patterns': [],
            'dependencies': []
        }
        
        # Analyse des modèles
        models_file = app_path / 'models.py'
        if models_file.exists():
            models_info = self.analyze_models_file(models_file)
            analysis['models_count'] = models_info['count']
            analysis['models_list'] = models_info['models']
        
        # Analyse des vues
        views_file = app_path / 'views.py'
        if views_file.exists():
            views_info = self.analyze_views_file(views_file)
            analysis['views_count'] = views_info['count']
            analysis['views_list'] = views_info['views']
        
        # Analyse des URLs
        urls_file = app_path / 'urls.py'
        if urls_file.exists():
            urls_info = self.analyze_urls_file(urls_file)
            analysis['urls_count'] = urls_info['count']
            analysis['url_patterns'] = urls_info['patterns']
        
        # Analyse des templates
        templates_path = self.project_path / 'templates' / app_name
        if templates_path.exists():
            analysis['templates_count'] = len(list(templates_path.glob('**/*.html')))
        
        # Analyse des dépendances
        analysis['dependencies'] = self.analyze_dependencies(app_path)
        
        return analysis
    
    def analyze_models_file(self, models_file):
        """Analyse un fichier models.py"""
        try:
            with open(models_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            models = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Vérifie si c'est un modèle Django
                    for base in node.bases:
                        if isinstance(base, ast.Name) and 'Model' in base.id:
                            models.append(node.name)
                            break
            
            return {'count': len(models), 'models': models}
        except Exception as e:
            return {'count': 0, 'models': [], 'error': str(e)}
    
    def analyze_views_file(self, views_file):
        """Analyse un fichier views.py"""
        try:
            with open(views_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            views = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Vérifie les décorateurs communs pour les vues Django
                    for decorator in node.decorator_list:
                        decorator_name = self.get_decorator_name(decorator)
                        if decorator_name in ['login_required', 'user_passes_test', 'permission_required']:
                            views.append(node.name)
                            break
                    else:
                        # Si pas de décorateur spécifique, considère comme vue
                        views.append(node.name)
            
            return {'count': len(views), 'views': views}
        except Exception as e:
            return {'count': 0, 'views': [], 'error': str(e)}
    
    def analyze_urls_file(self, urls_file):
        """Analyse un fichier urls.py"""
        try:
            with open(urls_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            patterns = []
            # Recherche simple des patterns d'URL
            lines = content.split('\n')
            for line in lines:
                if 'path(' in line or 're_path(' in line:
                    patterns.append(line.strip())
            
            return {'count': len(patterns), 'patterns': patterns}
        except Exception as e:
            return {'count': 0, 'patterns': [], 'error': str(e)}
    
    def analyze_dependencies(self, app_path):
        """Analyse les dépendances d'une application"""
        dependencies = []
        
        # Analyse des imports dans les fichiers Python
        for py_file in app_path.glob('**/*.py'):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            dependencies.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            dependencies.append(node.module)
            except:
                continue
        
        return list(set(dependencies))
    
    def analyze_agents_module_specifically(self):
        """Analyse spécifique du module agents"""
        print("🎯 Analyse spécifique du module agents...")
        
        agents_path = self.project_path / 'agents'
        if not agents_path.exists():
            self.analysis_results['agents_module_analysis']['error'] = "Module agents non trouvé"
            return
        
        analysis = {
            'models': self.analyze_agents_models(),
            'views': self.analyze_agents_views(),
            'urls': self.analyze_agents_urls(),
            'templates': self.analyze_agents_templates(),
            'functionality_coverage': self.analyze_agents_functionality(),
            'performance_metrics': self.analyze_agents_performance()
        }
        
        self.analysis_results['agents_module_analysis'] = analysis
    
    def analyze_agents_models(self):
        """Analyse détaillée des modèles agents"""
        models_file = self.project_path / 'agents' / 'models.py'
        if not models_file.exists():
            return {'error': 'Fichier models.py non trouvé'}
        
        try:
            with open(models_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            models = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for base in node.bases:
                        if isinstance(base, ast.Name) and 'Model' in base.id:
                            model_info = {
                                'name': node.name,
                                'fields': [],
                                'methods': []
                            }
                            
                            # Analyse des champs et méthodes
                            for item in node.body:
                                if isinstance(item, ast.Assign):
                                    for target in item.targets:
                                        if isinstance(target, ast.Name):
                                            model_info['fields'].append(target.id)
                                elif isinstance(item, ast.FunctionDef):
                                    model_info['methods'].append(item.name)
                            
                            models.append(model_info)
            
            return {'count': len(models), 'models': models}
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_agents_views(self):
        """Analyse détaillée des vues agents"""
        views_file = self.project_path / 'agents' / 'views.py'
        if not views_file.exists():
            return {'error': 'Fichier views.py non trouvé'}
        
        try:
            with open(views_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            views = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    view_info = {
                        'name': node.name,
                        'decorators': [],
                        'parameters': [arg.arg for arg in node.args.args],
                        'lines_of_code': len(node.body)
                    }
                    
                    # Analyse des décorateurs
                    for decorator in node.decorator_list:
                        decorator_name = self.get_decorator_name(decorator)
                        view_info['decorators'].append(decorator_name)
                    
                    views.append(view_info)
            
            return {'count': len(views), 'views': views}
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_agents_urls(self):
        """Analyse détaillée des URLs agents"""
        urls_file = self.project_path / 'agents' / 'urls.py'
        if not urls_file.exists():
            return {'error': 'Fichier urls.py non trouvé'}
        
        try:
            with open(urls_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analyse plus précise des URLs
            tree = ast.parse(content)
            url_patterns = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if (isinstance(node.func, ast.Name) and 
                        node.func.id in ['path', 're_path']):
                        
                        # Extraction des arguments
                        args = []
                        for arg in node.args:
                            if isinstance(arg, ast.Str):
                                args.append(arg.s)
                            elif isinstance(arg, ast.Constant):
                                args.append(arg.value)
                        
                        if len(args) >= 2:
                            url_patterns.append({
                                'pattern': args[0],
                                'view': args[1] if isinstance(args[1], str) else 'fonction/vue',
                                'name': self.extract_url_name(node)
                            })
            
            return {'count': len(url_patterns), 'patterns': url_patterns}
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_agents_templates(self):
        """Analyse des templates agents"""
        templates_path = self.project_path / 'templates' / 'agents'
        if not templates_path.exists():
            return {'error': 'Dossier templates/agents non trouvé'}
        
        templates = []
        for template_file in templates_path.glob('**/*.html'):
            template_info = {
                'name': template_file.name,
                'path': str(template_file.relative_to(self.project_path / 'templates')),
                'size': template_file.stat().st_size,
                'lines': self.count_file_lines(template_file)
            }
            templates.append(template_info)
        
        return {'count': len(templates), 'templates': templates}
    
    def analyze_agents_functionality(self):
        """Analyse la couverture fonctionnelle du module agents"""
        functionality = {
            'gestion_membres': False,
            'bons_soin': False,
            'verification_cotisations': False,
            'communication': False,
            'rapports': False,
            'tableau_bord': False
        }
        
        # Vérification basée sur l'analyse des vues et URLs
        views_analysis = self.analyze_agents_views()
        urls_analysis = self.analyze_agents_urls()
        
        if 'views' in views_analysis:
            view_names = [view['name'].lower() for view in views_analysis['views']]
            url_patterns = [pattern['pattern'].lower() for pattern in urls_analysis.get('patterns', [])]
            
            functionality['gestion_membres'] = any('membre' in name for name in view_names) or any('membre' in pattern for pattern in url_patterns)
            functionality['bons_soin'] = any('bon' in name for name in view_names) or any('bon' in pattern for pattern in url_patterns)
            functionality['verification_cotisations'] = any('cotisation' in name for name in view_names) or any('cotisation' in pattern for pattern in url_patterns)
            functionality['communication'] = any('message' in name or 'notification' in name for name in view_names)
            functionality['rapports'] = any('rapport' in name or 'performance' in name for name in view_names)
            functionality['tableau_bord'] = any('dashboard' in name or 'tableau' in name for name in view_names)
        
        return functionality
    
    def analyze_agents_performance(self):
        """Analyse les métriques de performance du module agents"""
        views_file = self.project_path / 'agents' / 'views.py'
        if not views_file.exists():
            return {'error': 'Fichier views.py non trouvé'}
        
        try:
            with open(views_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            metrics = {
                'total_views': 0,
                'views_with_decorators': 0,
                'average_lines_per_view': 0,
                'complex_views': 0  # vues avec plus de 50 lignes
            }
            
            tree = ast.parse(content)
            views = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    metrics['total_views'] += 1
                    lines = len(node.body)
                    metrics['average_lines_per_view'] += lines
                    
                    if node.decorator_list:
                        metrics['views_with_decorators'] += 1
                    
                    if lines > 50:
                        metrics['complex_views'] += 1
            
            if metrics['total_views'] > 0:
                metrics['average_lines_per_view'] = metrics['average_lines_per_view'] / metrics['total_views']
            
            return metrics
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_security(self):
        """Analyse de sécurité du projet"""
        print("🔒 Analyse de sécurité...")
        
        security_issues = []
        
        # Vérification des settings
        settings_file = self.project_path / 'settings.py'
        if settings_file.exists():
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings_content = f.read()
            
            if 'DEBUG = True' in settings_content:
                security_issues.append("DEBUG est activé - désactiver en production")
            
            if 'SECRET_KEY' in settings_content and 'get_random_secret_key' not in settings_content:
                security_issues.append("Clé secrète potentiellement exposée")
        
        # Vérification des vues sans authentification
        for app_name, app_analysis in self.analysis_results['apps_analysis'].items():
            if 'views' in app_analysis:
                for view in app_analysis['views']:
                    if not any(decorator in ['login_required', 'permission_required'] 
                              for decorator in view.get('decorators', [])):
                        security_issues.append(f"Vue {view['name']} dans {app_name} sans authentification")
        
        self.analysis_results['security_analysis']['issues'] = security_issues
    
    def analyze_performance(self):
        """Analyse des performances"""
        print("⚡ Analyse des performances...")
        
        performance_metrics = {
            'total_models': 0,
            'total_views': 0,
            'total_templates': 0,
            'large_models': 0,  # modèles avec plus de 10 champs
            'complex_views': 0  # vues avec plus de 100 lignes
        }
        
        for app_name, app_analysis in self.analysis_results['apps_analysis'].items():
            performance_metrics['total_models'] += app_analysis.get('models_count', 0)
            performance_metrics['total_views'] += app_analysis.get('views_count', 0)
            performance_metrics['total_templates'] += app_analysis.get('templates_count', 0)
        
        self.analysis_results['performance_analysis'] = performance_metrics
    
    def generate_recommendations(self):
        """Génère des recommandations basées sur l'analyse"""
        recommendations = []
        
        # Recommandations basées sur l'analyse des agents
        agents_analysis = self.analysis_results.get('agents_module_analysis', {})
        
        if agents_analysis:
            functionality = agents_analysis.get('functionality_coverage', {})
            
            if not functionality.get('gestion_membres'):
                recommendations.append("🔧 Module agents: Implémenter la gestion complète des membres")
            
            if not functionality.get('communication'):
                recommendations.append("🔧 Module agents: Ajouter le système de communication")
            
            if not functionality.get('rapports'):
                recommendations.append("🔧 Module agents: Développer les fonctionnalités de reporting")
        
        # Recommandations générales
        if self.analysis_results['project_info']['python_files'] > 100:
            recommendations.append("📁 Structurer le code en modules plus petits")
        
        security_issues = self.analysis_results['security_analysis'].get('issues', [])
        if security_issues:
            recommendations.append("🔒 Corriger les problèmes de sécurité identifiés")
        
        self.analysis_results['recommendations'] = recommendations
    
    def generate_report(self, output_file='rapport_analyse_projet.json'):
        """Génère un rapport complet"""
        print(f"📊 Génération du rapport: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
        
        # Génère également un résumé texte
        self.generate_text_summary(output_file.replace('.json', '_resume.txt'))
    
    def generate_text_summary(self, output_file):
        """Génère un résumé texte du rapport"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RAPPORT D'ANALYSE DU PROJET DJANGO\n")
            f.write("=" * 80 + "\n\n")
            
            # Informations générales
            f.write("📋 INFORMATIONS GÉNÉRALES\n")
            f.write("-" * 40 + "\n")
            project_info = self.analysis_results['project_info']
            f.write(f"Projet: {project_info['project_name']}\n")
            f.write(f"Fichiers Python: {project_info['python_files']}\n")
            f.write(f"Templates: {project_info['template_files']}\n")
            f.write(f"Fichiers statiques: {project_info['static_files']}\n")
            f.write(f"Migrations: {project_info['migration_files']}\n\n")
            
            # Applications
            f.write("📱 APPLICATIONS DJANGO\n")
            f.write("-" * 40 + "\n")
            for app_name, app_analysis in self.analysis_results['apps_analysis'].items():
                f.write(f"🔹 {app_name}:\n")
                f.write(f"   - Modèles: {app_analysis.get('models_count', 0)}\n")
                f.write(f"   - Vues: {app_analysis.get('views_count', 0)}\n")
                f.write(f"   - URLs: {app_analysis.get('urls_count', 0)}\n")
                f.write(f"   - Templates: {app_analysis.get('templates_count', 0)}\n\n")
            
            # Analyse spécifique du module agents
            f.write("🎯 MODULE AGENTS - ANALYSE DÉTAILLÉE\n")
            f.write("-" * 40 + "\n")
            agents_analysis = self.analysis_results.get('agents_module_analysis', {})
            if agents_analysis:
                f.write(f"Modèles: {agents_analysis.get('models', {}).get('count', 0)}\n")
                f.write(f"Vues: {agents_analysis.get('views', {}).get('count', 0)}\n")
                f.write(f"URLs: {agents_analysis.get('urls', {}).get('count', 0)}\n")
                f.write(f"Templates: {agents_analysis.get('templates', {}).get('count', 0)}\n\n")
                
                # Couverture fonctionnelle
                functionality = agents_analysis.get('functionality_coverage', {})
                f.write("📊 COUVERTURE FONCTIONNELLE:\n")
                for feature, implemented in functionality.items():
                    status = "✅" if implemented else "❌"
                    f.write(f"   {status} {feature.replace('_', ' ').title()}\n")
                f.write("\n")
            
            # Recommandations
            f.write("💡 RECOMMANDATIONS\n")
            f.write("-" * 40 + "\n")
            for recommendation in self.analysis_results.get('recommendations', []):
                f.write(f"• {recommendation}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"Rapport généré le: {self.analysis_results['timestamp']}\n")
            f.write("=" * 80 + "\n")
    
    # Méthodes utilitaires
    def get_directory_size(self, path):
        """Calcule la taille d'un répertoire"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        return total_size
    
    def get_decorator_name(self, decorator):
        """Extrait le nom d'un décorateur"""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id
        return "unknown"
    
    def extract_url_name(self, node):
        """Extrait le nom d'une URL"""
        for keyword in node.keywords:
            if keyword.arg == 'name' and isinstance(keyword.value, ast.Str):
                return keyword.value.s
        return "unnamed"
    
    def count_file_lines(self, file_path):
        """Compte le nombre de lignes d'un fichier"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return len(f.readlines())
        except:
            return 0

def main():
    """Fonction principale"""
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = input("Entrez le chemin du projet Django: ").strip()
    
    if not os.path.exists(project_path):
        print("❌ Le chemin spécifié n'existe pas!")
        sys.exit(1)
    
    print(f"🔍 Analyse du projet: {project_path}")
    print("=" * 60)
    
    analyzer = DjangoProjectAnalyzer(project_path)
    
    # Exécution des analyses
    analyzer.analyze_project_structure()
    analyzer.analyze_django_apps()
    analyzer.analyze_agents_module_specifically()
    analyzer.analyze_security()
    analyzer.analyze_performance()
    analyzer.generate_recommendations()
    analyzer.generate_report()
    
    print("✅ Analyse terminée!")
    print(f"📄 Rapport généré: rapport_analyse_projet.json")
    print(f"📋 Résumé généré: rapport_analyse_projet_resume.txt")

if __name__ == "__main__":
    main()