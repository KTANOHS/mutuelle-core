#!/usr/bin/env python
"""
DIAGNOSTIC GLOBAL COMPLET - TOUTES LES APPLICATIONS DJANGO
Analyse toutes les applications installées dans settings.INSTALLED_APPS
"""

import os
import sys
import django
import importlib
import inspect
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.db import connection
from django.conf import settings
from django.contrib.auth.models import User, Group

def print_header(title, level=1):
    """Affiche un en-tête de section"""
    if level == 1:
        print(f"\n{'='*80}")
        print(f"🎯 {title}")
        print(f"{'='*80}")
    elif level == 2:
        print(f"\n{'━'*60}")
        print(f"📁 {title}")
        print(f"{'━'*60}")

def print_check(name, status, details=""):
    """Affiche une vérification avec statut"""
    icons = {"✅": "✅", "⚠️": "⚠️ ", "❌": "❌", "🔍": "🔍"}
    icon = icons.get(status, "🔸")
    print(f"{icon} {name}")
    if details:
        print(f"   {details}")

def get_app_info(app_name):
    """Récupère les informations d'une application"""
    app_info = {
        "name": app_name,
        "path": None,
        "is_installed": False,
        "is_django_app": False,
        "is_third_party": False,
        "is_custom_app": False
    }
    
    # Vérifier si c'est une app Django ou tierce
    if app_name.startswith('django.'):
        app_info["is_django_app"] = True
        return app_info
    
    # Vérifier les apps tierces courantes
    third_party_apps = [
        'rest_framework', 'corsheaders', 'crispy_forms', 'channels',
        'django_extensions', 'rest_framework_simplejwt'
    ]
    
    for third_party in third_party_apps:
        if app_name.startswith(third_party):
            app_info["is_third_party"] = True
            return app_info
    
    # C'est une app personnalisée
    app_info["is_custom_app"] = True
    
    try:
        # Essayer d'importer l'app
        module = importlib.import_module(app_name)
        if hasattr(module, '__file__'):
            app_info["path"] = Path(module.__file__).parent
        
        # Vérifier dans apps Django
        try:
            app_config = apps.get_app_config(app_name.split('.')[-1])
            app_info["is_installed"] = True
        except:
            pass
            
    except ImportError:
        # Essayer de trouver le chemin autrement
        for path in sys.path:
            potential_path = Path(path) / app_name.replace('.', '/')
            if potential_path.exists():
                app_info["path"] = potential_path
                break
    
    return app_info

def analyze_models(app_name, app_path):
    """Analyse les modèles d'une application"""
    results = {
        "model_count": 0,
        "models": [],
        "tables": [],
        "errors": []
    }
    
    try:
        # Essayer d'obtenir la configuration de l'app
        try:
            app_config = apps.get_app_config(app_name.split('.')[-1])
            models_list = list(app_config.get_models())
        except:
            # Si l'app n'est pas dans apps, chercher manuellement
            models_list = []
            
            # Essayer d'importer models.py
            try:
                models_module = importlib.import_module(f"{app_name}.models")
                for name, obj in inspect.getmembers(models_module):
                    if inspect.isclass(obj) and hasattr(obj, '_meta'):
                        # C'est probablement un modèle Django
                        if hasattr(obj._meta, 'app_label'):
                            models_list.append(obj)
            except ImportError:
                pass
        
        results["model_count"] = len(models_list)
        
        for model in models_list:
            model_info = {
                "name": model.__name__,
                "table_name": getattr(model._meta, 'db_table', 'N/A'),
                "field_count": 0,
                "fields": []
            }
            
            # Compter les champs
            try:
                fields = model._meta.get_fields()
                field_names = [f.name for f in fields if not f.is_relation or f.one_to_one]
                model_info["field_count"] = len(field_names)
                model_info["fields"] = field_names[:10]  # Limiter à 10
            except:
                pass
            
            results["models"].append(model_info)
            
            # Vérifier la table en base
            table_name = model_info["table_name"]
            if table_name != 'N/A':
                try:
                    with connection.cursor() as cursor:
                        if connection.vendor == 'sqlite':
                            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                        elif connection.vendor == 'postgresql':
                            cursor.execute(f"SELECT tablename FROM pg_tables WHERE tablename='{table_name}'")
                        else:
                            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
                        
                        if cursor.fetchone():
                            # Compter les enregistrements
                            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                            count = cursor.fetchone()[0]
                            results["tables"].append({
                                "name": table_name,
                                "record_count": count,
                                "exists": True
                            })
                        else:
                            results["tables"].append({
                                "name": table_name,
                                "exists": False
                            })
                except Exception as e:
                    results["tables"].append({
                        "name": table_name,
                        "error": str(e)
                    })
    
    except Exception as e:
        results["errors"].append(f"Erreur analyse modèles: {e}")
    
    return results

