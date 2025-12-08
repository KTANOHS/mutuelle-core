import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SETTINGS_FILE = BASE_DIR / "mutuelle_core" / "settings.py"

def analyse_mutuelle_core():
    print("🔍 ANALYSE DU FICHIER mutuelle_core/settings.py")
    print("=" * 70)
    
    if not SETTINGS_FILE.exists():
        print("❌ Fichier settings.py introuvable.")
        return

    content = SETTINGS_FILE.read_text(encoding="utf-8")

    def check(label, condition):
        print(f"   {label}: {'✅ OK' if condition else '⚠️ Problème détecté'}")

    print("➡️ Vérification des configurations de base...")
    check("ROOT_URLCONF", "mutuelle_core.urls" in content)
    check("WSGI_APPLICATION", "mutuelle_core.wsgi.application" in content)

    print("\n➡️ Vérification des applications installées...")
    apps_section = re.search(r"INSTALLED_APPS\s*=\s*\[(.*?)\]", content, re.S)
    if apps_section:
        raw_apps = re.findall(r"'([\w_]+)'", apps_section.group(1))
    else:
        raw_apps = []

    # Mots à ignorer (valeurs ou clés, pas des apps)
    ignore_keywords = {
        'True', 'False', 'default', 'fr', 'en', 'INFO', 'DEBUG', 'Lax',
        'simple', 'verbose', 'format', 'formatter', 'handlers', 'NAME', 'OPTIONS',
        'BACKEND', 'ENGINE', 'APP_DIRS', 'DIRS', 'context_processors', 'English',
        'Français', 'locale', 'default', 'version', 'style', 'level', 'class',
        'filename', 'file', 'console', 'loggers', 'process', 'thread', 'message'
    }

    local_apps = [
        app for app in raw_apps
        if app not in ignore_keywords
        and not app.startswith("django.")
        and app not in ['rest_framework', 'rest_framework_simplejwt', 'corsheaders', 'django_extensions']
    ]

    existing = [a for a in local_apps if (BASE_DIR / a).exists()]
    missing = [a for a in local_apps if not (BASE_DIR / a).exists()]

    print(f"   📁 {len(existing)} apps locales trouvées.")
    if missing:
        print(f"⚠️ Dossiers manquants: {', '.join(missing)}")
    else:
        print("✅ Toutes les apps locales existent.")

    print("\n➡️ Vérification des middlewares critiques...")
    middlewares = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware'
    ]
    for mw in middlewares:
        print(f"   {'✅' if mw in content else '⚠️'} {mw}")

    print("\n➡️ Vérification de REST Framework / JWT...")
    print(f"   REST_FRAMEWORK: {'✅' if 'REST_FRAMEWORK' in content else '⚠️'}")
    print(f"   SIMPLE_JWT: {'✅' if 'SIMPLE_JWT' in content else '⚠️'}")

    print("\n➡️ Vérification des redirections LOGIN/LOGOUT...")
    for setting in ['LOGIN_URL', 'LOGIN_REDIRECT_URL', 'LOGOUT_REDIRECT_URL']:
        match = re.search(rf"{setting}\s*=\s*['\"]([^'\"]+)['\"]", content)
        if match:
            print(f"   ✅ {setting}: {match.group(1)}")
        else:
            print(f"   ⚠️ {setting} manquant")

    print("\n➡️ Vérification du dossier logs...")
    logs_dir = BASE_DIR / "logs"
    if logs_dir.exists():
        print("✅ Dossier logs présent")
    else:
        print("⚠️ Dossier logs manquant (sera créé automatiquement)")

    print("\n🎯 Analyse terminée.")
    print("=" * 70)


if __name__ == "__main__":
    analyse_mutuelle_core()
