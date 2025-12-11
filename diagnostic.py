#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC DJANGO - RENDER.COM
Version: 1.0
"""

import os
import sys
import subprocess
import platform
import importlib
import json
import requests
from pathlib import Path
from datetime import datetime

class DjangoDiagnostic:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "environment": {},
            "checks": {},
            "issues": [],
            "recommendations": []
        }
        
    def print_header(self, text):
        print(f"\n{'='*60}")
        print(f"{text.upper()}")
        print(f"{'='*60}")
    
    def print_check(self, name, status, message=""):
        icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{icon} {name}: {status} {message}")
        return status
    
    def check_environment(self):
        """Vérifie l'environnement système"""
        self.print_header("1. Environnement Système")
        
        self.results["environment"]["python_version"] = sys.version
        self.results["environment"]["platform"] = platform.platform()
        self.results["environment"]["cwd"] = os.getcwd()
        
        print(f"🐍 Python: {sys.version}")
        print(f"💻 Plateforme: {platform.platform()}")
        print(f"📁 Répertoire: {os.getcwd()}")
        
        # Vérifier si on est sur Render
        is_render = os.environ.get('RENDER') is not None
        self.results["environment"]["is_render"] = is_render
        print(f"🌐 Render: {'OUI' if is_render else 'NON'}")
        
        return is_render
    
    def check_essential_files(self):
        """Vérifie les fichiers essentiels"""
        self.print_header("2. Fichiers Essentiels")
        
        essential_files = [
            "manage.py",
            "requirements.txt",
            "app.py",
            "mutuelle_core/wsgi.py",
            "mutuelle_core/settings.py",
        ]
        
        for file in essential_files:
            exists = Path(file).exists()
            status = "PASS" if exists else "FAIL"
            message = "" if exists else "FICHIER MANQUANT!"
            self.print_check(file, status, message)
            
            if not exists:
                self.results["issues"].append(f"Fichier manquant: {file}")
    
    def check_dependencies(self):
        """Vérifie les dépendances"""
        self.print_header("3. Dépendances Python")
        
        try:
            # Lire requirements.txt
            req_file = "requirements.txt"
            if Path(req_file).exists():
                with open(req_file, 'r') as f:
                    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                
                print(f"📦 {len(requirements)} paquets dans requirements.txt")
                
                # Vérifier quelques dépendances critiques
                critical_deps = {
                    "Django": "django",
                    "Gunicorn": "gunicorn",
                    "WhiteNoise": "whitenoise",
                    "psycopg2": "psycopg2-binary",
                }
                
                for name, package in critical_deps.items():
                    try:
                        importlib.import_module(package.replace('-', '_') if package != 'django' else 'django')
                        self.print_check(f"{name} ({package})", "PASS")
                    except ImportError:
                        self.print_check(f"{name} ({package})", "FAIL", "NON INSTALLÉ")
                        self.results["issues"].append(f"Dépendance manquante: {package}")
            else:
                print("❌ requirements.txt non trouvé")
                self.results["issues"].append("requirements.txt manquant")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def check_django_configuration(self):
        """Vérifie la configuration Django"""
        self.print_header("4. Configuration Django")
        
        try:
            # Configurer les variables d'environnement pour Django
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
            
            import django
            django.setup()
            
            from django.conf import settings
            
            # Vérifications de configuration
            checks = [
                ("DEBUG", settings.DEBUG, False if os.environ.get('RENDER') else "VARIABLE"),
                ("ALLOWED_HOSTS", len(settings.ALLOWED_HOSTS) > 0, True),
                ("STATIC_ROOT", hasattr(settings, 'STATIC_ROOT'), True),
                ("DATABASES", 'default' in settings.DATABASES, True),
                ("SECRET_KEY", len(settings.SECRET_KEY) > 20, True),
                ("MIDDLEWARE", 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE, True),
            ]
            
            for check_name, value, expected in checks:
                if expected == "VARIABLE":
                    status = "INFO"
                    message = f"= {value}"
                else:
                    status = "PASS" if value == expected else "FAIL"
                    message = f"= {value} (attendu: {expected})"
                
                self.print_check(check_name, status, message)
                
                if status == "FAIL":
                    self.results["issues"].append(f"Configuration incorrecte: {check_name} = {value}")
            
            # Informations supplémentaires
            print(f"\n📊 Base de données: {settings.DATABASES['default']['ENGINE'].split('.')[-1]}")
            print(f"🌐 ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
            
        except Exception as e:
            print(f"❌ Impossible de charger Django: {e}")
            self.results["issues"].append(f"Erreur Django: {e}")
    
    def check_database(self):
        """Vérifie l'état de la base de données"""
        self.print_header("5. Base de Données")
        
        try:
            # Vérifier les migrations
            result = subprocess.run(
                ['python', 'manage.py', 'showmigrations'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Compter les migrations appliquées
                lines = result.stdout.split('\n')
                applied = sum(1 for line in lines if '[X]' in line)
                pending = sum(1 for line in lines if '[ ]' in line)
                
                print(f"✅ Commandes migrations accessibles")
                print(f"📊 Migrations appliquées: {applied}")
                print(f"📊 Migrations en attente: {pending}")
                
                if pending > 0:
                    self.print_check("Migrations en attente", "WARNING", f"{pending} migration(s) non appliquée(s)")
                    self.results["issues"].append(f"{pending} migration(s) en attente")
                    
                # Vérifier les tables essentielles
                try:
                    from django.db import connection
                    with connection.cursor() as cursor:
                        essential_tables = [
                            'django_session',
                            'auth_user',
                            'django_migrations',
                            'django_content_type'
                        ]
                        
                        print("\n📋 Vérification des tables essentielles:")
                        for table in essential_tables:
                            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                            exists = cursor.fetchone() is not None
                            status = "PASS" if exists else "FAIL"
                            self.print_check(f"Table {table}", status)
                            
                            if not exists:
                                self.results["issues"].append(f"Table manquante: {table}")
                except Exception as e:
                    print(f"⚠️ Impossible de vérifier les tables: {e}")
                    
            else:
                print(f"❌ Erreur migrations: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout lors de la vérification des migrations")
        except FileNotFoundError:
            print("❌ manage.py non trouvé")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def check_static_files(self):
        """Vérifie les fichiers statiques"""
        self.print_header("6. Fichiers Statiques")
        
        try:
            from django.conf import settings
            
            static_dirs = [
                settings.STATIC_ROOT,
                Path("static"),
                Path("staticfiles"),
            ]
            
            for static_dir in static_dirs:
                if static_dir and Path(static_dir).exists():
                    files = list(Path(static_dir).rglob("*"))
                    print(f"📁 {static_dir}: {len(files)} fichiers")
                    
                    # Vérifier quelques fichiers critiques
                    critical_files = [
                        "mutuelle_core/images/logo.jpg",
                        "js/messagerie-integration.js",
                        "img/favicon.ico",
                    ]
                    
                    for file in critical_files:
                        full_path = Path(static_dir) / file
                        exists = full_path.exists()
                        status = "PASS" if exists else "WARNING"
                        message = "" if exists else "FICHIER MANQUANT"
                        self.print_check(f"  {file}", status, message)
                else:
                    print(f"⚠️ Répertoire statique non trouvé: {static_dir}")
                    
        except Exception as e:
            print(f"⚠️ Erreur vérification statiques: {e}")
    
    def check_render_specific(self):
        """Vérifications spécifiques à Render"""
        self.print_header("7. Configuration Render")
        
        # Variables d'environnement Render
        render_vars = [
            'RENDER',
            'PYTHON_VERSION',
            'PORT',
            'WEB_CONCURRENCY',
            'DISABLE_COLLECTSTATIC',
        ]
        
        for var in render_vars:
            value = os.environ.get(var)
            status = "INFO"
            message = f"= {value}" if value else "NON DÉFINI"
            self.print_check(f"Variable {var}", status, message)
    
    def check_urls(self):
        """Teste les URLs principales"""
        self.print_header("8. URLs de l'Application")
        
        urls_to_test = [
            ("/", "Page d'accueil"),
            ("/admin/", "Admin Django"),
            ("/accounts/login/", "Connexion"),
            ("/api/", "API REST"),
        ]
        
        # Si nous sommes en local, testons avec runserver
        if not os.environ.get('RENDER'):
            print("⚠️ Tests URLs: Mode local uniquement")
            
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('127.0.0.1', 8000))
                
                if result == 0:
                    base_url = "http://127.0.0.1:8000"
                    
                    for path, description in urls_to_test:
                        try:
                            response = requests.get(f"{base_url}{path}", timeout=5)
                            status = "PASS" if response.status_code < 500 else "FAIL"
                            message = f"HTTP {response.status_code}"
                            self.print_check(description, status, message)
                        except requests.RequestException:
                            self.print_check(description, "FAIL", "INACCESSIBLE")
                else:
                    print("⚠️ Serveur local non détecté sur le port 8000")
                    
            except Exception as e:
                print(f"⚠️ Impossible de tester les URLs: {e}")
    
    def generate_report(self):
        """Génère un rapport complet"""
        self.print_header("📊 RAPPORT DE DIAGNOSTIC")
        
        # Compter les problèmes
        total_checks = sum(len(checks) for checks in self.results["checks"].values())
        issues = len(self.results["issues"])
        
        print(f"📈 Total vérifications: {total_checks}")
        print(f"🚨 Problèmes identifiés: {issues}")
        print(f"📅 Date du diagnostic: {self.results['timestamp']}")
        
        if issues > 0:
            print("\n🔴 PROBLÈMES À CORRIGER:")
            for issue in self.results["issues"]:
                print(f"  • {issue}")
            
            print("\n💡 RECOMMANDATIONS:")
            print("  1. Exécutez: python manage.py migrate")
            print("  2. Exécutez: python manage.py collectstatic")
            print("  3. Vérifiez que tous les fichiers essentiels existent")
            print("  4. Vérifiez les permissions des fichiers")
        else:
            print("\n🎉 Tous les tests sont passés avec succès!")
        
        # Sauvegarder le rapport
        report_file = "diagnostic_report.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n📄 Rapport sauvegardé dans: {report_file}")
    
    def run_all_checks(self):
        """Exécute toutes les vérifications"""
        print("🚀 LANCEMENT DU DIAGNOSTIC DJANGO-RENDER")
        print(f"⏰ {self.results['timestamp']}")
        
        self.check_environment()
        self.check_essential_files()
        self.check_dependencies()
        self.check_django_configuration()
        self.check_database()
        self.check_static_files()
        self.check_render_specific()
        self.check_urls()
        self.generate_report()
        
        return self.results

if __name__ == "__main__":
    diagnostic = DjangoDiagnostic()
    results = diagnostic.run_all_checks()
    
    # Code de sortie basé sur les problèmes
    exit_code = 0 if len(results["issues"]) == 0 else 1
    sys.exit(exit_code)