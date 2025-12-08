#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE DE L'ARBORESCENCE DU PROJET DJANGO
Auteur: Assistant Technique
Date: 2024
Description: Analyse complète de la structure du projet Django avant modifications
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# =============================================================================
# CONFIGURATION
# =============================================================================

# Définition des couleurs pour l'affichage
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
# FONCTIONS D'ANALYSE
# =============================================================================

def get_file_info(file_path):
    """Récupère les informations d'un fichier"""
    try:
        stat = file_path.stat()
        return {
            'size': stat.st_size,
            'lines': sum(1 for _ in open(file_path, 'r', encoding='utf-8', errors='ignore')),
            'modified': datetime.fromtimestamp(stat.st_mtime),
        }
    except:
        return {'size': 0, 'lines': 0, 'modified': None}

def analyze_django_file(file_path, app_name=None):
    """Analyse un fichier Django spécifique"""
    info = get_file_info(file_path)
    
    if file_path.name == 'models.py':
        return analyze_models_file(file_path, app_name)
    elif file_path.name == 'views.py':
        return analyze_views_file(file_path, app_name)
    elif file_path.name == 'urls.py':
        return analyze_urls_file(file_path, app_name)
    elif file_path.name == 'admin.py':
        return analyze_admin_file(file_path, app_name)
    elif file_path.name == 'apps.py':
        return analyze_apps_file(file_path, app_name)
    else:
        return {'type': 'other', 'info': info}

def analyze_models_file(file_path, app_name):
    """Analyse un fichier models.py"""
    info = get_file_info(file_path)
    result = {'type': 'models', 'info': info, 'models': [], 'count': 0}
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Compter les modèles
        model_count = content.count('class ') - content.count('class Meta')
        
        # Extraire les noms des modèles (simplifié)
        import re
        models = re.findall(r'class\s+(\w+)\s*\(', content)
        
        # Filtrer pour enlever 'Meta'
        models = [m for m in models if m != 'Meta']
        
        result['models'] = models
        result['count'] = len(models)
        
    except Exception as e:
        result['error'] = str(e)
    
    return result

def analyze_views_file(file_path, app_name):
    """Analyse un fichier views.py"""
    info = get_file_info(file_path)
    result = {'type': 'views', 'info': info, 'views_count': 0, 'function_views': [], 'class_views': []}
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Compter les vues (simplifié)
        # Fonctions de vue
        func_pattern = r'def\s+(\w+)\s*\(.*?\)\s*:'
        functions = re.findall(func_pattern, content, re.DOTALL)
        
        # Classes de vue (View, APIView, etc.)
        class_pattern = r'class\s+(\w+)\s*\(.*?(?:View|APIView|ViewSet)'
        classes = re.findall(class_pattern, content, re.DOTALL)
        
        result['function_views'] = functions[:5]  # Limiter à 5 pour l'affichage
        result['class_views'] = classes[:5]
        result['views_count'] = len(functions) + len(classes)
        
    except Exception as e:
        result['error'] = str(e)
    
    return result

def analyze_urls_file(file_path, app_name):
    """Analyse un fichier urls.py"""
    info = get_file_info(file_path)
    result = {'type': 'urls', 'info': info, 'patterns': [], 'count': 0, 'included': False}
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Compter les patterns
        pattern_count = content.count('path(') + content.count('url(') + content.count('re_path(')
        
        # Extraire les patterns (simplifié)
        import re
        patterns = re.findall(r'path\([\'"]([^\'"]+)[\'"]', content)
        
        result['patterns'] = patterns[:10]  # Limiter à 10 pour l'affichage
        result['count'] = pattern_count
        
    except Exception as e:
        result['error'] = str(e)
    
    return result

def analyze_admin_file(file_path, app_name):
    """Analyse un fichier admin.py"""
    info = get_file_info(file_path)
    result = {'type': 'admin', 'info': info, 'registered_models': [], 'count': 0}
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Compter les modèles enregistrés
        reg_count = content.count('admin.site.register(')
        
        # Extraire les modèles enregistrés
        import re
        registered = re.findall(r'admin\.site\.register\(([^,)]+)', content)
        
        result['registered_models'] = registered
        result['count'] = reg_count
        
    except Exception as e:
        result['error'] = str(e)
    
    return result

