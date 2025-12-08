#!/usr/bin/env python3
"""
Script d'analyse complète de l'application medecin - CORRIGÉ
Vérifie les modèles, vues, URLs, templates et configuration
"""

import os
import django
import sys
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.db import connection
from io import StringIO
import importlib

class MedecinAnalyzer:
    def __init__(self):
        self.problems = []
        self.warnings = []
        self.successes = []
    
    def analyze_medecin_app(self):
        """Analyse complète de l'application medecin"""
        print("🔍 ANALYSE COMPLÈTE DE L'APPLICATION MEDECIN")
        print("=" * 70)
        
        self.check_app_config()
        self.analyze_models()
        self.analyze_views()
        self.analyze_urls()
        self.analyze_templates()
        self.analyze_static_files()
        self.check_database()
        self.generate_report()
    
    def check_app_config(self):
        """Vérifie la configuration de l'application"""
        print("\n📦 CONFIGURATION DE L'APPLICATION")
        print("-" * 40)
        
        # Vérifier si l'app est dans INSTALLED_APPS
        if 'medecin' in settings.INSTALLED_APPS:
            self.successes.append("✅ Application 'medecin' dans INSTALLED_APPS")
            print("   ✅ Application 'medecin' dans INSTALLED_APPS")
        else:
            self.problems.append("❌ Application 'medecin' manquante dans INSTALLED_APPS")
            print("   ❌ Application 'medecin' manquante dans INSTALLED_APPS")
        
        # Vérifier la structure des dossiers
        app_path = BASE_DIR / 'medecin'
        required_dirs = ['migrations', 'templates', 'static']
        
        for dir_name in required_dirs:
            dir_path = app_path / dir_name
            if dir_path.exists():
                self.successes.append(f"✅ Dossier {dir_name} existe")
                print(f"   ✅ Dossier {dir_name} existe")
            else:
                self.warnings.append(f"⚠️  Dossier {dir_name} manquant")
                print(f"   ⚠️  Dossier {dir_name} manquant")
    
    def analyze_models(self):
        """Analyse les modèles de l'application medecin"""
        print("\n🗃️  MODÈLES")
        print("-" * 40)
        
        try:
            app_config = apps.get_app_config('medecin')
            models = list(app_config.get_models())  # CORRECTION: Convertir en liste
            
            if models:
                model_count = len(models)
                self.successes.append(f"✅ {model_count} modèle(s) trouvé(s)")
                print(f"   ✅ {model_count} modèle(s) trouvé(s)")
                
                for model in models:
                    print(f"   📋 {model._meta.model_name}:")
                    print(f"      - Table: {model._meta.db_table}")
                    print(f"      - Champs: {len(model._meta.fields)}")
                    
                    # Compter les objets
                    try:
                        count = model.objects.count()
                        print(f"      - Enregistrements: {count}")
                        
                        # Vérifier les champs importants
                        fields = [f.name for f in model._meta.fields]
                        if 'user' in fields:
                            print(f"      - Relation User: ✅")
                        
                        if count == 0:
                            self.warnings.append(f"⚠️  Modèle {model._meta.model_name} est vide")
                            
                    except Exception as e:
                        print(f"      - ❌ Erreur comptage: {e}")
                        
            else:
                self.problems.append("❌ Aucun modèle trouvé dans l'application medecin")
                print("   ❌ Aucun modèle trouvé dans l'application medecin")
                
        except LookupError:
            self.problems.append("❌ Application medecin non trouvée")
            print("   ❌ Application medecin non trouvée")
    
    def analyze_views(self):
        """Analyse les vues de l'application medecin"""
        print("\n👁️  VUES")
        print("-" * 40)
        
        try:
            # Essayer d'importer le module views
            views_module = importlib.import_module('medecin.views')
            view_functions = [attr for attr in dir(views_module) 
                            if not attr.startswith('_') and callable(getattr(views_module, attr))]
            
            if view_functions:
                self.successes.append(f"✅ {len(view_functions)} vue(s) trouvée(s)")
                print(f"   ✅ {len(view_functions)} vue(s) trouvée(s)")
                print(f"   Vues disponibles: {', '.join(view_functions[:10])}")
                
                # Vérifier les vues importantes
                important_views = ['dashboard', 'mes_ordonnances', 'creer_ordonnance']
                for view in important_views:
                    if view in view_functions:
                        self.successes.append(f"✅ Vue '{view}' trouvée")
                        print(f"   ✅ Vue '{view}' trouvée")
                    else:
                        self.warnings.append(f"⚠️  Vue '{view}' manquante")
                        print(f"   ⚠️  Vue '{view}' manquante")
            else:
                self.problems.append("❌ Aucune vue trouvée")
                print("   ❌ Aucune vue trouvée")
                
        except ImportError as e:
            self.problems.append(f"❌ Impossible d'importer medecin.views: {e}")
            print(f"   ❌ Impossible d'importer medecin.views: {e}")
    
    def analyze_urls(self):
        """Analyse les URLs de l'application medecin"""
        print("\n🌐 URLs")
        print("-" * 40)
        
        try:
            urls_module = importlib.import_module('medecin.urls')
            
            if hasattr(urls_module, 'urlpatterns'):
                url_count = len(urls_module.urlpatterns)
                self.successes.append(f"✅ {url_count} pattern(s) URL trouvé(s)")
                print(f"   ✅ {url_count} pattern(s) URL trouvé(s)")
                
                # Lister les URLs
                for pattern in urls_module.urlpatterns:
                    if hasattr(pattern, 'pattern'):
                        print(f"   📍 {pattern.pattern} -> {pattern.name}")
            else:
                self.problems.append("❌ Aucun urlpatterns trouvé")
                print("   ❌ Aucun urlpatterns trouvé")
                
        except ImportError:
            self.problems.append("❌ Fichier medecin/urls.py manquant ou invalide")
            print("   ❌ Fichier medecin/urls.py manquant ou invalide")
    
    def analyze_templates(self):
        """Analyse les templates de l'application medecin"""
        print("\n📄 TEMPLATES")
        print("-" * 40)
        
        template_dirs = [
            BASE_DIR / 'templates' / 'medecin',
            BASE_DIR / 'medecin' / 'templates' / 'medecin'
        ]
        
        templates_found = []
        for template_dir in template_dirs:
            if template_dir.exists():
                html_files = list(template_dir.glob('*.html'))
                templates_found.extend(html_files)
        
        if templates_found:
            self.successes.append(f"✅ {len(templates_found)} template(s) trouvé(s)")
            print(f"   ✅ {len(templates_found)} template(s) trouvé(s)")
            
            # Templates importants à vérifier
            important_templates = [
                'dashboard.html', 'base_medecin.html', 'mes_ordonnances.html',
                'creer_ordonnance.html', 'liste_ordonnances.html'
            ]
            
            for template in important_templates:
                template_paths = [BASE_DIR / 'templates' / 'medecin' / template,
                                BASE_DIR / 'medecin' / 'templates' / 'medecin' / template]
                
                found = any(path.exists() for path in template_paths)
                if found:
                    self.successes.append(f"✅ Template '{template}' trouvé")
                    print(f"   ✅ Template '{template}' trouvé")
                else:
                    self.warnings.append(f"⚠️  Template '{template}' manquant")
                    print(f"   ⚠️  Template '{template}' manquant")
        else:
            self.problems.append("❌ Aucun template trouvé")
            print("   ❌ Aucun template trouvé")
    
    def analyze_static_files(self):
        """Analyse les fichiers statiques de l'application medecin"""
        print("\n🎨 FICHIERS STATIQUES")
        print("-" * 40)
        
        static_dirs = [
            BASE_DIR / 'static' / 'medecin',
            BASE_DIR / 'medecin' / 'static' / 'medecin'
        ]
        
        static_files = []
        for static_dir in static_dirs:
            if static_dir.exists():
                css_files = list(static_dir.glob('**/*.css'))
                js_files = list(static_dir.glob('**/*.js'))
                static_files.extend(css_files + js_files)
        
        if static_files:
            self.successes.append(f"✅ {len(static_files)} fichier(s) statique(s) trouvé(s)")
            print(f"   ✅ {len(static_files)} fichier(s) statique(s) trouvé(s)")
        else:
            self.warnings.append("⚠️  Aucun fichier statique trouvé")
            print("   ⚠️  Aucun fichier statique trouvé")
    
    def check_database(self):
        """Vérifie l'état de la base de données pour medecin"""
        print("\n🗄️  BASE DE DONNÉES")
        print("-" * 40)
        
        try:
            # Vérifier les migrations
            output = StringIO()
            call_command('showmigrations', 'medecin', stdout=output)
            migrations_output = output.getvalue()
            
            if 'medecin' in migrations_output:
                lines = [line for line in migrations_output.split('\n') if 'medecin' in line]
                applied = [line for line in lines if '[X]' in line]
                pending = [line for line in lines if '[ ]' in line]
                
                print(f"   📋 Migrations appliquées: {len(applied)}")
                print(f"   📋 Migrations en attente: {len(pending)}")
                
                if pending:
                    self.warnings.append(f"⚠️  {len(pending)} migration(s) en attente")
                else:
                    self.successes.append("✅ Toutes les migrations sont appliquées")
            else:
                self.problems.append("❌ Aucune migration trouvée pour medecin")
                print("   ❌ Aucune migration trouvée pour medecin")
                
        except Exception as e:
            self.problems.append(f"❌ Erreur vérification migrations: {e}")
            print(f"   ❌ Erreur vérification migrations: {e}")
    
    def generate_report(self):
        """Génère un rapport complet"""
        print("\n📊 RAPPORT D'ANALYSE")
        print("=" * 70)
        
        print(f"✅ SUCCÈS ({len(self.successes)}):")
        for success in self.successes:
            print(f"   {success}")
        
        if self.warnings:
            print(f"\n⚠️  AVERTISSEMENTS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")
        
        if self.problems:
            print(f"\n❌ PROBLÈMES ({len(self.problems)}):")
            for problem in self.problems:
                print(f"   {problem}")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        if self.problems:
            print("   1. Résolvez les problèmes critiques listés ci-dessus")
        if self.warnings:
            print("   2. Traitez les avertissements pour améliorer l'application")
        
        print("   3. Vérifiez les URLs: http://127.0.0.1:8000/medecin/")
        print("   4. Testez le dashboard médecin")
        print("   5. Vérifiez la création d'ordonnances")

