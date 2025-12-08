#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET POUR PROJET DJANGO
Exécutez: python diagnostic.py
"""

import os
import sys
import platform
import subprocess
import json
import datetime
from pathlib import Path
import importlib
import inspect

# =============================================================================
# CONFIGURATION
# =============================================================================

class Colors:
    """Codes couleurs pour le terminal"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class DiagnosticReport:
    """Classe pour générer le rapport"""
    def __init__(self):
        self.results = []
        self.errors = []
        self.warnings = []
        self.successes = []
        
    def add_result(self, category, test, status, details=""):
        """Ajouter un résultat"""
        result = {
            'category': category,
            'test': test,
            'status': status,
            'details': details,
            'timestamp': datetime.datetime.now().isoformat()
        }
        self.results.append(result)
        
        if status == "ERROR":
            self.errors.append(result)
        elif status == "WARNING":
            self.warnings.append(result)
        elif status == "SUCCESS":
            self.successes.append(result)
            
        return result
    
    def print_summary(self):
        """Afficher le résumé"""
        print(f"\n{Colors.BOLD}{'='*80}{Colors.END}")
        print(f"{Colors.BOLD}📊 RÉSUMÉ DU DIAGNOSTIC{Colors.END}")
        print(f"{Colors.BOLD}{'='*80}{Colors.END}")
        print(f"✅ {Colors.GREEN}{len(self.successes)} tests réussis{Colors.END}")
        print(f"⚠️  {Colors.YELLOW}{len(self.warnings)} avertissements{Colors.END}")
        print(f"❌ {Colors.RED}{len(self.errors)} erreurs{Colors.END}")
        print(f"{Colors.BOLD}{'='*80}{Colors.END}")
        
    def save_report(self, filename="diagnostic_report.json"):
        """Sauvegarder le rapport JSON"""
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'summary': {
                'total': len(self.results),
                'successes': len(self.successes),
                'warnings': len(self.warnings),
                'errors': len(self.errors)
            },
            'results': self.results,
            'system_info': get_system_info()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"\n📄 Rapport sauvegardé: {filename}")

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def print_header(text):
    """Afficher un en-tête"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}  {text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")

def print_test_result(test, status, details=""):
    """Afficher le résultat d'un test"""
    if status == "SUCCESS":
        print(f"  ✅ {Colors.GREEN}{test}{Colors.END}")
    elif status == "WARNING":
        print(f"  ⚠️  {Colors.YELLOW}{test}{Colors.END}")
    elif status == "ERROR":
        print(f"  ❌ {Colors.RED}{test}{Colors.END}")
    
    if details:
        print(f"     {Colors.GRAY}{details}{Colors.END}")

def get_system_info():
    """Obtenir les informations système"""
    return {
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'processor': platform.processor(),
        'cwd': os.getcwd(),
        'user': os.getenv('USER') or os.getenv('USERNAME'),
        'timestamp': datetime.datetime.now().isoformat()
    }

# =============================================================================
# TESTS DE DIAGNOSTIC
# =============================================================================

