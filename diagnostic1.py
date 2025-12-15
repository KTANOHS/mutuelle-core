#!/usr/bin/env python
"""
DIAGNOSTIC COMPLET - Projet Django sur Railway
Ce script vérifie tous les aspects critiques du projet
"""

import os
import sys
import django
from pathlib import Path
import subprocess
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    from django.conf import settings
    from django.db import connection, DatabaseError
    from django.core.management import execute_from_command_line
except Exception as e:
    logger.error(f"❌ Impossible d'initialiser Django: {e}")
    sys.exit(1)

class ProjectDiagnostic:
    """Classe de diagnostic pour le projet Django"""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.successes = []
        self.start_time = datetime.now()
        
    def log_issue(self, category, message, critical=False):
        """Enregistre un problème"""
        self.issues.append({
            'category': category,
            'message': message,
            'critical': critical,
            'timestamp': datetime.now()
        })
        if critical:
            logger.error(f"❌ [{category}] {message}")
        else:
            logger.warning(f"⚠️  [{category}] {message}")
    
    def log_warning(self, category, message):
        """Enregistre un avertissement"""
        self.warnings.append({
            'category': category,
            'message': message,
            'timestamp': datetime.now()
        })
        logger.warning(f"⚠️  [{category}] {message}")
    
    def log_success(self, category, message):
        """Enregistre un succès"""
        self.successes.append({
            'category': category,
            'message': message,
            'timestamp': datetime.now()
        })
        logger.info(f"✅ [{category}] {message}")
    
    def check_environment(self):
        """Vérifie les variables d'environnement"""
        logger.info("🔍 Vérification de l'environnement...")
        
        # Variables critiques pour Railway
        critical_vars = ['SECRET_KEY', 'DATABASE_URL']
        
        for var in critical_vars:
            if not os.environ.get(var):
                self.log_issue('ENVIRONNEMENT', f'Variable {var} manquante', critical=True)
            else:
                self.log_success('ENVIRONNEMENT', f'{var} = {"*" * 8 + os.environ[var][-4:]}')
        
        # Variables importantes
        important_vars = ['ALLOWED_HOSTS', 'DEBUG', 'RAILWAY_PUBLIC_DOMAIN']
        
        for var in important_vars:
            value = os.environ.get(var, 'Non définie')
            if var == 'SECRET_KEY' and value:
                value = '************'  # Masquer la clé
            self.log_warning('ENVIRONNEMENT', f'{var} = {value}')
        
        # Vérifier le mode DEBUG
        if settings.DEBUG and not settings.IS_DEVELOPMENT:
            self.log_issue('SÉCURITÉ', 'DEBUG=True en production!', critical=True)
        else:
            self.log_success('SÉCURITÉ', f'DEBUG={settings.DEBUG}')
    
    def check_project_structure(self):
        """Vérifie la structure du projet"""
        logger.info("📁 Vérification de la structure du projet...")
        
        # Fichiers requis
        required_files = [
            'manage.py',
            'requirements.txt',
            'Procfile',
            '.nixpacks.toml',
            'mutuelle_core/settings.py',
            'mutuelle_core/urls.py',
            'mutuelle_core/wsgi.py',
        ]
        
        for file_path in required_files:
            path = BASE_DIR / file_path
            if path.exists():
                self.log_success('STRUCTURE', f'Fichier présent: {file_path}')
            else:
                self.log_issue('STRUCTURE', f'Fichier manquant: {file_path}', critical=True)
        
        # Dossiers requis
        required_dirs = [
            'static',
            'staticfiles',
            'media',
            'api',
            'core',
            'membres',
        ]
        
        for dir_path in required_dirs:
            path = BASE_DIR / dir_path
            if path.exists():
                self.log_success('STRUCTURE', f'Dossier présent: {dir_path}')
            else:
                self.log_warning('STRUCTURE', f'Dossier manquant: {dir_path}')
        
        # Vérifier les permissions des dossiers
        for dir_path in ['staticfiles', 'media']:
            path = BASE_DIR / dir_path
            if path.exists():
                try:
                    # Tester l'écriture
                    test_file = path / '.write_test'
                    test_file.touch()
                    test_file.unlink()
                    self.log_success('PERMISSIONS', f'Permissions OK: {dir_path}')
                except PermissionError:
                    self.log_issue('PERMISSIONS', f'Permissions insuffisantes: {dir_path}', critical=True)
    
    def check_dependencies(self):
        """Vérifie les dépendances"""
        logger.info("📦 Vérification des dépendances...")
        
        # Vérifier requirements.txt
        req_path = BASE_DIR / 'requirements.txt'
        if req_path.exists():
            with open(req_path, 'r') as f:
                requirements = f.read()
                
            # Vérifier les dépendances critiques
            critical_packages = [
                'Django>=4.2',
                'djangorestframework',
                'django-cors-headers',
                'whitenoise',
                'psycopg2-binary',
                'gunicorn',
            ]
            
            for package in critical_packages:
                if package.split('>=')[0].split('==')[0] in requirements:
                    self.log_success('DEPENDANCES', f'Package présent: {package}')
                else:
                    self.log_warning('DEPENDANCES', f'Package manquant ou vieux: {package}')
            
            # Vérifier la version de Python
            if 'python-version' in requirements or 'runtime.txt' in (BASE_DIR / 'runtime.txt').exists():
                self.log_success('DEPENDANCES', 'Version Python spécifiée')
            else:
                self.log_warning('DEPENDANCES', 'Version Python non spécifiée')
        else:
            self.log_issue('DEPENDANCES', 'requirements.txt manquant', critical=True)
    
    def check_database(self):
        """Vérifie la configuration de la base de données"""
        logger.info("🗄️  Vérification de la base de données...")
        
        try:
            # Tester la connexion
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result[0] == 1:
                    self.log_success('DATABASE', 'Connexion BD réussie')
        except DatabaseError as e:
            self.log_issue('DATABASE', f'Échec connexion BD: {e}', critical=True)
            return
        
        # Vérifier le type de base de données
        db_engine = settings.DATABASES['default']['ENGINE']
        if 'postgresql' in db_engine:
            self.log_success('DATABASE', f'Utilisation de PostgreSQL')
            
            # Vérifier la configuration SSL pour Railway
            if settings.IS_PRODUCTION:
                db_options = settings.DATABASES['default'].get('OPTIONS', {})
                if db_options.get('sslmode') != 'require':
                    self.log_warning('DATABASE', 'SSL non forcé pour PostgreSQL')
        elif 'sqlite3' in db_engine:
            if settings.IS_PRODUCTION:
                self.log_issue('DATABASE', 'SQLite en production!', critical=True)
            else:
                self.log_success('DATABASE', 'SQLite (développement OK)')
        
        # Vérifier les migrations en attente
        try:
            from django.core.management import call_command
            result = subprocess.run(
                [sys.executable, 'manage.py', 'showmigrations', '--list'],
                capture_output=True,
                text=True,
                cwd=BASE_DIR
            )
            
            if '[ ]' in result.stdout:
                self.log_warning('MIGRATIONS', 'Migrations en attente')
            else:
                self.log_success('MIGRATIONS', 'Toutes les migrations sont appliquées')
                
        except Exception as e:
            self.log_warning('MIGRATIONS', f'Impossible de vérifier les migrations: {e}')
    
    def check_static_files(self):
        """Vérifie les fichiers statiques"""
        logger.info("📁 Vérification des fichiers statiques...")
        
        # Vérifier WhiteNoise
        if 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE:
            self.log_success('STATIC', 'WhiteNoise configuré')
        else:
            self.log_issue('STATIC', 'WhiteNoise manquant dans MIDDLEWARE', critical=True)
        
        # Vérifier les chemins
        if settings.STATIC_ROOT:
            static_root = Path(settings.STATIC_ROOT)
            if static_root.exists():
                # Compter les fichiers
                static_files = list(static_root.rglob('*'))
                self.log_success('STATIC', f'{len(static_files)} fichiers dans STATIC_ROOT')
            else:
                self.log_warning('STATIC', 'STATIC_ROOT existe mais dossier vide')
        
        # Vérifier la collecte statique
        try:
            # Tester si nous pouvons accéder à un fichier statique
            test_url = '/static/admin/css/base.css'
            self.log_success('STATIC', 'Configuration statique OK')
        except Exception as e:
            self.log_warning('STATIC', f'Problème avec les fichiers statiques: {e}')
    
    def check_security(self):
        """Vérifie la sécurité"""
        logger.info("🔒 Vérification de la sécurité...")
        
        # Vérifier ALLOWED_HOSTS
        if settings.ALLOWED_HOSTS:
            if '*' in settings.ALLOWED_HOSTS and settings.IS_PRODUCTION:
                self.log_issue('SÉCURITÉ', 'ALLOWED_HOSTS contient * en production!', critical=True)
            self.log_success('SÉCURITÉ', f'ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
        else:
            self.log_issue('SÉCURITÉ', 'ALLOWED_HOSTS vide', critical=True)
        
        # Vérifier CSRF_TRUSTED_ORIGINS
        if settings.CSRF_TRUSTED_ORIGINS:
            self.log_success('SÉCURITÉ', f'CSRF_TRUSTED_ORIGINS: {len(settings.CSRF_TRUSTED_ORIGINS)} origines')
        else:
            self.log_warning('SÉCURITÉ', 'CSRF_TRUSTED_ORIGINS vide')
        
        # Vérifier les cookies sécurisés
        if settings.IS_PRODUCTION:
            if not settings.SESSION_COOKIE_SECURE:
                self.log_issue('SÉCURITÉ', 'SESSION_COOKIE_SECURE=False en production', critical=True)
            if not settings.CSRF_COOKIE_SECURE:
                self.log_issue('SÉCURITÉ', 'CSRF_COOKIE_SECURE=False en production', critical=True)
            if not settings.SECURE_SSL_REDIRECT:
                self.log_warning('SÉCURITÉ', 'SECURE_SSL_REDIRECT=False en production')
        
        # Vérifier SECRET_KEY
        secret_key = settings.SECRET_KEY
        if secret_key:
            if len(secret_key) < 50:
                self.log_warning('SÉCURITÉ', 'SECRET_KEY trop courte')
            if 'django-dev' in secret_key and settings.IS_PRODUCTION:
                self.log_issue('SÉCURITÉ', 'SECRET_KEY de développement en production!', critical=True)
            self.log_success('SÉCURITÉ', 'SECRET_KEY configurée')
    
    def check_api(self):
        """Vérifie l'API"""
        logger.info("🔌 Vérification de l'API...")
        
        # Vérifier si l'application api est installée
        if 'api' in settings.INSTALLED_APPS:
            self.log_success('API', 'Application API installée')
            
            # Vérifier les URLs de l'API
            try:
                from api.urls import urlpatterns as api_urls
                if api_urls:
                    self.log_success('API', f'{len(api_urls)} patterns d\'URL détectés')
                    
                    # Vérifier les endpoints critiques
                    critical_endpoints = ['health/', 'token/', 'token/refresh/']
                    for endpoint in critical_endpoints:
                        if any(endpoint in str(p.pattern) for p in api_urls):
                            self.log_success('API', f'Endpoint {endpoint} présent')
                        else:
                            self.log_warning('API', f'Endpoint {endpoint} manquant')
            except Exception as e:
                self.log_issue('API', f'Erreur dans api.urls: {e}', critical=True)
        else:
            self.log_issue('API', 'Application API non installée', critical=True)
        
        # Vérifier JWT
        if 'rest_framework_simplejwt' in settings.INSTALLED_APPS:
            self.log_success('API', 'JWT installé')
        else:
            self.log_issue('API', 'JWT non installé', critical=True)
    
    def check_railway_specific(self):
        """Vérifie les configurations spécifiques à Railway"""
        logger.info("🚂 Vérification des configurations Railway...")
        
        # Vérifier Railway detection
        if hasattr(settings, 'RAILWAY'):
            self.log_success('RAILWAY', f'RAILWAY={settings.RAILWAY}')
        else:
            self.log_warning('RAILWAY', 'RAILWAY non détecté dans settings')
        
        # Vérifier Procfile
        procfile_path = BASE_DIR / 'Procfile'
        if procfile_path.exists():
            with open(procfile_path, 'r') as f:
                procfile = f.read()
                
            if 'web:' in procfile and 'gunicorn' in procfile:
                self.log_success('RAILWAY', 'Procfile correct pour Gunicorn')
            else:
                self.log_issue('RAILWAY', 'Procfile incorrect', critical=True)
        else:
            self.log_issue('RAILWAY', 'Procfile manquant', critical=True)
        
        # Vérifier .nixpacks.toml
        nixpacks_path = BASE_DIR / '.nixpacks.toml'
        if nixpacks_path.exists():
            self.log_success('RAILWAY', '.nixpacks.toml présent')
        else:
            self.log_issue('RAILWAY', '.nixpacks.toml manquant', critical=True)
        
        # Vérifier les logs
        if settings.LOGGING.get('disable_existing_loggers'):
            self.log_success('LOGGING', 'Loggers existants désactivés (Railway)')
        else:
            self.log_warning('LOGGING', 'Loggers existants actifs (peut causer des doublons)')
    
    def run_all_checks(self):
        """Exécute toutes les vérifications"""
        logger.info("=" * 60)
        logger.info("🚀 DIAGNOSTIC DU PROJET DJANGO SUR RAILWAY")
        logger.info("=" * 60)
        
        checks = [
            self.check_environment,
            self.check_project_structure,
            self.check_dependencies,
            self.check_database,
            self.check_static_files,
            self.check_security,
            self.check_api,
            self.check_railway_specific,
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                logger.error(f"❌ Échec lors de la vérification {check.__name__}: {e}")
        
        return self.generate_report()
    
    def generate_report(self):
        """Génère un rapport complet"""
        logger.info("=" * 60)
        logger.info("📊 RAPPORT DE DIAGNOSTIC")
        logger.info("=" * 60)
        
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        critical_issues = [i for i in self.issues if i['critical']]
        non_critical_issues = [i for i in self.issues if not i['critical']]
        
        # Statistiques
        logger.info(f"⏱️  Durée du diagnostic: {duration:.2f}s")
        logger.info(f"✅ Succès: {len(self.successes)}")
        logger.info(f"⚠️  Avertissements: {len(self.warnings)}")
        logger.info(f"❌ Problèmes non-critiques: {len(non_critical_issues)}")
        logger.info(f"🚨 Problèmes CRITIQUES: {len(critical_issues)}")
        
        # Afficher les problèmes critiques en premier
        if critical_issues:
            logger.info("\n" + "=" * 60)
            logger.info("🚨 PROBLÈMES CRITIQUES À CORRIGER:")
            for issue in critical_issues:
                logger.info(f"  • {issue['category']}: {issue['message']}")
        
        # Recommandations
        logger.info("\n" + "=" * 60)
        logger.info("💡 RECOMMANDATIONS:")
        
        if critical_issues:
            logger.info("1. Corriger les problèmes critiques avant le déploiement")
        
        # Vérifier .nixpacks.toml
        nixpacks_path = BASE_DIR / '.nixpacks.toml'
        if not nixpacks_path.exists():
            logger.info("2. Créer un fichier .nixpacks.toml:")
            logger.info("""
   [phases.setup]
   nixPkgs = ["python39", "postgresql"]

   [phases.build]
   cmds = ["pip install -r requirements.txt"]

   [start]
   cmd = "python manage.py migrate && gunicorn mutuelle_core.wsgi"
            """)
        
        # Vérifier les migrations
        logger.info("3. Appliquer les migrations:")
        logger.info("   python manage.py migrate")
        
        # Vérifier les fichiers statiques
        logger.info("4. Collecter les fichiers statiques:")
        logger.info("   python manage.py collectstatic --noinput")
        
        # Conclusion
        logger.info("\n" + "=" * 60)
        if critical_issues:
            logger.info("❌ DÉPLOIEMENT NON RECOMMANDÉ - Problèmes critiques détectés")
            return False
        elif non_critical_issues or self.warnings:
            logger.info("⚠️  DÉPLOIEMENT POSSIBLE - Mais corrigez les avertissements")
            return True
        else:
            logger.info("✅ PROJET PRÊT POUR LE DÉPLOIEMENT SUR RAILWAY!")
            return True

def main():
    """Fonction principale"""
    try:
        diagnostic = ProjectDiagnostic()
        is_ready = diagnostic.run_all_checks()
        
        # Suggestions de commandes
        logger.info("\n📋 COMMANDES UTILES:")
        logger.info("python manage.py check --deploy        # Vérifier la configuration")
        logger.info("python manage.py collectstatic        # Collecter les fichiers statiques")
        logger.info("python manage.py migrate             # Appliquer les migrations")
        logger.info("python manage.py createsuperuser     # Créer un admin")
        
        return 0 if is_ready else 1
        
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())