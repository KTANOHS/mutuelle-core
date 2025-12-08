"""
SCRIPT DE DIAGNOSTIC ASSUREUR - Mutuelle Core v2
Ce script vérifie la configuration de l'environnement Django pour l'assureur
"""

import os
import sys
import django
from pathlib import Path
from datetime import datetime

# Ajouter le chemin du projet Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def setup_django():
    """Configurer l'environnement Django"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        django.setup()
        print("✅ Django configuré avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du chargement de Django: {e}")
        return False

def diagnostic_assureur():
    """Exécute un diagnostic complet de la configuration assureur"""
    
    print("🔍 DIAGNOSTIC ASSUREUR - Mutuelle Core v2")
    print("=" * 60)
    print(f"Date du diagnostic: {datetime.now()}")
    print(f"Répertoire de base: {BASE_DIR}")
    
    if not setup_django():
        return
    
    from django.conf import settings
    
    print(f"Mode DEBUG: {settings.DEBUG}")
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print()
    
    # 1. Vérifier les applications installées
    print("📦 1. VÉRIFICATION DES APPLICATIONS")
    print("-" * 40)
    
    apps_assureur = [
        'assureur',
        'agents',
        'membres',
        'inscription',
        'paiements',
        'soins',
        'notifications',
        'communication',
        'ia_detection',
        'scoring',
        'relances',
        'dashboard'
    ]
    
    for app in apps_assureur:
        if app in settings.INSTALLED_APPS:
            print(f"✅ {app:20} - Installé")
        else:
            print(f"❌ {app:20} - NON installé")
    
    print()
    
    # 2. Vérifier les templates
    print("📝 2. VÉRIFICATION DES TEMPLATES")
    print("-" * 40)
    
    for template in settings.TEMPLATES:
        if 'DIRS' in template:
            for dir_path in template['DIRS']:
                if os.path.exists(dir_path):
                    print(f"✅ Templates: {dir_path}")
                    # Compter les fichiers
                    html_files = []
                    for root, _, files in os.walk(dir_path):
                        html_files.extend([f for f in files if f.endswith('.html')])
                    
                    if html_files:
                        print(f"   → {len(html_files)} fichiers HTML trouvés")
                        # Afficher quelques fichiers
                        sample_files = html_files[:5]
                        for f in sample_files:
                            print(f"     • {f}")
                        if len(html_files) > 5:
                            print(f"     ... et {len(html_files) - 5} autres")
                else:
                    print(f"⚠️  Répertoire non trouvé: {dir_path}")
    
    print()
    
    # 3. Vérifier les fichiers statiques
    print("🎨 3. VÉRIFICATION DES FICHIERS STATIQUES")
    print("-" * 40)
    
    for static_dir in settings.STATICFILES_DIRS:
        if os.path.exists(static_dir):
            print(f"✅ Statique: {static_dir}")
            static_files = []
            for root, _, files in os.walk(static_dir):
                static_files.extend(files)
            
            if static_files:
                categories = {
                    'CSS': [f for f in static_files if f.endswith('.css')],
                    'JS': [f for f in static_files if f.endswith('.js')],
                    'Images': [f for f in static_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg'))]
                }
                
                for cat, files in categories.items():
                    if files:
                        print(f"   {cat}: {len(files)} fichiers")
        else:
            print(f"⚠️  Répertoire statique non trouvé: {static_dir}")
    
    print(f"\n📊 STATS: URL={settings.STATIC_URL}, ROOT={settings.STATIC_ROOT}")
    
    print()
    
    # 4. Vérifier la base de données
    print("🗄️  4. VÉRIFICATION DE LA BASE DE DONNÉES")
    print("-" * 40)
    
    db_config = settings.DATABASES.get('default', {})
    engine = db_config.get('ENGINE', '').split('.')[-1]
    db_name = db_config.get('NAME', '')
    
    print(f"Type: {engine}")
    print(f"Nom: {db_name}")
    
    if os.path.exists(db_name):
        size = os.path.getsize(db_name)
        modified = datetime.fromtimestamp(os.path.getmtime(db_name))
        print(f"✅ Base trouvée: {size / 1024 / 1024:.2f} MB")
        print(f"   Modifiée: {modified}")
    else:
        print(f"⚠️  Base non trouvée: {db_name}")
    
    print()
    
    # 5. Vérifier la configuration assureur
    print("🏥 5. CONFIGURATION ASSUREUR")
    print("-" * 40)
    
    mutuelle_config = getattr(settings, 'MUTUELLE_CONFIG', {})
    
    if mutuelle_config:
        print("✅ Configuration mutuelle chargée")
        for key, value in mutuelle_config.items():
            print(f"   {key:30}: {value}")
    else:
        print("❌ Configuration mutuelle NON chargée")
    
    print()
    
    # 6. Tester l'import des modèles
    print("🧪 6. TEST DES IMPORTS")
    print("-" * 40)
    
    models_to_test = [
        ('assureur.models', 'Assureur'),
        ('agents.models', 'Agent'),
        ('membres.models', 'Membre'),
        ('soins.models', 'BonSoin'),
        ('paiements.models', 'Paiement'),
        ('notifications.models', 'Notification'),
    ]
    
    for module_path, model_name in models_to_test:
        try:
            module = __import__(module_path, fromlist=[model_name])
            model_class = getattr(module, model_name)
            print(f"✅ {model_name:20} - Importé")
        except ImportError as e:
            print(f"❌ {model_name:20} - ImportError: {str(e)[:50]}...")
        except AttributeError as e:
            print(f"❌ {model_name:20} - AttributeError: {str(e)[:50]}...")
        except Exception as e:
            print(f"❌ {model_name:20} - Erreur: {type(e).__name__}")
    
    print()
    
    # 7. Vérifier les migrations
    print("🔄 7. ÉTAT DES MIGRATIONS")
    print("-" * 40)
    
    try:
        from django.db import connection
        from django.db.migrations.recorder import MigrationRecorder
        
        recorder = MigrationRecorder(connection)
        migrations = recorder.migration_qs.count()
        print(f"✅ Migrations enregistrées: {migrations}")
        
        # Vérifier les migrations pour chaque app assureur
        for app in apps_assureur:
            try:
                app_migrations = recorder.migration_qs.filter(app=app).count()
                if app_migrations > 0:
                    print(f"   {app:20}: {app_migrations} migrations")
            except:
                pass
                
    except Exception as e:
        print(f"⚠️  Erreur vérification migrations: {e}")
    
    print()
    
    # 8. Vérifier les URLs
    print("🌐 8. URLS DISPONIBLES")
    print("-" * 40)
    
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        
        # URLs importantes pour l'assureur
        important_urls = [
            'assureur',
            'agent',
            'dashboard',
            'membre',
            'api',
            'login',
            'logout',
            'admin'
        ]
        
        found_urls = []
        
        def explore_urls(urlpatterns, prefix=''):
            for pattern in urlpatterns:
                if hasattr(pattern, 'pattern'):
                    pattern_str = str(pattern.pattern)
                    full_pattern = f"{prefix}/{pattern_str}".replace('//', '/')
                    
                    # Vérifier si c'est une URL importante
                    for important in important_urls:
                        if important in full_pattern.lower():
                            if full_pattern not in found_urls:
                                found_urls.append(full_pattern)
                    
                    # Explorer les sous-patterns
                    if hasattr(pattern, 'url_patterns'):
                        explore_urls(pattern.url_patterns, full_pattern)
        
        explore_urls(resolver.url_patterns)
        
        if found_urls:
            print(f"✅ {len(found_urls)} URLs importantes trouvées:")
            for url in sorted(found_urls):
                print(f"   • {url}")
        else:
            print("⚠️  Aucune URL importante trouvée")
            
    except Exception as e:
        print(f"❌ Erreur vérification URLs: {e}")
    
    print()
    
    # 9. Vérifier les permissions
    print("🔐 9. PERMISSIONS ET GROUPES")
    print("-" * 40)
    
    try:
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        
        groups_count = Group.objects.count()
        permissions_count = Permission.objects.count()
        
        print(f"✅ Groupes: {groups_count}")
        print(f"✅ Permissions: {permissions_count}")
        
        # Afficher les groupes existants
        if groups_count > 0:
            print("   Groupes disponibles:")
            for group in Group.objects.all()[:5]:
                print(f"     • {group.name}")
            if groups_count > 5:
                print(f"     ... et {groups_count - 5} autres")
                
    except Exception as e:
        print(f"⚠️  Erreur vérification permissions: {e}")
    
    print()
    
    # 10. Analyse de sécurité
    print("🛡️  10. ANALYSE DE SÉCURITÉ")
    print("-" * 40)
    
    issues = []
    
    if settings.DEBUG:
        issues.append("DEBUG activé (désactiver en production)")
    
    if not settings.SECRET_KEY or settings.SECRET_KEY == 'django-insecure-':
        issues.append("SECRET_KEY faible ou par défaut")
    
    if 'sqlite3' in engine:
        issues.append("SQLite utilisé (préférer PostgreSQL en production)")
    
    if settings.SESSION_COOKIE_AGE > 1209600:  # > 2 semaines
        issues.append("Durée de session trop longue")
    
    if not issues:
        print("✅ Aucun problème de sécurité majeur détecté")
    else:
        print(f"⚠️  {len(issues)} problèmes de sécurité détectés:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    
    print()
    print("=" * 60)
    print("📊 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 60)
    
    # Statistiques
    apps_installed = sum(1 for app in apps_assureur if app in settings.INSTALLED_APPS)
    models_imported = len([m for m in models_to_test if "✅" in locals().get('test_results', '')])
    
    print(f"• Applications assureur: {apps_installed}/{len(apps_assureur)} installées")
    print(f"• Modèles importés: {models_imported}/{len(models_to_test)}")
    print(f"• Base de données: {'✅ OK' if os.path.exists(db_name) else '❌ Problème'}")
    print(f"• Configuration: {'✅ Chargée' if mutuelle_config else '❌ Manquante'}")
    print(f"• Sécurité: {'⚠️  À améliorer' if issues else '✅ Correct'}")
    print(f"• Mode: {'🚨 DÉVELOPPEMENT' if settings.DEBUG else '🏭 PRODUCTION'}")
    
    print()
    print("💡 RECOMMANDATIONS:")
    
    if settings.DEBUG:
        print("1. Désactiver DEBUG avant la mise en production")
        print("2. Configurer une SECRET_KEY forte")
    
    if 'sqlite3' in engine:
        print("3. Migrer vers PostgreSQL pour la production")
    
    if not mutuelle_config:
        print("4. Vérifier la configuration MUTUELLE_CONFIG")
    
    if apps_installed < len(apps_assureur):
        print("5. Installer les applications manquantes")
    
    print()
    print("✅ DIAGNOSTIC TERMINÉ - " + datetime.now().strftime("%H:%M:%S"))

def verifier_systeme():
    """Vérifie le système d'exploitation et l'environnement"""
    print("\n💻 INFORMATION SYSTÈME")
    print("-" * 40)
    
    import platform
    print(f"Système: {platform.system()} {platform.release()}")
    print(f"Python: {platform.python_version()}")
    print(f"Django: {django.get_version()}")
    
    # Vérifier l'espace disque
    import shutil
    total, used, free = shutil.disk_usage("/")
    print(f"Espace disque: {free // (2**30)} GB libre sur {total // (2**30)} GB")

def verifier_services():
    """Vérifie les services externes"""
    print("\n🔌 SERVICES EXTERNES")
    print("-" * 40)
    
    # Vérifier la connexion à la base de données
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Base de données: Connectée")
    except Exception as e:
        print(f"❌ Base de données: {e}")
    
    # Vérifier l'accès aux fichiers
    check_dirs = [
        BASE_DIR / 'media',
        BASE_DIR / 'static',
        BASE_DIR / 'logs',
    ]
    
    for dir_path in check_dirs:
        if dir_path.exists():
            print(f"✅ Répertoire {dir_path.name}: Existe")
        else:
            print(f"⚠️  Répertoire {dir_path.name}: Absent")

if __name__ == "__main__":
    diagnostic_assureur()
    verifier_systeme()
    verifier_services()
    
    print("\n" + "=" * 60)
    print("🎯 POUR EXÉCUTER CE DIAGNOSTIC:")
    print("=" * 60)
    print("1. Enregistrez ce fichier sous: diagnostic_assureur.py")
    print("2. Placez-le à côté de manage.py")
    print("3. Exécutez: python diagnostic_assureur.py")
    print("\n🔄 POUR METTRE À JOUR:")
    print("python manage.py check")
    print("python manage.py migrate")
    print("python manage.py collectstatic")