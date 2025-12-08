#!/usr/bin/env python3
"""
Script d'analyse complète d'un projet Django avant mise en production
Vérifie la sécurité, la configuration, la structure et les bonnes pratiques
"""

import os
import sys
import ast
import re
import subprocess
from pathlib import Path
from datetime import datetime
import django
from django.conf import settings
from django.core.management import execute_from_command_line

class ProjectAnalyzer:
    """Analyseur complet de projet Django"""
    
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.issues = {
            'critical': [],
            'warning': [],
            'info': [],
            'recommendation': []
        }
        self.stats = {
            'files_analyzed': 0,
            'lines_analyzed': 0,
            'security_issues': 0,
            'performance_issues': 0
        }
        
    def analyze_all(self):
        """Exécute toutes les analyses"""
        print("🔍 Démarrage de l'analyse du projet Django...")
        print("=" * 60)
        
        self.analyze_project_structure()
        self.analyze_settings()
        self.analyze_requirements()
        self.analyze_models()
        self.analyze_views()
        self.analyze_urls()
        self.analyze_static_files()
        self.analyze_templates()
        self.analyze_middleware()
        self.analyze_security()
        self.analyze_performance()
        self.analyze_database()
        
        self.generate_report()
        
    def add_issue(self, level, category, message, file=None, line=None):
        """Ajoute un problème au rapport"""
        issue = {
            'category': category,
            'message': message,
            'file': file,
            'line': line,
            'timestamp': datetime.now()
        }
        self.issues[level].append(issue)
        
        if level in ['critical', 'warning']:
            self.stats['security_issues'] += 1

    def analyze_project_structure(self):
        """Analyse la structure du projet"""
        print("\n📁 Analyse de la structure du projet...")
        
        required_dirs = [
            'static',
            'media',
            'templates',
            'logs',
            'locale'
        ]
        
        required_files = [
            'manage.py',
            'requirements.txt',
            '.env.example',
            'README.md',
            '.gitignore'
        ]
        
        for dir_name in required_dirs:
            dir_path = self.project_path / dir_name
            if not dir_path.exists():
                self.add_issue('warning', 'Structure', f"Dossier manquant: {dir_name}")
            else:
                self.add_issue('info', 'Structure', f"Dossier présent: {dir_name}")

        for file_name in required_files:
            file_path = self.project_path / file_name
            if not file_path.exists():
                self.add_issue('warning', 'Structure', f"Fichier manquant: {file_name}")
            else:
                self.add_issue('info', 'Structure', f"Fichier présent: {file_name}")

    def analyze_settings(self):
        """Analyse le fichier settings.py"""
        print("\n⚙️  Analyse de la configuration...")
        
        settings_file = self.project_path / 'settings.py'
        if not settings_file.exists():
            self.add_issue('critical', 'Configuration', "Fichier settings.py introuvable")
            return
            
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.stats['lines_analyzed'] += len(content.split('\n'))
            
        # Vérifications de sécurité
        security_checks = [
            (r'DEBUG\s*=\s*True', 'DEBUG doit être False en production', 'critical'),
            (r'SECRET_KEY\s*=\s*[\'"][^\'"]+[\'"]', 'SECRET_KEY en dur dans le code', 'critical'),
            (r'DATABASES.*sqlite3', 'SQLite utilisé - non recommandé en production', 'warning'),
            (r'EMAIL_BACKEND.*console', 'Email en mode console - configurer SMTP', 'warning'),
            (r'SESSION_COOKIE_SECURE\s*=\s*False', 'Session cookie non sécurisé', 'critical'),
            (r'CSRF_COOKIE_SECURE\s*=\s*False', 'CSRF cookie non sécurisé', 'critical'),
            (r'ALLOWED_HOSTS\s*=\s*\[\]', 'ALLOWED_HOSTS vide', 'critical'),
            (r'ALLOWED_HOSTS\s*=\s*\[.*\*.*\]', 'ALLOWED_HOSTS contient * - trop permissif', 'critical'),
        ]
        
        for pattern, message, level in security_checks:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                self.add_issue(level, 'Sécurité', message, 'settings.py')

        # Vérifications de configuration
        config_checks = [
            (r'STATIC_ROOT', 'STATIC_ROOT configuré', 'info'),
            (r'MEDIA_ROOT', 'MEDIA_ROOT configuré', 'info'),
            (r'LOGGING', 'Configuration des logs présente', 'info'),
            (r'CACHES', 'Cache configuré', 'info'),
            (r'SECURE_SSL_REDIRECT', 'SSL redirect activé', 'info'),
        ]
        
        for pattern, message, level in config_checks:
            if re.search(pattern, content):
                self.add_issue(level, 'Configuration', message, 'settings.py')
            else:
                self.add_issue('warning', 'Configuration', f"Configuration manquante: {message}", 'settings.py')

    def analyze_requirements(self):
        """Analyse le fichier requirements.txt"""
        print("\n📦 Analyse des dépendances...")
        
        req_file = self.project_path / 'requirements.txt'
        if not req_file.exists():
            self.add_issue('critical', 'Dépendances', "Fichier requirements.txt introuvable")
            return
            
        with open(req_file, 'r') as f:
            requirements = f.read()
            
        # Vérifier les versions spécifiques
        if not re.search(r'==\d+\.\d+', requirements):
            self.add_issue('warning', 'Dépendances', "Versions de dépendances non spécifiées")
            
        # Vérifier les dépendances critiques
        critical_deps = ['django', 'gunicorn', 'whitenoise', 'psycopg2-binary', 'python-dotenv']
        for dep in critical_deps:
            if dep not in requirements.lower():
                self.add_issue('warning', 'Dépendances', f"Dépendance recommandée manquante: {dep}")

    def analyze_models(self):
        """Analyse les modèles Django"""
        print("\n🗄️  Analyse des modèles...")
        
        models_dir = self.project_path / 'models'
        if not models_dir.exists():
            # Chercher dans les apps
            for app in self.project_path.iterdir():
                if app.is_dir() and (app / 'models.py').exists():
                    self.analyze_model_file(app / 'models.py')

    def analyze_model_file(self, model_file):
        """Analyse un fichier models.py spécifique"""
        try:
            with open(model_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifier les modèles sans __str__
            if 'class Meta:' in content and '__str__' not in content:
                self.add_issue('warning', 'Modèles', 
                             f"Modèle sans méthode __str__ dans {model_file.name}")
                             
            # Vérifier les imports de sécurité
            if 'models.TextField()' in content and 'strip' not in content:
                self.add_issue('info', 'Modèles', 
                             f"TextField sans validation dans {model_file.name}")

        except Exception as e:
            self.add_issue('warning', 'Modèles', f"Erreur analyse {model_file}: {str(e)}")

    def analyze_views(self):
        """Analyse les vues"""
        print("\n👁️  Analyse des vues...")
        
        # Recherche des fichiers views.py
        for app in self.project_path.iterdir():
            if app.is_dir() and (app / 'views.py').exists():
                self.analyze_view_file(app / 'views.py')

    def analyze_view_file(self, view_file):
        """Analyse un fichier views.py spécifique"""
        try:
            with open(view_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifications de sécurité
            security_patterns = [
                (r'@csrf_exempt', 'CSRF exemption détectée', 'warning'),
                (r'execute\(', 'Appel execute() potentiellement dangereux', 'critical'),
                (r'eval\(', 'Appel eval() détecté', 'critical'),
                (r'raw\(.*\)', 'Query raw() sans validation', 'warning'),
            ]
            
            for pattern, message, level in security_patterns:
                if re.search(pattern, content):
                    self.add_issue(level, 'Vues', f"{message} dans {view_file.name}")

        except Exception as e:
            self.add_issue('warning', 'Vues', f"Erreur analyse {view_file}: {str(e)}")

    def analyze_urls(self):
        """Analyse les configurations d'URLs"""
        print("\n🔗 Analyse des URLs...")
        
        urls_file = self.project_path / 'urls.py'
        if urls_file.exists():
            with open(urls_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifier la présence d'admin
            if 'admin/' in content:
                self.add_issue('info', 'URLs', "Interface admin activée")
                
            # Vérifier les URLs sans trailing slash
            if re.search(r'path\([^)]*[^/]\)', content):
                self.add_issue('warning', 'URLs', "URLs sans trailing slash détectées")

    def analyze_static_files(self):
        """Analyse les fichiers statiques"""
        print("\n📄 Analyse des fichiers statiques...")
        
        static_dir = self.project_path / 'static'
        if static_dir.exists():
            # Vérifier la taille des fichiers
            for file_path in static_dir.rglob('*'):
                if file_path.is_file():
                    size = file_path.stat().st_size
                    if size > 5 * 1024 * 1024:  # 5MB
                        self.add_issue('warning', 'Statiques', 
                                     f"Fichier statique volumineux: {file_path} ({size//1024}KB)")

    def analyze_templates(self):
        """Analyse les templates"""
        print("\n🎨 Analyse des templates...")
        
        templates_dir = self.project_path / 'templates'
        if templates_dir.exists():
            for template_file in templates_dir.rglob('*.html'):
                self.analyze_template_file(template_file)

    def analyze_template_file(self, template_file):
        """Analyse un template spécifique"""
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifier les balises autoescape
            if '{% autoescape off %}' in content and '{% endautoescape %}' not in content:
                self.add_issue('warning', 'Templates', 
                             f"Autoescape désactivé sans fin dans {template_file.name}")
                             
            # Vérifier les URLs hardcodées
            if 'http://' in content:
                self.add_issue('warning', 'Templates', 
                             f"URL HTTP (non sécurisée) dans {template_file.name}")

        except Exception as e:
            self.add_issue('warning', 'Templates', f"Erreur analyse {template_file}: {str(e)}")

    def analyze_middleware(self):
        """Analyse la configuration du middleware"""
        print("\n🛡️  Analyse du middleware...")
        
        settings_file = self.project_path / 'settings.py'
        if settings_file.exists():
            with open(settings_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifier les middlewares essentiels
            essential_middleware = [
                'SecurityMiddleware',
                'SessionMiddleware',
                'CsrfViewMiddleware',
                'AuthenticationMiddleware'
            ]
            
            for middleware in essential_middleware:
                if middleware not in content:
                    self.add_issue('warning', 'Middleware', 
                                 f"Middleware essentiel manquant: {middleware}")

    def analyze_security(self):
        """Analyse de sécurité approfondie"""
        print("\n🔐 Analyse de sécurité...")
        
        # Vérifier les permissions de fichiers
        sensitive_files = ['.env', 'settings.py', 'wsgi.py']
        for file_name in sensitive_files:
            file_path = self.project_path / file_name
            if file_path.exists():
                mode = file_path.stat().st_mode
                if mode & 0o777 != 0o600:  # Trop permissif
                    self.add_issue('warning', 'Sécurité', 
                                 f"Permissions trop permissives pour {file_name}: {oct(mode)}")

    def analyze_performance(self):
        """Analyse des performances"""
        print("\n⚡ Analyse des performances...")
        
        settings_file = self.project_path / 'settings.py'
        if settings_file.exists():
            with open(settings_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifications performance
            if 'DEBUG_TOOLBAR' in content:
                self.add_issue('warning', 'Performance', 
                             "Django Debug Toolbar activé - désactiver en production")
                             
            if 'LocMemCache' in content and not 'Redis' in content and not 'Memcached' in content:
                self.add_issue('info', 'Performance', 
                             "Cache en mémoire local - envisager Redis/Memcached pour la production")

    def analyze_database(self):
        """Analyse de la configuration base de données"""
        print("\n🗃️  Analyse de la base de données...")
        
        settings_file = self.project_path / 'settings.py'
        if settings_file.exists():
            with open(settings_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifier la configuration DB
            if 'sqlite3' in content.lower():
                self.add_issue('critical', 'Base de données', 
                             "SQLite utilisé - migrer vers PostgreSQL pour la production")
            elif 'postgresql' in content.lower():
                self.add_issue('info', 'Base de données', 
                             "PostgreSQL configuré - bon choix pour la production")
                
            # Vérifier la connexion persistante
            if 'CONN_MAX_AGE' not in content:
                self.add_issue('warning', 'Base de données', 
                             "CONN_MAX_AGE non configuré - recommandé pour les performances")

    def generate_report(self):
        """Génère le rapport final"""
        print("\n" + "=" * 60)
        print("📊 RAPPORT D'ANALYSE COMPLET")
        print("=" * 60)
        
        # Statistiques
        print(f"\n📈 STATISTIQUES:")
        print(f"• Fichiers analysés: {self.stats['files_analyzed']}")
        print(f"• Lignes analysées: {self.stats['lines_analyzed']}")
        print(f"• Problèmes de sécurité: {self.stats['security_issues']}")
        
        # Problèmes critiques
        if self.issues['critical']:
            print(f"\n❌ PROBLÈMES CRITIQUES ({len(self.issues['critical'])}):")
            for issue in self.issues['critical']:
                print(f"  • {issue['category']}: {issue['message']}")
                if issue['file']:
                    print(f"    Fichier: {issue['file']}")
        
        # Avertissements
        if self.issues['warning']:
            print(f"\n⚠️  AVERTISSEMENTS ({len(self.issues['warning'])}):")
            for issue in self.issues['warning']:
                print(f"  • {issue['category']}: {issue['message']}")
                if issue['file']:
                    print(f"    Fichier: {issue['file']}")
        
        # Recommandations
        if self.issues['recommendation']:
            print(f"\n💡 RECOMMANDATIONS ({len(self.issues['recommendation'])}):")
            for issue in self.issues['recommendation']:
                print(f"  • {issue['category']}: {issue['message']}")
        
        # Score global
        critical_count = len(self.issues['critical'])
        warning_count = len(self.issues['warning'])
        
        if critical_count > 0:
            status = "❌ PROJET NON PRÊT POUR LA PRODUCTION"
        elif warning_count > 5:
            status = "⚠️  PROJET AVEC RÉSERVES"
        else:
            status = "✅ PROJET PRÊT POUR LA PRODUCTION"
            
        print(f"\n🎯 STATUT FINAL: {status}")
        
        # Actions recommandées
        self.print_recommended_actions()

    def print_recommended_actions(self):
        """Affiche les actions recommandées"""
        print(f"\n🚀 ACTIONS RECOMMANDÉES:")
        
        actions = [
            "1. Configurer DEBUG=False en production",
            "2. Définir SECRET_KEY via variable d'environnement",
            "3. Configurer ALLOWED_HOSTS avec les domaines de production",
            "4. Migrer de SQLite vers PostgreSQL",
            "5. Configurer un serveur SMTP pour les emails",
            "6. Activer SESSION_COOKIE_SECURE et CSRF_COOKIE_SECURE",
            "7. Configurer HTTPS et redirections SSL",
            "8. Configurer les backups de base de données",
            "9. Mettre en place la surveillance (monitoring)",
            "10. Tester les procédures de déploiement"
        ]
        
        for action in actions:
            print(f"   {action}")

def main():
    """Point d'entrée principal"""
    if len(sys.argv) != 2:
        print("Usage: python analyze_project2.py /Users/koffitanohsoualiho/Documents/projet")
        sys.exit(1)
        
    project_path = sys.argv[1]
    
    if not os.path.exists(project_path):
        print(f"Erreur: Le chemin {project_path} n'existe pas")
        sys.exit(1)
        
    analyzer = ProjectAnalyzer(project_path)
    analyzer.analyze_all()

if __name__ == "__main__":
    main()