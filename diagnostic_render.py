#!/usr/bin/env python3
"""
SCRIPT DE DIAGNOSTIC POUR DÉPLOIEMENT RENDER
Vérifie tous les points critiques pour un déploiement réussi.
"""

import os
import sys
import yaml
import subprocess
import re
from pathlib import Path
from packaging import version

def print_section(title):
    """Affiche une section du diagnostic."""
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def print_check(message, status):
    """Affiche une vérification avec un statut."""
    if status == "OK":
        print(f"✅ {message}")
    elif status == "WARNING":
        print(f"⚠️  {message}")
    else:
        print(f"❌ {message}")

def check_file_exists(filepath, description):
    """Vérifie si un fichier existe."""
    if os.path.exists(filepath):
        print_check(f"{description}: {filepath}", "OK")
        return True
    else:
        print_check(f"{description}: {filepath} - FICHIER MANQUANT", "ERROR")
        return False

def check_render_yaml():
    """Vérifie le fichier render.yaml."""
    print_section("1. CONFIGURATION RENDER.YAML")
    
    if not check_file_exists("render.yaml", "Fichier render.yaml"):
        return False
    
    try:
        with open("render.yaml", 'r') as f:
            content = f.read()
            
        # Vérifie la syntaxe YAML
        config = yaml.safe_load(content)
        
        if not config or 'services' not in config:
            print_check("Structure YAML incorrecte (pas de 'services')", "ERROR")
            return False
        
        service = config['services'][0]
        
        # Vérifications critiques
        checks = [
            ("Type de service défini", 'type' in service and service['type'] == 'web', "OK"),
            ("Nom du service défini", 'name' in service, "OK"),
            ("Environnement Python défini", 'env' in service and service['env'] == 'python', "OK"),
            ("Commande de build présente", 'buildCommand' in service, "OK"),
            ("Commande de démarrage présente", 'startCommand' in service, "OK"),
        ]
        
        for desc, condition, _ in checks:
            print_check(desc, "OK" if condition else "ERROR")
        
        # Vérifie spécifiquement la commande start
        if 'startCommand' in service:
            start_cmd = service['startCommand']
            if 'mutuelle_core.wsgi:application' in start_cmd:
                print_check("StartCommand pointe vers le bon module WSGI", "OK")
            else:
                print_check(f"StartCommand incorrect: {start_cmd}", "ERROR")
                return False
        
        # Vérifie les variables d'environnement
        if 'envVars' in service:
            env_vars = {v['key']: v.get('value', '') for v in service['envVars']}
            required_vars = ['DJANGO_SETTINGS_MODULE', 'SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS']
            
            for var in required_vars:
                if var in env_vars:
                    print_check(f"Variable {var} définie", "OK")
                else:
                    print_check(f"Variable {var} manquante", "WARNING")
        
        return True
        
    except yaml.YAMLError as e:
        print_check(f"Erreur de syntaxe YAML: {e}", "ERROR")
        return False
    except Exception as e:
        print_check(f"Erreur inattendue: {e}", "ERROR")
        return False

def check_project_structure():
    """Vérifie la structure du projet Django."""
    print_section("2. STRUCTURE DU PROJET DJANGO")
    
    required_files = [
        ("manage.py", "Fichier manage.py"),
        ("mutuelle_core/__init__.py", "Package Django principal"),
        ("mutuelle_core/settings.py", "Fichier de configuration Django"),
        ("mutuelle_core/wsgi.py", "Fichier WSGI (critique pour Render)"),
        ("mutuelle_core/urls.py", "Fichier de routage URL"),
        ("requirements.txt", "Fichier des dépendances"),
    ]
    
    all_exist = True
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_exist = False
    
    return all_exist