def analyze_apps_file(file_path, app_name):
    """Analyse un fichier apps.py"""
    info = get_file_info(file_path)
    result = {'type': 'apps', 'info': info, 'config_name': '', 'verbose_name': ''}
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Extraire le nom de la classe de configuration
        import re
        config_match = re.search(r'class\s+(\w+Config)\s*\(.*?AppConfig', content)
        if config_match:
            result['config_name'] = config_match.group(1)
        
        # Extraire le verbose_name
        verbose_match = re.search(r'verbose_name\s*=\s*[\'"]([^\'"]+)[\'"]', content)
        if verbose_match:
            result['verbose_name'] = verbose_match.group(1)
        
    except Exception as e:
        result['error'] = str(e)
    
    return result

def analyze_templates_dir(app_dir):
    """Analyse le dossier templates d'une application"""
    templates_dir = app_dir / 'templates'
    
    if not templates_dir.exists():
        return None
    
    templates = []
    total_size = 0
    total_files = 0
    
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = Path(root) / file
                rel_path = file_path.relative_to(templates_dir)
                file_info = get_file_info(file_path)
                
                templates.append({
                    'path': str(rel_path),
                    'size': file_info['size'],
                    'lines': file_info['lines'],
                })
                
                total_size += file_info['size']
                total_files += 1
    
    return {
        'exists': True,
        'total_files': total_files,
        'total_size': total_size,
        'templates': templates[:20],  # Limiter à 20 pour l'affichage
    }

def analyze_static_dir(app_dir):
    """Analyse le dossier static d'une application"""
    static_dir = app_dir / 'static'
    
    if not static_dir.exists():
        return None
    
    files_by_type = {}
    total_size = 0
    total_files = 0
    
    for root, dirs, files in os.walk(static_dir):
        for file in files:
            file_path = Path(root) / file
            ext = file_path.suffix.lower()
            
            file_info = get_file_info(file_path)
            
            if ext not in files_by_type:
                files_by_type[ext] = {'count': 0, 'size': 0}
            
            files_by_type[ext]['count'] += 1
            files_by_type[ext]['size'] += file_info['size']
            
            total_size += file_info['size']
            total_files += 1
    
    return {
        'exists': True,
        'total_files': total_files,
        'total_size': total_size,
        'files_by_type': files_by_type,
    }

def analyze_application(app_name, app_dir):
    """Analyse une application Django complète"""
    print(f"{Colors.CYAN}📁 Analyse de l'application: {app_name}{Colors.END}")
    
    result = {
        'name': app_name,
        'path': str(app_dir),
        'exists': app_dir.exists(),
        'files': {},
        'templates': None,
        'static': None,
        'size': 0,
        'issues': [],
    }
    
    if not app_dir.exists():
        result['issues'].append('Dossier inexistant')
        return result
    
    # Fichiers essentiels Django
    essential_files = ['models.py', 'views.py', 'urls.py', 'admin.py', 'apps.py', '__init__.py']
    
    for file_name in essential_files:
        file_path = app_dir / file_name
        if file_path.exists():
            analysis = analyze_django_file(file_path, app_name)
            result['files'][file_name] = analysis
            result['size'] += analysis['info']['size'] if 'info' in analysis else 0
        else:
            result['files'][file_name] = {'exists': False}
            if file_name != '__init__.py':  # __init__.py est optionnel
                result['issues'].append(f'Fichier {file_name} manquant')
    
    # Analyse des templates
    templates_analysis = analyze_templates_dir(app_dir)
    result['templates'] = templates_analysis
    
    # Analyse des fichiers statiques
    static_analysis = analyze_static_dir(app_dir)
    result['static'] = static_analysis
    
    return result

