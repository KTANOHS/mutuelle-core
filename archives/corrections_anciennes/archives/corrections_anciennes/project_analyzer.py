#!/usr/bin/env python3
"""
ANALYSEUR COMPLET DE PROJET DJANGO
Scan tous les aspects du projet : templates, URLs, vues, modèles, statics, etc.
"""

import os
import re
import django
from pathlib import Path
import sys
import subprocess
from django.conf import settings
from django.urls.resolvers import get_resolver

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

BASE_DIR = Path(__file__).parent

class ProjectAnalyzer:
    def __init__(self):
        self.project_root = BASE_DIR
        self.analysis_results = {
            'templates': {},
            'urls': {},
            'views': {},
            'models': {},
            'static_files': {},
            'media_files': {},
            'settings': {},
            'requirements': {},
            'issues': []
        }
    
    def run_complete_analysis(self):
        """Exécute l'analyse complète du projet"""
        print("🔍 LANCEMENT DE L'ANALYSE COMPLÈTE DU PROJET...")
        print("=" * 60)
        
        self.analyze_templates()
        self.analyze_urls()
        self.analyze_views()
        self.analyze_models()
        self.analyze_static_files()
        self.analyze_media_files()
        self.analyze_settings()
        self.analyze_requirements()
        self.check_common_issues()
        
        self.generate_comprehensive_report()
    
    def analyze_templates(self):
        """Analyse tous les templates du projet"""
        print("\n📁 ANALYSE DES TEMPLATES...")
        
        templates_dir = self.project_root / 'templates'
        template_files = list(templates_dir.rglob('*.html'))
        
        self.analysis_results['templates']['total'] = len(template_files)
        self.analysis_results['templates']['by_folder'] = {}
        self.analysis_results['templates']['errors'] = []
        
        for template_file in template_files:
            relative_path = template_file.relative_to(templates_dir)
            folder = str(relative_path.parent)
            
            if folder not in self.analysis_results['templates']['by_folder']:
                self.analysis_results['templates']['by_folder'][folder] = 0
            self.analysis_results['templates']['by_folder'][folder] += 1
            
            # Analyse syntaxique
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                issues = self.analyze_template_content(content, str(relative_path))
                if issues:
                    self.analysis_results['templates']['errors'].append({
                        'file': str(relative_path),
                        'issues': issues
                    })
                    
            except Exception as e:
                self.analysis_results['templates']['errors'].append({
                    'file': str(relative_path),
                    'issues': [f'Erreur lecture: {e}']
                })
        
        print(f"✅ Templates analysés: {len(template_files)}")
    
    def analyze_template_content(self, content, template_path):
        """Analyse le contenu d'un template pour détecter les problèmes"""
        issues = []
        
        # Vérifier load static manquant
        static_patterns = [r"{% static '", r'{% static "']
        if any(re.search(pattern, content) for pattern in static_patterns):
            if '{% load static %}' not in content:
                issues.append("MISSING_STATIC_LOAD")
        
        # Vérifier les doubles accolades
        double_curly = re.findall(r'{{%.*?%}}', content)
        if double_curly:
            issues.append(f"DOUBLE_CURLY_BRACES: {len(double_curly)}")
        
        # Vérifier les URLs non résolues
        url_patterns = [
            r"href=\"/(\w+)/\"",
            r"href='/(\w+)/'",
            r"{% url '[^']*'[^%]*%}",
        ]
        
        for pattern in url_patterns:
            if re.search(pattern, content):
                # Vérifier si les URLs existent
                pass
        
        # Vérifier les balises fermantes manquantes
        if content.count('<div') > content.count('</div'):
            issues.append("DIVS_NON_FERMES")
        
        if content.count('<p') > content.count('</p'):
            issues.append("PARAGRAPHES_NON_FERMES")
        
        return issues
    
    def analyze_urls(self):
        """Analyse toutes les URLs du projet"""
        print("\n🔗 ANALYSE DES URLs...")
        
        try:
            resolver = get_resolver()
            url_patterns = self.extract_url_patterns(resolver)
            
            self.analysis_results['urls']['total'] = len(url_patterns)
            self.analysis_results['urls']['patterns'] = url_patterns
            self.analysis_results['urls']['by_app'] = {}
            
            for pattern in url_patterns:
                app_name = pattern.get('app_name', 'core')
                if app_name not in self.analysis_results['urls']['by_app']:
                    self.analysis_results['urls']['by_app'][app_name] = 0
                self.analysis_results['urls']['by_app'][app_name] += 1
            
            print(f"✅ URLs analysées: {len(url_patterns)}")
            
        except Exception as e:
            self.analysis_results['urls']['error'] = str(e)
            print(f"❌ Erreur analyse URLs: {e}")
    
    def extract_url_patterns(self, resolver, namespace=''):
        """Extrait récursivement tous les motifs d'URL"""
        patterns = []
        
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):
                # Include pattern
                if namespace:
                    new_namespace = f"{namespace}:{pattern.namespace}"
                else:
                    new_namespace = pattern.namespace
                patterns.extend(self.extract_url_patterns(pattern, new_namespace))
            else:
                # URL pattern
                try:
                    pattern_info = {
                        'pattern': str(pattern.pattern),
                        'name': getattr(pattern, 'name', ''),
                        'namespace': namespace,
                        'app_name': getattr(pattern, 'app_name', 'core')
                    }
                    patterns.append(pattern_info)
                except Exception as e:
                    patterns.append({
                        'error': str(e),
                        'namespace': namespace
                    })
        
        return patterns
    
    def analyze_views(self):
        """Analyse les vues du projet"""
        print("\n👁️ ANALYSE DES VUES...")
        
        views_dir = self.project_root
        view_files = list(views_dir.rglob('views.py'))
        
        self.analysis_results['views']['total_files'] = len(view_files)
        self.analysis_results['views']['views_count'] = 0
        self.analysis_results['views']['by_app'] = {}
        
        for view_file in view_files:
            app_name = view_file.parent.name
            try:
                with open(view_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Compter les fonctions et classes de vues
                function_views = len(re.findall(r'def (\w+)\(request', content))
                class_views = len(re.findall(r'class (\w+)\(.*View\)', content))
                total_views = function_views + class_views
                
                self.analysis_results['views']['views_count'] += total_views
                self.analysis_results['views']['by_app'][app_name] = total_views
                
            except Exception as e:
                print(f"❌ Erreur analyse vue {view_file}: {e}")
        
        print(f"✅ Vues analysées: {self.analysis_results['views']['views_count']}")
    
    def analyze_models(self):
        """Analyse les modèles du projet"""
        print("\n🗄️ ANALYSE DES MODÈLES...")
        
        models_dir = self.project_root
        model_files = list(models_dir.rglob('models.py'))
        
        self.analysis_results['models']['total_files'] = len(model_files)
        self.analysis_results['models']['models_count'] = 0
        self.analysis_results['models']['by_app'] = {}
        
        for model_file in model_files:
            app_name = model_file.parent.name
            try:
                with open(model_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Compter les modèles
                model_count = len(re.findall(r'class (\w+)\(models\.Model\)', content))
                self.analysis_results['models']['models_count'] += model_count
                self.analysis_results['models']['by_app'][app_name] = model_count
                
            except Exception as e:
                print(f"❌ Erreur analyse modèle {model_file}: {e}")
        
        print(f"✅ Modèles analysés: {self.analysis_results['models']['models_count']}")
    
    def analyze_static_files(self):
        """Analyse les fichiers statiques"""
        print("\n🎨 ANALYSE DES FICHIERS STATIQUES...")
        
        static_dir = self.project_root / 'static'
        if not static_dir.exists():
            self.analysis_results['static_files']['error'] = "Dossier static non trouvé"
            print("❌ Dossier static non trouvé")
            return
        
        static_files = list(static_dir.rglob('*'))
        
        self.analysis_results['static_files']['total'] = len(static_files)
        self.analysis_results['static_files']['by_type'] = {}
        
        for static_file in static_files:
            if static_file.is_file():
                extension = static_file.suffix.lower()
                if extension not in self.analysis_results['static_files']['by_type']:
                    self.analysis_results['static_files']['by_type'][extension] = 0
                self.analysis_results['static_files']['by_type'][extension] += 1
        
        print(f"✅ Fichiers statiques: {len(static_files)}")
    
    def analyze_media_files(self):
        """Analyse les fichiers media"""
        print("\n📸 ANALYSE DES FICHIERS MÉDIA...")
        
        media_dir = self.project_root / 'media'
        if not media_dir.exists():
            self.analysis_results['media_files']['info'] = "Dossier media non trouvé"
            print("ℹ️  Dossier media non trouvé")
            return
        
        media_files = list(media_dir.rglob('*'))
        self.analysis_results['media_files']['total'] = len(media_files)
        self.analysis_results['media_files']['by_type'] = {}
        
        for media_file in media_files:
            if media_file.is_file():
                extension = media_file.suffix.lower()
                if extension not in self.analysis_results['media_files']['by_type']:
                    self.analysis_results['media_files']['by_type'][extension] = 0
                self.analysis_results['media_files']['by_type'][extension] += 1
        
        print(f"✅ Fichiers média: {len(media_files)}")
    
    def analyze_settings(self):
        """Analyse la configuration du projet"""
        print("\n⚙️ ANALYSE DES PARAMÈTRES...")
        
        try:
            self.analysis_results['settings'] = {
                'debug': settings.DEBUG,
                'allowed_hosts': settings.ALLOWED_HOSTS,
                'installed_apps': len(settings.INSTALLED_APPS),
                'databases': settings.DATABASES['default']['ENGINE'],
                'static_url': settings.STATIC_URL,
                'media_url': settings.MEDIA_URL,
                'auth_user_model': getattr(settings, 'AUTH_USER_MODEL', 'Non défini')
            }
            print("✅ Paramètres analysés")
        except Exception as e:
            self.analysis_results['settings']['error'] = str(e)
            print(f"❌ Erreur analyse paramètres: {e}")
    
    def analyze_requirements(self):
        """Analyse le fichier requirements"""
        print("\n📦 ANALYSE DES DEPENDANCES...")
        
        req_files = [
            self.project_root / 'requirements.txt',
            self.project_root / 'requirements',
            self.project_root / 'pyproject.toml'
        ]
        
        for req_file in req_files:
            if req_file.exists():
                try:
                    if req_file.name == 'pyproject.toml':
                        # Analyse simplifiée de pyproject.toml
                        with open(req_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        dependencies = re.findall(r'(\w+)\s*=', content)
                        self.analysis_results['requirements']['file'] = 'pyproject.toml'
                        self.analysis_results['requirements']['dependencies'] = len(dependencies)
                    else:
                        with open(req_file, 'r', encoding='utf-8') as f:
                            dependencies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                        self.analysis_results['requirements']['file'] = req_file.name
                        self.analysis_results['requirements']['dependencies'] = len(dependencies)
                    
                    print(f"✅ Dépendances analysées: {self.analysis_results['requirements']['dependencies']}")
                    break
                    
                except Exception as e:
                    self.analysis_results['requirements']['error'] = str(e)
            else:
                self.analysis_results['requirements']['info'] = "Fichier requirements non trouvé"
    
    def check_common_issues(self):
        """Vérifie les problèmes courants"""
        print("\n🔧 VÉRIFICATION DES PROBLÈMES COURANTS...")
        
        issues = []
        
        # Vérifier les migrations en attente
        try:
            from django.core.management import call_command
            from io import StringIO
            out = StringIO()
            call_command('makemigrations', '--check', '--dry-run', stdout=out)
            if out.getvalue():
                issues.append("MIGRATIONS_EN_ATTENTE: Des migrations sont nécessaires")
        except Exception:
            pass
        
        # Vérifier les staticfiles
        if not (self.project_root / 'static').exists():
            issues.append("STATIC_DIR_MANQUANT: Dossier static non trouvé")
        
        # Vérifier les templates de base
        base_templates = ['base.html', 'includes/navbar.html', 'includes/footer.html']
        for template in base_templates:
            if not (self.project_root / 'templates' / template).exists():
                issues.append(f"TEMPLATE_BASE_MANQUANT: {template}")
        
        # Vérifier les URLs de messagerie
        messaging_urls = [
            'communication:messagerie_membre',
            'communication:messagerie_agent',
            'communication:messagerie_assureur',
            'communication:messagerie_medecin'
        ]
        
        for url_name in messaging_urls:
            try:
                from django.urls import reverse
                reverse(url_name)
            except Exception:
                issues.append(f"URL_MESSAGERIE_MANQUANTE: {url_name}")
        
        self.analysis_results['issues'] = issues
        print(f"✅ Vérifications terminées: {len(issues)} problème(s) détecté(s)")
    
    def generate_comprehensive_report(self):
        """Génère un rapport complet d'analyse"""
        print("\n" + "=" * 80)
        print("📊 RAPPORT COMPLET D'ANALYSE DU PROJET")
        print("=" * 80)
        
        # Résumé général
        print(f"\n🎯 RÉSUMÉ GÉNÉRAL:")
        print(f"   📁 Templates: {self.analysis_results['templates']['total']}")
        print(f"   🔗 URLs: {self.analysis_results['urls']['total']}")
        print(f"   👁️ Vues: {self.analysis_results['views']['views_count']}")
        print(f"   🗄️ Modèles: {self.analysis_results['models']['models_count']}")
        print(f"   🎨 Fichiers statiques: {self.analysis_results['static_files']['total']}")
        
        # Détails templates
        print(f"\n📁 TEMPLATES ({self.analysis_results['templates']['total']}):")
        for folder, count in sorted(self.analysis_results['templates']['by_folder'].items()):
            print(f"   📂 {folder}: {count} templates")
        
        if self.analysis_results['templates']['errors']:
            print(f"\n❌ ERREURS TEMPLATES ({len(self.analysis_results['templates']['errors'])}):")
            for error in self.analysis_results['templates']['errors'][:10]:  # Limiter l'affichage
                print(f"   📄 {error['file']}:")
                for issue in error['issues']:
                    print(f"      - {issue}")
        
        # URLs par app
        print(f"\n🔗 URLs PAR APPLICATION:")
        for app, count in self.analysis_results['urls']['by_app'].items():
            print(f"   📱 {app}: {count} URLs")
        
        # Vues et modèles
        print(f"\n👁️ VUES PAR APPLICATION:")
        for app, count in self.analysis_results['views']['by_app'].items():
            print(f"   🔧 {app}: {count} vues")
        
        print(f"\n🗄️ MODÈLES PAR APPLICATION:")
        for app, count in self.analysis_results['models']['by_app'].items():
            print(f"   🗃️ {app}: {count} modèles")
        
        # Fichiers statiques
        if 'by_type' in self.analysis_results['static_files']:
            print(f"\n🎨 FICHIERS STATIQUES:")
            for ext, count in self.analysis_results['static_files']['by_type'].items():
                print(f"   {ext or 'sans extension'}: {count}")
        
        # Paramètres
        print(f"\n⚙️ PARAMÈTRES:")
        for key, value in self.analysis_results['settings'].items():
            print(f"   {key}: {value}")
        
        # Dépendances
        if 'dependencies' in self.analysis_results['requirements']:
            print(f"\n📦 DÉPENDANCES: {self.analysis_results['requirements']['dependencies']} packages")
        
        # Problèmes détectés
        if self.analysis_results['issues']:
            print(f"\n🚨 PROBLÈMES DÉTECTÉS ({len(self.analysis_results['issues'])}):")
            for issue in self.analysis_results['issues']:
                print(f"   ❌ {issue}")
        else:
            print(f"\n✅ AUCUN PROBLÈME CRITIQUE DÉTECTÉ")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        if self.analysis_results['templates']['errors']:
            print("   1. Exécutez le correcteur de templates: python fix_template_errors.py --fix")
        if any("MIGRATIONS_EN_ATTENTE" in issue for issue in self.analysis_results['issues']):
            print("   2. Exécutez les migrations: python manage.py makemigrations && python manage.py migrate")
        if any("URL_MESSAGERIE_MANQUANTE" in issue for issue in self.analysis_results['issues']):
            print("   3. Vérifiez les URLs de messagerie dans urls.py")
        
        print(f"\n🎉 ANALYSE TERMINÉE!")
        
        # Sauvegarde du rapport
        self.save_report_to_file()
    
    def save_report_to_file(self):
        """Sauvegarde le rapport dans un fichier"""
        report_file = self.project_root / 'PROJECT_ANALYSIS_REPORT.md'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# RAPPORT D'ANALYSE DU PROJET\n\n")
            f.write("## 📊 RÉSUMÉ GÉNÉRAL\n\n")
            f.write(f"- **Templates**: {self.analysis_results['templates']['total']}\n")
            f.write(f"- **URLs**: {self.analysis_results['urls']['total']}\n")
            f.write(f"- **Vues**: {self.analysis_results['views']['views_count']}\n")
            f.write(f"- **Modèles**: {self.analysis_results['models']['models_count']}\n")
            f.write(f"- **Fichiers statiques**: {self.analysis_results['static_files']['total']}\n\n")
            
            if self.analysis_results['issues']:
                f.write("## 🚨 PROBLÈMES DÉTECTÉS\n\n")
                for issue in self.analysis_results['issues']:
                    f.write(f"- {issue}\n")
            
            f.write("\n## 📁 STRUCTURE DES TEMPLATES\n\n")
            for folder, count in sorted(self.analysis_results['templates']['by_folder'].items()):
                f.write(f"- `{folder}`: {count} templates\n")
        
        print(f"📄 Rapport sauvegardé: {report_file}")

def main():
    analyzer = ProjectAnalyzer()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()