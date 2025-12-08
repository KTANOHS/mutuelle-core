#!/usr/bin/env python3
"""
Script de diagnostic complet pour l'application assureur
Analyse la structure, les modèles, les vues, les URLs et les templates
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    DJANGO_LOADED = True
except Exception as e:
    print(f"⚠️  Django non chargé: {e}")
    DJANGO_LOADED = False

BASE_DIR = Path(__file__).resolve().parent.parent

def analyse_structure_assureur():
    """Analyse la structure de l'application assureur"""
    print("\n" + "="*80)
    print("DIAGNOSTIC ASSUREUR - ANALYSE STRUCTURELLE")
    print("="*80)
    
    assureur_dir = BASE_DIR / "assureur"
    templates_assureur_dir = BASE_DIR / "templates" / "assureur"
    apps_assureur_dir = BASE_DIR / "apps" / "assureur"
    
    print(f"\n📁 Répertoire assureur principal: {assureur_dir}")
    print(f"📁 Templates assureur: {templates_assureur_dir}")
    print(f"📁 Apps assureur: {apps_assureur_dir}")
    
    # Vérifier l'existence des répertoires
    for nom, chemin in [
        ("assureur", assureur_dir),
        ("templates/assureur", templates_assureur_dir),
        ("apps/assureur", apps_assureur_dir)
    ]:
        if chemin.exists():
            print(f"✅ {nom}: EXISTE")
            # Lister les fichiers
            fichiers = list(chemin.rglob("*"))
            print(f"   {len(fichiers)} éléments trouvés")
            for f in fichiers:
                if f.is_file():
                    rel_path = f.relative_to(chemin)
                    print(f"   - {rel_path}")
        else:
            print(f"❌ {nom}: MANQUANT")

def analyse_models_assureur():
    """Analyse les modèles de l'assureur"""
    print("\n" + "="*80)
    print("DIAGNOSTIC ASSUREUR - ANALYSE DES MODÈLES")
    print("="*80)
    
    if not DJANGO_LOADED:
        print("❌ Django non chargé - impossible d'analyser les modèles")
        return
    
    try:
        from django.apps import apps
        from django.db import models
        
        # Chercher tous les modèles liés à l'assureur
        print("\n🔍 Recherche des modèles assureur...")
        
        model_count = 0
        for app in apps.get_app_configs():
            for model in app.get_models():
                model_name = model.__name__
                app_label = model._meta.app_label
                
                # Vérifier si c'est un modèle lié à l'assureur
                if 'assureur' in app_label.lower() or 'assureur' in model_name.lower():
                    model_count += 1
                    print(f"\n📊 Modèle: {model_name}")
                    print(f"   App: {app_label}")
                    print(f"   Table: {model._meta.db_table}")
                    
                    # Afficher les champs
                    print("   Champs:")
                    for field in model._meta.fields:
                        print(f"   - {field.name}: {field.get_internal_type()}")
                    
                    # Vérifier les relations
                    relations = []
                    for field in model._meta.fields:
                        if field.is_relation:
                            relations.append(f"{field.name} -> {field.related_model.__name__}")
                    
                    if relations:
                        print("   Relations:")
                        for rel in relations:
                            print(f"   - {rel}")
        
        if model_count == 0:
            print("⚠️  Aucun modèle spécifique à l'assureur trouvé")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse des modèles: {e}")