def test_environment(report):
    """Tester l'environnement"""
    print_header("1. ENVIRONNEMENT SYSTÈME")
    
    # Version Python
    python_version = platform.python_version()
    required = (3, 8, 0)
    current = tuple(map(int, python_version.split('.')[:3]))
    
    if current >= required:
        report.add_result("ENV", "Version Python", "SUCCESS", f"Version: {python_version}")
        print_test_result("Version Python", "SUCCESS", f"Version: {python_version}")
    else:
        report.add_result("ENV", "Version Python", "ERROR", 
                         f"Version: {python_version} (Requis: >=3.8)")
        print_test_result("Version Python", "ERROR", 
                         f"Version: {python_version} (Requis: >=3.8)")
    
    # Gestionnaire de paquets
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            report.add_result("ENV", "Pip installé", "SUCCESS", result.stdout.split('\n')[0])
            print_test_result("Pip installé", "SUCCESS")
        else:
            report.add_result("ENV", "Pip installé", "ERROR", "Pip non trouvé")
            print_test_result("Pip installé", "ERROR")
    except:
        report.add_result("ENV", "Pip installé", "ERROR", "Erreur lors de la vérification")
        print_test_result("Pip installé", "ERROR")
    
    # Dossier courant
    cwd = os.getcwd()
    report.add_result("ENV", "Dossier courant", "SUCCESS", cwd)
    print_test_result("Dossier courant", "SUCCESS", cwd)
    
    # Fichier manage.py
    if os.path.exists('manage.py'):
        report.add_result("ENV", "Fichier manage.py", "SUCCESS", "Trouvé")
        print_test_result("Fichier manage.py", "SUCCESS")
    else:
        report.add_result("ENV", "Fichier manage.py", "ERROR", 
                         "Non trouvé - Êtes-vous dans le dossier Django ?")
        print_test_result("Fichier manage.py", "ERROR")

def test_project_structure(report):
    """Tester la structure du projet"""
    print_header("2. STRUCTURE DU PROJET")
    
    # Dossiers essentiels
    essential_dirs = [
        ('mutuelle_core', 'Package principal'),
        ('core', 'Application core'),
        ('membres', 'Application membres'),
        ('static', 'Fichiers statiques'),
        ('templates', 'Templates'),
    ]
    
    for dir_name, description in essential_dirs:
        if os.path.exists(dir_name):
            report.add_result("STRUCTURE", f"Dossier {dir_name}", "SUCCESS", description)
            print_test_result(f"Dossier {dir_name}", "SUCCESS", description)
        else:
            report.add_result("STRUCTURE", f"Dossier {dir_name}", "WARNING", 
                             f"Non trouvé - {description}")
            print_test_result(f"Dossier {dir_name}", "WARNING", f"Non trouvé - {description}")
    
    # Fichiers essentiels
    essential_files = [
        ('requirements.txt', 'Dépendances Python'),
        ('.env', 'Variables d\'environnement (optionnel)'),
        ('.gitignore', 'Fichiers à ignorer par Git'),
        ('render.yaml', 'Configuration Render (déploiement)'),
        ('Procfile', 'Configuration processus (déploiement)'),
        ('build.sh', 'Script de build (déploiement)'),
    ]
    
    for file_name, description in essential_files:
        if os.path.exists(file_name):
            report.add_result("STRUCTURE", f"Fichier {file_name}", "SUCCESS", description)
            print_test_result(f"Fichier {file_name}", "SUCCESS", description)
        else:
            status = "WARNING" if file_name in ['.env', 'render.yaml', 'Procfile', 'build.sh'] else "ERROR"
            report.add_result("STRUCTURE", f"Fichier {file_name}", status, 
                             f"Non trouvé - {description}")
            print_test_result(f"Fichier {file_name}", status, f"Non trouvé - {description}")

