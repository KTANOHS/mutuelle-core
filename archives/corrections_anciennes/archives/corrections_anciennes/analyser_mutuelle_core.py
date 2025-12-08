import os
import importlib
import django
from pathlib import Path
import sys
import re

BASE_DIR = Path(__file__).resolve().parent
SETTINGS_FILE = BASE_DIR / "mutuelle_core" / "settings.py"

def analyse_mutuelle_core():
    print("🔍 ANALYSE DU FICHIER mutuelle_core/settings.py")
    print("=" * 70)
    
    # Vérification du fichier settings.py
    if not SETTINGS_FILE.exists():
        print("❌ Fichier settings.py introuvable.")
        sys.exit(1)

    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Vérifier si mutuelle_core est bien le ROOT_URLCONF et WSGI
    print("➡️ Vérification des configurations de base...")
    checks = {
        "ROOT_URLCONF": "mutuelle_core.urls" in content,
        "WSGI_APPLICATION": "mutuelle_core.wsgi.application" in content,
    }
    for key, ok in checks.items():
        print(f"   {key}: {'✅ OK' if ok else '⚠️ Manquant ou incorrect'}")

    # Vérifier les applications installées
    print("\n➡️ Vérification des applications installées (INSTALLED_APPS)...")
    apps = re.findall(r"'([\w_]+)'", content)
    if "mutuelle_core" not in apps:
        print("⚠️ L'application 'mutuelle_core' n'est pas déclarée dans INSTALLED_APPS")
    else:
        print("✅ 'mutuelle_core' est bien installée.")
    
    # Vérification des chemins statiques et médias
    print("\n➡️ Vérification des chemins STATIC et MEDIA...")
    static_root = re.search(r"STATIC_ROOT\s*=\s*os\.path\.join\(BASE_DIR,\s*'([^']+)'\)", content)
    media_root = re.search(r"MEDIA_ROOT\s*=\s*os\.path\.join\(BASE_DIR,\s*'([^']+)'\)", content)
    print(f"   STATIC_ROOT: {'✅' if static_root else '⚠️ Non défini correctement'}")
    print(f"   MEDIA_ROOT: {'✅' if media_root else '⚠️ Non défini correctement'}")

    # Vérifier les middlewares critiques
    print("\n➡️ Vérification des middlewares...")
    required_mw = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware'
    ]
    for mw in required_mw:
        if mw in content:
            print(f"   ✅ {mw}")
        else:
            print(f"   ⚠️ {mw} manquant")

    # Vérifier la présence de l’authentification JWT
    print("\n➡️ Vérification de la configuration JWT / REST Framework...")
    jwt_found = "rest_framework_simplejwt" in content
    rest_found = "REST_FRAMEWORK" in content
    print(f"   REST_FRAMEWORK: {'✅' if rest_found else '⚠️ Manquant'}")
    print(f"   JWT (SimpleJWT): {'✅' if jwt_found else '⚠️ Non configuré'}")

    # Vérifier les URL de login
    print("\n➡️ Vérification des URLs de redirection login/logout...")
    redirect_settings = {
        "LOGIN_URL": re.search(r"LOGIN_URL\s*=\s*['\"]([^'\"]+)['\"]", content),
        "LOGIN_REDIRECT_URL": re.search(r"LOGIN_REDIRECT_URL\s*=\s*['\"]([^'\"]+)['\"]", content),
        "LOGOUT_REDIRECT_URL": re.search(r"LOGOUT_REDIRECT_URL\s*=\s*['\"]([^'\"]+)['\"]", content),
    }
    for key, val in redirect_settings.items():
        if val:
            print(f"   ✅ {key}: {val.group(1)}")
        else:
            print(f"   ⚠️ {key} non défini")

    # Vérifier la base de données
    print("\n➡️ Vérification de la base de données...")
    db_engine = re.search(r"'ENGINE':\s*'([^']+)'", content)
    if db_engine:
        print(f"   ✅ Base de données: {db_engine.group(1)}")
    else:
        print("⚠️ Moteur de base de données non trouvé")

    # Vérifier les logs
    print("\n➡️ Vérification du dossier logs...")
    logs_dir = BASE_DIR / "logs"
    if logs_dir.exists():
        print("✅ Dossier logs présent")
    else:
        print("⚠️ Dossier logs manquant (sera créé automatiquement au run)")

    # Vérifier si les apps déclarées existent dans le projet
    print("\n➡️ Vérification de la présence physique des applications...")
    app_dirs = [a for a in apps if (BASE_DIR / a).exists()]
    missing_dirs = [a for a in apps if not (BASE_DIR / a).exists() and a not in [
        'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
        'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
        'rest_framework','corsheaders','django_extensions','rest_framework_simplejwt']]
    print(f"   📁 Dossiers trouvés: {len(app_dirs)} apps locales présentes.")
    if missing_dirs:
        print("⚠️ Dossiers manquants:", ", ".join(missing_dirs))
    else:
        print("✅ Toutes les apps locales existent.")

    print("\n🎯 Analyse terminée.")
    print("=" * 70)


if __name__ == "__main__":
    try:
        analyse_mutuelle_core()
    except Exception as e:
        print(f"❌ Erreur pendant l’analyse : {e}")
