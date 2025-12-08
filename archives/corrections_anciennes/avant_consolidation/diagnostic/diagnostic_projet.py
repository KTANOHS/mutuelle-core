#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET - MUTUELLE CORE
Vérifie l'état de santé de tous les composants du projet
"""
import os
import sys
import django
import sqlite3
from pathlib import Path
from datetime import datetime

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Impossible de configurer Django: {e}")
    sys.exit(1)

def print_section(title):
    """Affiche une section du diagnostic"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def diagnostic_initial():
    """Diagnostic initial du projet"""
    print_section("DIAGNOSTIC INITIAL DU PROJET")
    
    # Vérification de l'environnement
    print(f"📁 Répertoire de base: {BASE_DIR}")
    print(f"🐍 Python: {sys.version}")
    print(f"⚙️  Django: {django.get_version()}")
    print(f"🔧 Mode DEBUG: {os.environ.get('DJANGO_DEBUG', 'Non défini')}")

def diagnostic_settings():
    """Diagnostic des paramètres Django"""
    print_section("PARAMÈTRES DJANGO")
    
    from django.conf import settings
    
    # Applications installées
    print(f"📱 Applications installées: {len(settings.INSTALLED_APPS)}")
    print("   - " + "\n   - ".join(settings.INSTALLED_APPS))
    
    # Base de données
    db_engine = settings.DATABASES['default']['ENGINE']
    db_name = settings.DATABASES['default']['NAME']
    print(f"🗄️  Base de données: {db_engine}")
    print(f"📂 Fichier DB: {db_name}")
    
    # URLs importantes
    print(f"🔗 Login URL: {settings.LOGIN_URL}")
    print(f"🔄 Login Redirect: {settings.LOGIN_REDIRECT_URL}")

def diagnostic_base_donnees():
    """Diagnostic de la base de données"""
    print_section("BASE DE DONNÉES")
    
    from django.db import connection
    from django.core.management import execute_from_command_line
    
    # Vérifier la connexion
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT sqlite_version()")
            version = cursor.fetchone()[0]
            print(f"✅ SQLite version: {version}")
    except Exception as e:
        print(f"❌ Erreur connexion DB: {e}")
        return
    
    # Vérifier les migrations en attente
    try:
        from django.core.management import call_command
        from io import StringIO
        output = StringIO()
        call_command('showmigrations', '--list', stdout=output)
        migrations = output.getvalue()
        
        pending_migrations = [line for line in migrations.split('\n') if '[ ]' in line]
        if pending_migrations:
            print(f"⚠️  Migrations en attente: {len(pending_migrations)}")
            for mig in pending_migrations[:5]:  # Afficher les 5 premières
                print(f"   - {mig.strip()}")
        else:
            print("✅ Toutes les migrations sont appliquées")
            
    except Exception as e:
        print(f"❌ Erreur vérification migrations: {e}")
    
    # Vérifier les tables principales
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                ORDER BY name
            """)
            tables = cursor.fetchall()
            print(f"📊 Tables dans la base: {len(tables)}")
            
            # Tables critiques à vérifier
            critical_tables = [
                'auth_user', 'membres_membre', 'medecin_medecin', 
                'pharmacien_pharmacien', 'medecin_ordonnance', 'ordonnance_partage'
            ]
            
            print("\n🔍 Tables critiques:")
            existing_tables = [table[0] for table in tables]
            for table in critical_tables:
                status = "✅" if table in existing_tables else "❌"
                print(f"   {status} {table}")
                
    except Exception as e:
        print(f"❌ Erreur lecture tables: {e}")

def diagnostic_modeles():
    """Diagnostic des modèles Django"""
    print_section("MODÈLES DJANGO")
    
    from django.apps import apps
    
    # Compter les modèles par application
    app_models = {}
    for app_config in apps.get_app_configs():
        models_count = len(app_config.get_models())
        if models_count > 0:
            app_models[app_config.label] = models_count
    
    print("📦 Modèles par application:")
    for app, count in sorted(app_models.items()):
        print(f"   {app}: {count} modèles")
    
    # Vérifier les modèles critiques
    critical_models = [
        ('membres', 'Membre'),
        ('medecin', 'Medecin'),
        ('medecin', 'Ordonnance'),
        ('pharmacien', 'Pharmacien'),
        ('agents', 'Agent'),
    ]
    
    print("\n🔍 Modèles critiques:")
    for app, model in critical_models:
        try:
            model_class = apps.get_model(app, model)
            count = model_class.objects.count()
            print(f"   ✅ {app}.{model}: {count} instances")
        except LookupError:
            print(f"   ❌ {app}.{model}: Modèle non trouvé")
        except Exception as e:
            print(f"   ⚠️  {app}.{model}: Erreur ({e})")

def diagnostic_ordonnances():
    """Diagnostic spécifique du système d'ordonnances"""
    print_section("SYSTÈME ORDONNANCES")
    
    from django.db import connection
    
    try:
        with connection.cursor() as cursor:
            # Compteurs ordonnances
            cursor.execute("SELECT COUNT(*) FROM medecin_ordonnance")
            ord_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM ordonnance_partage")
            partage_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM pharmacien_ordonnances_view")
            view_count = cursor.fetchone()[0]
            
            print(f"💊 Ordonnances créées: {ord_count}")
            print(f"🔗 Partages établis: {partage_count}")
            print(f"👁️  Ordonnances visibles (vue): {view_count}")
            
            # Vérifier la vue
            if view_count > 0:
                cursor.execute("""
                    SELECT ordonnance_id, numero, patient_nom, medicaments 
                    FROM pharmacien_ordonnances_view 
                    LIMIT 2
                """)
                examples = cursor.fetchall()
                print(f"\n📋 Exemples d'ordonnances visibles:")
                for ord in examples:
                    print(f"   - #{ord[0]}: {ord[1]} - {ord[2]} - {ord[3]}")
            else:
                print("❌ Aucune ordonnance visible dans la vue pharmacien")
                
    except Exception as e:
        print(f"❌ Erreur diagnostic ordonnances: {e}")

