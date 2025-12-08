# detect_project.py
import os
import sys
from pathlib import Path

def detecter_structure_projet():
    """Détecte automatiquement la structure du projet Django"""
    print("🔍 Détection de la structure du projet...")
    
    current_dir = Path(__file__).parent
    
    # Chercher manage.py
    manage_py = current_dir / "manage.py"
    if not manage_py.exists():
        print("❌ manage.py non trouvé - Ce n'est pas un projet Django valide")
        return None
    
    print("✅ manage.py trouvé")
    
    # Chercher le module settings
    modules_possibles = [
        'core', 'mutuelle_core', 'config', 'projet', 'settings',
        'mutuelle', 'mysite', 'project'
    ]
    
    for module in modules_possibles:
        settings_path = current_dir / module / "settings.py"
        if settings_path.exists():
            print(f"✅ Module trouvé: {module}")
            return module
        
        # Vérifier aussi si settings.py est à la racine
        settings_root = current_dir / "settings.py"
        if settings_root.exists():
            print("✅ settings.py trouvé à la racine")
            return current_dir.name
    
    # Lister tous les dossiers pour aide manuelle
    print("\n📁 Dossiers disponibles:")
    for item in current_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.') and not item.name in ['venv', '__pycache__', 'static', 'media', 'logs']:
            print(f"   📂 {item.name}")
            # Vérifier si ce dossier contient settings.py
            settings_test = item / "settings.py"
            if settings_test.exists():
                print(f"      ✅ Contient settings.py! → Module probable: {item.name}")
                return item.name
    
    return None

def trouver_module_via_manage_py():
    """Lit manage.py pour trouver le module Django"""
    manage_py = Path("manage.py")
    if manage_py.exists():
        with open(manage_py, 'r') as f:
            content = f.read()
            if 'os.environ.setdefault' in content:
                import re
                match = re.search(r"os\.environ\.setdefault\('DJANGO_SETTINGS_MODULE', '([^']+)'", content)
                if match:
                    full_module = match.group(1)
                    module_name = full_module.split('.')[0]
                    print(f"✅ Module détecté via manage.py: {module_name}")
                    return module_name
    return None

# Exécution de la détection
print("=" * 50)
print("🎯 DÉTECTION AUTOMATIQUE DU PROJET DJANGO")
print("=" * 50)

module_detecte = trouver_module_via_manage_py()

if not module_detecte:
    module_detecte = detecter_structure_projet()

if module_detecte:
    print(f"\n🎉 Module Django identifié: {module_detecte}")
    print(f"💡 Utilisez: os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{module_detecte}.settings')")
else:
    print("\n❌ Impossible de détecter automatiquement le module Django")
    print("🔧 Solution manuelle nécessaire")