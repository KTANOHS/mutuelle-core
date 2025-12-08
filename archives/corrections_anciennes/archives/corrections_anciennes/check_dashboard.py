#!/usr/bin/env python
"""
Script de vérification automatique pour les problèmes Django Dashboard
"""

import os
import sys
import django
from pathlib import Path
import importlib.util

def setup_django():
    """Configurer l'environnement Django"""
    try:
        # Trouver le fichier settings.py
        project_dir = Path.cwd()
        settings_path = None
        
        for path in project_dir.rglob('settings.py'):
            if 'env' not in str(path) and 'venv' not in str(path):
                settings_path = path
                break
        
        if not settings_path:
            print("❌ Fichier settings.py non trouvé")
            return False
        
        # Ajouter le répertoire parent au path Python
        project_root = settings_path.parent.parent
        sys.path.append(str(project_root))
        
        # Définir le module settings
        settings_module = f"{settings_path.parent.name}.settings"
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
        
        django.setup()
        return True
        
    except Exception as e:
        print(f"❌ Erreur configuration Django: {e}")
        return False

def check_project_structure():
    """Vérifier la structure du projet"""
    print("\n" + "="*50)
    print("VÉRIFICATION DE LA STRUCTURE DU PROJET")
    print("="*50)
    
    structure_ok = True
    required_files = [
        'manage.py',
        'requirements.txt',
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} trouvé")
        else:
            print(f"❌ {file} manquant")
            structure_ok = False
    
    return structure_ok

def check_app_structure():
    """Vérifier la structure de l'application dashboard"""
    print("\n" + "="*50)
    print("VÉRIFICATION DE L'APPLICATION DASHBOARD")
    print("="*50)
    
    app_ok = True
    dashboard_path = Path('dashboard')
    
    if dashboard_path.exists():
        print("✅ Dossier dashboard trouvé")
        
        required_app_files = [
            '__init__.py',
            'views.py',
            'urls.py',
            'apps.py',
        ]
        
        for file in required_app_files:
            file_path = dashboard_path / file
            if file_path.exists():
                print(f"✅ {file_path} trouvé")
            else:
                print(f"❌ {file_path} manquant")
                app_ok = False
        
        # Vérifier les templates
        templates_path = dashboard_path / 'templates' / 'dashboard'
        if templates_path.exists():
            print(f"✅ Templates trouvés: {templates_path}")
        else:
            print(f"⚠️  Dossier templates manquant: {templates_path}")
            
    else:
        print("❌ Dossier 'dashboard' non trouvé")
        app_ok = False
    
    return app_ok

def check_settings():
    """Vérifier la configuration Django"""
    print("\n" + "="*50)
    print("VÉRIFICATION DES SETTINGS DJANGO")
    print("="*50)
    
    from django.conf import settings
    
    settings_ok = True
    
    # Vérifier l'app dashboard dans INSTALLED_APPS
    if 'dashboard' in settings.INSTALLED_APPS:
        print("✅ 'dashboard' dans INSTALLED_APPS")
    else:
        print("❌ 'dashboard' PAS dans INSTALLED_APPS")
        settings_ok = False
    
    # Vérifier TEMPLATES configuration
    templates_dirs = [str(dir) for dir in settings.TEMPLATES[0]['DIRS']]
    has_templates = any('templates' in dir for dir in templates_dirs)
    if has_templates:
        print("✅ Configuration TEMPLATES OK")
    else:
        print("⚠️  Vérifiez la configuration TEMPLATES")
    
    return settings_ok

def check_urls():
    """Vérifier la configuration des URLs"""
    print("\n" + "="*50)
    print("VÉRIFICATION DES URLS")
    print("="*50)
    
    from django.urls import get_resolver
    from django.core.handlers.wsgi import WSGIHandler
    
    urls_ok = True
    
    try:
        # Obtenir le résolveur d'URLs
        resolver = get_resolver()
        
        # Vérifier les URLs enregistrées
        url_patterns = []
        
        def extract_urls(urls, prefix=''):
            for pattern in urls:
                if hasattr(pattern, 'url_patterns'):
                    # C'est un include
                    new_prefix = f"{prefix}{pattern.pattern}"
                    extract_urls(pattern.url_patterns, new_prefix)
                else:
                    url_patterns.append(f"{prefix}{pattern.pattern}")
        
        extract_urls(resolver.url_patterns)
        
        print("URLs configurées:")
        for url in sorted(url_patterns):
            print(f"  - {url}")
        
        # Vérifier spécifiquement les URLs dashboard
        dashboard_urls = [url for url in url_patterns if 'dashboard' in url]
        if dashboard_urls:
            print("✅ URLs dashboard trouvées:")
            for url in dashboard_urls:
                print(f"  - {url}")
        else:
            print("❌ Aucune URL dashboard trouvée")
            urls_ok = False
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des URLs: {e}")
        urls_ok = False
    
    return urls_ok

