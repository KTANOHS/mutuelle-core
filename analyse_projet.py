#!/usr/bin/env python3
"""
Script d'analyse d'arborescence Django
Version complète avec détection de problèmes, statistiques et recommandations
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import re

class AnalyseurProjetDjango:
    def __init__(self, chemin_racine=None):
        """Initialise l'analyseur avec le chemin racine"""
        self.chemin_racine = chemin_racine or os.getcwd()
        self.stats = {
            'total_fichiers': 0,
            'total_dossiers': 0,
            'fichiers_par_type': {},
            'dossiers_critiques': [],
            'fichiers_manquants': [],
            'problemes': [],
            'applications': [],
            'configurations': {}
        }
        
        # Fichiers et dossiers critiques pour Django
        self.fichiers_critiques = [
            'manage.py',
            'requirements.txt',
            'runtime.txt',
            'Procfile',
            'render.yaml',
            'Dockerfile',
            '.env',
            '.env.example',
            '.gitignore',
            'README.md',
            'gunicorn_config.py',
            'start_prod.sh'
        ]
        
        self.dossiers_critiques = [
            'static',
            'staticfiles',
            'media',
            'templates',
            'migrations',
            'logs',
            'locale'
        ]
        
        # Extensions à analyser
        self.extensions_python = ['.py', '.pyc', '.pyo', '.pyd']
        self.extensions_static = ['.html', '.css', '.js', '.json', '.xml']
        self.extensions_media = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.mp4', '.webm']
        
    def analyser(self):
        """Lance l'analyse complète du projet"""
        print("🔍 ANALYSE DU PROJET DJANGO")
        print("=" * 80)
        
        self._afficher_infos_generales()
        self._analyser_arborescence()
        self._verifier_structure_django()
        self._verifier_dependances()
        self._analyser_settings()
        self._verifier_git()
        self._analyser_securite()
        self._generer_rapport()
        
        return self.stats
    
    def _afficher_infos_generales(self):
        """Affiche les informations générales du projet"""
        print(f"📁 Projet: {os.path.basename(self.chemin_racine)}")
        print(f"📂 Chemin: {self.chemin_racine}")
        print(f"📅 Date analyse: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 80)
        
    def _analyser_arborescence(self, niveau_max=4):
        """Analyse l'arborescence du projet"""
        print("\n🌳 ARBORESCENCE DU PROJET (max niveau {})".format(niveau_max))
        print("-" * 80)
        
        applications = []
        
        for root, dirs, files in os.walk(self.chemin_racine):
            # Calculer le niveau de profondeur
            niveau = root.replace(self.chemin_racine, '').count(os.sep)
            
            if niveau > niveau_max:
                continue
            
            # Ignorer les dossiers cachés et virtuels
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', 'venv', '.venv']]
            
            # Affichage avec indentation
            indent = "  " * niveau
            rel_path = os.path.relpath(root, self.chemin_racine)
            
            if rel_path == '.':
                print("📦 /")
            else:
                print(f"{indent}📁 {os.path.basename(root)}/")
            
            # Compter les fichiers
            for file in sorted(files):
                if not file.startswith('.'):
                    self.stats['total_fichiers'] += 1
                    
                    # Détecter les applications Django
                    if file == 'apps.py' and '__init__.py' in files:
                        app_name = os.path.basename(root)
                        applications.append({
                            'nom': app_name,
                            'chemin': rel_path,
                            'fichiers': len(files)
                        })
                    
                    # Classer par extension
                    ext = os.path.splitext(file)[1].lower()
                    if ext:
                        self.stats['fichiers_par_type'][ext] = self.stats['fichiers_par_type'].get(ext, 0) + 1
                    
                    # Afficher les fichiers importants
                    if niveau <= 3 or file in self.fichiers_critiques:
                        file_indent = "  " * (niveau + 1)
                        prefix = "⭐" if file in self.fichiers_critiques else "📄"
                        print(f"{file_indent}{prefix} {file}")
            
            self.stats['total_dossiers'] += 1
        
        self.stats['applications'] = applications
        
        # Afficher le récapitulatif des applications
        if applications:
            print("\n📦 APPLICATIONS DJANGO DÉTECTÉES:")
            for app in applications:
                print(f"  • {app['nom']} (dans {app['chemin']}) - {app['fichiers']} fichiers")
    
    def _verifier_structure_django(self):
        """Vérifie la structure Django standard"""
        print("\n🔍 VÉRIFICATION STRUCTURE DJANGO")
        print("-" * 80)
        
        # Vérifier manage.py
        manage_py = os.path.join(self.chemin_racine, 'manage.py')
        if os.path.exists(manage_py):
            print("✅ manage.py présent")
            
            # Vérifier si manage.py est exécutable
            if os.access(manage_py, os.X_OK):
                print("✅ manage.py est exécutable")
            else:
                print("⚠️  manage.py n'est pas exécutable (chmod +x manage.py)")
        else:
            print("❌ manage.py MANQUANT")
            self.stats['problemes'].append('manage.py manquant')
        
        # Vérifier settings.py
        settings_py = self._trouver_fichier('settings.py')
        if settings_py:
            print(f"✅ settings.py trouvé: {os.path.relpath(settings_py, self.chemin_racine)}")
            
            # Analyser rapidement settings.py
            with open(settings_py, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'DEBUG = True' in content:
                    print("⚠️  DEBUG=True détecté dans settings.py")
                if 'SECRET_KEY' in content and 'get_random_secret_key' not in content:
                    print("⚠️  Vérifiez que SECRET_KEY est sécurisée en production")
        else:
            print("❌ settings.py NON TROUVÉ")
            self.stats['problemes'].append('settings.py non trouvé')
        
        # Vérifier les dossiers critiques
        print("\n📁 VÉRIFICATION DES DOSSIERS:")
        for dossier in self.dossiers_critiques:
            chemin = os.path.join(self.chemin_racine, dossier)
            if os.path.exists(chemin):
                taille = self._calculer_taille_dossier(chemin)
                print(f"  ✅ {dossier}/ ({taille})")
                self.stats['dossiers_critiques'].append(dossier)
            else:
                print(f"  ⚠️  {dossier}/ MANQUANT")
                self.stats['fichiers_manquants'].append(dossier)
        
        # Vérifier les fichiers critiques
        print("\n📄 VÉRIFICATION DES FICHIERS:")
        for fichier in self.fichiers_critiques:
            chemin = os.path.join(self.chemin_racine, fichier)
            if os.path.exists(chemin):
                taille = os.path.getsize(chemin)
                print(f"  ✅ {fichier} ({taille} octets)")
            else:
                niveau = "⚠️" if fichier in ['README.md', '.env.example'] else "❌"
                print(f"  {niveau} {fichier} MANQUANT")
                if niveau == "❌":
                    self.stats['fichiers_manquants'].append(fichier)
    
    def _verifier_dependances(self):
        """Vérifie les dépendances Python"""
        print("\n🐍 VÉRIFICATION DES DÉPENDANCES")
        print("-" * 80)
        
        requirements_files = [
            'requirements.txt',
            'requirements-prod.txt',
            'Pipfile',
            'pyproject.toml',
            'setup.py'
        ]
        
        found = False
        for req_file in requirements_files:
            chemin = os.path.join(self.chemin_racine, req_file)
            if os.path.exists(chemin):
                found = True
                print(f"✅ {req_file} trouvé")
                
                # Analyser requirements.txt
                if req_file == 'requirements.txt':
                    with open(chemin, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        deps = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
                        print(f"  📦 {len(deps)} dépendances trouvées")
                        
                        # Vérifier les dépendances critiques
                        dep_critiques = ['Django', 'gunicorn', 'whitenoise', 'psycopg2-binary']
                        for dep in dep_critiques:
                            if any(dep in d for d in deps):
                                print(f"  ✅ {dep} présent")
                            else:
                                print(f"  ⚠️  {dep} MANQUANT")
        
        if not found:
            print("❌ Aucun fichier de dépendances trouvé")
            self.stats['problemes'].append('Fichier de dépendances manquant')
        
        # Vérifier runtime.txt pour Python version
        runtime = os.path.join(self.chemin_racine, 'runtime.txt')
        if os.path.exists(runtime):
            with open(runtime, 'r') as f:
                version = f.read().strip()
                print(f"✅ runtime.txt: {version}")
        else:
            print("⚠️  runtime.txt manquant (recommandé pour Render)")
    
    def _analyser_settings(self):
        """Analyse rapide du fichier settings.py"""
        print("\n⚙️  ANALYSE RAPIDE SETTINGS.PY")
        print("-" * 80)
        
        settings_path = self._trouver_fichier('settings.py')
        if not settings_path:
            return
        
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extraire les configurations importantes
            configs = {}
            
            # DEBUG
            debug_match = re.search(r'DEBUG\s*=\s*(True|False)', content)
            if debug_match:
                configs['DEBUG'] = debug_match.group(1)
                print(f"🔧 DEBUG = {debug_match.group(1)}")
            
            # ALLOWED_HOSTS
            hosts_match = re.search(r'ALLOWED_HOSTS\s*=\s*\[(.*?)\]', content, re.DOTALL)
            if hosts_match:
                hosts = hosts_match.group(1)
                num_hosts = len([h for h in hosts.split(',') if h.strip()])
                print(f"🌐 ALLOWED_HOSTS = {num_hosts} hôtes")
            
            # DATABASES
            if 'dj_database_url' in content:
                print("🗄️  DATABASE: PostgreSQL (dj_database_url)")
                configs['DATABASE'] = 'PostgreSQL'
            elif 'sqlite3' in content:
                print("🗄️  DATABASE: SQLite")
                configs['DATABASE'] = 'SQLite'
            
            # STATIC
            if 'whitenoise' in content:
                print("📁 STATIC: WhiteNoise configuré")
                configs['STATIC'] = 'WhiteNoise'
            elif 'STATICFILES_STORAGE' in content:
                print("📁 STATIC: Stockage Django")
                configs['STATIC'] = 'Django'
            
            # SECURITY
            security_flags = []
            if 'SECURE_SSL_REDIRECT' in content and 'True' in content:
                security_flags.append('SSL Redirect')
            if 'SESSION_COOKIE_SECURE' in content and 'True' in content:
                security_flags.append('Secure Cookies')
            if 'CSRF_COOKIE_SECURE' in content and 'True' in content:
                security_flags.append('Secure CSRF')
            
            if security_flags:
                print(f"🔒 Sécurité: {', '.join(security_flags)}")
            
            self.stats['configurations'] = configs
            
        except Exception as e:
            print(f"⚠️  Erreur lors de l'analyse de settings.py: {e}")
    
    def _verifier_git(self):
        """Vérifie la configuration Git"""
        print("\n📚 VÉRIFICATION GIT")
        print("-" * 80)
        
        git_dir = os.path.join(self.chemin_racine, '.git')
        if os.path.exists(git_dir):
            print("✅ Repository Git initialisé")
            
            # Vérifier .gitignore
            gitignore = os.path.join(self.chemin_racine, '.gitignore')
            if os.path.exists(gitignore):
                with open(gitignore, 'r', encoding='utf-8') as f:
                    lines = [l.strip() for l in f.readlines() if l.strip()]
                    print(f"✅ .gitignore: {len(lines)} règles")
                    
                    # Vérifier les exclusions critiques
                    patterns_critiques = [
                        '*.pyc',
                        '__pycache__',
                        '.env',
                        'db.sqlite3',
                        '*.log',
                        'staticfiles/',
                        'media/'
                    ]
                    
                    manquants = []
                    for pattern in patterns_critiques:
                        if not any(pattern in line for line in lines):
                            manquants.append(pattern)
                    
                    if manquants:
                        print(f"⚠️  .gitignore manque: {', '.join(manquants)}")
            else:
                print("❌ .gitignore manquant")
        else:
            print("⚠️  Repository Git non initialisé")
    
    def _analyser_securite(self):
        """Analyse de sécurité rapide"""
        print("\n🛡️  ANALYSE DE SÉCURITÉ RAPIDE")
        print("-" * 80)
        
        # Vérifier .env
        env_file = os.path.join(self.chemin_racine, '.env')
        if os.path.exists(env_file):
            print("⚠️  .env présent - Vérifiez qu'il n'est pas commité")
            
            # Vérifier s'il contient des secrets
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'SECRET_KEY' in content and 'password' in content.lower():
                    print("⚠️  SECRET_KEY détectée dans .env")
        
        # Vérifier permissions
        manage_py = os.path.join(self.chemin_racine, 'manage.py')
        if os.path.exists(manage_py):
            perms = oct(os.stat(manage_py).st_mode)[-3:]
            if perms != '755' and perms != '744':
                print(f"⚠️  manage.py permissions: {perms} (recommandé: 755)")
        
        # Vérifier SQLite en production
        settings_path = self._trouver_fichier('settings.py')
        if settings_path:
            with open(settings_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'sqlite3' in content and 'DEBUG = False' in content:
                    print("⚠️  SQLite détecté avec DEBUG=False - Non recommandé pour production")
    
    def _generer_rapport(self):
        """Génère un rapport complet"""
        print("\n📊 RAPPORT D'ANALYSE")
        print("=" * 80)
        
        # Statistiques
        print(f"\n📈 STATISTIQUES:")
        print(f"  • Fichiers totaux: {self.stats['total_fichiers']}")
        print(f"  • Dossiers totaux: {self.stats['total_dossiers']}")
        print(f"  • Applications Django: {len(self.stats['applications'])}")
        
        if self.stats['fichiers_par_type']:
            print(f"\n📁 FICHIERS PAR TYPE:")
            for ext, count in sorted(self.stats['fichiers_par_type'].items(), key=lambda x: x[1], reverse=True):
                print(f"  • {ext}: {count}")
        
        # Problèmes détectés
        if self.stats['problemes']:
            print(f"\n❌ PROBLÈMES CRITIQUES:")
            for probleme in self.stats['problemes']:
                print(f"  • {probleme}")
        
        if self.stats['fichiers_manquants']:
            print(f"\n⚠️  FICHIERS/DOSSIERS MANQUANTS:")
            for manquant in self.stats['fichiers_manquants']:
                print(f"  • {manquant}")
        
        # Recommandations
        print("\n💡 RECOMMANDATIONS:")
        
        # Vérifier Render configuration
        render_yaml = os.path.join(self.chemin_racine, 'render.yaml')
        if not os.path.exists(render_yaml):
            print("  • Créer un fichier render.yaml pour le déploiement Render")
        
        # Vérifier runtime.txt
        runtime = os.path.join(self.chemin_racine, 'runtime.txt')
        if not os.path.exists(runtime):
            print("  • Ajouter runtime.txt avec 'python-3.11.10'")
        
        # Vérifier Procfile
        procfile = os.path.join(self.chemin_racine, 'Procfile')
        if not os.path.exists(procfile):
            print("  • Créer un Procfile avec 'web: gunicorn mutuelle_core.wsgi:application'")
        
        # Sauvegarder le rapport
        rapport_file = os.path.join(self.chemin_racine, 'rapport_analyse.json')
        with open(rappont_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Rapport sauvegardé: {rapport_file}")
    
    def _trouver_fichier(self, nom_fichier):
        """Cherche un fichier dans l'arborescence"""
        for root, dirs, files in os.walk(self.chemin_racine):
            if nom_fichier in files:
                return os.path.join(root, nom_fichier)
        return None
    
    def _calculer_taille_dossier(self, chemin):
        """Calcule la taille d'un dossier en format lisible"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(chemin):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total_size += os.path.getsize(fp)
        
        # Formatage
        for unit in ['octets', 'Ko', 'Mo', 'Go']:
            if total_size < 1024.0:
                return f"{total_size:.1f} {unit}"
            total_size /= 1024.0
        return f"{total_size:.1f} To"

def main():
    """Fonction principale"""
    if len(sys.argv) > 1:
        chemin = sys.argv[1]
    else:
        chemin = os.getcwd()
    
    # Vérifier que le chemin existe
    if not os.path.exists(chemin):
        print(f"❌ Chemin non trouvé: {chemin}")
        sys.exit(1)
    
    # Créer et exécuter l'analyseur
    analyseur = AnalyseurProjetDjango(chemin)
    
    try:
        stats = analyseur.analyser()
        print(f"\n{'=' * 80}")
        print("✅ Analyse terminée avec succès!")
        
        # Code de sortie basé sur les problèmes
        if stats['problemes']:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Analyse interrompue par l'utilisateur")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Erreur lors de l'analyse: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()