def check_python_environment():
    """Vérifie l'environnement Python et les dépendances."""
    print_section("3. ENVIRONNEMENT PYTHON & DÉPENDANCES")
    
    try:
        # Version Python
        python_version = sys.version.split()[0]
        print_check(f"Version Python locale: {python_version}", "OK")
        
        # Vérifie si c'est Python 3.11+
        if version.parse(python_version) >= version.parse("3.11.0"):
            print_check("Python 3.11+ (bon pour compatibilité)", "OK")
        else:
            print_check(f"Python {python_version} - pourrait causer des problèmes", "WARNING")
        
        # Vérifie requirements.txt
        if check_file_exists("requirements.txt", "Fichier requirements.txt"):
            with open("requirements.txt", 'r') as f:
                requirements = f.read()
            
            # Vérifie les dépendances critiques
            critical_deps = {
                'Django': 'Framework Django',
                'gunicorn': 'Serveur WSGI',
                'whitenoise': 'Fichiers statiques',
                'psycopg2-binary': 'PostgreSQL',
                'dj-database-url': 'Configuration DB',
                'Pillow': 'Traitement images',
            }
            
            for dep, desc in critical_deps.items():
                if re.search(rf'^{dep}[>=<]', requirements, re.MULTILINE):
                    print_check(f"{desc} ({dep}) présent", "OK")
                else:
                    print_check(f"{desc} ({dep}) MANQUANT", "ERROR")
            
            # Vérifie les versions compatibles Python 3.13
            problematic_deps = [
                (r'Pillow==10\.[0-5]\.', 'Pillow 10.0-10.5 incompatible Python 3.13'),
                (r'gevent<25\.0\.0', 'gevent <25.0.0 incompatible Python 3.13'),
                (r'eventlet<0\.37\.0', 'eventlet <0.37.0 incompatible Python 3.13'),
            ]
            
            for pattern, message in problematic_deps:
                if re.search(pattern, requirements):
                    print_check(message, "ERROR")
        
        return True
        
    except Exception as e:
        print_check(f"Erreur lors de la vérification Python: {e}", "ERROR")
        return False

def check_poetry_interference():
    """Vérifie l'interférence de Poetry."""
    print_section("4. VÉRIFICATION POETRY INTERFÉRENCE")
    
    poetry_files = [
        ("pyproject.toml", "Fichier de configuration Poetry"),
        ("poetry.lock", "Fichier de verrouillage Poetry"),
    ]
    
    has_poetry = False
    for filepath, description in poetry_files:
        if os.path.exists(filepath):
            print_check(f"{description} PRÉSENT - Problème potentiel", "ERROR")
            has_poetry = True
        else:
            print_check(f"{description} absent (bon)", "OK")
    
    if has_poetry:
        print("\n⚠️  ATTENTION: Render détectera automatiquement Poetry")
        print("   et ignorera PYTHON_VERSION dans render.yaml")
        print("   Solution: Supprimez ces fichiers ou utilisez Python 3.13+")
    
    return not has_poetry

def check_django_settings():
    """Vérifie la configuration Django pour la production."""
    print_section("5. CONFIGURATION DJANGO PRODUCTION")
    
    if not check_file_exists("mutuelle_core/settings.py", "Fichier settings.py"):
        return False
    
    try:
        with open("mutuelle_core/settings.py", 'r') as f:
            settings_content = f.read()
        
        checks = [
            ("SECRET_KEY défini", 'SECRET_KEY' in settings_content, "WARNING"),
            ("DEBUG peut être False", 'DEBUG\s*=\s*False' in settings_content or 'DEBUG\s*=\s*os.environ' in settings_content, "OK"),
            ("ALLOWED_HOSTS configuré", 'ALLOWED_HOSTS' in settings_content and not 'ALLOWED_HOSTS\s*=\s*\[\]' in settings_content, "OK"),
            ("STATIC_ROOT défini", 'STATIC_ROOT' in settings_content, "OK"),
            ("Base de données configurée", 'DATABASES' in settings_content, "OK"),
            ("Middleware WhiteNoise", 'whitenoise.middleware.WhiteNoiseMiddleware' in settings_content, "OK"),
            ("dj-database-url importé", 'import dj_database_url' in settings_content or 'dj_database_url.config' in settings_content, "OK"),
        ]
        
        all_ok = True
        for desc, condition, default_status in checks:
            if condition:
                print_check(desc, "OK")
            else:
                print_check(desc, default_status)
                if default_status == "ERROR":
                    all_ok = False
        
        return all_ok
        
    except Exception as e:
        print_check(f"Erreur lecture settings.py: {e}", "ERROR")
        return False

def check_wsgi_configuration():
    """Vérifie la configuration WSGI."""
    print_section("6. CONFIGURATION WSGI")
    
    if not check_file_exists("mutuelle_core/wsgi.py", "Fichier wsgi.py"):
        return False
    
    try:
        with open("mutuelle_core/wsgi.py", 'r') as f:
            wsgi_content = f.read()
        
        checks = [
            ("Import get_wsgi_application", 'from django.core.wsgi import get_wsgi_application' in wsgi_content, "OK"),
            ("DJANGO_SETTINGS_MODULE défini", 'DJANGO_SETTINGS_MODULE' in wsgi_content, "OK"),
            ("Variable 'application' définie", 'application\s*=' in wsgi_content, "OK"),
            ("Module correct: mutuelle_core.settings", 'mutuelle_core.settings' in wsgi_content, "OK"),
        ]
        
        all_ok = True
        for desc, condition, _ in checks:
            status = "OK" if condition else "ERROR"
            print_check(desc, status)
            if not condition:
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print_check(f"Erreur lecture wsgi.py: {e}", "ERROR")
        return False

