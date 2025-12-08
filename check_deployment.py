#!/usr/bin/env python
"""
Script de vérification pour le déploiement sur Render.com
Exécutez: python check_deployment.py
"""
import os
import sys
import django
import subprocess
import platform
import shutil
from pathlib import Path

def print_header(text):
    """Afficher un en-tête stylisé"""
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60)

def print_success(text):
    """Afficher un message de succès"""
    print(f"✅ {text}")

def print_warning(text):
    """Afficher un message d'avertissement"""
    print(f"⚠️  {text}")

def print_error(text):
    """Afficher un message d'erreur"""
    print(f"❌ {text}")

def print_info(text):
    """Afficher un message d'information"""
    print(f"ℹ️  {text}")

def check_python_version():
    """Vérifier la version de Python"""
    print_header("1. VÉRIFICATION PYTHON")
    
    python_version = platform.python_version()
    required_version = (3, 8, 0)
    current_version = tuple(map(int, python_version.split('.')[:3]))
    
    print_info(f"Version Python actuelle: {python_version}")
    
    if current_version >= required_version:
        print_success(f"Version Python compatible (>=3.8)")
        return True
    else:
        print_error(f"Version Python trop ancienne. Requis: >=3.8")
        return False

def check_django_settings():
    """Vérifier les paramètres Django"""
    print_header("2. VÉRIFICATION SETTINGS DJANGO")
    
    try:
        # Configurer Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        django.setup()
        
        from django.conf import settings
        
        checks = []
        
        # Vérifier DEBUG
        if not settings.DEBUG:
            print_success("DEBUG = False (bon pour la production)")
        else:
            print_warning("DEBUG = True (à désactiver en production)")
        
        # Vérifier SECRET_KEY
        if settings.SECRET_KEY and settings.SECRET_KEY != 'django-insecure-development-key-change-in-production':
            print_success("SECRET_KEY configurée")
        else:
            print_error("SECRET_KEY doit être changée pour la production!")
        
        # Vérifier ALLOWED_HOSTS
        if settings.ALLOWED_HOSTS:
            print_success(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        else:
            print_warning("ALLOWED_HOSTS est vide")
        
        # Vérifier STATIC_ROOT
        if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
            print_success(f"STATIC_ROOT: {settings.STATIC_ROOT}")
        else:
            print_warning("STATIC_ROOT non défini")
        
        # Vérifier DATABASES
        db_engine = settings.DATABASES['default']['ENGINE']
        if 'postgresql' in db_engine or 'mysql' in db_engine:
            print_success(f"Base de données production: {db_engine}")
        else:
            print_warning(f"Base de données développement: {db_engine}")
        
        return True
        
    except Exception as e:
        print_error(f"Erreur lors de la vérification Django: {e}")
        return False

def check_requirements():
    """Vérifier les dépendances"""
    print_header("3. VÉRIFICATION DES DÉPENDANCES")
    
    requirements_file = 'requirements.txt'
    
    if not os.path.exists(requirements_file):
        print_error(f"Fichier {requirements_file} introuvable")
        return False
    
    print_info(f"Fichier {requirements_file} trouvé")
    
    # Lire les dépendances
    with open(requirements_file, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print_info(f"Nombre de dépendances: {len(requirements)}")
    
    # Vérifier les dépendances critiques
    critical_deps = [
        'Django',
        'gunicorn',
        'whitenoise',
        'psycopg2-binary',
        'dj-database-url'
    ]
    
    missing_critical = []
    for dep in critical_deps:
        found = any(dep.lower() in req.lower() for req in requirements)
        if not found:
            missing_critical.append(dep)
    
    if missing_critical:
        print_error(f"Dépendances critiques manquantes: {missing_critical}")
        return False
    else:
        print_success("Toutes les dépendances critiques sont présentes")
    
    return True

def check_build_files():
    """Vérifier les fichiers de build pour Render"""
    print_header("4. VÉRIFICATION FICHIERS RENDER")
    
    required_files = [
        ('render.yaml', True),
        ('build.sh', True),
        ('Procfile', True),
        ('requirements.txt', True),
        ('.gitignore', False),
        ('.env', False)
    ]
    
    all_ok = True
    
    for file_name, required in required_files:
        if os.path.exists(file_name):
            print_success(f"{file_name} - OK")
            
            # Vérifier les permissions pour build.sh
            if file_name == 'build.sh':
                if os.access(file_name, os.X_OK):
                    print_success("  Permissions d'exécution - OK")
                else:
                    print_warning("  Permissions d'exécution manquantes")
                    print_info("  Exécutez: chmod +x build.sh")
                    
        else:
            if required:
                print_error(f"{file_name} - MANQUANT (obligatoire)")
                all_ok = False
            else:
                print_warning(f"{file_name} - MANQUANT (optionnel)")
    
    return all_ok

def check_static_files():
    """Vérifier les fichiers statiques"""
    print_header("5. VÉRIFICATION FICHIERS STATIQUES")
    
    try:
        # Tester collectstatic
        print_info("Test de collectstatic...")
        result = subprocess.run(
            ['python', 'manage.py', 'collectstatic', '--noinput', '--dry-run'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success("collectstatic fonctionne")
            # Extraire le nombre de fichiers
            for line in result.stdout.split('\n'):
                if 'static files copied' in line or 'static file' in line:
                    print_info(f"  {line.strip()}")
        else:
            print_error(f"collectstatic échoué: {result.stderr}")
            return False
        
        # Vérifier STATICFILES_DIRS
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        django.setup()
        
        from django.conf import settings
        
        if hasattr(settings, 'STATICFILES_DIRS'):
            for static_dir in settings.STATICFILES_DIRS:
                if os.path.exists(static_dir):
                    print_success(f"Répertoire statique trouvé: {static_dir}")
                else:
                    print_warning(f"Répertoire statique introuvable: {static_dir}")
        
        return True
        
    except Exception as e:
        print_error(f"Erreur lors de la vérification statique: {e}")
        return False

def check_database():
    """Vérifier la base de données"""
    print_header("6. VÉRIFICATION BASE DE DONNÉES")
    
    try:
        # Tester les migrations
        print_info("Test des migrations...")
        result = subprocess.run(
            ['python', 'manage.py', 'makemigrations', '--check', '--dry-run'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success("Aucune migration en attente")
        else:
            print_warning("Migrations en attente détectées")
            print_info("  Exécutez: python manage.py makemigrations")
        
        # Tester la connexion DB
        print_info("Test de connexion base de données...")
        result = subprocess.run(
            ['python', 'manage.py', 'check', '--database', 'default'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success("Connexion base de données OK")
        else:
            print_error(f"Erreur connexion DB: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Erreur lors de la vérification DB: {e}")
        return False

def check_gunicorn():
    """Vérifier Gunicorn"""
    print_header("7. VÉRIFICATION GUNICORN")
    
    try:
        # Tester l'import de l'application WSGI
        import mutuelle_core.wsgi
        print_success("Application WSGI importée avec succès")
        
        # Vérifier la commande gunicorn
        print_info("Test de la commande Gunicorn (version)...")
        result = subprocess.run(
            ['gunicorn', '--version'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success(f"Gunicorn installé: {result.stdout.strip()}")
        else:
            print_warning("Gunicorn non trouvé")
            print_info("  Installez avec: pip install gunicorn")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Erreur Gunicorn: {e}")
        return False

def check_render_specific():
    """Vérifications spécifiques à Render"""
    print_header("8. VÉRIFICATIONS SPÉCIFIQUES RENDER")
    
    checks_passed = 0
    total_checks = 6
    
    # 1. Vérifier que DEBUG est configurable via env
    if 'DEBUG = os.environ.get' in open('mutuelle_core/settings.py').read():
        print_success("DEBUG configurable via variable d'environnement")
        checks_passed += 1
    else:
        print_warning("DEBUG devrait être configurable via variable d'environnement")
    
    # 2. Vérifier ALLOWED_HOSTS avec RENDER_EXTERNAL_HOSTNAME
    settings_content = open('mutuelle_core/settings.py').read()
    if 'RENDER_EXTERNAL_HOSTNAME' in settings_content:
        print_success("RENDER_EXTERNAL_HOSTNAME géré")
        checks_passed += 1
    else:
        print_warning("RENDER_EXTERNAL_HOSTNAME non géré")
    
    # 3. Vérifier DATABASE_URL
    if 'DATABASE_URL' in settings_content:
        print_success("DATABASE_URL géré")
        checks_passed += 1
    else:
        print_warning("DATABASE_URL non géré")
    
    # 4. Vérifier whitenoise
    if 'whitenoise' in settings_content.lower():
        print_success("WhiteNoise configuré")
        checks_passed += 1
    else:
        print_error("WhiteNoise non configuré (obligatoire pour Render)")
    
    # 5. Vérifier build.sh
    if os.path.exists('build.sh'):
        with open('build.sh', 'r') as f:
            content = f.read()
            if 'collectstatic' in content and 'migrate' in content:
                print_success("build.sh contient collectstatic et migrate")
                checks_passed += 1
            else:
                print_warning("build.sh incomplet")
    
    # 6. Vérifier health check
    urls_content = open('mutuelle_core/urls.py').read()
    if 'health' in urls_content.lower():
        print_success("Health check configuré")
        checks_passed += 1
    else:
        print_warning("Health check non configuré (recommandé pour Render)")
    
    print_info(f"Checks Render: {checks_passed}/{total_checks}")
    
    return checks_passed >= 4  # Au moins 4/6 checks

def generate_report(results):
    """Générer un rapport final"""
    print_header("📊 RAPPORT FINAL DE VÉRIFICATION")
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results if result)
    failed_tests = total_tests - passed_tests
    
    print(f"Tests exécutés: {total_tests}")
    print(f"✅ Tests réussis: {passed_tests}")
    print(f"❌ Tests échoués: {failed_tests}")
    
    if failed_tests == 0:
        print_success("🎉 Tous les tests ont réussi! Prêt pour le déploiement.")
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. Poussez votre code sur GitHub/GitLab")
        print("2. Créez un nouveau service Web sur Render.com")
        print("3. Connectez votre dépôt")
        print("4. Configurez les variables d'environnement:")
        print("   - SECRET_KEY (générée)")
        print("   - DEBUG=False")
        print("   - DATABASE_URL (auto depuis Render)")
        print("5. Déployez! 🚀")
    else:
        print_error("⚠️  Des problèmes ont été détectés. Corrigez-les avant le déploiement.")
        print("\n🔧 ACTIONS RECOMMANDÉES:")
        print("1. Vérifiez les erreurs ci-dessus")
        print("2. Corrigez les fichiers manquants ou incorrects")
        print("3. Relancez ce script: python check_deployment.py")
    
    return failed_tests == 0

def main():
    """Fonction principale"""
    print("🚀 VÉRIFICATION DÉPLOIEMENT RENDER.COM")
    print("Version: 1.0.0")
    print("="*60)
    
    # Vérifier qu'on est dans le bon répertoire
    if not os.path.exists('manage.py'):
        print_error("Exécutez ce script depuis la racine de votre projet Django")
        print_info("(là où se trouve manage.py)")
        sys.exit(1)
    
    # Exécuter toutes les vérifications
    results = []
    
    results.append(check_python_version())
    results.append(check_django_settings())
    results.append(check_requirements())
    results.append(check_build_files())
    results.append(check_static_files())
    results.append(check_database())
    results.append(check_gunicorn())
    results.append(check_render_specific())
    
    # Générer le rapport
    deployment_ready = generate_report(results)
    
    # Code de sortie
    sys.exit(0 if deployment_ready else 1)

if __name__ == '__main__':
    main()