def test_django_settings(report):
    """Tester les paramètres Django"""
    print_header("3. PARAMÈTRES DJANGO")
    
    try:
        # Essayer d'importer les settings
        sys.path.insert(0, os.getcwd())
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        
        import django
        django.setup()
        
        from django.conf import settings
        
        # DEBUG mode
        debug_status = "DEBUG activé" if settings.DEBUG else "DEBUG désactivé"
        status = "WARNING" if settings.DEBUG else "SUCCESS"
        report.add_result("DJANGO", "Mode DEBUG", status, debug_status)
        print_test_result("Mode DEBUG", status, debug_status)
        
        # ALLOWED_HOSTS
        if settings.ALLOWED_HOSTS:
            report.add_result("DJANGO", "ALLOWED_HOSTS", "SUCCESS", 
                            f"Configuré: {settings.ALLOWED_HOSTS}")
            print_test_result("ALLOWED_HOSTS", "SUCCESS", 
                            f"{len(settings.ALLOWED_HOSTS)} host(s) configuré(s)")
        else:
            report.add_result("DJANGO", "ALLOWED_HOSTS", "WARNING", "Vide - Risque en production")
            print_test_result("ALLOWED_HOSTS", "WARNING", "Vide - Risque en production")
        
        # SECRET_KEY
        secret_key = settings.SECRET_KEY
        if secret_key and 'insecure' not in secret_key and len(secret_key) >= 20:
            report.add_result("DJANGO", "SECRET_KEY", "SUCCESS", "Configurée (sécurisée)")
            print_test_result("SECRET_KEY", "SUCCESS", "Configurée (sécurisée)")
        else:
            report.add_result("DJANGO", "SECRET_KEY", "ERROR", 
                            "Non sécurisée ou trop courte - À changer en production")
            print_test_result("SECRET_KEY", "ERROR", 
                            "Non sécurisée ou trop courte - À changer en production")
        
        # Base de données
        db_engine = settings.DATABASES['default']['ENGINE']
        if 'sqlite3' in db_engine:
            report.add_result("DJANGO", "Base de données", "WARNING", 
                            f"SQLite - OK pour développement seulement")
            print_test_result("Base de données", "WARNING", "SQLite - Développement seulement")
        elif 'postgresql' in db_engine or 'mysql' in db_engine:
            report.add_result("DJANGO", "Base de données", "SUCCESS", 
                            f"Production: {db_engine}")
            print_test_result("Base de données", "SUCCESS", f"Production: {db_engine}")
        else:
            report.add_result("DJANGO", "Base de données", "SUCCESS", f"{db_engine}")
            print_test_result("Base de données", "SUCCESS", f"{db_engine}")
        
        # Applications installées
        installed_apps = len(settings.INSTALLED_APPS)
        report.add_result("DJANGO", "Applications", "SUCCESS", 
                         f"{installed_apps} application(s) installée(s)")
        print_test_result("Applications", "SUCCESS", f"{installed_apps} application(s)")
        
        # Fichiers statiques
        if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
            report.add_result("DJANGO", "STATIC_ROOT", "SUCCESS", settings.STATIC_ROOT)
            print_test_result("STATIC_ROOT", "SUCCESS", "Configuré")
        else:
            report.add_result("DJANGO", "STATIC_ROOT", "WARNING", 
                             "Non configuré - Obligatoire pour collectstatic")
            print_test_result("STATIC_ROOT", "WARNING", "Non configuré")
        
        # Middleware
        middleware_count = len(settings.MIDDLEWARE)
        report.add_result("DJANGO", "Middleware", "SUCCESS", f"{middleware_count} middleware(s)")
        print_test_result("Middleware", "SUCCESS", f"{middleware_count} middleware(s)")
        
        # WhiteNoise (pour Render)
        if 'whitenoise' in str(settings.MIDDLEWARE).lower():
            report.add_result("DJANGO", "WhiteNoise", "SUCCESS", "Configuré pour Render")
            print_test_result("WhiteNoise", "SUCCESS", "Configuré pour Render")
        else:
            report.add_result("DJANGO", "WhiteNoise", "WARNING", 
                             "Non configuré - Recommandé pour Render")
            print_test_result("WhiteNoise", "WARNING", "Non configuré")
            
    except Exception as e:
        report.add_result("DJANGO", "Chargement settings", "ERROR", str(e))
        print_test_result("Chargement settings", "ERROR", str(e))