def analyse_vues_assureur():
    """Analyse les vues de l'assureur"""
    print("\n" + "="*80)
    print("DIAGNOSTIC ASSUREUR - ANALYSE DES VUES")
    print("="*80)
    
    # Chercher les fichiers views.py dans les dossiers assureur
    views_files = []
    
    for root, dirs, files in os.walk(BASE_DIR):
        if 'assureur' in root and 'views.py' in files:
            views_files.append(Path(root) / 'views.py')
    
    print(f"\n🔍 {len(views_files)} fichier(s) views.py trouvé(s):")
    
    for vf in views_files:
        print(f"\n📄 {vf.relative_to(BASE_DIR)}")
        
        try:
            with open(vf, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Compter les fonctions et classes de vue
            import re
            
            # Rechercher les fonctions de vue
            func_pattern = r'def (\w+)\s*\(.*?\).*?:'
            functions = re.findall(func_pattern, content, re.DOTALL)
            
            # Rechercher les classes de vue
            class_pattern = r'class (\w+)\(.*?View.*?\):'
            classes = re.findall(class_pattern, content, re.DOTALL)
            
            print(f"   Fonctions: {len(functions)}")
            for func in functions:
                print(f"   - {func}")
                
            print(f"   Classes View: {len(classes)}")
            for cls in classes:
                print(f"   - {cls}")
                
        except Exception as e:
            print(f"   ❌ Erreur de lecture: {e}")

def analyse_urls_assureur():
    """Analyse les URLs de l'assureur"""
    print("\n" + "="*80)
    print("DIAGNOSTIC ASSUREUR - ANALYSE DES URLs")
    print("="*80)
    
    # Chercher les fichiers urls.py dans les dossiers assureur
    urls_files = []
    
    for root, dirs, files in os.walk(BASE_DIR):
        if 'assureur' in root and 'urls.py' in files:
            urls_files.append(Path(root) / 'urls.py')
    
    print(f"\n🔍 {len(urls_files)} fichier(s) urls.py trouvé(s):")
    
    for uf in urls_files:
        print(f"\n🔗 {uf.relative_to(BASE_DIR)}")
        
        try:
            with open(uf, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Analyser les patterns d'URL
            import re
            
            # Rechercher les patterns d'URL
            url_patterns = re.findall(r'path\s*\(\s*[\'"]([^\'"]+)[\'"]', content)
            
            print(f"   URLs définies: {len(urlpatterns)}")
            for url in urlpatterns:
                print(f"   - {url}")
                
            # Rechercher les includes
            includes = re.findall(r'include\s*\(\s*[\'"]([^\'"]+)[\'"]', content)
            if includes:
                print(f"   Includes: {len(includes)}")
                for inc in includes:
                    print(f"   - {inc}")
                    
        except Exception as e:
            print(f"   ❌ Erreur de lecture: {e}")

def analyse_templates_assureur():
    """Analyse les templates de l'assureur"""
    print("\n" + "="*80)
    print("DIAGNOSTIC ASSUREUR - ANALYSE DES TEMPLATES")
    print("="*80)
    
    templates_dir = BASE_DIR / "templates" / "assureur"
    
    if not templates_dir.exists():
        print("❌ Dossier templates/assureur non trouvé")
        return
    
    # Lister tous les templates
    templates = list(templates_dir.rglob("*.html"))
    
    print(f"\n🎨 {len(templates)} template(s) HTML trouvé(s):")
    
    for template in templates:
        rel_path = template.relative_to(templates_dir)
        size_kb = template.stat().st_size / 1024
        
        print(f"\n📄 {rel_path} ({size_kb:.1f} KB)")
        
        # Analyser le contenu
        try:
            with open(template, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les balises importantes
            checks = {
                'extends': '{% extends' in content,
                'block content': '{% block content' in content,
                'csrf_token': 'csrf_token' in content,
                'form': '<form' in content,
                'table': '<table' in content,
                'bootstrap': 'bootstrap' in content or 'btn-' in content,
            }
            
            for check, result in checks.items():
                if result:
                    print(f"   ✅ {check}")
                else:
                    print(f"   ⚠️  {check} (absent)")
                    
        except Exception as e:
            print(f"   ❌ Erreur de lecture: {e}")

def analyse_fichiers_python():
    """Analyse les fichiers Python spécifiques à l'assureur"""
    print("\n" + "="*80)
    print("DIAGNOSTIC ASSUREUR - FICHIERS PYTHON")
    print("="*80)
    
    # Chercher tous les fichiers Python dans les dossiers assureur
    python_files = []
    
    for root, dirs, files in os.walk(BASE_DIR):
        root_path = Path(root)
        if 'assureur' in root.lower():
            for file in files:
                if file.endswith('.py'):
                    python_files.append(root_path / file)
    
    print(f"\n🐍 {len(python_files)} fichier(s) Python trouvé(s):")
    
    # Grouper par type
    files_by_type = {
        'models': [],
        'views': [],
        'urls': [],
        'admin': [],
        'forms': [],
        'tests': [],
        'autres': []
    }
    
    for pf in python_files:
        filename = pf.name
        
        if filename == 'models.py':
            files_by_type['models'].append(pf)
        elif filename == 'views.py':
            files_by_type['views'].append(pf)
        elif filename == 'urls.py':
            files_by_type['urls'].append(pf)
        elif filename == 'admin.py':
            files_by_type['admin'].append(pf)
        elif filename == 'forms.py':
            files_by_type['forms'].append(pf)
        elif 'test' in filename.lower():
            files_by_type['tests'].append(pf)
        else:
            files_by_type['autres'].append(pf)
    
    for type_name, files in files_by_type.items():
        if files:
            print(f"\n📁 {type_name.upper()}: {len(files)} fichier(s)")
            for f in files:
                rel_path = f.relative_to(BASE_DIR)
                size_kb = f.stat().st_size / 1024
                print(f"   - {rel_path} ({size_kb:.1f} KB)")

def verifier_problemes_communs():
    """Vérifie les problèmes courants dans l'application assureur"""
    print("\n" + "="*80)
    print("DIAGNOSTIC ASSUREUR - VÉRIFICATION DES PROBLÈMES COURANTS")
    print("="*80)
    
    problemes = []
    
    # 1. Vérifier si le dossier templates/assureur existe
    templates_dir = BASE_DIR / "templates" / "assureur"
    if not templates_dir.exists():
        problemes.append("❌ Dossier templates/assureur manquant")
    
    # 2. Vérifier les imports dans les fichiers Python
    python_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        if 'assureur' in root.lower():
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
    
    for pf in python_files:
        try:
            with open(pf, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les imports Django manquants
            if 'from django.' in content or 'import django.' in content:
                # Vérifier les imports courants
                required_imports = [
                    'HttpResponse', 'render', 'redirect',
                    'get_object_or_404', 'login_required'
                ]
                
                for imp in required_imports:
                    if imp in content and f'from django.' not in content.split(imp)[0][-100:]:
                        # Vérifier plus précisément
                        lines = content.split('\n')
                        for line in lines:
                            if imp in line and 'from django.' not in line and 'import django.' not in line:
                                problemes.append(f"⚠️  Import potentiellement manquant dans {pf.name}: {imp}")
                                break
                                
        except Exception as e:
            problemes.append(f"❌ Erreur lecture {pf.name}: {e}")
    
    # 3. Vérifier les templates manquants référencés dans les vues
    views_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        if 'assureur' in root and 'views.py' in files:
            views_files.append(Path(root) / 'views.py')
    
    for vf in views_files:
        try:
            with open(vf, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Chercher les références de templates
            import re
            template_refs = re.findall(r'[\'"](assureur/[^\'"]+\.html)[\'"]', content)
            
            for template_ref in template_refs:
                template_path = BASE_DIR / "templates" / template_ref
                if not template_path.exists():
                    problemes.append(f"❌ Template manquant: {template_ref} (référencé dans {vf.name})")
                    
        except Exception as e:
            problemes.append(f"❌ Erreur analyse vues {vf.name}: {e}")
    
    # Afficher les problèmes
    if problemes:
        print(f"\n🔍 {len(problemes)} problème(s) détecté(s):")
        for probleme in problemes:
            print(f"\n{probleme}")
    else:
        print("\n✅ Aucun problème courant détecté")

def generer_recommandations():
    """Génère des recommandations basées sur l'analyse"""
    print("\n" + "="*80)
    print("DIAGNOSTIC ASSUREUR - RECOMMANDATIONS")
    print("="*80)
    
    recommandations = []
    
    # Vérifier la structure de base
    assureur_dir = BASE_DIR / "assureur"
    if not assureur_dir.exists():
        recommandations.append("📌 Créer la structure de base de l'application assureur")
        recommandations.append("   mkdir -p assureur/{templates/assureur,static/assureur}")
        recommandations.append("   touch assureur/__init__.py assureur/apps.py assureur/models.py")
        recommandations.append("   touch assureur/views.py assureur/urls.py assureur/admin.py")
        recommandations.append("   touch assureur/forms.py assureur/tests.py")
    
    # Vérifier les templates essentiels
    templates_essentiels = [
        'dashboard.html',
        'membres/liste.html',
        'cotisations/liste.html',
        'statistiques.html',
        'parametres.html'
    ]
    
    templates_dir = BASE_DIR / "templates" / "assureur"
    if templates_dir.exists():
        for template in templates_essentiels:
            template_path = templates_dir / template
            if not template_path.exists():
                recommandations.append(f"📌 Créer le template: assureur/{template}")
    
    # Vérifier les URLs de base
    urls_file = assureur_dir / "urls.py"
    if urls_file.exists():
        with open(urls_file, 'r') as f:
            content = f.read()
        
        if 'dashboard' not in content:
            recommandations.append("📌 Ajouter une URL pour le dashboard assureur")
        
        if 'membres' not in content:
            recommandations.append("📌 Ajouter des URLs pour la gestion des membres")
        
        if 'cotisations' not in content:
            recommandations.append("📌 Ajouter des URLs pour la gestion des cotisations")
    
    # Recommandations générales
    recommandations.append("\n📌 Mettre en place un système d'authentification spécifique assureur")
    recommandations.append("📌 Implémenter les vues de base (CRUD pour membres, cotisations)")
    recommandations.append("📌 Créer des formulaires pour les opérations assureur")
    recommandations.append("📌 Ajouter des tests unitaires pour les fonctionnalités assureur")
    recommandations.append("📌 Documenter l'API assureur si applicable")
    
    # Afficher les recommandations
    print("\n💡 Recommandations:")
    for i, rec in enumerate(recommandations, 1):
        print(f"\n{i}. {rec}")

def main():
    """Fonction principale"""
    print("🚀 DIAGNOSTIC COMPLET DE L'APPLICATION ASSUREUR")
    print("="*80)
    
    # Exécuter toutes les analyses
    analyse_structure_assureur()
    analyse_models_assureur()
    analyse_vues_assureur()
    analyse_urls_assureur()
    analyse_templates_assureur()
    analyse_fichiers_python()
    verifier_problemes_communs()
    generer_recommandations()
    
    print("\n" + "="*80)
    print("✅ DIAGNOSTIC TERMINÉ")
    print("="*80)

if __name__ == "__main__":
    main()