# tree_view.py - Visualiseur d'arborescence Django
import os
from pathlib import Path
import sys

def print_tree(startpath, max_depth=3, exclude_dirs=None, exclude_files=None):
    """
    Affiche l'arborescence du projet
    """
    if exclude_dirs is None:
        exclude_dirs = {'.git', '__pycache__', 'node_modules', '.idea', '.vscode', 'venv', 'env'}
    if exclude_files is None:
        exclude_files = {'.DS_Store', '*.pyc', '*.pyo', '*.pyd'}
    
    print("\n" + "="*80)
    print("📁 ARBORESCENCE DU PROJET DJANGO")
    print("="*80)
    
    start_path = Path(startpath).resolve()
    print(f"Racine: {start_path}")
    print(f"Profondeur max: {max_depth}")
    print("-"*80)
    
    def _print_tree(path, prefix="", depth=0):
        if depth > max_depth:
            return
            
        # Liste les éléments
        try:
            items = list(path.iterdir())
        except PermissionError:
            return
            
        # Trie: dossiers d'abord, puis fichiers
        dirs = sorted([item for item in items if item.is_dir() and item.name not in exclude_dirs])
        files = sorted([item for item in items if item.is_file()])
        
        # Affiche les dossiers
        for i, d in enumerate(dirs):
            is_last = (i == len(dirs) - 1) and (len(files) == 0)
            print(f"{prefix}{'└── ' if is_last else '├── '}📂 {d.name}/")
            extension = "    " if is_last else "│   "
            _print_tree(d, prefix + extension, depth + 1)
        
        # Affiche les fichiers
        for i, f in enumerate(files):
            is_last = i == len(files) - 1
            # Ignorer certains fichiers
            if any(f.name.endswith(ext) for ext in ['.pyc', '.pyo', '.pyd']) or f.name in exclude_files:
                continue
                
            # Icône selon l'extension
            if f.name.endswith('.py'):
                icon = "🐍"
            elif f.name.endswith('.html'):
                icon = "📄"
            elif f.name.endswith('.css') or f.name.endswith('.js'):
                icon = "🎨"
            elif f.name.endswith('.json'):
                icon = "📋"
            elif f.name.endswith('.sqlite3') or f.name.endswith('.db'):
                icon = "🗄️ "
            elif f.name in ['requirements.txt', 'Pipfile', 'pyproject.toml']:
                icon = "📦"
            elif f.name in ['manage.py', 'Dockerfile', 'docker-compose.yml']:
                icon = "⚙️ "
            elif f.name in ['README.md', 'CHANGELOG.md', 'LICENSE']:
                icon = "📝"
            else:
                icon = "📄"
                
            size = f.stat().st_size
            size_str = f" ({size:,} bytes)" if size > 1000 else ""
            print(f"{prefix}{'└── ' if is_last else '├── '}{icon} {f.name}{size_str}")
    
    _print_tree(start_path)
    print("="*80)

def analyze_django_project(startpath):
    """
    Analyse spécifique d'un projet Django
    """
    start_path = Path(startpath).resolve()
    
    print("\n" + "="*80)
    print("🔍 ANALYSE DU PROJET DJANGO")
    print("="*80)
    
    # 1. Structure Django
    print("\n📋 STRUCTURE DJANGO:")
    
    django_files = {
        'manage.py': start_path / 'manage.py',
        'requirements.txt': start_path / 'requirements.txt',
        'settings.py': start_path / 'mutuelle_core' / 'settings.py',
        'urls.py': start_path / 'mutuelle_core' / 'urls.py',
        'wsgi.py': start_path / 'mutuelle_core' / 'wsgi.py',
        'asgi.py': start_path / 'mutuelle_core' / 'asgi.py',
    }
    
    for name, path in django_files.items():
        if path.exists():
            print(f"  ✅ {name}: {path}")
        else:
            print(f"  ❌ {name}: MANQUANT")
    
    # 2. Applications Django
    print("\n📱 APPLICATIONS DJANGO:")
    apps_dir = start_path / 'mutuelle_core'
    if apps_dir.exists():
        for item in apps_dir.iterdir():
            if item.is_dir() and (item / 'apps.py').exists():
                print(f"  📦 {item.name}")
    
    # 3. Fichiers de configuration
    print("\n⚙️  FICHIERS DE CONFIGURATION:")
    config_files = [
        'settings.py', 'settings_dev.py', 'settings_prod.py',
        'Procfile', 'runtime.txt', 'render.yaml', 'Dockerfile',
        '.env', '.env.example', '.gitignore'
    ]
    
    for file in config_files:
        path = start_path / file
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {file} ({size:,} bytes)")
    
    # 4. Base de données
    print("\n🗄️  BASES DE DONNÉES:")
    db_files = list(start_path.glob("*.sqlite3")) + list(start_path.glob("*.db"))
    for db in db_files:
        size = db.stat().st_size
        print(f"  📊 {db.name} ({size:,} bytes)")
    
    # 5. Fichiers statiques et médias
    print("\n🎨 FICHIERS STATIQUES ET MÉDIAS:")
    static_dirs = ['static', 'staticfiles', 'media', 'assets']
    for dir_name in static_dirs:
        dir_path = start_path / dir_name
        if dir_path.exists():
            file_count = len(list(dir_path.rglob("*")))
            size = sum(f.stat().st_size for f in dir_path.rglob("*") if f.is_file())
            print(f"  📁 {dir_name}/: {file_count} fichiers ({size:,} bytes)")
    
    # 6. Dépendances Python
    print("\n📦 DÉPENDANCES PYTHON:")
    req_files = ['requirements.txt', 'Pipfile', 'pyproject.toml']
    for req_file in req_files:
        path = start_path / req_file
        if path.exists():
            try:
                with open(path, 'r') as f:
                    lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    print(f"  📄 {req_file}: {len(lines)} paquets")
            except:
                print(f"  📄 {req_file}: présent")