def diagnostic_urls():
    """Diagnostic des URLs"""
    print_section("URLS ET ROUTING")
    
    try:
        from django.urls import get_resolver
        from django.core.handlers.base import BaseHandler
        
        resolver = get_resolver()
        url_patterns = []
        
        def extract_urls(urlpatterns, namespace=None, prefix=''):
            for pattern in urlpatterns:
                if hasattr(pattern, 'url_patterns'):
                    # Namespace
                    new_namespace = pattern.namespace if pattern.namespace else namespace
                    new_prefix = prefix + str(pattern.pattern)
                    extract_urls(pattern.url_patterns, new_namespace, new_prefix)
                else:
                    # URL simple
                    url_path = prefix + str(pattern.pattern)
                    if namespace:
                        url_path = f"{namespace}:{url_path}"
                    url_patterns.append(url_path)
        
        extract_urls(resolver.url_patterns)
        
        print(f"🌐 URLs définies: {len(url_patterns)}")
        
        # URLs critiques
        critical_urls = [
            '/admin/',
            '/accounts/login/',
            '/medecin/',
            '/pharmacien/',
            '/agents/',
            '/api/'
        ]
        
        print("\n🔍 URLs critiques:")
        for url in critical_urls:
            if any(url in pattern for pattern in url_patterns):
                print(f"   ✅ {url}")
            else:
                print(f"   ❌ {url} (manquante)")
                
    except Exception as e:
        print(f"❌ Erreur diagnostic URLs: {e}")

def diagnostic_securite():
    """Diagnostic de sécurité"""
    print_section("SÉCURITÉ")
    
    from django.conf import settings
    
    security_checks = [
        ("Mode DEBUG désactivé", not settings.DEBUG),
        ("SECRET_KEY défini", bool(settings.SECRET_KEY)),
        ("Validation mots de passe activée", len(settings.AUTH_PASSWORD_VALIDATORS) > 0),
        ("Cookies sécurisés", settings.SESSION_COOKIE_SECURE),
        ("CSRF protection", True),  # Toujours activée par défaut
    ]
    
    for check, status in security_checks:
        icon = "✅" if status else "⚠️"
        print(f"   {icon} {check}")