def check_git_status():
    """Vérifie l'état Git."""
    print_section("7. ÉTAT GIT")
    
    try:
        # Vérifie si c'est un dépôt Git
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print_check("Dépôt Git valide", "OK")
            
            # Vérifie les fichiers non commités
            result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
            if result.stdout.strip():
                print_check("Fichiers non commités présents", "WARNING")
                print("   " + result.stdout.replace('\n', '\n   '))
            else:
                print_check("Tout est commité", "OK")
            
            # Branche actuelle
            result = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True)
            branch = result.stdout.strip()
            print_check(f"Branche actuelle: {branch}", "OK")
            
            return True
        else:
            print_check("Pas un dépôt Git ou erreur Git", "WARNING")
            return False
            
    except Exception as e:
        print_check(f"Erreur Git: {e}", "WARNING")
        return False

def generate_summary(results):
    """Génère un résumé des résultats."""
    print_section("📊 RÉSUMÉ DU DIAGNOSTIC")
    
    total_checks = len(results)
    passed = sum(1 for _, status in results if status == "OK")
    warnings = sum(1 for _, status in results if status == "WARNING")
    errors = sum(1 for _, status in results if status == "ERROR")
    
    print(f"Total vérifications: {total_checks}")
    print(f"✅ Succès: {passed}")
    print(f"⚠️  Avertissements: {warnings}")
    print(f"❌ Erreurs: {errors}")
    
    if errors == 0:
        print("\n🎉 Votre projet est PRÊT pour le déploiement sur Render!")
    else:
        print("\n🔧 Actions requises avant déploiement:")
        
        # Recommandations basées sur les erreurs
        for check_name, status in results:
            if status == "ERROR":
                if "render.yaml" in check_name:
                    print("  • Corrigez votre fichier render.yaml (voir ci-dessus)")
                elif "FICHIER MANQUANT" in check_name:
                    print(f"  • Créez le fichier manquant: {check_name.split(':')[0]}")
                elif "Poetry" in check_name:
                    print("  • Supprimez pyproject.toml et poetry.lock")
                elif "StartCommand" in check_name:
                    print("  • Corrigez la startCommand dans render.yaml")
                elif "Dépendance" in check_name:
                    print("  • Mettez à jour requirements.txt avec versions compatibles")

def main():
    """Fonction principale."""
    print("="*60)
    print("🩺 DIAGNOSTIC COMPLET - DÉPLOIEMENT RENDER")
    print("="*60)
    
    # Vérifie le répertoire courant
    current_dir = os.getcwd()
    print(f"\n📁 Répertoire courant: {current_dir}")
    
    # Exécute toutes les vérifications
    results = []
    
    results.append(("Structure projet", "OK" if check_project_structure() else "ERROR"))
    results.append(("Configuration Render", "OK" if check_render_yaml() else "ERROR"))
    results.append(("Environnement Python", "OK" if check_python_environment() else "WARNING"))
    results.append(("Interférence Poetry", "OK" if check_poetry_interference() else "ERROR"))
    results.append(("Settings Django", "OK" if check_django_settings() else "WARNING"))
    results.append(("Configuration WSGI", "OK" if check_wsgi_configuration() else "ERROR"))
    results.append(("État Git", "OK" if check_git_status() else "WARNING"))
    
    # Résumé final
    generate_summary(results)
    
    # Recommandations finales
    print_section("🚀 PROCHAINES ÉTAPES RECOMMANDÉES")
    
    print("1. Si des erreurs ❌ sont présentes:")
    print("   • Corrigez-les en suivant les suggestions ci-dessus")
    print("   • Relancez ce diagnostic: python diagnostic_render.py")
    
    print("\n2. Pour forcer le déploiement sur Render:")
    print("   • Poussez vos corrections: git add . && git commit -m 'fix' && git push")
    print("   • Sur Render: Settings > Manual Deploy > 'Clear build cache & deploy'")
    
    print("\n3. Si Render ignore toujours render.yaml:")
    print("   • OPTION A: Configurez manuellement dans l'interface Render")
    print("     - Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput")
    print("     - Start Command: gunicorn mutuelle_core.wsgi:application --bind 0.0.0.0:$PORT")
    print("   • OPTION B: Créez un nouveau service Web sur Render")

if __name__ == "__main__":
    # Vérifie si packaging est installé
    try:
        import packaging
    except ImportError:
        print("⚠️  Installation du module 'packaging' requis...")
        subprocess.run([sys.executable, "-m", "pip", "install", "packaging"])
    
    # Vérifie si PyYAML est installé
    try:
        import yaml
    except ImportError:
        print("⚠️  Installation du module 'PyYAML' requis...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyYAML"])
    
    main()