def check_views():
    """Vérifier les vues"""
    print("\n" + "="*50)
    print("VÉRIFICATION DES VUES")
    print("="*50)
    
    views_ok = True
    
    try:
        # Essayer d'importer les vues dashboard
        from dashboard import views
        
        # Vérifier les fonctions de vue
        view_functions = [func for func in dir(views) 
                         if not func.startswith('_') and callable(getattr(views, func))]
        
        if view_functions:
            print("✅ Fonctions de vue trouvées:")
            for func in view_functions:
                print(f"  - {func}")
        else:
            print("❌ Aucune fonction de vue trouvée")
            views_ok = False
            
    except ImportError as e:
        print(f"❌ Impossible d'importer les vues dashboard: {e}")
        views_ok = False
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des vues: {e}")
        views_ok = False
    
    return views_ok

def check_migrations():
    """Vérifier l'état des migrations"""
    print("\n" + "="*50)
    print("VÉRIFICATION DES MIGRATIONS")
    print("="*50)
    
    from django.core.management import execute_from_command_line
    from django.db import connection
    
    migrations_ok = True
    
    try:
        # Vérifier les migrations en attente
        print("Vérification des migrations...")
        os.system('python manage.py makemigrations --check --dry-run')
        
        # Vérifier si les migrations sont appliquées
        print("\nStatut des migrations:")
        os.system('python manage.py showmigrations')
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des migrations: {e}")
        migrations_ok = False
    
    return migrations_ok

def generate_fix_suggestions():
    """Générer des suggestions de correction"""
    print("\n" + "="*50)
    print("SUGGESTIONS DE CORRECTION")
    print("="*50)
    
    suggestions = []
    
    # Vérifier si le fichier urls.py de dashboard existe
    if not Path('dashboard/urls.py').exists():
        suggestions.append("""
📝 CRÉER dashboard/urls.py:

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('agents/', views.agents_dashboard, name='agents_dashboard'),
    path('', views.dashboard_index, name='index'),
]
""")
    
    # Vérifier si la vue existe
    try:
        from dashboard import views
        if not hasattr(views, 'agents_dashboard'):
            suggestions.append("""
📝 AJOUTER dans dashboard/views.py:

from django.shortcuts import render

def agents_dashboard(request):
    return render(request, 'dashboard/agents.html')

def dashboard_index(request):
    return render(request, 'dashboard/index.html')
""")
    except ImportError:
        pass
    
    # Vérifier l'URL principale
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        urls_found = False
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):
                for subpattern in pattern.url_patterns:
                    if 'dashboard' in str(subpattern.pattern):
                        urls_found = True
                        break
        if not urls_found:
            suggestions.append("""
📝 AJOUTER dans le urls.py principal:

from django.urls import path, include

urlpatterns = [
    # ... autres URLs
    path('dashboard/', include('dashboard.urls')),
]
""")
    except:
        pass
    
    if suggestions:
        for suggestion in suggestions:
            print(suggestion)
    else:
        print("✅ Aucune correction majeure nécessaire")

def main():
    """Fonction principale"""
    print("🔍 DIAGNOSTIC DASHBOARD DJANGO")
    print("="*50)
    
    # Vérifier si nous sommes dans un projet Django
    if not Path('manage.py').exists():
        print("❌ Ce script doit être exécuté dans la racine d'un projet Django")
        sys.exit(1)
    
    # Configurer Django
    if not setup_django():
        print("❌ Impossible de configurer Django")
        sys.exit(1)
    
    # Exécuter toutes les vérifications
    checks = [
        check_project_structure,
        check_app_structure,
        check_settings,
        check_urls,
        check_views,
        check_migrations,
    ]
    
    all_ok = True
    for check in checks:
        if not check():
            all_ok = False
    
    # Générer les suggestions
    generate_fix_suggestions()
    
    # Résumé final
    print("\n" + "="*50)
    print("RÉSUMÉ DU DIAGNOSTIC")
    print("="*50)
    
    if all_ok:
        print("✅ Toutes les vérifications sont passées!")
        print("\n🔧 Prochaines étapes:")
        print("1. Redémarrer le serveur: python manage.py runserver")
        print("2. Visiter: http://127.0.0.1:8000/dashboard/agents/")
    else:
        print("❌ Certaines vérifications ont échoué")
        print("\n🔧 Appliquez les suggestions ci-dessus et relancez ce script")
    
    print("\n📋 Commandes utiles:")
    print("python manage.py runserver")
    print("python manage.py makemigrations")
    print("python manage.py migrate")

if __name__ == "__main__":
    main()