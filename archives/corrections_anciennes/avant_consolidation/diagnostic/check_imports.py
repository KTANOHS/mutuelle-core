#!/usr/bin/env python
"""
SCRIPT D'ANALYSE COMPLÈTE POUR DÉTECTER LES ERREURS D'IMPORT
Exécutez: python check_imports.py
"""

import os
import sys
import django
import importlib
import inspect
from pathlib import Path
from django.apps import apps
from django.conf import settings

# Ajouter le répertoire du projet au path Python
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_django():
    """Configurer l'environnement Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()

def check_settings():
    """Vérifier la configuration des settings"""
    print("=" * 80)
    print("🔧 ANALYSE DE LA CONFIGURATION DJANGO")
    print("=" * 80)
    
    issues = []
    
    # Vérifier les apps installées
    print("\n📋 APPLICATIONS INSTALLÉES:")
    for app in settings.INSTALLED_APPS:
        print(f"  ✅ {app}")
        
        # Vérifier si l'app existe
        try:
            importlib.import_module(app)
        except ImportError as e:
            issues.append(f"❌ App '{app}' - ImportError: {e}")
            print(f"  ❌ {app} - ERREUR: {e}")
    
    # Vérifier les templates
    print(f"\n📁 TEMPLATES DIRS: {settings.TEMPLATES[0]['DIRS']}")
    
    # Vérifier les static files
    print(f"📁 STATIC DIRS: {settings.STATICFILES_DIRS}")
    
    return issues

def check_models():
    """Vérifier tous les modèles"""
    print("\n" + "=" * 80)
    print("🗄️  ANALYSE DES MODÈLES")
    print("=" * 80)
    
    issues = []
    
    for app_config in apps.get_app_configs():
        print(f"\n📦 Application: {app_config.name}")
        
        try:
            models = app_config.get_models()
            for model in models:
                print(f"  ✅ Modèle: {model.__name__}")
                
                # Vérifier les champs du modèle
                try:
                    fields = [f.name for f in model._meta.get_fields()]
                    print(f"    Champs: {', '.join(fields[:5])}{'...' if len(fields) > 5 else ''}")
                except Exception as e:
                    issues.append(f"❌ Erreur champs {model.__name__}: {e}")
                    
        except Exception as e:
            issues.append(f"❌ Erreur app {app_config.name}: {e}")
            print(f"  ❌ ERREUR: {e}")
    
    return issues

def check_admin_registrations():
    """Vérifier les enregistrements admin"""
    print("\n" + "=" * 80)
    print("👨‍💼 ANALYSE DES ENREGISTREMENTS ADMIN")
    print("=" * 80)
    
    issues = []
    
    # Vérifier chaque fichier admin.py
    admin_files = [
        'scoring.admin',
        'ia_detection.admin', 
        'relances.admin',
        'dashboard.admin'
    ]
    
    for admin_module in admin_files:
        try:
            module = importlib.import_module(admin_module)
            print(f"✅ {admin_module} chargé avec succès")
            
            # Vérifier les classes admin dans le module
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if name.endswith('Admin') and hasattr(obj, 'model'):
                    print(f"  🎯 Admin: {name} -> {obj.model.__name__}")
                    
        except ImportError as e:
            if "No module named" not in str(e):
                issues.append(f"❌ {admin_module}: {e}")
                print(f"❌ {admin_module}: {e}")
            else:
                print(f"⚠️  {admin_module}: non trouvé (normal si pas encore créé)")
    
    return issues

def check_views():
    """Vérifier les vues"""
    print("\n" + "=" * 80)
    print("🌐 ANALYSE DES VUES")
    print("=" * 80)
    
    issues = []
    
    # Vérifier les vues principales
    view_modules = [
        'scoring.views',
        'ia_detection.views',
        'relances.views',
        'dashboard.views'
    ]
    
    for view_module in view_modules:
        try:
            module = importlib.import_module(view_module)
            print(f"✅ {view_module} chargé avec succès")
            
            # Compter les vues dans le module
            view_count = sum(1 for name, obj in inspect.getmembers(module) 
                           if inspect.isfunction(obj) and hasattr(obj, '__module__'))
            print(f"  📊 {view_count} vues/fonctions trouvées")
            
        except ImportError as e:
            if "No module named" not in str(e):
                issues.append(f"❌ {view_module}: {e}")
                print(f"❌ {view_module}: {e}")
            else:
                print(f"⚠️  {view_module}: non trouvé")
    
    return issues

def check_urls():
    """Vérifier les configurations URLs"""
    print("\n" + "=" * 80)
    print("🔗 ANALYSE DES URLS")
    print("=" * 80)
    
    issues = []
    
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        url_patterns = resolver.url_patterns
        
        print("✅ URLs principales chargées")
        print(f"📊 Nombre de patterns racine: {len(url_patterns)}")
        
        # Vérifier les URLs incluses
        for pattern in url_patterns:
            if hasattr(pattern, 'urlconf_module'):
                print(f"  📁 Inclus: {pattern.urlconf_module}")
                
    except Exception as e:
        issues.append(f"❌ Erreur URLs: {e}")
        print(f"❌ Erreur URLs: {e}")
    
    return issues

def check_double_admin_registration():
    """Vérifier spécifiquement les doubles enregistrements admin"""
    print("\n" + "=" * 80)
    print("🔍 RECHERCHE DE DOUBLES ENREGISTREMENTS ADMIN")
    print("=" * 80)
    
    issues = []
    
    try:
        from django.contrib import admin
        from django.contrib.admin.sites import site
        
        # Obtenir tous les modèles enregistrés
        registered_models = site._registry.keys()
        model_registrations = {}
        
        print("📋 Modèles actuellement enregistrés dans l'admin:")
        for model in registered_models:
            app_label = model._meta.app_label
            model_name = model.__name__
            key = f"{app_label}.{model_name}"
            
            if key in model_registrations:
                issues.append(f"❌ DOUBLE ENREGISTREMENT: {key}")
                print(f"  ❌ DOUBLE: {key}")
            else:
                model_registrations[key] = model
                print(f"  ✅ {key}")
        
        # Vérifier spécifiquement les modèles problématiques
        problematic_models = ['ModeleIA', 'AnalyseIA', 'RegleScoring']
        for model_name in problematic_models:
            count = sum(1 for model in registered_models if model.__name__ == model_name)
            if count > 1:
                issues.append(f"❌ {model_name} enregistré {count} fois!")
                print(f"  🚨 ALERTE: {model_name} enregistré {count} fois!")
                
    except Exception as e:
        issues.append(f"❌ Erreur vérification admin: {e}")
    
    return issues

def check_database():
    """Vérifier la connexion base de données"""
    print("\n" + "=" * 80)
    print("🗃️  ANALYSE BASE DE DONNÉES")
    print("=" * 80)
    
    issues = []
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Connexion BD fonctionnelle")
            
        # Vérifier les migrations en attente
        from django.core.management import call_command
        from io import StringIO
        out = StringIO()
        call_command('showmigrations', '--list', stdout=out)
        migrations_output = out.getvalue()
        
        print("📋 État des migrations:")
        for line in migrations_output.split('\n'):
            if line.strip():
                print(f"  {line}")
                
    except Exception as e:
        issues.append(f"❌ Erreur BD: {e}")
        print(f"❌ Erreur BD: {e}")
    
    return issues

def generate_fix_recommendations(issues):
    """Générer des recommandations de correction"""
    print("\n" + "=" * 80)
    print("🔧 RECOMMANDATIONS DE CORRECTION")
    print("=" * 80)
    
    if not issues:
        print("✅ Aucun problème détecté! Votre configuration semble correcte.")
        return
    
    print(f"📊 {len(issues)} problèmes détectés:")
    
    recommendations = []
    
    for issue in issues:
        print(f"\n❌ Problème: {issue}")
        
        if "double enregistrement" in issue.lower() or "enregistré plusieurs fois" in issue.lower():
            if "ModeleIA" in issue:
                print("  💡 Solution: Supprimez l'enregistrement de ModeleIA de scoring/admin.py")
                print("  📝 Code:")
                print("     # Dans scoring/admin.py - COMMENTEZ OU SUPPRIMEZ:")
                print("     # @admin.register(ModeleIA)")
                print("     # class ModeleIAAdmin(admin.ModelAdmin):")
                print("     #     ...")
                
        elif "ImportError" in issue:
            app_name = issue.split("'")[1] if "'" in issue else "inconnu"
            print(f"  💡 Solution: Vérifiez que l'application '{app_name}' existe")
            print(f"  📝 Commande: python manage.py startapp {app_name.split('.')[-1]}")
            
        elif "admin" in issue.lower():
            print("  💡 Solution: Vérifiez les fichiers admin.py pour les doublons")
            print("  📝 Commande: grep -r '@admin.register' . --include='*.py'")
    
    return recommendations

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DE L'ANALYSE COMPLÈTE DU PROJET")
    print("⏳ Cette analyse peut prendre quelques secondes...\n")
    
    try:
        # Configuration Django
        setup_django()
        
        # Exécuter toutes les vérifications
        all_issues = []
        
        all_issues.extend(check_settings())
        all_issues.extend(check_models())
        all_issues.extend(check_admin_registrations())
        all_issues.extend(check_views())
        all_issues.extend(check_urls())
        all_issues.extend(check_double_admin_registration())
        all_issues.extend(check_database())
        
        # Générer les recommandations
        generate_fix_recommendations(all_issues)
        
        # Résumé final
        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ DE L'ANALYSE")
        print("=" * 80)
        print(f"✅ Vérifications terminées")
        print(f"❌ Problèmes détectés: {len(all_issues)}")
        
        if all_issues:
            print(f"\n🔧 Pour résoudre le problème principal (double enregistrement admin):")
            print("1. Ouvrez scoring/admin.py")
            print("2. Commentez ou supprimez les enregistrements de ModeleIA et AnalyseIA")
            print("3. Redémarrez: python manage.py runserver")
            
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE: {e}")
        print("Assurez-vous d'exécuter ce script depuis le répertoire racine de votre projet Django")
        return 1
    
    return 0 if not all_issues else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)