def analyze_project_structure(project_path):
    """Analyse la structure complète du projet"""
    print(f"{Colors.BOLD}{Colors.MAGENTA}🔍 ANALYSE DE LA STRUCTURE DU PROJET DJANGO{Colors.END}")
    print(f"{Colors.GRAY}Chemin: {project_path}{Colors.END}")
    print("=" * 100)
    
    results = {
        'project_path': str(project_path),
        'analysis_date': datetime.now().isoformat(),
        'applications': [],
        'total_size': 0,
        'total_apps': 0,
        'summary': {},
    }
    
    # Vérifier les fichiers de projet Django
    project_files = ['manage.py', 'requirements.txt', 'README.md', '.env', 'settings.py']
    print(f"{Colors.YELLOW}📋 FICHIERS DU PROJET:{Colors.END}")
    
    for file_name in project_files:
        file_path = project_path / file_name
        if file_path.exists():
            info = get_file_info(file_path)
            print(f"  ✅ {file_name}: {info['size']:,} octets, {info['lines']} lignes")
        else:
            print(f"  ❌ {file_name}: MANQUANT")
    
    print()
    
    # Lister tous les dossiers potentiellement d'applications
    all_dirs = [d for d in project_path.iterdir() if d.is_dir()]
    
    # Applications Django détectées (basé sur la présence de models.py ou apps.py)
    django_apps = []
    for dir_path in all_dirs:
        if (dir_path / 'apps.py').exists() or (dir_path / 'models.py').exists():
            django_apps.append(dir_path.name)
    
    print(f"{Colors.YELLOW}📦 APPLICATIONS DJANGO DÉTECTÉES ({len(django_apps)}):{Colors.END}")
    print(", ".join(django_apps))
    print()
    
    # Analyser chaque application
    print(f"{Colors.YELLOW}🔍 ANALYSE DÉTAILLÉE DES APPLICATIONS:{Colors.END}")
    
    for app_name in sorted(django_apps):
        app_dir = project_path / app_name
        app_analysis = analyze_application(app_name, app_dir)
        results['applications'].append(app_analysis)
        results['total_size'] += app_analysis['size']
        results['total_apps'] += 1
        
        # Afficher le résumé
        print(f"  {Colors.CYAN}{app_name}{Colors.END}")
        
        # Fichiers essentiels
        files_summary = []
        for file_name in ['models.py', 'views.py', 'urls.py', 'admin.py']:
            file_data = app_analysis['files'].get(file_name, {})
            if file_data.get('exists', True):
                if 'count' in file_data:
                    files_summary.append(f"{file_name}: {file_data['count']}")
                else:
                    files_summary.append(f"{file_name}: ✓")
            else:
                files_summary.append(f"{file_name}: ✗")
        
        print(f"    📄 {' | '.join(files_summary)}")
        
        # Templates
        if app_analysis['templates']:
            print(f"    🎨 Templates: {app_analysis['templates']['total_files']} fichiers")
        
        # Problèmes
        if app_analysis['issues']:
            print(f"    ⚠️  Problèmes: {', '.join(app_analysis['issues'])}")
        
        print()
    
    # Analyser les dossiers principaux
    print(f"{Colors.YELLOW}📁 STRUCTURE DES DOSSIERS PRINCIPAUX:{Colors.END}")
    
    main_dirs = ['templates', 'static', 'media', 'logs', 'migrations', 'tests']
    for dir_name in main_dirs:
        dir_path = project_path / dir_name
        if dir_path.exists():
            # Compter les fichiers
            file_count = sum(1 for _ in dir_path.rglob('*') if _.is_file())
            dir_count = sum(1 for _ in dir_path.rglob('*') if _.is_dir()) - 1  # -1 pour le dossier lui-même
            print(f"  📂 {dir_name}/: {file_count} fichiers, {dir_count} sous-dossiers")
        else:
            print(f"  📂 {dir_name}/: ABSENT")
    
    print()
    
    # Générer un résumé
    print(f"{Colors.YELLOW}📊 RÉSUMÉ STATISTIQUE:{Colors.END}")
    
    total_models = 0
    total_views = 0
    total_url_patterns = 0
    total_templates = 0
    
    for app in results['applications']:
        # Modèles
        models_data = app['files'].get('models.py', {})
        total_models += models_data.get('count', 0)
        
        # Vues
        views_data = app['files'].get('views.py', {})
        total_views += views_data.get('views_count', 0)
        
        # URLs
        urls_data = app['files'].get('urls.py', {})
        total_url_patterns += urls_data.get('count', 0)
        
        # Templates
        if app['templates']:
            total_templates += app['templates']['total_files']
    
    print(f"  • Applications Django: {results['total_apps']}")
    print(f"  • Modèles définis: {total_models}")
    print(f"  • Vues détectées: {total_views}")
    print(f"  • Patterns URL: {total_url_patterns}")
    print(f"  • Templates HTML: {total_templates}")
    print(f"  • Taille totale du code: {results['total_size']:,} octets")
    
    # Identifier les problèmes globaux
    print()
    print(f"{Colors.YELLOW}⚠️  PROBLÈMES IDENTIFIÉS:{Colors.END}")
    
    global_issues = []
    for app in results['applications']:
        if app['issues']:
            global_issues.append(f"{app['name']}: {', '.join(app['issues'])}")
    
    if global_issues:
        for issue in global_issues:
            print(f"  • {issue}")
    else:
        print(f"  ✅ Aucun problème majeur détecté")
    
    # Sauvegarder le rapport
    save_report(results, project_path)
    
    return results

