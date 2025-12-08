# liste_problemes_specifiques.py
import os
from pathlib import Path

def find_problematic_files():
    """Trouve les fichiers problématiques spécifiques"""
    BASE_DIR = Path(__file__).resolve().parent.parent
    apps_dir = BASE_DIR / 'apps'
    
    problems = []
    
    for app_dir in apps_dir.iterdir():
        if app_dir.is_dir():
            app_name = app_dir.name
            
            # Vérifier les fichiers critiques manquants
            critical_files = ['models.py', 'views.py', 'urls.py']
            for file in critical_files:
                if not (app_dir / file).exists():
                    problems.append(f"❌ {app_name}/ {file} MANQUANT")
            
            # Vérifier les templates de dashboard
            templates_dir = app_dir / 'templates' / app_name
            dashboard_template = templates_dir / 'dashboard.html'
            if not dashboard_template.exists():
                problems.append(f"❌ {app_name}/templates/{app_name}/dashboard.html MANQUANT")
    
    # Afficher tous les problèmes
    print("📋 LISTE DES PROBLÈMES IDENTIFIÉS:")
    for problem in sorted(problems):
        print(problem)

if __name__ == "__main__":
    find_problematic_files()