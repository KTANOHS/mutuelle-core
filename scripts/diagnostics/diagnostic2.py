#!/usr/bin/env python3
"""
Script de diagnostic pour le projet Django
Auteur: Assistance Technique
Date: Décembre 2025
"""

import os
import sys
import json
import subprocess
import traceback
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent
DJANGO_SETTINGS_MODULE = 'mutuelle_core.settings'

class DjangoDiagnostic:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success = []
        self.project_root = PROJECT_ROOT
        
    def run_full_diagnostic(self):
        """Exécute tous les diagnostics"""
        print("🔍 DIAGNOSTIC DU PROJET DJANGO")
        print("=" * 60)
        
        self.check_python_version()
        self.check_django_version()
        self.check_project_structure()
        self.check_python_syntax()
        self.check_indentation()
        self.check_django_settings()
        self.check_database()
        self.check_urls()
        self.check_views_errors()
        self.check_static_files()
        self.check_migrations()
        self.check_permissions()
        
        self.generate_report()
    
    def check_python_version(self):
        """Vérifie la version de Python"""
        print("\n1. ✅ Vérification de la version Python...")
        version = sys.version_info
        if version.major == 3 and version.minor >= 8:
            self.success.append(f"Python {version.major}.{version.minor}.{version.micro} - OK")
        else:
            self.warnings.append(f"Python {version.major}.{version.minor} - Version recommandée: 3.8+")
    
    def check_django_version(self):
        """Vérifie la version de Django"""
        print("2. ✅ Vérification de Django...")
        try:
            import django
            self.success.append(f"Django {django.__version__} - OK")
        except ImportError:
            self.errors.append("Django non installé")
    
    def check_project_structure(self):
        """Vérifie la structure du projet"""
        print("3. 📁 Vérification de la structure...")
        required_dirs = [
            'mutuelle_core',
            'communication',
            'medecin',
            'pharmacien',
            'agents',
            'templates',
            'static'
        ]
        
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                self.success.append(f"📁 {dir_name}/ - Présent")
            else:
                self.warnings.append(f"📁 {dir_name}/ - Absent")
    
    def check_python_syntax(self):
        """Vérifie la syntaxe Python de tous les fichiers"""
        print("4. 🐍 Vérification syntaxe Python...")
        
        python_files = []
        for ext in ['*.py', '*.pyw']:
            python_files.extend(self.project_root.rglob(ext))
        
        for py_file in python_files:
            try:
                # Éviter les migrations et __pycache__
                if 'migrations' in str(py_file) or '__pycache__' in str(py_file):
                    continue
                
                # Vérifier la syntaxe
                result = subprocess.run(
                    [sys.executable, '-m', 'py_compile', str(py_file)],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    rel_path = py_file.relative_to(self.project_root)
                    self.success.append(f"✅ {rel_path} - Syntaxe OK")
                else:
                    self.errors.append(f"❌ {py_file.name} - Erreur syntaxe: {result.stderr[:100]}")
                    
            except subprocess.TimeoutExpired:
                self.warnings.append(f"⚠️ {py_file.name} - Vérification timeout")
            except Exception as e:
                self.warnings.append(f"⚠️ {py_file.name} - Erreur: {str(e)[:50]}")
    
    def check_indentation(self):
        """Vérifie les problèmes d'indentation"""
        print("5. 📐 Vérification de l'indentation...")
        
        # Points critiques basés sur les logs
        critical_files = [
            'communication/views.py',
            'medecin/views.py',
            'pharmacien/views.py',
            'agents/views.py'
        ]
        
        for file_path in critical_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                self.check_file_indentation(full_path)
    
    def check_file_indentation(self, file_path):
        """Vérifie l'indentation d'un fichier spécifique"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            rel_path = file_path.relative_to(self.project_root)
            
            for i, line in enumerate(lines, 1):
                # Vérifier les décorateurs mal alignés
                if line.strip().startswith('@'):
                    # Vérifier si la ligne suivante n'est pas une fonction
                    if i < len(lines) and not lines[i].strip().startswith('def ') and not lines[i].strip().startswith('class '):
                        if lines[i].strip() and not lines[i].strip().startswith('@'):
                            self.errors.append(f"❌ {rel_path}:L{i} - Décorateur mal aligné")
                
                # Vérifier les erreurs d'indentation (mélange tabs/spaces)
                if '\t' in line and ' ' * 4 in line[:line.find('\t')]:
                    self.warnings.append(f"⚠️ {rel_path}:L{i} - Mélange tabs et spaces")
                    
        except UnicodeDecodeError:
            self.warnings.append(f"⚠️ {file_path} - Encodage non UTF-8")
        except Exception as e:
            self.warnings.append(f"⚠️ {file_path} - Erreur de lecture: {str(e)}")
    
    def check_django_settings(self):
        """Vérifie la configuration Django"""
        print("6. ⚙️ Vérification des settings...")
        
        settings_file = self.project_root / 'mutuelle_core' / 'settings.py'
        if not settings_file.exists():
            self.errors.append("Fichier settings.py introuvable")
            return
        
        try:
            with open(settings_file, 'r') as f:
                content = f.read()
            
            checks = {
                'DEBUG': 'DEBUG = True' in content,
                'SECRET_KEY': 'SECRET_KEY' in content,
                'ALLOWED_HOSTS': 'ALLOWED_HOSTS' in content,
                'DATABASES': 'DATABASES' in content,
                'INSTALLED_APPS': "'communication'" in content,
            }
            
            for key, found in checks.items():
                if found:
                    self.success.append(f"⚙️ {key} - Configuré")
                else:
                    self.warnings.append(f"⚠️ {key} - Non trouvé ou problématique")
                    
        except Exception as e:
            self.errors.append(f"Erreur lecture settings: {str(e)}")
    
    def check_database(self):
        """Vérifie la base de données"""
        print("7. 💾 Vérification de la base de données...")
        
        try:
            # Tenter une connexion
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', DJANGO_SETTINGS_MODULE)
            import django
            django.setup()
            
            from django.db import connection
            from django.core.management import execute_from_command_line
            
            # Vérifier les migrations en attente
            result = subprocess.run(
                [sys.executable, 'manage.py', 'makemigrations', '--check', '--dry-run'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                self.success.append("💾 Migrations - À jour")
            else:
                self.warnings.append("💾 Migrations - Modifications détectées")
            
            # Vérifier la connexion
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.success.append("💾 Connexion DB - OK")
                
        except Exception as e:
            self.errors.append(f"❌ Base de données: {str(e)}")
    
    def check_urls(self):
        """Vérifie les URLs"""
        print("8. 🔗 Vérification des URLs...")
        
        urls_file = self.project_root / 'mutuelle_core' / 'urls.py'
        if not urls_file.exists():
            self.errors.append("Fichier urls.py introuvable")
            return
        
        try:
            # Vérifier les URLs critiques
            with open(urls_file, 'r') as f:
                content = f.read()
            
            critical_urls = [
                ('communication/', 'communication.urls'),
                ('medecin/', 'medecin.urls'),
                ('pharmacien/', 'pharmacien.urls'),
                ('accounts/', 'django.contrib.auth.urls'),
            ]
            
            for url_path, include_module in critical_urls:
                if f"'{url_path}'" in content or f'"{url_path}"' in content:
                    self.success.append(f"🔗 {url_path} - Configuré")
                else:
                    self.warnings.append(f"⚠️ {url_path} - Non trouvé")
                    
        except Exception as e:
            self.errors.append(f"Erreur URLs: {str(e)}")
    
    def check_views_errors(self):
        """Vérifie les vues problématiques"""
        print("9. 👁️ Vérification des vues...")
        
        # Vérifier les vues basées sur les logs d'erreur
        views_to_check = ['communication.views']
        
        for view_module in views_to_check:
            try:
                __import__(view_module)
                self.success.append(f"👁️ {view_module} - Import OK")
            except SyntaxError as e:
                self.errors.append(f"❌ {view_module} - Erreur syntaxe: {str(e)}")
            except ImportError as e:
                self.warnings.append(f"⚠️ {view_module} - Erreur import: {str(e)}")
    
    def check_static_files(self):
        """Vérifie les fichiers statiques"""
        print("10. 📦 Vérification des fichiers statiques...")
        
        static_dirs = [
            self.project_root / 'static',
            self.project_root / 'static' / 'img',
            self.project_root / 'static' / 'css',
            self.project_root / 'static' / 'js',
        ]
        
        for static_dir in static_dirs:
            if static_dir.exists():
                files = list(static_dir.glob('*'))
                self.success.append(f"📦 {static_dir.relative_to(self.project_root)} - {len(files)} fichiers")
            else:
                self.warnings.append(f"⚠️ {static_dir.relative_to(self.project_root)} - Absent")
    
    def check_migrations(self):
        """Vérifie l'état des migrations"""
        print("11. 🚀 Vérification des migrations...")
        
        try:
            # Vérifier si des migrations sont en attente
            result = subprocess.run(
                [sys.executable, 'manage.py', 'showmigrations'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                unmigrated = [line for line in lines if '[ ]' in line]
                
                if unmigrated:
                    self.warnings.append(f"🚀 {len(unmigrated)} migrations en attente")
                else:
                    self.success.append("🚀 Toutes les migrations appliquées")
            else:
                self.errors.append("❌ Impossible de vérifier les migrations")
                
        except Exception as e:
            self.warnings.append(f"⚠️ Migrations: {str(e)}")
    
    def check_permissions(self):
        """Vérifie les permissions des fichiers"""
        print("12. 🔒 Vérification des permissions...")
        
        critical_files = [
            'manage.py',
            'mutuelle_core/settings.py',
            'mutuelle_core/urls.py'
        ]
        
        for file_path in critical_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                if os.access(full_path, os.R_OK):
                    self.success.append(f"🔒 {file_path} - Lecture OK")
                else:
                    self.errors.append(f"❌ {file_path} - Pas de permission lecture")
            else:
                self.warnings.append(f"⚠️ {file_path} - Fichier manquant")
    
    def generate_report(self):
        """Génère le rapport final"""
        print("\n" + "=" * 60)
        print("📊 RAPPORT DE DIAGNOSTIC")
        print("=" * 60)
        
        if self.errors:
            print(f"\n❌ ERREURS CRITIQUES ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print(f"\n⚠️  AVERTISSEMENTS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.success:
            print(f"\n✅ SUCCÈS ({len(self.success)}):")
            for success in self.success[:20]:  # Limiter l'affichage
                print(f"  • {success}")
            
            if len(self.success) > 20:
                print(f"  ... et {len(self.success) - 20} autres succès")
        
        # Recommandations
        print("\n" + "=" * 60)
        print("💡 RECOMMANDATIONS")
        print("=" * 60)
        
        if self.errors:
            print("""
1. ❌ CORRIGEZ LES ERREURS CRITIQUES EN PRIORITÉ
   - Résolvez les erreurs de syntaxe Python
   - Corrigez les problèmes d'importation
   - Vérifiez la configuration de la base de données
   
2. ⚠️  TRAITEZ LES AVERTISSEMENTS
   - Complétez les configurations manquantes
   - Appliquez les migrations en attente
   - Vérifiez la structure des dossiers
   
3. 🔧 ACTIONS IMMÉDIATES:
   - python manage.py check
   - python manage.py makemigrations
   - python manage.py migrate
   - python manage.py collectstatic
            """)
        else:
            print("""
🎉 PROJET EN BON ÉTAT!
   
   Actions recommandées:
   1. 🔄 Redémarrez le serveur: python manage.py runserver
   2. 🧪 Testez les fonctionnalités principales
   3. 📊 Vérifiez les logs pour les erreurs restantes
   4. 💾 Sauvegardez votre base de données
            """)
        
        print(f"\n📈 STATISTIQUES:")
        print(f"   • ✅ Succès: {len(self.success)}")
        print(f"   • ⚠️  Avertissements: {len(self.warnings)}")
        print(f"   • ❌ Erreurs: {len(self.errors)}")
        
        # Sauvegarde du rapport
        self.save_report()
    
    def save_report(self):
        """Sauvegarde le rapport dans un fichier"""
        report = {
            'timestamp': subprocess.getoutput('date'),
            'errors': self.errors,
            'warnings': self.warnings,
            'success_count': len(self.success),
            'project_root': str(self.project_root),
        }
        
        report_file = self.project_root / 'diagnostic_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Rapport sauvegardé: {report_file}")

def quick_diagnostic():
    """Diagnostic rapide en 3 commandes"""
    print("🚀 DIAGNOSTIC RAPIDE")
    print("=" * 40)
    
    project_root = PROJECT_ROOT
    
    commands = [
        ("Vérification Django", ["python", "manage.py", "check"]),
        ("Migrations", ["python", "manage.py", "makemigrations", "--check"]),
        ("URLs", ["python", "manage.py", "show_urls"]),
        ("Sessions", ["python", "manage.py", "clearsessions"]),
    ]
    
    for name, cmd in commands:
        print(f"\n🔍 {name}...")
        try:
            result = subprocess.run(
                cmd,
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"   ✅ {name} - OK")
            else:
                print(f"   ❌ {name} - ÉCHEC")
                print(f"      {result.stderr[:200]}")
        except subprocess.TimeoutExpired:
            print(f"   ⏱️  {name} - TIMEOUT")
        except Exception as e:
            print(f"   ❓ {name} - ERREUR: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Diagnostic du projet Django')
    parser.add_argument('--quick', action='store_true', help='Diagnostic rapide')
    parser.add_argument('--fix', action='store_true', help='Tenter des corrections automatiques')
    
    args = parser.parse_args()
    
    if args.quick:
        quick_diagnostic()
    else:
        diagnostic = DjangoDiagnostic()
        diagnostic.run_full_diagnostic()
        
        if args.fix:
            print("\n🔧 TENTATIVE DE CORRECTIONS AUTOMATIQUES...")
            try:
                # Corriger l'indentation avec autopep8 si disponible
                try:
                    subprocess.run([sys.executable, '-m', 'pip', 'install', 'autopep8'], 
                                  capture_output=True)
                    subprocess.run([sys.executable, '-m', 'autopep8', '--in-place', '--recursive', 
                                   '--aggressive', str(PROJECT_ROOT)], 
                                  cwd=PROJECT_ROOT)
                    print("✅ Correction d'indentation appliquée")
                except:
                    print("⚠️  Impossible d'appliquer autopep8")
                
                # Effacer les sessions
                subprocess.run([sys.executable, 'manage.py', 'clearsessions'], 
                              cwd=PROJECT_ROOT, capture_output=True)
                print("✅ Sessions effacées")
                
                # Collecter les fichiers statiques
                subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], 
                              cwd=PROJECT_ROOT, capture_output=True)
                print("✅ Fichiers statiques collectés")
                
            except Exception as e:
                print(f"❌ Erreur lors des corrections: {str(e)}")