def save_report(results, project_path):
    """Sauvegarde le rapport d'analyse dans un fichier"""
    report_path = project_path / 'project_analysis_report.json'
    
    # Convertir les objets datetime en string pour JSON
    def datetime_handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        elif isinstance(obj, Path):
            return str(obj)
        else:
            return str(obj)
    
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=datetime_handler)
        
        print()
        print(f"{Colors.GREEN}✅ Rapport sauvegardé: {report_path}{Colors.END}")
        
        # Créer aussi un rapport texte
        text_report_path = project_path / 'project_analysis_summary.txt'
        with open(text_report_path, 'w', encoding='utf-8') as f:
            f.write(f"RAPPORT D'ANALYSE DU PROJET DJANGO\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Chemin: {project_path}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("APPLICATIONS ANALYSÉES:\n")
            for app in results['applications']:
                f.write(f"\n{app['name']}:\n")
                f.write(f"  - Chemin: {app['path']}\n")
                
                # Fichiers
                for file_name in ['models.py', 'views.py', 'urls.py', 'admin.py', 'apps.py']:
                    file_data = app['files'].get(file_name, {})
                    if file_data.get('exists', True):
                        if 'count' in file_data:
                            f.write(f"  - {file_name}: {file_data['count']} éléments\n")
                        else:
                            f.write(f"  - {file_name}: Présent\n")
                    else:
                        f.write(f"  - {file_name}: MANQUANT\n")
                
                # Problèmes
                if app['issues']:
                    f.write(f"  - Problèmes: {', '.join(app['issues'])}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("STATISTIQUES GLOBALES:\n")
            f.write(f"- Applications: {results['total_apps']}\n")
            
            # Calculer les totaux
            total_models = sum(app['files'].get('models.py', {}).get('count', 0) for app in results['applications'])
            total_views = sum(app['files'].get('views.py', {}).get('views_count', 0) for app in results['applications'])
            total_templates = sum(app['templates']['total_files'] if app['templates'] else 0 for app in results['applications'])
            
            f.write(f"- Modèles: {total_models}\n")
            f.write(f"- Vues: {total_views}\n")
            f.write(f"- Templates: {total_templates}\n")
            f.write(f"- Taille code: {results['total_size']:,} octets\n")
        
        print(f"{Colors.GREEN}✅ Résumé texte sauvegardé: {text_report_path}{Colors.END}")
        
    except Exception as e:
        print(f"{Colors.RED}❌ Erreur lors de la sauvegarde du rapport: {e}{Colors.END}")

def generate_tree_view(project_path, max_depth=3):
    """Génère une vue en arbre du projet"""
    print(f"{Colors.YELLOW}🌳 ARBORESCENCE DU PROJET (max depth={max_depth}):{Colors.END}")
    
    def print_tree(dir_path, prefix="", depth=0):
        if depth > max_depth:
            return
        
        # Obtenir les éléments triés
        try:
            items = sorted(dir_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        except:
            return
        
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "
            
            # Ignorer certains dossiers/fichiers
            ignore_patterns = ['.git', '__pycache__', '.pyc', '.DS_Store', 'node_modules', 'venv']
            if any(pattern in str(item) for pattern in ignore_patterns):
                continue
            
            # Afficher l'élément
            icon = "📁" if item.is_dir() else "📄"
            color = Colors.CYAN if item.is_dir() else Colors.WHITE
            
            # Informations supplémentaires pour les fichiers
            info = ""
            if item.is_file():
                try:
                    size = item.stat().st_size
                    if size > 1024*1024:
                        info = f" ({size//(1024*1024)} MB)"
                    elif size > 1024:
                        info = f" ({size//1024} KB)"
                    else:
                        info = f" ({size} B)"
                except:
                    pass
            
            print(f"{prefix}{connector}{icon} {color}{item.name}{Colors.END}{info}")
            
            # Récursion pour les dossiers
            if item.is_dir():
                extension = "    " if is_last else "│   "
                print_tree(item, prefix + extension, depth + 1)
    
    print_tree(project_path)

# =============================================================================
# FONCTION PRINCIPALE
# =============================================================================

def main():
    """Fonction principale"""
    print(f"{Colors.BOLD}{Colors.MAGENTA}🌐 ANALYSEUR DE PROJET DJANGO{Colors.END}")
    print(f"{Colors.GRAY}Version 1.0 - Analyse structurelle complète{Colors.END}")
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
        if (path / "manage.py").exists():
            project_path = path
            break
    
    if not project_path:
        print(f"{Colors.RED}❌ Impossible de trouver un projet Django dans les chemins suivants:{Colors.END}")
        for path in possible_paths:
            print(f"  • {path}")
        
        # Demander le chemin manuellement
        user_path = input(f"\n{Colors.YELLOW}📁 Entrez le chemin du projet Django: {Colors.END}").strip()
        if user_path:
            project_path = Path(user_path)
            if not (project_path / "manage.py").exists():
                print(f"{Colors.RED}❌ Le chemin spécifié ne contient pas de projet Django (manage.py manquant){Colors.END}")
                return
    
    print(f"{Colors.GREEN}✅ Projet trouvé: {project_path}{Colors.END}")
    print()
    
    # Menu d'analyse
    print(f"{Colors.BOLD}{Colors.CYAN}📊 MENU D'ANALYSE:{Colors.END}")
    print("  1. 🌳 Afficher l'arborescence du projet")
    print("  2. 🔍 Analyser la structure Django")
    print("  3. 📋 Générer un rapport complet")
    print("  4. 🚪 Quitter")
    
    choice = input(f"\n{Colors.YELLOW}👉 Votre choix (1-4): {Colors.END}").strip()
    
    if choice == '1':
        generate_tree_view(project_path)
    elif choice == '2':
        analyze_project_structure(project_path)
    elif choice == '3':
        print(f"{Colors.YELLOW}📋 Génération du rapport complet...{Colors.END}")
        results = analyze_project_structure(project_path)
        generate_tree_view(project_path)
    elif choice == '4':
        print(f"{Colors.GREEN}👋 Au revoir!{Colors.END}")
    else:
        print(f"{Colors.RED}❌ Choix invalide{Colors.END}")

# =============================================================================
# EXÉCUTION
# =============================================================================

if __name__ == "__main__":
    # Import regex pour les fonctions d'analyse
    import re
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Analyse interrompue par l'utilisateur{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ Erreur lors de l'analyse: {e}{Colors.END}")
        import traceback
        traceback.print_exc()