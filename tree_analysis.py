#!/usr/bin/env python3
"""
Visualisation d'arborescence avec coloration et filtres
"""

import os
import sys
from pathlib import Path

COLORS = {
    'directory': '\033[94m',
    'python': '\033[92m',
    'html': '\033[93m',
    'css': '\033[96m',
    'js': '\033[95m',
    'json': '\033[91m',
    'reset': '\033[0m'
}

def print_tree(startpath, max_depth=3, show_hidden=False):
    """Affiche l'arborescence avec couleurs"""
    
    ignore_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'staticfiles', 'media'}
    important_files = {'manage.py', 'settings.py', 'urls.py', 'wsgi.py', 'asgi.py', 
                      'requirements.txt', 'runtime.txt', 'Procfile', 'render.yaml'}
    
    for root, dirs, files in os.walk(startpath):
        # Filtrer les dossiers
        level = root.replace(startpath, '').count(os.sep)
        if level > max_depth:
            continue
        
        if not show_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ignore_dirs]
        
        # Afficher le dossier
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
        print(f"{COLORS['directory']}{indent}{os.path.basename(root)}/{COLORS['reset']}")
        
        # Afficher les fichiers importants
        subindent = '│   ' * level + '├── '
        
        for file in sorted(files):
            if not show_hidden and file.startswith('.'):
                continue
            
            ext = os.path.splitext(file)[1].lower()
            color = COLORS['reset']
            
            if ext == '.py':
                color = COLORS['python']
            elif ext in ['.html', '.htm']:
                color = COLORS['html']
            elif ext == '.css':
                color = COLORS['css']
            elif ext == '.js':
                color = COLORS['js']
            elif ext == '.json':
                color = COLORS['json']
            
            # Marquer les fichiers importants
            prefix = '⭐ ' if file in important_files else '  '
            
            if level < 2 or file in important_files:
                print(f"{subindent}{prefix}{color}{file}{COLORS['reset']}")

def analyze_project_structure():
    """Analyse la structure du projet Django"""
    structure = {
        'has_manage_py': False,
        'has_settings': False,
        'has_urls': False,
        'apps': [],
        'static_dirs': [],
        'template_dirs': []
    }
    
    # Chercher manage.py
    if os.path.exists('manage.py'):
        structure['has_manage_py'] = True
    
    # Chercher settings
    for root, dirs, files in os.walk('.'):
        if 'settings.py' in files:
            structure['has_settings'] = True
        if 'urls.py' in files:
            structure['has_urls'] = True
        
        # Applications Django
        if 'apps.py' in files and '__init__.py' in files:
            structure['apps'].append(os.path.basename(root))
        
        # Dossiers static
        if 'static' in dirs:
            structure['static_dirs'].append(os.path.relpath(root))
        
        # Dossiers templates
        if 'templates' in dirs:
            structure['template_dirs'].append(os.path.relpath(root))
    
    return structure

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print("🌳 ARBORESCENCE DU PROJET DJANGO")
    print("=" * 60)
    print_tree(path)
    
    print("\n" + "=" * 60)
    print("📊 ANALYSE DE STRUCTURE")
    
    structure = analyze_project_structure()
    
    if structure['has_manage_py']:
        print("✅ manage.py présent")
    else:
        print("❌ manage.py MANQUANT")
    
    if structure['has_settings']:
        print("✅ settings.py présent")
    else:
        print("❌ settings.py MANQUANT")
    
    if structure['apps']:
        print(f"✅ Applications Django ({len(structure['apps'])}):")
        for app in structure['apps']:
            print(f"   • {app}")
    else:
        print("⚠️  Aucune application Django détectée")
    
    if structure['static_dirs']:
        print(f"✅ Dossiers static ({len(structure['static_dirs'])}):")
        for static in structure['static_dirs'][:3]:
            print(f"   • {static}/static/")
    else:
        print("⚠️  Aucun dossier static détecté")
    
    if structure['template_dirs']:
        print(f"✅ Dossiers templates ({len(structure['template_dirs'])}):")
        for template in structure['template_dirs'][:3]:
            print(f"   • {template}/templates/")
    else:
        print("⚠️  Aucun dossier templates détecté")