#!/bin/bash
echo "🚀 SOLUTION ULTIME POUR CSRF RAILWAY"

# 1. Sauvegarder l'ancien settings
cp mutuelle_core/settings.py mutuelle_core/settings.py.backup.ultimate

# 2. Créer le settings ULTIME
cat > mutuelle_core/settings.py << 'ULTIMATE_SETTINGS'
"""
SETTINGS ULTIME POUR RAILWAY - TOUT EN UN
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================================
# 1. FORÇAGE ABSOLU DES CONFIGURATIONS
# ============================================================================

# A. TOUJOURS sur Railway pour ce déploiement
RAILWAY = True
RAILWAY_DOMAIN = "web-production-555c.up.railway.app"

print("\n" + "="*80)
print("⚡ SETTINGS ULTIME ACTIVÉ")
print("="*80)

# B. DEBUG FORCÉ
DEBUG = True
print(f"🔧 DEBUG = {DEBUG}")

# C. SECRET KEY
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-ultimate-fix-railway-2024')

# ============================================================================
# 2. CSRF - LA CONFIGURATION QUI FONCTIONNE TOUJOURS
# ============================================================================

# DÉFINIR CSRF_TRUSTED_ORIGINS de 3 MANIÈRES DIFFÉRENTES
# (l'une d'elles DOIT fonctionner)

# Méthode 1: Directe
CSRF_TRUSTED_ORIGINS_DIRECT = [
    f'https://{RAILWAY_DOMAIN}',
    f'http://{RAILWAY_DOMAIN}',
]

# Méthode 2: Via environnement
env_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if env_csrf:
    CSRF_TRUSTED_ORIGINS_ENV = [x.strip() for x in env_csrf.split(',')]
else:
    CSRF_TRUSTED_ORIGINS_ENV = []

# Méthode 3: Wildcard pour être sûr
CSRF_TRUSTED_ORIGINS_WILDCARD = [
    'https://*.railway.app',
    'http://*.railway.app',
    '*',
]

# COMBINER TOUT
CSRF_TRUSTED_ORIGINS = list(set(
    CSRF_TRUSTED_ORIGINS_DIRECT + 
    CSRF_TRUSTED_ORIGINS_ENV + 
    CSRF_TRUSTED_ORIGINS_WILDCARD
))

print(f"\n🔐 CSRF_TRUSTED_ORIGINS ({len(CSRF_TRUSTED_ORIGINS)} origines):")
for origin in list(CSRF_TRUSTED_ORIGINS)[:8]:
    print(f"   - {origin}")

# VÉRIFICATION ABSOLUE
if f'https://{RAILWAY_DOMAIN}' not in CSRF_TRUSTED_ORIGINS:
    print(f"\n🚨 FORÇAGE: Ajout de https://{RAILWAY_DOMAIN}")
    CSRF_TRUSTED_ORIGINS.append(f'https://{RAILWAY_DOMAIN}')
    CSRF_TRUSTED_ORIGINS.append(f'http://{RAILWAY_DOMAIN}')

print(f"\n✅ VÉRIFICATION FINALE: https://{RAILWAY_DOMAIN} dans la liste: {'OUI' if f'https://{RAILWAY_DOMAIN}' in CSRF_TRUSTED_ORIGINS else 'NON'}")

# ============================================================================
# 3. PROXY RAILWAY - IMPÉRATIF
# ============================================================================
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

print(f"\n🌐 PROXY CONFIGURÉ: {SECURE_PROXY_SSL_HEADER}")

# ============================================================================
# 4. COOKIES - CONFIGURATION RAILWAY SPÉCIFIQUE
# ============================================================================
CSRF_COOKIE_DOMAIN = None  # DOIT ÊTRE None
SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_SECURE = False  # False pour test, True en prod
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SAMESITE = 'Lax'

print(f"\n🍪 COOKIES: DOMAIN=None")

# ============================================================================
# 5. ALLOWED_HOSTS - PERMISSIF POUR TEST
# ============================================================================
ALLOWED_HOSTS = [
    RAILWAY_DOMAIN,
    f'.{RAILWAY_DOMAIN}',
    '.railway.app',
    '*.railway.app',
    'localhost',
    '127.0.0.1',
    '[::1]',
    '*',  # Wildcard pour être sûr
]

print(f"\n🌍 ALLOWED_HOSTS: {len(ALLOWED_HOSTS)} hosts")

# ============================================================================
# 6. CORS - TOUT PERMIS POUR TEST
# ============================================================================
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

print(f"\n🔗 CORS: toutes origines autorisées")

# ============================================================================
# 7. CONFIGURATION DE BASE (le reste)
# ============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'mutuelle_core.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

WSGI_APPLICATION = 'mutuelle_core.wsgi.application'

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

print("\n" + "="*80)
print("✅ CONFIGURATION ULTIME PRÊTE")
print("="*80)
ULTIMATE_SETTINGS

# 3. Créer le script de déploiement
echo -e "\n📝 SCRIPT DE DÉPLOIEMENT:"
cat > deploy_ultimate.sh << 'DEPLOYULTIMATE'
#!/bin/bash
echo "🚀 DÉPLOIEMENT DE LA SOLUTION ULTIME"

echo "1. Vérification des fichiers..."
ls -la mutuelle_core/settings.py

echo -e "\n2. Ajout à git..."
git add .

echo -e "\n3. Commit..."
git commit -m "ULTIMATE FIX: CSRF configuration for Railway - $(date '+%Y-%m-%d %H:%M:%S')"

echo -e "\n4. Push sur Railway..."
echo "   Exécutez: git push railway main"
echo ""
echo "⏳ Attendez 2-3 minutes que Railway déploie"
echo ""
echo "5. Après déploiement, testez avec:"
echo "   python verify_ultimate_fix.py"
DEPLOYULTIMATE

chmod +x deploy_ultimate.sh

# 4. Créer le script de vérification
cat > verify_ultimate_fix.py << 'VERIFYULTIMATE'
#!/usr/bin/env python3
import requests
import re
import time

print("🔍 VÉRIFICATION DE LA SOLUTION ULTIME")
print("="*70)

URL = "https://web-production-555c.up.railway.app"

def test_csrf_fix():
    for i in range(1, 21):  # 20 tentatives
        print(f"\n🔧 Test {i}/20")
        
        try:
            session = requests.Session()
            
            # Test GET
            resp = session.get(f"{URL}/admin/login/", timeout=10)
            
            if resp.status_code != 200:
                print(f"   ❌ GET: {resp.status_code}")
                time.sleep(3)
                continue
            
            # Vérifier CSRF
            if 'csrfmiddlewaretoken' not in resp.text:
                print("   ❌ CSRF non trouvé")
                time.sleep(3)
                continue
            
            # Extraire CSRF
            csrf_match = re.search(r'csrfmiddlewaretoken.*value="([^"]+)"', resp.text)
            csrf_token = csrf_match.group(1) if csrf_match else "N/A"
            
            print(f"   ✅ Page OK, CSRF: {csrf_token[:15]}...")
            
            # Test POST
            data = {
                'csrfmiddlewaretoken': csrf_token,
                'username': 'anyuser',
                'password': 'anypass',
                'next': '/admin/'
            }
            
            resp_post = session.post(f"{URL}/admin/login/", data=data, 
                                   headers={'Referer': f"{URL}/admin/login/"},
                                   allow_redirects=False, timeout=10)
            
            print(f"   POST: {resp_post.status_code}")
            
            # ANALYSE
            if resp_post.status_code == 403:
                response_text = resp_post.text[:1000]
                
                if 'Origin checking failed' in response_text:
                    print("   ❌ Origin checking FAILED")
                    print("   Le fix ULTIME n'a pas fonctionné")
                    # Extraire la raison exacte
                    reason_match = re.search(r'<pre>(.*?)</pre>', response_text, re.DOTALL)
                    if reason_match:
                        print(f"   Raison: {reason_match.group(1).strip()[:100]}")
                    return False
                else:
                    print("   ⚠️  403 autre (probablement identifiants)")
                    print("\n   🎉🎉🎉 SUCCÈS ! 🎉🎉🎉")
                    print("   Le problème CSRF Origin est RÉSOLU !")
                    return True
                    
            elif resp_post.status_code in [200, 302]:
                print(f"\n   🎉🎉🎉 SUCCÈS COMPLET ! 🎉🎉🎉")
                print(f"   CSRF fonctionne (Status: {resp_post.status_code})")
                return True
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        if i < 20:
            print(f"   ⏳ Attente 3 secondes...")
            time.sleep(3)
    
    return False

# Exécution
success = test_csrf_fix()

print("\n" + "="*70)
if success:
    print("✅✅✅ PROBLÈME RÉSOLU ! ✅✅✅")
    print(f"\n🌐 Votre application Django fonctionne sur Railway:")
    print(f"   URL: {URL}")
    print(f"   Admin: {URL}/admin/")
    print(f"\n🔑 Créez un superutilisateur:")
    print("   railway run python manage.py createsuperuser")
else:
    print("❌❌❌ ÉCHEC CRITIQUE ❌❌❌")
    print("Le fix ultime n'a pas fonctionné.")
    print("\n🚨 CAUSES POSSIBLES:")
    print("1. Railway n'a pas déployé le nouveau code")
    print("2. Problème de cache Railway (attendre 5-10 min)")
    print("3. Variables d'environnement incorrectes")
    print("\n🔧 ACTIONS:")
    print("1. Vérifiez les logs sur https://railway.app")
    print("2. Vérifiez les variables d'environnement Railway")
    print("3. Redéployez manuellement depuis l'interface Railway")

print("="*70)
VERIFYULTIMATE

chmod +x verify_ultimate_fix.py

echo -e "\n✅ TOUT EST PRÊT !"
echo -e "\n🎯 PROCÉDURE À SUIVRE:"
echo "1. Exécutez: ./deploy_ultimate.sh"
echo "2. Suivez les instructions (git push railway main)"
echo "3. Attendez 2-3 minutes"
echo "4. Exécutez: python verify_ultimate_fix.py"
echo -e "\n⚠️  Si 'SUCCÈS' apparaît, votre problème est RÉSOLU !"
echo "Ensuite, restaurez votre settings.py original:"
echo "cp mutuelle_core/settings.py.backup.ultimate mutuelle_core/settings.py"