def analyze_views(app_name, app_path):
    """Analyse les vues d'une application"""
    results = {
        "view_file_exists": False,
        "view_count": 0,
        "function_views": [],
        "class_views": [],
        "decorators": defaultdict(int)
    }
    
    # Chercher le fichier views.py
    views_file = app_path / "views.py"
    if not views_file.exists():
        # Chercher dans les sous-dossiers
        for root, dirs, files in os.walk(app_path):
            if "views.py" in files:
                views_file = Path(root) / "views.py"
                break
    
    if not views_file.exists():
        return results
    
    results["view_file_exists"] = True
    
    try:
        with open(views_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Analyser les fonctions et classes
        for line in lines:
            stripped = line.strip()
            
            # Compter les décorateurs courants
            decorators_to_check = [
                '@login_required', '@permission_required', '@csrf_exempt',
                '@api_view', '@action', '@list_route', '@detail_route',
                '@require_http_methods', '@require_GET', '@require_POST'
            ]
            
            for decorator in decorators_to_check:
                if decorator in line:
                    results["decorators"][decorator] += 1
            
            # Détecter les fonctions de vue
            if stripped.startswith('def '):
                func_name = stripped[4:].split('(')[0].strip()
                if not func_name.startswith('_'):  # Ignorer les fonctions privées
                    results["function_views"].append(func_name)
                    results["view_count"] += 1
            
            # Détecter les classes de vue
            elif stripped.startswith('class ') and ('View' in stripped or 'APIView' in stripped):
                class_name = stripped[6:].split('(')[0].split(':')[0].strip()
                results["class_views"].append(class_name)
                results["view_count"] += 1
        
        # Limiter les listes pour l'affichage
        results["function_views"] = results["function_views"][:10]
        results["class_views"] = results["class_views"][:10]
        
    except Exception as e:
        results["error"] = str(e)
    
    return results

def analyze_urls(app_name, app_path):
    """Analyse les URLs d'une application"""
    results = {
        "urls_file_exists": False,
        "url_patterns": [],
        "included_in_project": False
    }
    
    # Chercher le fichier urls.py
    urls_file = app_path / "urls.py"
    if urls_file.exists():
        results["urls_file_exists"] = True
        
        try:
            with open(urls_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extraire les patterns d'URL simples
            import re
            
            # Chercher les patterns path()
            path_patterns = re.findall(r'path\([\'"]([^\'"]+)[\'"]', content)
            if path_patterns:
                results["url_patterns"].extend(path_patterns)
            
            # Chercher les patterns re_path()
            re_path_patterns = re.findall(r're_path\([\'"]([^\'"]+)[\'"]', content)
            if re_path_patterns:
                results["url_patterns"].extend(re_path_patterns)
            
            # Si pas de patterns trouvés, chercher des include()
            if not results["url_patterns"]:
                include_patterns = re.findall(r'include\([\'"]([^\'"]+)[\'"]', content)
                results["url_patterns"] = [f"Include: {p}" for p in include_patterns]
        
        except Exception as e:
            results["error"] = str(e)
    
    # Vérifier si l'app est incluse dans les URLs du projet
    try:
        project_urls = BASE_DIR / "mutuelle_core" / "urls.py"
        if project_urls.exists():
            with open(project_urls, 'r', encoding='utf-8') as f:
                project_content = f.read()
            
            app_base_name = app_name.split('.')[-1]
            if f"'{app_name}.urls'" in project_content or f'"{app_name}.urls"' in project_content:
                results["included_in_project"] = True
            elif f"'{app_base_name}.urls'" in project_content or f'"{app_base_name}.urls"' in project_content:
                results["included_in_project"] = True
    except:
        pass
    
    return results

def analyze_templates(app_name, app_path):
    """Analyse les templates d'une application"""
    results = {
        "templates_dir_exists": False,
        "template_count": 0,
        "html_files": [],
        "template_path": None
    }
    
    # Chercher le dossier templates
    possible_paths = [
        app_path / "templates",
        app_path / "templates" / app_name.split('.')[-1],
        BASE_DIR / "templates" / app_name.split('.')[-1]
    ]
    
    for template_path in possible_paths:
        if template_path.exists() and template_path.is_dir():
            results["templates_dir_exists"] = True
            results["template_path"] = str(template_path)
            
            # Compter les fichiers HTML
            try:
                for root, dirs, files in os.walk(template_path):
                    for file in files:
                        if file.endswith('.html'):
                            rel_path = os.path.relpath(os.path.join(root, file), template_path)
                            results["html_files"].append(rel_path)
                            results["template_count"] += 1
                
                # Limiter la liste
                results["html_files"] = results["html_files"][:20]
                break
            except:
                pass
    
    return results

def analyze_admin(app_name, app_path):
    """Analyse l'administration d'une application"""
    results = {
        "admin_file_exists": False,
        "registered_models": [],
        "modeladmin_classes": []
    }
    
    admin_file = app_path / "admin.py"
    if admin_file.exists():
        results["admin_file_exists"] = True
        
        try:
            with open(admin_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Chercher les enregistrements admin.site.register
            import re
            registrations = re.findall(r'admin\.site\.register\(([^)]+)\)', content)
            if registrations:
                results["registered_models"] = [r.strip() for r in registrations]
            
            # Chercher les classes ModelAdmin
            lines = content.split('\n')
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('class ') and 'Admin' in stripped:
                    class_name = stripped.split('class ')[1].split('(')[0].strip()
                    results["modeladmin_classes"].append(class_name)
        
        except Exception as e:
            results["error"] = str(e)
    
    return results

def analyze_files_structure(app_path):
    """Analyse la structure des fichiers d'une application"""
    results = {
        "essential_files": {},
        "optional_files": {},
        "directory_structure": []
    }
    
    essential_files = [
        '__init__.py',
        'models.py',
        'views.py',
        'urls.py',
        'admin.py',
        'apps.py'
    ]
    
    optional_files = [
        'forms.py',
        'tests.py',
        'signals.py',
        'managers.py',
        'serializers.py',
        'permissions.py',
        'middleware.py',
        'context_processors.py'
    ]
    
    # Vérifier les fichiers essentiels
    for file in essential_files:
        file_path = app_path / file
        if file_path.exists():
            try:
                size = file_path.stat().st_size
                results["essential_files"][file] = {
                    "exists": True,
                    "size": size,
                    "lines": len(open(file_path, 'r', encoding='utf-8').readlines())
                }
            except:
                results["essential_files"][file] = {"exists": True, "error": "Cannot read"}
        else:
            results["essential_files"][file] = {"exists": False}
    
    # Vérifier les fichiers optionnels
    for file in optional_files:
        file_path = app_path / file
        if file_path.exists():
            try:
                size = file_path.stat().st_size
                results["optional_files"][file] = {
                    "exists": True,
                    "size": size,
                    "lines": len(open(file_path, 'r', encoding='utf-8').readlines())
                }
            except:
                results["optional_files"][file] = {"exists": True, "error": "Cannot read"}
    
    # Analyser la structure de dossiers
    try:
        for root, dirs, files in os.walk(app_path, topdown=True):
            level = root.replace(str(app_path), '').count(os.sep)
            indent = ' ' * 2 * level
            folder_name = os.path.basename(root)
            
            if level == 0:
                results["directory_structure"].append(f"{folder_name}/")
            else:
                results["directory_structure"].append(f"{indent}├── {folder_name}/")
            
            subindent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # Limiter à 5 fichiers par dossier
                if file.endswith('.py') or file.endswith('.html'):
                    results["directory_structure"].append(f"{subindent}├── {file}")
            
            if len(files) > 5:
                results["directory_structure"].append(f"{subindent}└── ... et {len(files) - 5} autres fichiers")
    except:
        pass
    
    return results

def analyze_app_database(app_name):
    """Analyse les tables de base de données de l'application"""
    results = {
        "tables": [],
        "total_records": 0,
        "table_count": 0
    }
    
    try:
        with connection.cursor() as cursor:
            if connection.vendor == 'sqlite':
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                all_tables = [row[0] for row in cursor.fetchall()]
            elif connection.vendor == 'postgresql':
                cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'")
                all_tables = [row[0] for row in cursor.fetchall()]
            else:
                cursor.execute("SHOW TABLES")
                all_tables = [row[0] for row in cursor.fetchall()]
            
            # Filtrer les tables de l'application
            app_prefix = app_name.split('.')[-1] + '_'
            app_tables = [t for t in all_tables if t.startswith(app_prefix)]
            results["table_count"] = len(app_tables)
            
            for table in app_tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    results["tables"].append({
                        "name": table,
                        "record_count": count
                    })
                    results["total_records"] += count
                except Exception as e:
                    results["tables"].append({
                        "name": table,
                        "error": str(e)
                    })
    
    except Exception as e:
        results["error"] = str(e)
    
    return results

def diagnostic_global_toutes_applications():
    """Diagnostic global de toutes les applications"""
    print_header("DIAGNOSTIC GLOBAL - TOUTES LES APPLICATIONS", 1)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Projet: {BASE_DIR.name}")
    print(f"🔧 Django version: {django.get_version()}")
    print(f"📊 Applications installées: {len(settings.INSTALLED_APPS)}")
    
    all_results = {}
    custom_apps = []
    django_apps = []
    third_party_apps = []
    
    # Analyser chaque application
    for app_name in settings.INSTALLED_APPS:
        app_info = get_app_info(app_name)
        
        if app_info["is_django_app"]:
            django_apps.append(app_name)
        elif app_info["is_third_party"]:
            third_party_apps.append(app_name)
        elif app_info["is_custom_app"]:
            custom_apps.append(app_name)
            
            print_header(f"Application: {app_name}", 2)
            
            if not app_info["path"]:
                print_check("Chemin application", "❌", "Introuvable")
                all_results[app_name] = {"error": "Application path not found"}
                continue
            
            print_check("Chemin application", "✅", str(app_info["path"]))
            print_check("Installée dans Django", "✅" if app_info["is_installed"] else "⚠️")
            
            # Analyser la structure des fichiers
            files_structure = analyze_files_structure(app_info["path"])
            
            # Afficher les fichiers essentiels
            print("\n📄 Fichiers essentiels:")
            for file, info in files_structure["essential_files"].items():
                if info.get("exists"):
                    size = info.get("size", 0)
                    lines = info.get("lines", 0)
                    print_check(file, "✅", f"{size} octets, {lines} lignes")
                else:
                    print_check(file, "❌", "Manquant")
            
            # Analyser les modèles
            print("\n🗄️  Modèles:")
            models_result = analyze_models(app_name, app_info["path"])
            if models_result["model_count"] > 0:
                print_check("Nombre de modèles", "✅", f"{models_result['model_count']}")
                for model_info in models_result["models"][:3]:  # Afficher 3 modèles max
                    print(f"   • {model_info['name']} ({model_info['field_count']} champs)")
                if models_result["model_count"] > 3:
                    print(f"   ... et {models_result['model_count'] - 3} autres modèles")
            else:
                print_check("Modèles", "⚠️", "Aucun modèle détecté")
            
            # Analyser les vues
            print("\n👁️  Vues:")
            views_result = analyze_views(app_name, app_info["path"])
            if views_result["view_file_exists"]:
                if views_result["view_count"] > 0:
                    print_check("Fichier views.py", "✅", f"{views_result['view_count']} vues")
                    if views_result["function_views"]:
                        print(f"   • Fonctions: {', '.join(views_result['function_views'][:3])}")
                    if views_result["class_views"]:
                        print(f"   • Classes: {', '.join(views_result['class_views'][:3])}")
                else:
                    print_check("Fichier views.py", "⚠️", "Aucune vue détectée")
            else:
                print_check("Fichier views.py", "⚠️", "Non trouvé")
            
            # Analyser les URLs
            print("\n🔗 URLs:")
            urls_result = analyze_urls(app_name, app_info["path"])
            if urls_result["urls_file_exists"]:
                if urls_result["url_patterns"]:
                    print_check("Fichier urls.py", "✅", f"{len(urls_result['url_patterns'])} patterns")
                    for pattern in urls_result["url_patterns"][:3]:
                        print(f"   • {pattern}")
                    if len(urls_result["url_patterns"]) > 3:
                        print(f"   ... et {len(urls_result['url_patterns']) - 3} autres")
                else:
                    print_check("Fichier urls.py", "⚠️", "Aucun pattern détecté")
            else:
                print_check("Fichier urls.py", "⚠️", "Non trouvé")
            
            if urls_result.get("included_in_project"):
                print_check("Incluse dans URLs projet", "✅")
            else:
                print_check("Incluse dans URLs projet", "⚠️", "Non vérifiée ou non incluse")
            
            # Analyser les templates
            print("\n📄 Templates:")
            templates_result = analyze_templates(app_name, app_info["path"])
            if templates_result["templates_dir_exists"]:
                print_check("Dossier templates", "✅", f"{templates_result['template_count']} fichiers HTML")
                if templates_result["html_files"]:
                    for template in templates_result["html_files"][:3]:
                        print(f"   • {template}")
                    if templates_result["template_count"] > 3:
                        print(f"   ... et {templates_result['template_count'] - 3} autres")
            else:
                print_check("Dossier templates", "⚠️", "Non trouvé")
            
            # Analyser l'admin
            print("\n⚙️  Administration:")
            admin_result = analyze_admin(app_name, app_info["path"])
            if admin_result["admin_file_exists"]:
                if admin_result["registered_models"]:
                    print_check("Fichier admin.py", "✅", f"{len(admin_result['registered_models'])} modèles enregistrés")
                    for model in admin_result["registered_models"][:3]:
                        print(f"   • {model}")
                else:
                    print_check("Fichier admin.py", "⚠️", "Aucun modèle enregistré")
            else:
                print_check("Fichier admin.py", "⚠️", "Non trouvé")
            
            # Analyser la base de données
            print("\n💾 Base de données:")
            db_result = analyze_app_database(app_name)
            if db_result["table_count"] > 0:
                print_check("Tables", "✅", f"{db_result['table_count']} tables, {db_result['total_records']} enregistrements")
                for table_info in db_result["tables"][:3]:
                    if "error" in table_info:
                        print(f"   • {table_info['name']}: ❌ {table_info['error']}")
                    else:
                        print(f"   • {table_info['name']}: {table_info['record_count']} lignes")
                if db_result["table_count"] > 3:
                    print(f"   ... et {db_result['table_count'] - 3} autres tables")
            else:
                print_check("Tables", "⚠️", "Aucune table trouvée")
            
            # Stocker les résultats
            all_results[app_name] = {
                "info": app_info,
                "files": files_structure,
                "models": models_result,
                "views": views_result,
                "urls": urls_result,
                "templates": templates_result,
                "admin": admin_result,
                "database": db_result
            }
    
    # Afficher le résumé
    print_header("📊 RÉSUMÉ GLOBAL", 1)
    
    print("\n📈 STATISTIQUES PAR CATÉGORIE:")
    print("-"*60)
    
    print(f"\n🔧 Applications Django intégrées: {len(django_apps)}")
    for app in django_apps[:5]:
        print(f"   • {app}")
    if len(django_apps) > 5:
        print(f"   ... et {len(django_apps) - 5} autres")
    
    print(f"\n📦 Applications tierces: {len(third_party_apps)}")
    for app in third_party_apps[:5]:
        print(f"   • {app}")
    if len(third_party_apps) > 5:
        print(f"   ... et {len(third_party_apps) - 5} autres")
    
    print(f"\n🎯 Applications personnalisées: {len(custom_apps)}")
    for app in custom_apps:
        print(f"   • {app}")
    
    # Calculer les statistiques globales
    total_models = 0
    total_views = 0
    total_tables = 0
    total_records = 0
    
    for app_name, results in all_results.items():
        if "models" in results:
            total_models += results["models"].get("model_count", 0)
        if "views" in results:
            total_views += results["views"].get("view_count", 0)
        if "database" in results:
            total_tables += results["database"].get("table_count", 0)
            total_records += results["database"].get("total_records", 0)
    
    print(f"\n📊 STATISTIQUES CUMULÉES:")
    print(f"   • Modèles: {total_models}")
    print(f"   • Vues: {total_views}")
    print(f"   • Tables BDD: {total_tables}")
    print(f"   • Enregistrements BDD: {total_records}")
    
    # Identifier les problèmes potentiels
    print_header("🔍 PROBLÈMES IDENTIFIÉS", 1)
    
    problems = []
    
    for app_name, results in all_results.items():
        app_problems = []
        
        # Vérifier les fichiers manquants
        if "files" in results:
            for file, info in results["files"].get("essential_files", {}).items():
                if not info.get("exists"):
                    app_problems.append(f"Fichier {file} manquant")
        
        # Vérifier les modèles sans table
        if "models" in results and "database" in results:
            model_count = results["models"].get("model_count", 0)
            table_count = results["database"].get("table_count", 0)
            if model_count > 0 and table_count == 0:
                app_problems.append(f"{model_count} modèles mais 0 table en BDD")
        
        # Vérifier les URLs non incluses
        if "urls" in results:
            if not results["urls"].get("included_in_project", False):
                app_problems.append("URLs non incluses dans le projet")
        
        if app_problems:
            problems.append(f"{app_name}: {', '.join(app_problems)}")
    
    if problems:
        print("\n❌ Problèmes détectés:")
        for problem in problems:
            print(f"   • {problem}")
    else:
        print("\n✅ Aucun problème critique détecté")
    
    # Recommandations
    print_header("🎯 RECOMMANDATIONS", 1)
    
    recommendations = [
        "1. Vérifier que toutes les applications personnalisées ont des modèles enregistrés dans admin.py",
        "2. S'assurer que toutes les applications ont leur fichier urls.py et sont incluses dans les URLs principales",
        "3. Tester chaque vue pour vérifier qu'elle fonctionne correctement",
        "4. Vérifier les migrations pour les applications avec modèles mais sans tables",
        "5. Documenter les applications manquantes ou incomplètes",
        "6. Mettre à jour les dépendances des applications tierces",
        "7. Configurer les logs spécifiques pour chaque application",
        "8. Implémenter des tests unitaires pour les applications critiques"
    ]
    
    for rec in recommendations:
        print(f"   • {rec}")
    
    # Générer un rapport JSON
    generate_global_report(all_results, custom_apps, django_apps, third_party_apps, 
                          total_models, total_views, total_tables, total_records)
    
    print_header("✅ DIAGNOSTIC GLOBAL TERMINÉ", 1)

def generate_global_report(all_results, custom_apps, django_apps, third_party_apps,
                          total_models, total_views, total_tables, total_records):
    """Génère un rapport JSON détaillé"""
    report_data = {
        "metadata": {
            "date": datetime.now().isoformat(),
            "project_name": BASE_DIR.name,
            "django_version": django.get_version(),
            "total_apps": len(settings.INSTALLED_APPS)
        },
        "statistics": {
            "django_apps": len(django_apps),
            "third_party_apps": len(third_party_apps),
            "custom_apps": len(custom_apps),
            "total_models": total_models,
            "total_views": total_views,
            "total_tables": total_tables,
            "total_records": total_records
        },
        "applications": {
            "django": django_apps,
            "third_party": third_party_apps,
            "custom": custom_apps
        },
        "detailed_results": all_results
    }
    
    report_file = BASE_DIR / f"rapport_global_applications_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Rapport global généré: {report_file}")
        
        # Générer également un résumé texte
        summary_file = BASE_DIR / f"resume_global_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"RAPPORT GLOBAL - PROJET DJANGO\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Projet: {BASE_DIR.name}\n")
            f.write(f"="*60 + "\n\n")
            
            f.write(f"APPLICATIONS ({len(settings.INSTALLED_APPS)} total):\n")
            f.write(f"  • Django: {len(django_apps)}\n")
            f.write(f"  • Tierces: {len(third_party_apps)}\n")
            f.write(f"  • Personnalisées: {len(custom_apps)}\n\n")
            
            f.write(f"APPLICATIONS PERSONNALISÉES DÉTAILLÉES:\n")
            for app in custom_apps:
                f.write(f"\n  📁 {app}:\n")
                if app in all_results:
                    results = all_results[app]
                    f.write(f"    • Modèles: {results.get('models', {}).get('model_count', 0)}\n")
                    f.write(f"    • Vues: {results.get('views', {}).get('view_count', 0)}\n")
                    f.write(f"    • Tables: {results.get('database', {}).get('table_count', 0)}\n")
            
            f.write(f"\n" + "="*60 + "\n")
            f.write(f"STATISTIQUES CUMULÉES:\n")
            f.write(f"  • Modèles totaux: {total_models}\n")
            f.write(f"  • Vues totales: {total_views}\n")
            f.write(f"  • Tables totales: {total_tables}\n")
            f.write(f"  • Enregistrements totaux: {total_records}\n")
        
        print(f"📝 Résumé texte généré: {summary_file}")
        
    except Exception as e:
        print(f"⚠️  Erreur génération rapport: {e}")

def menu_principal():
    """Menu principal interactif"""
    while True:
        print_header("🛠️  DIAGNOSTIC GLOBAL - TOUTES LES APPLICATIONS", 1)
        print("\nMENU:")
        print("1. 🔍 Diagnostic complet (toutes les applications)")
        print("2. 📊 Diagnostic applications personnalisées seulement")
        print("3. 🎯 Diagnostic application spécifique")
        print("4. 📄 Générer rapport seulement")
        print("5. 🚪 Quitter")
        
        try:
            choix = input("\nVotre choix (1-5): ").strip()
            
            if choix == "1":
                print("\n🔄 Exécution du diagnostic complet...")
                diagnostic_global_toutes_applications()
                input("\n📌 Appuyez sur Entrée pour continuer...")
            
            elif choix == "2":
                print("\n🎯 Exécution du diagnostic applications personnalisées...")
                # Filtrer pour ne garder que les apps personnalisées
                diagnostic_global_toutes_applications()  # Le script filtre déjà
                input("\n📌 Appuyez sur Entrée pour continuer...")
            
            elif choix == "3":
                print("\n🎯 Applications disponibles:")
                for i, app in enumerate(settings.INSTALLED_APPS, 1):
                    print(f"  {i}. {app}")
                
                try:
                    app_index = int(input("\nNuméro de l'application: ")) - 1
                    if 0 <= app_index < len(settings.INSTALLED_APPS):
                        app_name = settings.INSTALLED_APPS[app_index]
                        print(f"\n🔍 Analyse de: {app_name}")
                        
                        # Ici, vous pourriez appeler une fonction spécifique
                        # Pour l'instant, on exécute le diagnostic complet
                        diagnostic_global_toutes_applications()
                    else:
                        print("❌ Numéro invalide!")
                except ValueError:
                    print("❌ Veuillez entrer un nombre valide")
                
                input("\n📌 Appuyez sur Entrée pour continuer...")
            
            elif choix == "4":
                print("\n📄 Génération du rapport...")
                # Exécuter le diagnostic pour générer le rapport
                diagnostic_global_toutes_applications()
                input("\n📌 Appuyez sur Entrée pour continuer...")
            
            elif choix == "5":
                print("\n👋 Au revoir!")
                break
            
            else:
                print("❌ Choix invalide! Veuillez choisir 1-5")
        
        except KeyboardInterrupt:
            print("\n\n👋 Opération annulée")
            break
        
        except Exception as e:
            print(f"❌ Erreur: {e}")
            input("\n📌 Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    # Mode simple sans arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--auto':
            print("🔧 Mode automatique activé")
            diagnostic_global_toutes_applications()
        elif sys.argv[1] == '--report':
            generate_global_report({}, [], [], [], 0, 0, 0, 0)
        elif sys.argv[1] == '--help':
            print("Utilisation: python diagnostic_global_applications.py")
            print("Options:")
            print("  --auto    : Exécution automatique sans menu")
            print("  --report  : Générer seulement un rapport")
            print("  --help    : Afficher cette aide")
        else:
            print(f"❌ Argument inconnu: {sys.argv[1]}")
            print("Utilisation: python diagnostic_global_applications.py [--auto|--report|--help]")
    else:
        # Mode interactif
        menu_principal()