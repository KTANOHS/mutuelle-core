#!/usr/bin/env python3
"""
🚨 SCRIPT DE DIAGNOSTIC COMPLET POUR RAILWAY
Diagnostique tous les problèmes courants de déploiement Django sur Railway
"""

import os
import sys
import subprocess
import requests
import json
import socket
import platform
from datetime import datetime
from urllib.parse import urlparse

class RailwayDiagnostic:
    def __init__(self):
        self.results = []
        self.errors = []
        self.warnings = []
        self.url = "https://web-production-abe5.up.railway.app"
        
    def log(self, message, status="ℹ️"):
        """Ajoute un message aux résultats"""
        self.results.append(f"{status} {message}")
        print(f"{status} {message}")
        
    def error(self, message):
        """Ajoute une erreur"""
        self.errors.append(message)
        self.log(message, "❌")
        
    def warning(self, message):
        """Ajoute un avertissement"""
        self.warnings.append(message)
        self.log(message, "⚠️")
        
    def success(self, message):
        """Ajoute un succès"""
        self.log(message, "✅")
        
    def header(self, title):
        """Affiche un en-tête"""
        print(f"\n{'='*60}")
        print(f"📋 {title}")
        print(f"{'='*60}")
        
    def run_all_checks(self):
        """Exécute tous les diagnostics"""
        self.header("DIAGNOSTIC COMPLET RAILWAY DJANGO")
        
        # 1. Environnement système
        self.check_system()
        
        # 2. Configuration Django
        self.check_django_settings()
        
        # 3. Réseau et DNS
        self.check_network()
        
        # 4. Sécurité et CSRF
        self.check_security()
        
        # 5. Base de données
        self.check_database()
        
        # 6. Fichiers statiques
        self.check_static_files()
        
        # 7. Test API
        self.test_api_endpoints()
        
        # 8. Vérification finale
        self.final_report()
        
    def check_system(self):
        """Vérifie l'environnement système"""
        self.header("1. SYSTÈME ET ENVIRONNEMENT")
        
        # Informations système
        self.success(f"Système: {platform.system()} {platform.release()}")
        self.success(f"Python: {sys.version}")
        
        # Variables d'environnement critiques
        critical_vars = [
            'DEBUG', 'SECRET_KEY', 'CSRF_TRUSTED_ORIGINS',
            'DATABASE_URL', 'ALLOWED_HOSTS', 'RAILWAY_ENVIRONMENT'
        ]
        
        for var in critical_vars:
            value = os.environ.get(var, 'NON DÉFINIE')
            if value == 'NON DÉFINIE':
                self.error(f"{var}: {value}")
            else:
                truncated = value[:50] + "..." if len(value) > 50 else value
                self.success(f"{var}: {truncated}")
                
                # Vérifications spécifiques
                if var == 'DEBUG' and value.lower() == 'true':
                    self.warning("DEBUG=True en production (dangereux)")
                elif var == 'SECRET_KEY' and 'django-insecure' in value:
                    self.error("SECRET_KEY utilise la valeur par défaut insecure")
                elif var == 'CSRF_TRUSTED_ORIGINS' and 'web-production-abe5.up.railway.app' not in value:
                    self.error("Domaine Railway manquant dans CSRF_TRUSTED_ORIGINS")
    
    def check_django_settings(self):
        """Vérifie la configuration Django"""
        self.header("2. CONFIGURATION DJANGO")
        
        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
            import django
            django.setup()
            
            from django.conf import settings
            
            # DEBUG
            if settings.DEBUG:
                self.warning(f"DEBUG={settings.DEBUG} (dangereux en production)")
            else:
                self.success(f"DEBUG={settings.DEBUG}")
            
            # ALLOWED_HOSTS
            allowed_hosts = settings.ALLOWED_HOSTS
            self.success(f"ALLOWED_HOSTS: {len(allowed_hosts)} hôtes")
            for host in allowed_hosts[:5]:
                self.log(f"  - {host}", "  ")
            
            # CSRF_TRUSTED_ORIGINS
            csrf_origins = settings.CSRF_TRUSTED_ORIGINS
            self.success(f"CSRF_TRUSTED_ORIGINS: {len(csrf_origins)} origines")
            
            current_domain = "https://web-production-abe5.up.railway.app"
            if current_domain in csrf_origins:
                self.success(f"  ✅ {current_domain} dans la liste")
            else:
                self.error(f"  ❌ {current_domain} MANQUANT dans la liste")
            
            # Cookies
            self.success(f"CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
            self.success(f"SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
            self.success(f"CSRF_COOKIE_DOMAIN: {settings.CSRF_COOKIE_DOMAIN}")
            
            if not settings.CSRF_COOKIE_SECURE:
                self.warning("CSRF_COOKIE_SECURE=False (devrait être True en production)")
            
            # INSTALLED_APPS
            self.success(f"Applications installées: {len(settings.INSTALLED_APPS)}")
            
        except Exception as e:
            self.error(f"Erreur chargement Django: {e}")
    
    def check_network(self):
        """Vérifie la connectivité réseau"""
        self.header("3. RÉSEAU ET CONNECTIVITÉ")
        
        # Résolution DNS
        try:
            hostname = urlparse(self.url).hostname
            ip = socket.gethostbyname(hostname)
            self.success(f"DNS résolu: {hostname} → {ip}")
        except socket.gaierror:
            self.error(f"Échec résolution DNS pour {hostname}")
        
        # Ping HTTP
        try:
            response = requests.get(f"{self.url}/api/health/", timeout=10)
            if response.status_code == 200:
                self.success(f"API santé accessible: HTTP {response.status_code}")
                try:
                    data = response.json()
                    self.log(f"  Status: {data.get('status', 'N/A')}", "  ")
                    self.log(f"  Database: {data.get('database', 'N/A')}", "  ")
                except:
                    pass
            else:
                self.warning(f"API santé: HTTP {response.status_code}")
        except requests.RequestException as e:
            self.error(f"API santé inaccessible: {e}")
        
        # Test admin (doit rediriger vers login)
        try:
            response = requests.get(f"{self.url}/admin/", timeout=10, allow_redirects=False)
            if response.status_code in [302, 301]:
                self.success(f"Admin redirige vers login: HTTP {response.status_code}")
            elif response.status_code == 200:
                self.warning("Admin accessible sans authentification")
            else:
                self.warning(f"Admin: HTTP {response.status_code}")
        except requests.RequestException as e:
            self.error(f"Admin inaccessible: {e}")
    
    def check_security(self):
        """Vérifie les configurations de sécurité"""
        self.header("4. SÉCURITÉ")
        
        # HTTPS
        try:
            response = requests.get(f"{self.url}/api/health/", timeout=10)
            if response.url.startswith('https://'):
                self.success("HTTPS activé")
            else:
                self.error("HTTP au lieu de HTTPS")
        except:
            pass
        
        # Headers de sécurité
        try:
            response = requests.head(self.url, timeout=10)
            headers = response.headers
            
            security_headers = {
                'Strict-Transport-Security': 'HSTS',
                'X-Content-Type-Options': 'Content type nosniff',
                'X-Frame-Options': 'Frame protection',
                'X-XSS-Protection': 'XSS protection'
            }
            
            for header, desc in security_headers.items():
                if header in headers:
                    self.success(f"{desc}: {headers[header]}")
                else:
                    self.warning(f"{desc}: Manquant")
                    
        except requests.RequestException as e:
            self.warning(f"Impossible de vérifier les headers: {e}")
    
    def check_database(self):
        """Vérifie la base de données"""
        self.header("5. BASE DE DONNÉES")
        
        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
            import django
            django.setup()
            
            from django.db import connection
            from django.contrib.auth import get_user_model
            
            # Test connexion
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.success("Connexion BD: OK")
            
            # Compteurs
            User = get_user_model()
            user_count = User.objects.count()
            superuser_count = User.objects.filter(is_superuser=True).count()
            
            self.success(f"Utilisateurs: {user_count}")
            self.success(f"Superutilisateurs: {superuser_count}")
            
            if superuser_count == 0:
                self.error("AUCUN superutilisateur - impossible de se connecter à l'admin")
            else:
                self.success("Superutilisateurs disponibles:")
                for user in User.objects.filter(is_superuser=True)[:5]:
                    self.log(f"  - {user.username} ({user.email})", "  ")
            
        except Exception as e:
            self.error(f"Erreur base de données: {e}")
    
    def check_static_files(self):
        """Vérifie les fichiers statiques"""
        self.header("6. FICHIERS STATIQUES")
        
        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
            import django
            django.setup()
            
            from django.conf import settings
            
            # Vérifier STATIC_ROOT
            static_root = settings.STATIC_ROOT
            if os.path.exists(static_root):
                file_count = len([f for f in os.listdir(static_root) if os.path.isfile(os.path.join(static_root, f))])
                self.success(f"STATIC_ROOT: {static_root} ({file_count} fichiers)")
            else:
                self.warning(f"STATIC_ROOT inexistant: {static_root}")
            
            # Tester un fichier statique
            try:
                response = requests.get(f"{self.url}/static/admin/css/base.css", timeout=5)
                if response.status_code == 200:
                    self.success("Fichiers statiques servis")
                else:
                    self.warning(f"Fichiers statiques: HTTP {response.status_code}")
            except:
                self.warning("Impossible de tester les fichiers statiques")
                
        except Exception as e:
            self.error(f"Erreur vérification fichiers statiques: {e}")
    
    def test_api_endpoints(self):
        """Teste les endpoints API"""
        self.header("7. ENDPOINTS API")
        
        endpoints = [
            ("/api/health/", "GET", "Santé"),
            ("/api/", "GET", "API racine"),
            ("/admin/login/", "GET", "Login admin"),
        ]
        
        for endpoint, method, description in endpoints:
            try:
                url = f"{self.url}{endpoint}"
                if method == "GET":
                    response = requests.get(url, timeout=10, allow_redirects=False)
                else:
                    response = requests.post(url, timeout=10, allow_redirects=False)
                
                status_emoji = "✅" if response.status_code < 400 else "⚠️"
                self.log(f"{status_emoji} {description}: HTTP {response.status_code} ({response.reason})")
                
            except requests.RequestException as e:
                self.error(f"❌ {description}: {e}")
    
    def final_report(self):
        """Génère le rapport final"""
        self.header("📊 RAPPORT FINAL DE DIAGNOSTIC")
        
        print(f"\n📈 STATISTIQUES:")
        print(f"   ✅ Succès: {len([r for r in self.results if '✅' in r])}")
        print(f"   ⚠️  Avertissements: {len(self.warnings)}")
        print(f"   ❌ Erreurs: {len(self.errors)}")
        
        if self.errors:
            print(f"\n🚨 ERREURS CRITIQUES ({len(self.errors)}):")
            for error in self.errors[:10]:  # Limiter à 10 erreurs
                print(f"   • {error}")
        
        if self.warnings:
            print(f"\n⚠️  AVERTISSEMENTS ({len(self.warnings)}):")
            for warning in self.warnings[:10]:
                print(f"   • {warning}")
        
        print(f"\n🔗 URL DE VOTRE APPLICATION:")
        print(f"   {self.url}")
        
        print(f"\n🔑 VOS SUPERUTILISATEURS:")
        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
            import django
            django.setup()
            from django.contrib.auth import get_user_model
            User = get_user_model()
            for user in User.objects.filter(is_superuser=True):
                print(f"   👤 {user.username} ({user.email})")
        except:
            print("   (Impossible de récupérer les utilisateurs)")
        
        print(f"\n🎯 RECOMMANDATIONS PRIORITAIRES:")
        
        recommendations = []
        
        # Vérifier CSRF
        if any("CSRF" in error or "csrf" in error.lower() for error in self.errors):
            recommendations.append("1. Ajoutez CSRF_TRUSTED_ORIGINS sur Railway: https://web-production-abe5.up.railway.app,https://*.railway.app")
        
        # Vérifier superutilisateurs
        if any("superutilisateur" in error.lower() or "AUCUN superutilisateur" in error for error in self.errors):
            recommendations.append("2. Créez un superutilisateur: railway run python manage.py createsuperuser")
        
        # Vérifier DEBUG
        if any("DEBUG=True" in warning for warning in self.warnings):
            recommendations.append("3. Définissez DEBUG=false sur Railway")
        
        # Vérifier SECRET_KEY
        if any("SECRET_KEY" in error for error in self.errors):
            recommendations.append("4. Définissez une SECRET_KEY sécurisée sur Railway")
        
        if not recommendations:
            recommendations.append("✅ Toutes les configurations semblent correctes")
            recommendations.append("🔗 Testez: open https://web-production-abe5.up.railway.app/admin/")
        
        for rec in recommendations:
            print(f"   {rec}")
        
        print(f"\n{'='*60}")
        print("🚀 DIAGNOSTIC TERMINÉ")
        print(f"{'='*60}")
        
        # Générer un fichier de rapport
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"railway_diagnostic_{timestamp}.txt"
        
        with open(report_file, 'w') as f:
            f.write(f"RAILWAY DIAGNOSTIC REPORT - {timestamp}\n")
            f.write("="*60 + "\n\n")
            f.write(f"URL: {self.url}\n")
            f.write(f"Date: {datetime.now()}\n\n")
            
            f.write("RÉSULTATS:\n")
            for result in self.results:
                f.write(f"{result}\n")
            
            f.write(f"\nERREURS: {len(self.errors)}\n")
            for error in self.errors:
                f.write(f"• {error}\n")
            
            f.write(f"\nAVERTISSEMENTS: {len(self.warnings)}\n")
            for warning in self.warnings:
                f.write(f"• {warning}\n")
        
        print(f"\n📄 Rapport sauvegardé: {report_file}")

def main():
    """Fonction principale"""
    diagnostic = RailwayDiagnostic()
    
    try:
        diagnostic.run_all_checks()
        
        # Demander action
        print(f"\n{'='*60}")
        print("🎯 ACTIONS RECOMMANDÉES")
        print(f"{'='*60}")
        
        if diagnostic.errors:
            print("\n1. CORRIGER LES ERREURS CRITIQUES :")
            print("   railway variables CSRF_TRUSTED_ORIGINS=\"https://web-production-abe5.up.railway.app,https://*.railway.app\"")
            print("   railway variables DEBUG=false")
            print("   railway run python manage.py createsuperuser")
        
        print("\n2. REDÉPLOYER :")
        print("   railway up")
        
        print("\n3. TESTER :")
        print(f"   open {diagnostic.url}/admin/")
        print(f"   curl {diagnostic.url}/api/health/")
        
        print(f"\n{'='*60}")
        response = input("\n📱 Voulez-vous ouvrir l'interface Railway ? (oui/non): ")
        
        if response.lower() in ['oui', 'o', 'yes', 'y']:
            import webbrowser
            webbrowser.open("https://railway.app/project/5e1edecb-8b7f-48be-8b84-b779d78fb4da")
            
    except KeyboardInterrupt:
        print("\n\n❌ Diagnostic interrompu")
    except Exception as e:
        print(f"\n⚠️ Erreur lors du diagnostic: {e}")

if __name__ == "__main__":
    # Rendre le script exécutable
    if not sys.argv[0].endswith('.py'):
        print("Pour exécuter: python diagnostic_railway.py")
    
    main()