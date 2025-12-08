#!/usr/bin/env python
"""
Vérification du déploiement Django
"""
import os
import sys
import django
from pathlib import Path

# Ajouter le chemin du projet
project_path = Path(__file__).parent.parent.parent
sys.path.append(str(project_path))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings_production')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur Django: {e}")
    sys.exit(1)

def check_database():
    """Vérifier la connexion à la base de données"""
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result and result[0] == 1:
                print("✅ Base de données: Connecté")
                return True
    except Exception as e:
        print(f"❌ Base de données: Erreur - {e}")
        return False

def check_static_files():
    """Vérifier les fichiers statiques"""
    from django.conf import settings
    static_root = Path(settings.STATIC_ROOT)
    
    if static_root.exists():
        files = list(static_root.rglob('*'))
        print(f"✅ Fichiers statiques: {len(files)} fichiers trouvés")
        return True
    else:
        print("❌ Fichiers statiques: Dossier non trouvé")
        return False

def check_installed_apps():
    """Vérifier les applications installées"""
    from django.conf import settings
    
    print(f"📦 Applications installées: {len(settings.INSTALLED_APPS)}")
    
    apps_essentielles = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'core',
        'membres',
        'assureur',
        'medecin',
        'agents',
        'communication',
    ]
    
    for app in apps_essentielles:
        if app in settings.INSTALLED_APPS:
            print(f"  ✅ {app}")
        else:
            print(f"  ❌ {app} (MANQUANT)")
    
    return all(app in settings.INSTALLED_APPS for app in apps_essentielles)

def check_middleware():
    """Vérifier les middlewares"""
    from django.conf import settings
    
    print(f"🔧 Middlewares: {len(settings.MIDDLEWARE)}")
    
    middlewares_essentiels = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
    for mw in middlewares_essentiels:
        if mw in settings.MIDDLEWARE:
            print(f"  ✅ {mw.split('.')[-1]}")
        else:
            print(f"  ⚠️  {mw.split('.')[-1]} (MANQUANT)")
    
    return True

def check_security():
    """Vérifier les paramètres de sécurité"""
    from django.conf import settings
    
    print("🔒 Vérification de sécurité:")
    
    checks = [
        ("DEBUG", not settings.DEBUG, "DEBUG doit être False en production"),
        ("SECURE_SSL_REDIRECT", settings.SECURE_SSL_REDIRECT, "SSL Redirect activé"),
        ("SESSION_COOKIE_SECURE", settings.SESSION_COOKIE_SECURE, "Session Cookie Secure"),
        ("CSRF_COOKIE_SECURE", settings.CSRF_COOKIE_SECURE, "CSRF Cookie Secure"),
        ("SECURE_BROWSER_XSS_FILTER", settings.SECURE_BROWSER_XSS_FILTER, "XSS Filter"),
        ("SECURE_CONTENT_TYPE_NOSNIFF", settings.SECURE_CONTENT_TYPE_NOSNIFF, "Content Type Nosniff"),
    ]
    
    all_ok = True
    for name, value, description in checks:
        if value:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_ok = False
    
    return all_ok

def check_urls():
    """Vérifier les URLs"""
    from django.urls import get_resolver
    
    try:
        resolver = get_resolver()
        url_count = len(list(resolver.reverse_dict.keys()))
        print(f"🌐 URLs: {url_count} motifs d'URL trouvés")
        return True
    except Exception as e:
        print(f"❌ URLs: Erreur - {e}")
        return False

def main():
    print("🔍 Vérification du déploiement Django")
    print("=" * 50)
    
    checks = [
        ("Base de données", check_database),
        ("Fichiers statiques", check_static_files),
        ("Applications", check_installed_apps),
        ("Middlewares", check_middleware),
        ("Sécurité", check_security),
        ("URLs", check_urls),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        print("-" * 30)
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
    
    print(f"\n🎯 Score: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n✅ Toutes les vérifications ont réussi!")
        return 0
    else:
        print("\n⚠️  Certaines vérifications ont échoué. Corrigez les problèmes avant le déploiement.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
