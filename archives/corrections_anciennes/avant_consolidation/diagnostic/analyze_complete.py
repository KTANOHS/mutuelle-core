#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE COMPLÈTE DE L'ARBORESCENCE DU PROJET
Auteur: Assistant Technique
Date: 2024
Description: Analyse exhaustive de toute la structure du projet Django
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

# =============================================================================
# CONFIGURATION DES COULEURS
# =============================================================================

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# =============================================================================
# CLASSES D'ANALYSE
# =============================================================================

class FileAnalyzer:
    """Analyse un fichier individuel"""
    
    @staticmethod
    def analyze(file_path):
        """Analyse complète d'un fichier"""
        try:
            stat = file_path.stat()
            info = {
                'path': str(file_path),
                'name': file_path.name,
                'size': stat.st_size,
                'size_human': FileAnalyzer.human_size(stat.st_size),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'created': datetime.fromtimestamp(stat.st_ctime),
                'is_file': True,
                'is_dir': False,
            }
            
            # Analyse spécifique par extension
            if file_path.suffix.lower() in ['.py', '.html', '.js', '.css', '.json', '.txt', '.md', '.sh']:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    info['lines'] = content.count('\n') + 1
                    info['content_hash'] = hashlib.md5(content.encode()).hexdigest()[:8]
                    
                    # Analyse spécifique Python
                    if file_path.suffix.lower() == '.py':
                        info['python_info'] = FileAnalyzer.analyze_python_file(content, file_path)
                    
                    # Analyse spécifique HTML
                    elif file_path.suffix.lower() == '.html':
                        info['html_info'] = FileAnalyzer.analyze_html_file(content)
                
                except Exception as e:
                    info['read_error'] = str(e)
                    info['lines'] = 0
            
            return info
            
        except Exception as e:
            return {
                'path': str(file_path),
                'name': file_path.name,
                'error': str(e),
                'is_file': True,
                'is_dir': False,
            }
    
    @staticmethod
    def analyze_python_file(content, file_path):
        """Analyse spécifique d'un fichier Python"""
        info = {
            'imports': [],
            'classes': [],
            'functions': [],
            'decorators': [],
            'models_count': 0,
            'views_count': 0,
            'urls_count': 0,
        }
        
        import re
        
        # Détecter les imports
        import_pattern = r'^(?:from\s+(\S+)\s+import|import\s+([\w\s,]+))'
        imports = re.findall(import_pattern, content, re.MULTILINE)
        for imp in imports:
            info['imports'].append(imp[0] if imp[0] else imp[1])
        
        # Détecter les classes
        class_pattern = r'^class\s+(\w+)'
        info['classes'] = re.findall(class_pattern, content, re.MULTILINE)
        
        # Détecter les fonctions
        func_pattern = r'^def\s+(\w+)\s*\('
        info['functions'] = re.findall(func_pattern, content, re.MULTILINE)
        
        # Détecter les décorateurs
        decorator_pattern = r'^@(\w+)'
        info['decorators'] = re.findall(decorator_pattern, content, re.MULTILINE)
        
        # Compter les modèles, vues, URLs basé sur le nom du fichier
        if file_path.name == 'models.py':
            info['models_count'] = len(info['classes'])
        elif file_path.name == 'views.py':
            info['views_count'] = len(info['functions']) + len(info['classes'])
        elif file_path.name == 'urls.py':
            info['urls_count'] = content.count('path(') + content.count('url(')
        
        return info
    
    @staticmethod
    def analyze_html_file(content):
        """Analyse spécifique d'un fichier HTML"""
        info = {
            'templates_used': [],
            'blocks': [],
            'includes': [],
            'forms': 0,
            'tables': 0,
        }
        
        import re
        
        # Détecter les templates Django
        template_pattern = r'\{%\s*(?:extends|include)\s+[\'"]([^\'"]+)[\'"]'
        info['templates_used'] = re.findall(template_pattern, content)
        
        # Détecter les blocs
        block_pattern = r'\{%\s*block\s+(\w+)'
        info['blocks'] = re.findall(block_pattern, content)
        
        # Détecter les includes
        include_pattern = r'\{%\s*include\s+[\'"]([^\'"]+)[\'"]'
        info['includes'] = re.findall(include_pattern, content)
        
        # Compter les formulaires et tables
        info['forms'] = content.count('<form')
        info['tables'] = content.count('<table')
        
        return info
    
    @staticmethod
    def human_size(size_bytes):
        """Convertit la taille en format lisible"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

class ProjectAnalyzer:
    """Analyse complète du projet"""
    
    def __init__(self, project_path):
        self.project_path = Path(project_path).resolve()
        self.excluded_patterns = [
            '__pycache__', '.pyc', '.pyo', '.pyd', '.so',
            '.DS_Store', 'Thumbs.db', 'desktop.ini',
            'node_modules', 'venv', '.venv', 'env', '.env',
            '.git', '.svn', '.hg', '.idea', '.vscode',
            '*.log', '*.tmp', '*.temp', '*.bak', '*.backup',
        ]
        self.results = {
            'project_path': str(self.project_path),
            'analysis_date': datetime.now().isoformat(),
            'summary': defaultdict(int),
            'files_by_type': defaultdict(list),
            'files_by_size': defaultdict(list),
            'duplicate_files': defaultdict(list),
            'largest_files': [],
            'oldest_files': [],
            'applications': {},
            'issues': [],
            'statistics': defaultdict(int),
        }
    
    def should_exclude(self, path):
        """Vérifie si un chemin doit être exclu"""
        path_str = str(path)
        name = path.name
        
        for pattern in self.excluded_patterns:
            if pattern.startswith('*'):
                if name.endswith(pattern[1:]):
                    return True
            elif pattern in name or pattern in path_str:
                return True
        
        return False
    
    def analyze_directory(self, dir_path, depth=0, max_depth=5):
        """Analyse récursive d'un répertoire"""
        if depth > max_depth:
            return []
        
        items = []
        
        try:
            for item in dir_path.iterdir():
                if self.should_exclude(item):
                    continue
                
                if item.is_dir():
                    dir_info = {
                        'path': str(item),
                        'name': item.name,
                        'is_dir': True,
                        'is_file': False,
                        'items': self.analyze_directory(item, depth + 1, max_depth),
                        'file_count': 0,
                        'dir_count': 0,
                        'total_size': 0,
                    }
                    
                    # Compter les fichiers et dossiers
                    for subitem in dir_info['items']:
                        if subitem.get('is_dir'):
                            dir_info['dir_count'] += 1
                        else:
                            dir_info['file_count'] += 1
                            dir_info['total_size'] += subitem.get('size', 0)
                    
                    items.append(dir_info)
                    
                else:
                    file_info = FileAnalyzer.analyze(item)
                    
                    # Mettre à jour les statistiques globales
                    self.update_statistics(item, file_info)
                    
                    items.append(file_info)
        
        except PermissionError:
            self.results['issues'].append(f"Permission refusée: {dir_path}")
        except Exception as e:
            self.results['issues'].append(f"Erreur dans {dir_path}: {str(e)}")
        
        return items
    
    def update_statistics(self, file_path, file_info):
        """Met à jour les statistiques globales"""
        # Par type de fichier
        ext = file_path.suffix.lower()
        self.results['files_by_type'][ext].append(file_info)
        
        # Par taille
        size = file_info.get('size', 0)
        if size > 1024 * 1024:  # > 1MB
            self.results['files_by_size']['large'].append(file_info)
        elif size > 1024 * 100:  # > 100KB
            self.results['files_by_size']['medium'].append(file_info)
        else:
            self.results['files_by_size']['small'].append(file_info)
        
        # Les plus gros fichiers
        self.results['largest_files'].append(file_info)
        self.results['largest_files'].sort(key=lambda x: x.get('size', 0), reverse=True)
        self.results['largest_files'] = self.results['largest_files'][:100]
        
        # Les plus vieux fichiers
        self.results['oldest_files'].append(file_info)
        self.results['oldest_files'].sort(key=lambda x: x.get('created', datetime.now()))
        self.results['oldest_files'] = self.results['oldest_files'][:100]
        
        # Statistiques générales
        self.results['summary']['total_files'] += 1
        self.results['summary']['total_size'] += size
        
        # Par extension spécifique
        if ext in ['.py', '.html', '.js', '.css', '.json', '.txt', '.md', '.sh']:
            self.results['statistics'][f'files_{ext[1:]}'] += 1
        
        # Détection des doublons par hash
        if 'content_hash' in file_info:
            self.results['duplicate_files'][file_info['content_hash']].append(file_info)
    
    def analyze_django_applications(self):
        """Analyse spécifique des applications Django"""
        apps = {}
        
        for item in self.project_path.iterdir():
            if item.is_dir():
                # Vérifier si c'est une application Django
                is_django_app = False
                app_info = {'name': item.name, 'files': {}}
                
                # Vérifier les fichiers Django essentiels
                for file_name in ['models.py', 'views.py', 'urls.py', 'admin.py', 'apps.py']:
                    file_path = item / file_name
                    if file_path.exists():
                        is_django_app = True
                        app_info['files'][file_name] = FileAnalyzer.analyze(file_path)
                
                if is_django_app:
                    # Analyser les templates
                    templates_dir = item / 'templates'
                    if templates_dir.exists():
                        app_info['templates'] = self.analyze_directory(templates_dir, max_depth=3)
                    
                    # Analyser les fichiers statiques
                    static_dir = item / 'static'
                    if static_dir.exists():
                        app_info['static'] = self.analyze_directory(static_dir, max_depth=3)
                    
                    apps[item.name] = app_info
        
        self.results['applications'] = apps
        self.results['summary']['django_apps'] = len(apps)
    
    def analyze_special_files(self):
        """Analyse des fichiers spéciaux (scripts, tests, etc.)"""
        special_categories = {
            'correction': ['correction', 'fix', 'correct', 'repair'],
            'test': ['test', 'test_', '_test'],
            'diagnostic': ['diagnostic', 'analyze', 'analyse', 'check'],
            'script': ['script', '.sh', '.bat'],
            'report': ['report', 'rapport', 'log'],
            'config': ['settings', 'config', '.env', 'requirements'],
        }
        
        for category, patterns in special_categories.items():
            self.results[category] = []
        
        # Parcourir tous les fichiers analysés
        def search_files(items):
            for item in items:
                if item.get('is_dir'):
                    search_files(item.get('items', []))
                else:
                    path_lower = item['path'].lower()
                    name_lower = item['name'].lower()
                    
                    for category, patterns in special_categories.items():
                        for pattern in patterns:
                            if pattern in path_lower or pattern in name_lower:
                                self.results[category].append(item)
                                break
        
        search_files(self.results.get('structure', []))
    
    def generate_report(self):
        """Génère un rapport complet"""
        print(f"{Colors.BOLD}{Colors.MAGENTA}🔍 ANALYSE COMPLÈTE DU PROJET{Colors.END}")
        print(f"{Colors.GRAY}Projet: {self.project_path}{Colors.END}")
        print(f"{Colors.GRAY}Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
        print("=" * 100)
        
        # Analyse de la structure
        print(f"\n{Colors.BOLD}{Colors.CYAN}📁 STRUCTURE DU PROJET{Colors.END}")
        self.results['structure'] = self.analyze_directory(self.project_path, max_depth=3)
        
        # Analyse des applications Django
        print(f"\n{Colors.BOLD}{Colors.CYAN}🎯 APPLICATIONS DJANGO{Colors.END}")
        self.analyze_django_applications()
        
        # Analyse des fichiers spéciaux
        print(f"\n{Colors.BOLD}{Colors.CYAN}🔧 FICHIERS SPÉCIAUX{Colors.END}")
        self.analyze_special_files()
        
        # Générer les statistiques
        self.generate_statistics()
        
        # Générer les rapports
        self.save_reports()
        
        return self.results
    
    def generate_statistics(self):
        """Génère les statistiques globales"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}📊 STATISTIQUES GLOBALES{Colors.END}")
        
        # Statistiques de base
        stats = self.results['summary']
        print(f"  • Fichiers totaux: {stats.get('total_files', 0):,}")
        print(f"  • Taille totale: {FileAnalyzer.human_size(stats.get('total_size', 0))}")
        print(f"  • Applications Django: {stats.get('django_apps', 0)}")
        
        # Par type de fichier
        print(f"\n  {Colors.YELLOW}📄 RÉPARTITION PAR TYPE:{Colors.END}")
        type_stats = Counter()
        for ext, files in self.results['files_by_type'].items():
            type_stats[ext] = len(files)
        
        for ext, count in type_stats.most_common(10):
            print(f"    {ext}: {count:,} fichiers")
        
        # Fichiers de correction
        print(f"\n  {Colors.YELLOW}🔧 FICHIERS DE CORRECTION/TEST:{Colors.END}")
        for category in ['correction', 'test', 'diagnostic']:
            count = len(self.results.get(category, []))
            if count > 0:
                print(f"    {category}: {count:,} fichiers")
        
        # Les plus gros fichiers
        print(f"\n  {Colors.YELLOW}🏆 LES 10 PLUS GROS FICHIERS:{Colors.END}")
        for i, file_info in enumerate(self.results['largest_files'][:10], 1):
            print(f"    {i}. {file_info['name']} ({file_info['size_human']})")
        
        # Fichiers en double
        duplicate_count = sum(1 for files in self.results['duplicate_files'].values() if len(files) > 1)
        if duplicate_count > 0:
            print(f"\n  {Colors.YELLOW}⚠️  FICHIERS EN DOUBLE DÉTECTÉS:{Colors.END}")
            print(f"    {duplicate_count} groupes de doublons")
    
    def save_reports(self):
        """Sauvegarde les rapports dans des fichiers"""
        import json
        
        # Rapport JSON complet
        json_report = self.project_path / 'complete_project_analysis.json'
        
        # Fonction pour sérialiser les objets datetime
        def json_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, Path):
                return str(obj)
            raise TypeError(f"Type {type(obj)} not serializable")
        
        with open(json_report, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=json_serializer)
        
        print(f"\n{Colors.GREEN}✅ Rapport JSON sauvegardé: {json_report}{Colors.END}")
        
        # Rapport texte résumé
        text_report = self.project_path / 'project_analysis_summary.txt'
        with open(text_report, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RAPPORT D'ANALYSE COMPLÈTE DU PROJET\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Projet: {self.project_path}\n")
            f.write(f"Date d'analyse: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("📊 STATISTIQUES GLOBALES\n")
            f.write("-" * 40 + "\n")
            f.write(f"Fichiers totaux: {self.results['summary'].get('total_files', 0):,}\n")
            f.write(f"Taille totale: {FileAnalyzer.human_size(self.results['summary'].get('total_size', 0))}\n")
            f.write(f"Applications Django: {self.results['summary'].get('django_apps', 0)}\n\n")
            
            f.write("📁 APPLICATIONS DJANGO\n")
            f.write("-" * 40 + "\n")
            for app_name, app_info in self.results['applications'].items():
                f.write(f"\n{app_name}:\n")
                for file_name in ['models.py', 'views.py', 'urls.py', 'admin.py', 'apps.py']:
                    if file_name in app_info['files']:
                        file_data = app_info['files'][file_name]
                        if 'python_info' in file_data:
                            pi = file_data['python_info']
                            f.write(f"  - {file_name}: ")
                            if file_name == 'models.py':
                                f.write(f"{pi.get('models_count', 0)} modèles\n")
                            elif file_name == 'views.py':
                                f.write(f"{pi.get('views_count', 0)} vues\n")
                            elif file_name == 'urls.py':
                                f.write(f"{pi.get('urls_count', 0)} URLs\n")
                            else:
                                f.write("✓\n")
                        else:
                            f.write(f"  - {file_name}: ✓\n")
            
            f.write("\n🔧 FICHIERS DE CORRECTION/TEST\n")
            f.write("-" * 40 + "\n")
            for category in ['correction', 'test', 'diagnostic']:
                files = self.results.get(category, [])
                if files:
                    f.write(f"\n{category.upper()} ({len(files)} fichiers):\n")
                    for file_info in files[:20]:  # Limiter à 20
                        f.write(f"  - {file_info['name']} ({file_info['size_human']})\n")
                    if len(files) > 20:
                        f.write(f"  ... et {len(files) - 20} autres\n")
            
            f.write("\n⚠️  PROBLÈMES IDENTIFIÉS\n")
            f.write("-" * 40 + "\n")
            for issue in self.results.get('issues', []):
                f.write(f"• {issue}\n")
            if not self.results.get('issues'):
                f.write("Aucun problème majeur détecté\n")
        
        print(f"{Colors.GREEN}✅ Résumé texte sauvegardé: {text_report}{Colors.END}")
        
        # Rapport CSV des fichiers
        csv_report = self.project_path / 'project_files.csv'
        try:
            import csv
            
            with open(csv_report, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Chemin', 'Nom', 'Taille', 'Lignes', 'Modifié', 'Type'])
                
                def write_files(items):
                    for item in items:
                        if item.get('is_dir'):
                            write_files(item.get('items', []))
                        else:
                            writer.writerow([
                                item.get('path', ''),
                                item.get('name', ''),
                                item.get('size', 0),
                                item.get('lines', 'N/A'),
                                item.get('modified', '').isoformat()[:19] if isinstance(item.get('modified'), datetime) else '',
                                Path(item.get('path', '')).suffix
                            ])
                
                write_files(self.results['structure'])
            
            print(f"{Colors.GREEN}✅ Fichier CSV sauvegardé: {csv_report}{Colors.END}")
        
        except ImportError:
            print(f"{Colors.YELLOW}⚠️  CSV non disponible (module csv manquant){Colors.END}")

# =============================================================================
# FONCTION POUR AFFICHER L'ARBORESCENCE
# =============================================================================

def display_tree(project_path, max_depth=3):
    """Affiche l'arborescence du projet"""
    print(f"{Colors.BOLD}{Colors.MAGENTA}🌳 ARBORESCENCE DU PROJET{Colors.END}")
    print(f"{Colors.GRAY}Profondeur maximale: {max_depth}{Colors.END}")
    print("=" * 100)
    
    def print_tree(dir_path, prefix="", depth=0, is_last_stack=None):
        if is_last_stack is None:
            is_last_stack = []
        
        if depth > max_depth:
            return
        
        try:
            items = sorted(dir_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        except PermissionError:
            print(f"{prefix}└── {Colors.RED}[Permission refusée]{Colors.END}")
            return
        
        # Filtrer les éléments exclus
        excluded_patterns = ['__pycache__', '.pyc', '.git', '.DS_Store', 'venv', 'node_modules']
        items = [item for item in items if not any(pattern in str(item) for pattern in excluded_patterns)]
        
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            is_last_stack.append(is_last)
            
            connector = "└── " if is_last else "├── "
            
            # Icône et couleur
            if item.is_dir():
                icon = "📁"
                color = Colors.CYAN
            else:
                icon = "📄"
                color = Colors.WHITE
                
                # Couleur spécifique par extension
                ext = item.suffix.lower()
                if ext == '.py':
                    color = Colors.GREEN
                elif ext == '.html':
                    color = Colors.YELLOW
                elif ext == '.js':
                    color = Colors.BLUE
                elif ext == '.css':
                    color = Colors.MAGENTA
                elif ext in ['.json', '.md', '.txt']:
                    color = Colors.GRAY
            
            # Informations supplémentaires
            info = ""
            if item.is_file():
                try:
                    size = item.stat().st_size
                    info = f" ({FileAnalyzer.human_size(size)})"
                except:
                    pass
            
            # Afficher l'élément
            line_prefix = ""
            for j in range(depth):
                line_prefix += "    " if is_last_stack[j] else "│   "
            
            print(f"{line_prefix}{connector}{icon} {color}{item.name}{Colors.END}{info}")
            
            # Récursion pour les dossiers
            if item.is_dir():
                print_tree(item, prefix, depth + 1, is_last_stack)
            
            is_last_stack.pop()
    
    print_tree(project_path)

# =============================================================================
# FONCTION PRINCIPALE
# =============================================================================

def main():
    """Fonction principale"""
    print(f"{Colors.BOLD}{Colors.MAGENTA}🌐 ANALYSEUR COMPLET DE PROJET DJANGO{Colors.END}")
    print(f"{Colors.GRAY}Version 2.0 - Analyse exhaustive{Colors.END}")
    print("=" * 100)
    
    # Déterminer le chemin du projet
    script_path = Path(__file__).resolve()
    
    # Essayer de trouver le dossier du projet
    possible_paths = [
        Path.cwd(),
        script_path.parent,
        Path("/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30"),
    ]
    
    project_path = None
    for path in possible_paths:
        if (path / "manage.py").exists() or (path / "requirements.txt").exists():
            project_path = path
            break
    
    if not project_path:
        print(f"{Colors.RED}❌ Impossible de trouver un projet Django{Colors.END}")
        
        # Demander le chemin manuellement
        user_path = input(f"\n{Colors.YELLOW}📁 Entrez le chemin du projet: {Colors.END}").strip()
        if user_path:
            project_path = Path(user_path)
        else:
            print(f"{Colors.RED}❌ Aucun chemin fourni{Colors.END}")
            return
    
    print(f"{Colors.GREEN}✅ Projet trouvé: {project_path}{Colors.END}")
    print()
    
    # Menu d'analyse
    print(f"{Colors.BOLD}{Colors.CYAN}📊 MENU D'ANALYSE:{Colors.END}")
    print("  1. 🌳 Afficher l'arborescence complète")
    print("  2. 🔍 Analyser la structure en détail")
    print("  3. 📋 Générer un rapport complet")
    print("  4. 🎯 Analyser uniquement les applications Django")
    print("  5. 🔧 Lister tous les fichiers de correction")
    print("  6. 🚪 Quitter")
    
    choice = input(f"\n{Colors.YELLOW}👉 Votre choix (1-6): {Colors.END}").strip()
    
    if choice == '1':
        depth = input(f"{Colors.YELLOW}Profondeur (défaut: 3): {Colors.END}").strip()
        depth = int(depth) if depth.isdigit() else 3
        display_tree(project_path, max_depth=depth)
    
    elif choice == '2':
        analyzer = ProjectAnalyzer(project_path)
        analyzer.generate_report()
    
    elif choice == '3':
        print(f"{Colors.YELLOW}📋 Génération du rapport complet...{Colors.END}")
        analyzer = ProjectAnalyzer(project_path)
        results = analyzer.generate_report()
        display_tree(project_path, max_depth=2)
    
    elif choice == '4':
        print(f"{Colors.YELLOW}🎯 Analyse des applications Django...{Colors.END}")
        analyzer = ProjectAnalyzer(project_path)
        analyzer.analyze_django_applications()
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}📊 APPLICATIONS DJANGO DÉTECTÉES:{Colors.END}")
        for app_name, app_info in analyzer.results['applications'].items():
            print(f"\n{Colors.GREEN}{app_name}{Colors.END}")
            for file_name in ['models.py', 'views.py', 'urls.py', 'admin.py', 'apps.py']:
                if file_name in app_info['files']:
                    file_data = app_info['files'][file_name]
                    if 'python_info' in file_data:
                        pi = file_data['python_info']
                        print(f"  📄 {file_name}: ", end="")
                        if file_name == 'models.py':
                            print(f"{pi.get('models_count', 0)} modèles")
                        elif file_name == 'views.py':
                            print(f"{pi.get('views_count', 0)} vues")
                        elif file_name == 'urls.py':
                            print(f"{pi.get('urls_count', 0)} URLs")
                        else:
                            print("✓")
                    else:
                        print(f"  📄 {file_name}: ✓")
                else:
                    print(f"  ❌ {file_name}: MANQUANT")
    
    elif choice == '5':
        print(f"{Colors.YELLOW}🔧 Liste des fichiers de correction...{Colors.END}")
        
        correction_patterns = [
            'correction', 'fix', 'correct', 'repair', 'debug', 'diagnostic',
            'test_', '_test', 'verify', 'verification', 'check', 'validate',
            'urgence', 'emergency', 'hotfix', 'patch', 'solution',
        ]
        
        correction_files = []
        total_size = 0
        
        for root, dirs, files in os.walk(project_path):
            # Ignorer certains dossiers
            if any(pattern in root for pattern in ['__pycache__', '.git', 'venv', 'node_modules']):
                continue
            
            for file in files:
                file_lower = file.lower()
                if any(pattern in file_lower for pattern in correction_patterns):
                    file_path = Path(root) / file
                    try:
                        size = file_path.stat().st_size
                        correction_files.append({
                            'path': str(file_path.relative_to(project_path)),
                            'size': size,
                            'size_human': FileAnalyzer.human_size(size),
                        })
                        total_size += size
                    except:
                        pass
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}📊 FICHIERS DE CORRECTION ({len(correction_files)}):{Colors.END}")
        print(f"Taille totale: {FileAnalyzer.human_size(total_size)}\n")
        
        # Grouper par type
        from collections import defaultdict
        by_type = defaultdict(list)
        
        for file_info in correction_files:
            ext = Path(file_info['path']).suffix.lower()
            by_type[ext].append(file_info)
        
        for ext, files in sorted(by_type.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"{Colors.YELLOW}{ext or 'sans extension'}: {len(files)} fichiers{Colors.END}")
            for file_info in files[:5]:  # Afficher les 5 premiers
                print(f"  • {file_info['path']} ({file_info['size_human']})")
            if len(files) > 5:
                print(f"  ... et {len(files) - 5} autres")
            print()
        
        # Sauvegarder la liste
        list_path = project_path / 'correction_files_list.txt'
        with open(list_path, 'w', encoding='utf-8') as f:
            f.write("LISTE DES FICHIERS DE CORRECTION/TEST\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Total: {len(correction_files)} fichiers\n")
            f.write(f"Taille totale: {FileAnalyzer.human_size(total_size)}\n\n")
            
            for file_info in sorted(correction_files, key=lambda x: x['path']):
                f.write(f"{file_info['path']} ({file_info['size_human']})\n")
        
        print(f"{Colors.GREEN}✅ Liste sauvegardée: {list_path}{Colors.END}")
    
    elif choice == '6':
        print(f"{Colors.GREEN}👋 Au revoir!{Colors.END}")
    
    else:
        print(f"{Colors.RED}❌ Choix invalide{Colors.END}")

# =============================================================================
# EXÉCUTION
# =============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Analyse interrompue par l'utilisateur{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ Erreur lors de l'analyse: {e}{Colors.END}")
        import traceback
        traceback.print_exc()