def check_medecin_dependencies():
    """Vérifie les dépendances et relations avec autres apps"""
    print("\n🔗 DÉPENDANCES ET RELATIONS")
    print("-" * 40)
    
    # Vérifier les relations avec User
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Vérifier si le modèle Medecin a une relation avec User
        try:
            Medecin = apps.get_model('medecin', 'Medecin')
            for field in Medecin._meta.get_fields():
                if hasattr(field, 'related_model') and field.related_model == User:
                    print(f"   ✅ Relation avec User trouvée: {field.name}")
                    break
            else:
                print("   ⚠️  Aucune relation directe avec User trouvée")
        except LookupError:
            print("   ❌ Modèle Medecin non trouvé")
            
    except Exception as e:
        print(f"   ❌ Erreur vérification dépendances: {e}")

def main():
    print("🩺 ANALYSEUR DE L'APPLICATION MEDECIN - CORRIGÉ")
    print("=" * 70)
    
    analyzer = MedecinAnalyzer()
    analyzer.analyze_medecin_app()
    check_medecin_dependencies()
    
    print(f"\n🎯 SYNTHÈSE FINALE:")
    if analyzer.problems:
        print("❌ L'application medecin a des problèmes critiques")
    elif analyzer.warnings:
        print("⚠️  L'application medecin a des avertissements à traiter")
    else:
        print("✅ L'application medecin semble correctement configurée")

if __name__ == "__main__":
    main()