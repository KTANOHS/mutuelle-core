# check_agents_status.py
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

def verifier_etat_agents():
    print("🔍 VÉRIFICATION DE L'ÉTAT ACTUEL DE L'APPLICATION AGENTS")
    print("=" * 60)
    
    # Vérifier le contenu de views.py
    views_path = BASE_DIR / 'agents' / 'views.py'
    if views_path.exists():
        with open(views_path, 'r') as f:
            content = f.read()
            if 'recherche_membres_api' in content:
                print("✅ Vue 'recherche_membres_api' trouvée dans views.py")
            else:
                print("❌ Vue 'recherche_membres_api' MANQUANTE dans views.py")
                
            if 'verifier_cotisation_api' in content:
                print("✅ Vue 'verifier_cotisation_api' trouvée dans views.py")
            else:
                print("❌ Vue 'verifier_cotisation_api' MANQUANTE dans views.py")
    
    # Vérifier urls.py
    urls_path = BASE_DIR / 'agents' / 'urls.py'
    if urls_path.exists():
        with open(urls_path, 'r') as f:
            content = f.read()
            if 'recherche-membres' in content:
                print("✅ URL 'recherche-membres' trouvée dans urls.py")
            else:
                print("❌ URL 'recherche-membres' MANQUANTE dans urls.py")
    
    # Vérifier l'inclusion dans les URLs principales
    main_urls_path = BASE_DIR / 'mutuelle_core' / 'urls.py'
    if main_urls_path.exists():
        with open(main_urls_path, 'r') as f:
            content = f.read()
            if 'agents' in content and 'include' in content:
                print("✅ Application 'agents' incluse dans les URLs principales")
            else:
                print("❌ Application 'agents' NON INCLUSE dans les URLs principales")

if __name__ == "__main__":
    verifier_etat_agents()