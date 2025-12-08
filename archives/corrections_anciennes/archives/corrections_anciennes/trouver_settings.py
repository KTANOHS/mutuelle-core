#!/usr/bin/env python
"""
SOLUTION RAPIDE - Contourne le problème de settings
"""

import os
import sys

def solution_express():
    """Solution express pour trouver le projet"""
    
    print("⚡ SOLUTION EXPRESS")
    print("=" * 40)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"📁 Nous sommes ici: {current_dir}")
    
    # Essayer les solutions les plus courantes
    solutions = [
        # Solution 1: Même répertoire
        lambda: current_dir,
        # Solution 2: Parent directory  
        lambda: os.path.dirname(current_dir),
    ]
    
    for i, solution in enumerate(solutions, 1):
        test_dir = solution()
        print(f"\n🔄 Essai solution {i}: {test_dir}")
        
        # Chercher manage.py
        manage_py = os.path.join(test_dir, 'manage.py')
        if os.path.exists(manage_py):
            print(f"✅ manage.py trouvé: {manage_py}")
            
            # Deviner le settings module
            project_name = os.path.basename(test_dir)
            settings_candidates = [
                f"{project_name}.settings",
                "config.settings", 
                "core.settings",
                "settings"
            ]
            
            for settings_candidate in settings_candidates:
                try:
                    sys.path.append(test_dir)
                    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_candidate)
                    import django
                    django.setup()
                    print(f"🎯 SETTINGS TROUVÉ: {settings_candidate}")
                    
                    # Afficher les apps
                    from django.apps import apps
                    print(f"📦 Apps: {[app.name for app in apps.get_app_configs()]}")
                    
                    return settings_candidate, test_dir
                    
                except Exception as e:
                    print(f"   ❌ {settings_candidate}: {e}")
                    continue
    
    print("\n❌ Aucune solution automatique trouvée")
    print("\n🔧 FAITES CE CI:")
    print("1. Ouvrez un terminal dans le même dossier que manage.py")
    print("2. Exécutez: python manage.py shell")
    print("3. Dans le shell, tapez: import os; print(os.environ.get('DJANGO_SETTINGS_MODULE'))")
    print("4. Partagez-moi le résultat")
    
    return None, None

if __name__ == "__main__":
    settings, project_dir = solution_express()
    
    if settings:
        print(f"\n🎉 SOLUTION TROUVÉE!")
        print(f"📁 Dossier projet: {project_dir}")
        print(f"⚙️  Settings module: {settings}")
        
        # Créer un fichier de configuration
        config_content = f"""
# FICHIER DE CONFIGURATION POUR VOTRE PROJET
import os
import sys

# Ajouter le chemin du projet
sys.path.append(r'{project_dir}')

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{settings}')

import django
django.setup()

print("✅ Django configuré avec succès!")
"""
        
        with open('config_projet.py', 'w') as f:
            f.write(config_content)
        
        print("📄 Fichier 'config_projet.py' créé - utilisez-le dans vos scripts")