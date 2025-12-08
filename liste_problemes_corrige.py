# liste_problemes_corrige.py
import os
from pathlib import Path

def find_problematic_files():
    """Trouve les fichiers problématiques spécifiques à la racine"""
    BASE_DIR = Path(__file__).resolve().parent
    problems = []
    
    # Applications Django attendues
    expected_apps = ['medecin', 'membres', 'agents', 'pharmacien', 'assureur', 'core', 'soins', 'paiements', 'inscription', 'api']
    
    for app_name in expected_apps:
        app_dir = BASE_DIR / app_name
        
        if app_dir.exists() and (app_dir / 'apps.py').exists():
            # Vérifier les fichiers critiques manquants
            critical_files = ['models.py', 'views.py', 'urls.py']
            for file in critical_files:
                if not (app_dir / file).exists():
                    problems.append(f"❌ {app_name}/{file} MANQUANT")
            
            # Vérifier les templates de dashboard
            templates_dir = app_dir / 'templates' / app_name
            dashboard_template = templates_dir / 'dashboard.html'
            if not dashboard_template.exists():
                problems.append(f"❌ {app_name}/templates/{app_name}/dashboard.html MANQUANT")
        else:
            problems.append(f"❌ Application {app_name} NON TROUVÉE ou INCOMPLÈTE")
    
    # Afficher tous les problèmes
    print("📋 LISTE DES PROBLÈMES IDENTIFIÉS:")
    for problem in sorted(problems):
        print(problem)
    
    print(f"\n📊 Total: {len(problems)} problèmes identifiés")

if __name__ == "__main__":
    find_problematic_files()