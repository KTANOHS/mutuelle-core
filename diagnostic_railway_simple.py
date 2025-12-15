#!/usr/bin/env python
"""
DIAGNOSTIC RAILWAY - Version simple et fonctionnelle
"""

import os
import sys
from pathlib import Path
import datetime

# Couleurs pour la sortie
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")

def main():
    BASE_DIR = Path(__file__).parent
    
    print(f"\n{Colors.BOLD}🚀 DIAGNOSTIC RAILWAY{Colors.RESET}")
    print(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Répertoire: {BASE_DIR}\n")
    
    # Vérifier les fichiers essentiels
    print_header("FICHIERS ESSENTIELS")
    
    files_to_check = [
        'manage.py',
        'requirements.txt',
        'mutuelle_core/settings.py',
        'mutuelle_core/urls.py',
        'mutuelle_core/wsgi.py',
    ]
    
    for file in files_to_check:
        if (BASE_DIR / file).exists():
            print_success(file)
        else:
            print_error(f"{file} - MANQUANT")
    
    # Créer .nixpacks.toml si manquant
    print_header("CONFIGURATION RAILWAY")
    
    nixpacks = BASE_DIR / '.nixpacks.toml'
    if not nixpacks.exists():
        content = '''[phases.setup]
nixPkgs = ["python39", "postgresql"]

[phases.build]
cmds = [
    "pip install --upgrade pip",
    "pip install -r requirements.txt",
    "python manage.py collectstatic --noinput"
]

[start]
cmd = "python manage.py migrate && gunicorn mutuelle_core.wsgi:application --bind 0.0.0.0:$PORT --workers 3"
'''
        with open(nixpacks, 'w') as f:
            f.write(content)
        print_success(".nixpacks.toml généré")
    else:
        print_success(".nixpacks.toml existe")
    
    # Créer Procfile si manquant
    procfile = BASE_DIR / 'Procfile'
    if not procfile.exists():
        with open(procfile, 'w') as f:
            f.write('web: python manage.py migrate && gunicorn mutuelle_core.wsgi:application --bind 0.0.0.0:$PORT --workers 3\n')
        print_success("Procfile généré")
    else:
        print_success("Procfile existe")
    
    # Vérifier Django
    print_header("CONFIGURATION DJANGO")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        import django
        from django.conf import settings
        
        print_success(f"Django {django.__version__}")
        
        # Vérifications rapides
        checks = [
            ('DEBUG', not settings.DEBUG, "DEBUG doit être False en production"),
            ('SECRET_KEY', bool(settings.SECRET_KEY), "SECRET_KEY doit être définie"),
            ('ALLOWED_HOSTS', bool(settings.ALLOWED_HOSTS), "ALLOWED_HOSTS doit être configuré"),
        ]
        
        for name, condition, message in checks:
            if condition:
                print_success(f"{name}: OK")
            else:
                print_warning(f"{name}: {message}")
                
    except Exception as e:
        print_error(f"Erreur: {e}")
    
    # Recommandations finales
    print_header("RECOMMANDATIONS")
    
    print("1. Variables d'environnement Railway:")
    print("   SECRET_KEY=une_clé_très_longue_et_aléatoire")
    print("   DEBUG=False")
    print("   ALLOWED_HOSTS=*.railway.app")
    print("   DATABASE_URL=postgresql://... (fourni par Railway)")
    
    print("\n2. Commandes à exécuter localement:")
    print("   python manage.py collectstatic --noinput")
    print("   python manage.py migrate")
    
    print("\n3. Déploiement:")
    print("   - Poussez sur GitHub")
    print("   - Créez un projet sur railway.app")
    print("   - Importez depuis GitHub")
    print("   - Configurez les variables")
    print("   - Déployez!")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Diagnostic terminé!{Colors.RESET}")

if __name__ == '__main__':
    main()