def check_django_settings(startpath):
    """
    Vérifie la configuration Django
    """
    print("\n" + "="*80)
    print("🔧 VÉRIFICATION CONFIGURATION DJANGO")
    print("="*80)
    
    settings_path = Path(startpath) / 'mutuelle_core' / 'settings.py'
    
    if not settings_path.exists():
        print("❌ Fichier settings.py non trouvé!")
        return
    
    try:
        with open(settings_path, 'r') as f:
            content = f.read()
            
        print(f"✅ Fichier settings.py trouvé ({len(content)} caractères)")
        
        # Vérifications
        checks = [
            ('DEBUG', 'DEBUG ='),
            ('SECRET_KEY', 'SECRET_KEY ='),
            ('ALLOWED_HOSTS', 'ALLOWED_HOSTS ='),
            ('DATABASES', 'DATABASES ='),
            ('INSTALLED_APPS', 'INSTALLED_APPS ='),
            ('STATIC_URL', 'STATIC_URL ='),
            ('MEDIA_URL', 'MEDIA_URL ='),
        ]
        
        for check_name, check_str in checks:
            if check_str in content:
                print(f"  ✅ {check_name} défini")
            else:
                print(f"  ⚠  {check_name} non trouvé")
                
    except Exception as e:
        print(f"❌ Erreur lors de la lecture: {e}")

def main():
    """Fonction principale"""
    # Détermine le répertoire courant
    current_dir = Path.cwd()
    
    print("\n" + "="*80)
    print("🌳 ANALYSEUR D'ARBORESCENCE DJANGO")
    print("="*80)
    print(f"Répertoire: {current_dir}")
    print(f"Système: {sys.platform}")
    print(f"Python: {sys.version.split()[0]}")
    
    # 1. Afficher l'arborescence
    print_tree(current_dir, max_depth=4)
    
    # 2. Analyser spécifiquement Django
    analyze_django_project(current_dir)
    
    # 3. Vérifier la configuration
    check_django_settings(current_dir)
    
    # 4. Problèmes identifiés
    print("\n" + "="*80)
    print("🚨 PROBLÈMES IDENTIFIÉS")
    print("="*80)
    
    # Vérifier si production.py existe
    prod_path = current_dir / 'mutuelle_core' / 'production.py'
    dev_path = current_dir / 'mutuelle_core' / 'development.py'
    
    if not prod_path.exists():
        print("❌ mutuelle_core/production.py n'existe pas")
        print("   Solution: Créer le fichier ou modifier mutuelle_core/__init__.py")
        
    if not dev_path.exists():
        print("❌ mutuelle_core/development.py n'existe pas")
        print("   Solution: Créer le fichier ou modifier mutuelle_core/__init__.py")
    
    # Vérifier les fichiers Render
    render_files = ['Procfile', 'runtime.txt', 'build.sh', 'render.yaml']
    for file in render_files:
        if not (current_dir / file).exists():
            print(f"⚠  {file} manquant pour déploiement Render")
    
    print("\n" + "="*80)
    print("✅ ANALYSE TERMINÉE")
    print("="*80)

if __name__ == "__main__":
    main()