def diagnostic_performances():
    """Diagnostic des performances"""
    print_section("PERFORMANCES")
    
    from django.db import connection
    from django.core.cache import cache
    
    # Test cache
    try:
        cache.set('diagnostic_test', 'ok', 10)
        cache_status = cache.get('diagnostic_test') == 'ok'
        print(f"💾 Cache: {'✅ Opérationnel' if cache_status else '❌ Problème'}")
    except Exception as e:
        print(f"💾 Cache: ❌ Erreur ({e})")
    
    # Statistiques base de données
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name, 
                       (SELECT COUNT(*) FROM sqlite_master WHERE type='table') as total_tables
                FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                LIMIT 1
            """)
            result = cursor.fetchone()
            if result:
                print(f"🗄️  Tables totales: {result[1]}")
    except Exception as e:
        print(f"❌ Erreur statistiques DB: {e}")

def diagnostic_fichiers():
    """Diagnostic des fichiers et répertoires"""
    print_section("FICHIERS ET RÉPERTOIRES")
    
    critical_dirs = [
        BASE_DIR / 'media',
        BASE_DIR / 'static',
        BASE_DIR / 'logs',
        BASE_DIR / 'templates',
    ]
    
    print("📁 Répertoires critiques:")
    for directory in critical_dirs:
        status = "✅" if directory.exists() else "❌"
        print(f"   {status} {directory}")
    
    # Vérifier la taille de la base de données
    db_file = BASE_DIR / 'db.sqlite3'
    if db_file.exists():
        size_mb = db_file.stat().st_size / (1024 * 1024)
        print(f"💾 Taille DB: {size_mb:.2f} MB")

def diagnostic_application_specifique():
    """Diagnostic spécifique aux applications"""
    print_section("APPLICATIONS SPÉCIFIQUES")
    
    applications = {
        'agents': ['Agent', 'RoleAgent', 'PermissionAgent'],
        'medecin': ['Medecin', 'Ordonnance', 'Consultation'],
        'pharmacien': ['Pharmacien', 'OrdonnancePharmacien'],
        'membres': ['Membre', 'Profile'],
        'communication': ['Message', 'Conversation'],
    }
    
    for app, models in applications.items():
        print(f"\n📦 {app.upper()}:")
        for model_name in models:
            try:
                from django.apps import apps
                model = apps.get_model(app, model_name)
                count = model.objects.count()
                print(f"   ✅ {model_name}: {count} instances")
            except LookupError:
                print(f"   ❌ {model_name}: Modèle non trouvé")
            except Exception as e:
                print(f"   ⚠️  {model_name}: Erreur ({e})")

def diagnostic_resume():
    """Résumé du diagnostic"""
    print_section("RÉSUMÉ DU DIAGNOSTIC")
    
    # Ici vous pourriez compiler les résultats précédents
    # Pour l'instant, affichons juste des recommandations
    
    recommendations = [
        "✅ Vérifiez que toutes les migrations sont appliquées",
        "✅ Testez l'interface administrateur",
        "✅ Vérifiez le système d'ordonnances médecin→pharmacien", 
        "✅ Testez la création de membres et d'agents",
        "✅ Vérifiez les logs pour détecter des erreurs",
        "⚠️  En production: désactivez DEBUG et sécurisez les cookies",
    ]
    
    print("💡 Recommandations:")
    for rec in recommendations:
        print(f"   {rec}")

def main():
    """Fonction principale"""
    print("🚀 DIAGNOSTIC COMPLET - PROJET MUTUELLE CORE")
    print(f"📅 Exécuté le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        diagnostic_initial()
        diagnostic_settings()
        diagnostic_base_donnees()
        diagnostic_modeles()
        diagnostic_ordonnances()
        diagnostic_urls()
        diagnostic_securite()
        diagnostic_performances()
        diagnostic_fichiers()
        diagnostic_application_specifique()
        diagnostic_resume()
        
        print(f"\n🎉 DIAGNOSTIC TERMINÉ!")
        print("📋 Consultez les recommandations ci-dessus pour optimiser votre projet")
        
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE pendant le diagnostic: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())