def test_database(report):
    """Tester la base de données"""
    print_header("4. BASE DE DONNÉES")
    
    try:
        # Vérifier les migrations
        result = subprocess.run(
            [sys.executable, 'manage.py', 'makemigrations', '--check', '--dry-run'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            report.add_result("DATABASE", "Migrations", "SUCCESS", "Aucune migration en attente")
            print_test_result("Migrations", "SUCCESS")
        else:
            report.add_result("DATABASE", "Migrations", "WARNING", "Migrations en attente détectées")
            print_test_result("Migrations", "WARNING", "Exécutez: python manage.py makemigrations")
        
        # Tester la connexion
        result = subprocess.run(
            [sys.executable, 'manage.py', 'check', '--database', 'default'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            report.add_result("DATABASE", "Connexion DB", "SUCCESS", "Connexion établie")
            print_test_result("Connexion DB", "SUCCESS")
        else:
            report.add_result("DATABASE", "Connexion DB", "ERROR", result.stderr[:200])
            print_test_result("Connexion DB", "ERROR", result.stderr[:200])
            
    except Exception as e:
        report.add_result("DATABASE", "Tests DB", "ERROR", str(e))
        print_test_result("Tests DB", "ERROR", str(e))

def test_static_files(report):
    """Tester les fichiers statiques"""
    print_header("5. FICHIERS STATIQUES")
    
    try:
        # Tester collectstatic
        result = subprocess.run(
            [sys.executable, 'manage.py', 'collectstatic', '--noinput', '--dry-run'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # Extraire le nombre de fichiers
            for line in result.stdout.split('\n'):
                if 'static files copied' in line:
                    report.add_result("STATIC", "collectstatic", "SUCCESS", line.strip())
                    print_test_result("collectstatic", "SUCCESS", line.strip())
                    break
            else:
                report.add_result("STATIC", "collectstatic", "SUCCESS", "Fonctionne")
                print_test_result("collectstatic", "SUCCESS")
        else:
            report.add_result("STATIC", "collectstatic", "ERROR", result.stderr[:200])
            print_test_result("collectstatic", "ERROR", result.stderr[:200])
            
    except Exception as e:
        report.add_result("STATIC", "collectstatic", "ERROR", str(e))
        print_test_result("collectstatic", "ERROR", str(e))

def test_dependencies(report):
    """Tester les dépendances"""
    print_header("6. DÉPENDANCES")
    
    # Vérifier requirements.txt
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        report.add_result("DEPS", "requirements.txt", "SUCCESS", 
                         f"{len(requirements)} dépendance(s) listée(s)")
        print_test_result("requirements.txt", "SUCCESS", f"{len(requirements)} dépendance(s)")
        
        # Dépendances critiques
        critical_deps = [
            'Django',
            'whitenoise',
            'gunicorn',
            'psycopg2',
        ]
        
        missing = []
        for dep in critical_deps:
            if not any(dep.lower() in req.lower() for req in requirements):
                missing.append(dep)
        
        if missing:
            report.add_result("DEPS", "Dépendances critiques", "ERROR", 
                             f"Manquantes: {missing}")
            print_test_result("Dépendances critiques", "ERROR", f"Manquantes: {missing}")
        else:
            report.add_result("DEPS", "Dépendances critiques", "SUCCESS", "Toutes présentes")
            print_test_result("Dépendances critiques", "SUCCESS")
            
    else:
        report.add_result("DEPS", "requirements.txt", "ERROR", "Fichier non trouvé")
        print_test_result("requirements.txt", "ERROR")

def test_urls_and_views(report):
    """Tester les URLs et vues"""
    print_header("7. URLs ET VUES")
    
    try:
        # Vérifier les URLs principales
        from django.urls import get_resolver
        resolver = get_resolver()
        
        # URLs essentielles
        essential_urls = [
            ('/', 'Page d\'accueil'),
            ('/health/', 'Health check'),
            ('/admin/', 'Admin Django'),
            ('/dashboard/', 'Dashboard principal'),
        ]
        
        for url, description in essential_urls:
            try:
                resolver.resolve(url)
                report.add_result("URLS", f"URL {url}", "SUCCESS", description)
                print_test_result(f"URL {url}", "SUCCESS", description)
            except:
                report.add_result("URLS", f"URL {url}", "WARNING", f"Non résolue - {description}")
                print_test_result(f"URL {url}", "WARNING", f"Non résolue - {description}")
        
        # Compter les URLs
        url_patterns = []
        def collect_urls(urlpatterns, namespace=None):
            for pattern in urlpatterns:
                if hasattr(pattern, 'url_patterns'):  # Include
                    collect_urls(pattern.url_patterns, 
                                namespace or getattr(pattern, 'namespace', None))
                else:
                    url_patterns.append(pattern)
        
        collect_urls(resolver.url_patterns)
        report.add_result("URLS", "Nombre d'URLs", "SUCCESS", f"{len(url_patterns)} motif(s) d'URL")
        print_test_result("Nombre d'URLs", "SUCCESS", f"{len(url_patterns)} motif(s)")
        
    except Exception as e:
        report.add_result("URLS", "Tests URLs", "ERROR", str(e))
        print_test_result("Tests URLs", "ERROR", str(e))

def test_application_health(report):
    """Tester la santé des applications"""
    print_header("8. SANTÉ DES APPLICATIONS")
    
    try:
        # Lancer un check Django
        result = subprocess.run(
            [sys.executable, 'manage.py', 'check'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            report.add_result("HEALTH", "Check Django", "SUCCESS", "Aucune erreur détectée")
            print_test_result("Check Django", "SUCCESS")
        else:
            report.add_result("HEALTH", "Check Django", "ERROR", result.stderr[:500])
            print_test_result("Check Django", "ERROR", result.stderr[:500])
        
        # Check déploiement
        result = subprocess.run(
            [sys.executable, 'manage.py', 'check', '--deploy'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            report.add_result("HEALTH", "Check déploiement", "SUCCESS", "Prêt pour la production")
            print_test_result("Check déploiement", "SUCCESS", "Prêt pour la production")
        else:
            report.add_result("HEALTH", "Check déploiement", "WARNING", 
                             "Problèmes détectés pour la production")
            print_test_result("Check déploiement", "WARNING", 
                            "Problèmes détectés pour la production")
            
    except Exception as e:
        report.add_result("HEALTH", "Tests santé", "ERROR", str(e))
        print_test_result("Tests santé", "ERROR", str(e))

def test_deployment_readiness(report):
    """Tester la préparation au déploiement"""
    print_header("9. PRÉPARATION DÉPLOIEMENT")
    
    # Fichiers Render
    render_files = ['render.yaml', 'Procfile', 'build.sh']
    
    for file in render_files:
        if os.path.exists(file):
            report.add_result("DEPLOY", f"Fichier {file}", "SUCCESS", "Présent")
            print_test_result(f"Fichier {file}", "SUCCESS")
            
            # Vérifier le contenu de build.sh
            if file == 'build.sh':
                if os.access(file, os.X_OK):
                    report.add_result("DEPLOY", "Permissions build.sh", "SUCCESS", "Exécutable")
                    print_test_result("Permissions build.sh", "SUCCESS")
                else:
                    report.add_result("DEPLOY", "Permissions build.sh", "WARNING", 
                                     "Non exécutable - chmod +x build.sh")
                    print_test_result("Permissions build.sh", "WARNING", 
                                     "Non exécutable - chmod +x build.sh")
        else:
            report.add_result("DEPLOY", f"Fichier {file}", "WARNING", 
                             f"Manquant - Recommandé pour Render")
            print_test_result(f"Fichier {file}", "WARNING", "Manquant")
    
    # Health check
    try:
        import django
        from django.conf import settings
        
        if hasattr(settings, 'ALLOWED_HOSTS') and settings.ALLOWED_HOSTS:
            if any('.onrender.com' in host or '.herokuapp.com' in host for host in settings.ALLOWED_HOSTS):
                report.add_result("DEPLOY", "Hosts déploiement", "SUCCESS", 
                                 "Configuré pour plateforme cloud")
                print_test_result("Hosts déploiement", "SUCCESS")
            else:
                report.add_result("DEPLOY", "Hosts déploiement", "WARNING", 
                                 "À configurer pour votre domaine")
                print_test_result("Hosts déploiement", "WARNING", 
                                 "À configurer pour votre domaine")
    except:
        pass

def test_app_specific(report):
    """Tests spécifiques aux applications"""
    print_header("10. APPLICATIONS SPÉCIFIQUES")
    
    apps_to_check = [
        ('core', ['views.py', 'urls.py', 'models.py']),
        ('membres', ['views.py', 'urls.py', 'models.py']),
        ('agents', ['views.py', 'urls.py', 'models.py']),
        ('medecin', ['views.py', 'urls.py', 'models.py']),
        ('pharmacien', ['views.py', 'urls.py', 'models.py']),
        ('assureur', ['views.py', 'urls.py', 'models.py']),
    ]
    
    for app, files in apps_to_check:
        if os.path.exists(app):
            # Vérifier les fichiers essentiels
            missing_files = []
            for file in files:
                if not os.path.exists(os.path.join(app, file)):
                    missing_files.append(file)
            
            if not missing_files:
                report.add_result("APPS", f"Application {app}", "SUCCESS", "Complète")
                print_test_result(f"Application {app}", "SUCCESS")
            else:
                report.add_result("APPS", f"Application {app}", "WARNING", 
                                 f"Fichiers manquants: {missing_files}")
                print_test_result(f"Application {app}", "WARNING", 
                                 f"Fichiers manquants: {missing_files}")
        else:
            report.add_result("APPS", f"Application {app}", "WARNING", "Non trouvée")
            print_test_result(f"Application {app}", "WARNING", "Non trouvée")

# =============================================================================
# FONCTION PRINCIPALE
# =============================================================================

def run_full_diagnostic():
    """Exécuter le diagnostic complet"""
    print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}🔍 DIAGNOSTIC COMPLET DU PROJET DJANGO{Colors.END}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*80}{Colors.END}")
    print(f"{Colors.GRAY}Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    print(f"{Colors.GRAY}Répertoire: {os.getcwd()}{Colors.END}")
    print(f"{Colors.GRAY}Python: {platform.python_version()}{Colors.END}")
    
    # Initialiser le rapport
    report = DiagnosticReport()
    
    # Exécuter tous les tests
    try:
        test_environment(report)
        test_project_structure(report)
        test_django_settings(report)
        test_database(report)
        test_static_files(report)
        test_dependencies(report)
        test_urls_and_views(report)
        test_application_health(report)
        test_deployment_readiness(report)
        test_app_specific(report)
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Diagnostic interrompu par l'utilisateur{Colors.END}")
        report.add_result("SYSTEM", "Diagnostic", "ERROR", "Interrompu par l'utilisateur")
    
    except Exception as e:
        print(f"\n{Colors.RED}❌ Erreur lors du diagnostic: {e}{Colors.END}")
        report.add_result("SYSTEM", "Diagnostic", "ERROR", f"Erreur: {str(e)}")
    
    # Afficher le résumé
    report.print_summary()
    
    # Sauvegarder le rapport
    report.save_report()
    
    # Afficher les recommandations
    print_recommendations(report)
    
    return report

def print_recommendations(report):
    """Afficher les recommandations basées sur les résultats"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}📋 RECOMMANDATIONS{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    
    recommendations = []
    
    # Analyser les erreurs et avertissements
    for error in report.errors:
        if "SECRET_KEY" in error['test']:
            recommendations.append("🔐 Changez SECRET_KEY pour une clé sécurisée en production")
        elif "manage.py" in error['test']:
            recommendations.append("📁 Exécutez depuis le dossier racine du projet Django")
        elif "Pip" in error['test']:
            recommendations.append("📦 Installez pip: python -m ensurepip --upgrade")
        elif "Version Python" in error['test']:
            recommendations.append("🐍 Mettez à jour Python vers la version 3.8+")
    
    for warning in report.warnings:
        if "DEBUG" in warning['test'] and warning['details'] == "DEBUG activé":
            recommendations.append("🐛 Désactivez DEBUG (DEBUG=False) pour la production")
        elif "ALLOWED_HOSTS" in warning['test']:
            recommendations.append("🌐 Configurez ALLOWED_HOSTS avec votre domaine")
        elif "SQLite" in warning['test']:
            recommendations.append("🗄️  Passez à PostgreSQL pour la production")
        elif "Migrations" in warning['test']:
            recommendations.append("🔄 Exécutez les migrations: python manage.py makemigrations")
    
    # Recommandations générales
    if not os.path.exists('requirements.txt'):
        recommendations.append("📄 Créez un fichier requirements.txt: pip freeze > requirements.txt")
    
    if not os.path.exists('.env'):
        recommendations.append("🔧 Créez un fichier .env pour les variables d'environnement")
    
    if report.errors:
        recommendations.append("🚨 Corrigez les erreurs avant le déploiement")
    
    # Afficher les recommandations
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
    else:
        print(f"{Colors.GREEN}🎉 Aucune recommandation critique - Votre projet semble en bonne santé!{Colors.END}")
    
    print(f"\n{Colors.BOLD}Prochaines étapes:{Colors.END}")
    print("1. Corrigez les erreurs et avertissements ci-dessus")
    print("2. Testez localement: python manage.py runserver")
    print("3. Pour Render: configurez les variables d'environnement")
    print("4. Déployez! 🚀")

# =============================================================================
# COMMANDES UTILITAIRES
# =============================================================================

def quick_check():
    """Vérification rapide"""
    print(f"{Colors.BOLD}⚡ VÉRIFICATION RAPIDE{Colors.END}")
    
    checks = [
        ("manage.py", os.path.exists('manage.py'), "Fichier manage.py"),
        ("requirements.txt", os.path.exists('requirements.txt'), "Dépendances"),
        ("settings.py", os.path.exists('mutuelle_core/settings.py'), "Paramètres Django"),
        ("Base de données", test_db_quick(), "Connexion DB"),
        ("Collectstatic", test_collectstatic_quick(), "Fichiers statiques"),
    ]
    
    all_ok = True
    for name, result, desc in checks:
        if result:
            print(f"✅ {Colors.GREEN}{name}{Colors.END}: {desc}")
        else:
            print(f"❌ {Colors.RED}{name}{Colors.END}: {desc}")
            all_ok = False
    
    return all_ok

def test_db_quick():
    """Test rapide DB"""
    try:
        subprocess.run([sys.executable, 'manage.py', 'check', '--database', 'default'], 
                      capture_output=True, check=True)
        return True
    except:
        return False

def test_collectstatic_quick():
    """Test rapide collectstatic"""
    try:
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput', '--dry-run'], 
                      capture_output=True, check=True)
        return True
    except:
        return False

# =============================================================================
# POINT D'ENTRÉE
# =============================================================================

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Diagnostic du projet Django')
    parser.add_argument('--quick', action='store_true', help='Vérification rapide seulement')
    parser.add_argument('--fix', action='store_true', help='Essayer de corriger les problèmes')
    parser.add_argument('--output', type=str, default='diagnostic_report.json', 
                       help='Fichier de sortie du rapport')
    
    args = parser.parse_args()
    
    if args.quick:
        quick_check()
    else:
        report = run_full_diagnostic()
        
        if args.fix:
            print(f"\n{Colors.BOLD}🛠️  TENTATIVE DE CORRECTION AUTOMATIQUE{Colors.END}")
            try:
                # Essayer d'installer les dépendances manquantes
                if os.path.exists('requirements.txt'):
                    print("📦 Installation des dépendances...")
                    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
                
                # Appliquer les migrations
                print("🔄 Application des migrations...")
                subprocess.run([sys.executable, 'manage.py', 'migrate'])
                
                # Collectstatic
                print("📁 Collecte des fichiers statiques...")
                subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'])
                
                print(f"{Colors.GREEN}✅ Corrections appliquées!{Colors.END}")
                
            except Exception as e:
                print(f"{Colors.RED}❌ Erreur lors des corrections: {e}{Colors.END}")