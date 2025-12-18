"""
SETTINGS ULTIME POUR RAILWAY - VERSION FORCÉE CSRF
"""

import os
from pathlib import Path
import sys
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================================
# 🚨 FORÇAGE ABSOLU DES VARIABLES RAILWAY - URGENT
# ============================================================================

print("\n" + "="*80)
print("🚨 FORÇAGE URGENT DES VARIABLES RAILWAY")
print("="*80)

# Variables CRITIQUES pour Railway - FORÇAGE ABSOLU
RAILWAY_FORCE_VARS = {
    'DEBUG': 'false',
    'SECRET_KEY': '*ut#lmdlu*r&jr&%*6de=k_e1u9r)@exjifan1y%c9^jyd$br5',
    'CSRF_TRUSTED_ORIGINS': 'https://web-production-abe5.up.railway.app,https://*.railway.app',
    'CSRF_COOKIE_SECURE': 'true',
    'SESSION_COOKIE_SECURE': 'true',
    'SECURE_SSL_REDIRECT': 'true',
    'SECURE_HSTS_SECONDS': '31536000',
    'ALLOWED_HOSTS': '.railway.app,localhost,127.0.0.1,web-production-abe5.up.railway.app',
}

# FORÇER chaque variable ABSOLUMENT
forced_count = 0
for var_name, forced_value in RAILWAY_FORCE_VARS.items():
    os.environ[var_name] = forced_value  # FORÇAGE ABSOLU
    forced_count += 1
    print(f"✅ FORCÉ: {var_name} = {forced_value[:50]}...")

print(f"\n✅ {forced_count} VARIABLES FORCÉES POUR RAILWAY")
print("="*80)

# ============================================================================
# 1. DÉTECTION ET CONFIGURATION DE BASE - AVEC VARIABLES FORCÉES
# ============================================================================

# Détection Railway - avec variable forcée
RAILWAY = 'RAILWAY' in os.environ or 'RAILWAY_ENVIRONMENT' in os.environ or 'RAILWAY_SERVICE_NAME' in os.environ

# Domaine Railway ABSOLU
RAILWAY_DOMAIN = 'web-production-abe5.up.railway.app'  # FORCÉ

print("\n" + "="*80)
print("⚡ SETTINGS ULTIME ACTIVÉ - VARIABLES FORCÉES")
print("="*80)
print(f"✅ Domaine FORCÉ: {RAILWAY_DOMAIN}")
print(f"✅ Railway détecté: {RAILWAY}")

# SECRET KEY - avec valeur forcée
SECRET_KEY = os.environ.get('SECRET_KEY', '*ut#lmdlu*r&jr&%*6de=k_e1u9r)@exjifan1y%c9^jyd$br5')

# DEBUG - avec valeur forcée
DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'

print(f"🔧 DEBUG = {DEBUG} (FORCÉ)")

# ============================================================================
# 2. CSRF - CONFIGURATION ABSOLUE ET FORCÉE
# ============================================================================

# FORÇAGE ABSOLU des origines CSRF
CSRF_TRUSTED_ORIGINS = []

# 1. Depuis l'environnement (déjà forcé)
env_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if env_csrf:
    CSRF_TRUSTED_ORIGINS.extend([x.strip() for x in env_csrf.split(',') if x.strip()])

# 2. FORÇAGE ABSOLU du domaine Railway
REQUIRED_CSRF_ORIGINS = [
    f'https://{RAILWAY_DOMAIN}',
    f'http://{RAILWAY_DOMAIN}',
    'https://*.railway.app',
    'http://*.railway.app',
    'https://*.up.railway.app',
    'http://*.up.railway.app',
]

# Ajouter FORCÉMENT toutes les origines requises
for origin in REQUIRED_CSRF_ORIGINS:
    if origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(origin)

# Nettoyer et dédupliquer
CSRF_TRUSTED_ORIGINS = list(set(
    [origin for origin in CSRF_TRUSTED_ORIGINS 
     if origin.startswith(('http://', 'https://'))]
))

# VÉRIFICATION FINALE ABSOLUE
REQUIRED_ORIGIN = f'https://{RAILWAY_DOMAIN}'
if REQUIRED_ORIGIN not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append(REQUIRED_ORIGIN)
    print(f"\n🚨 AJOUT FORCÉ ULTIME: {REQUIRED_ORIGIN}")

print(f"\n🔐 CSRF_TRUSTED_ORIGINS ({len(CSRF_TRUSTED_ORIGINS)} origines FORCÉES):")
for origin in sorted(CSRF_TRUSTED_ORIGINS)[:8]:
    print(f"   - {origin}")

# ============================================================================
# 3. COOKIES - CONFIGURATION ABSOLUE POUR RAILWAY
# ============================================================================

# Domain ABSOLU pour Railway (None est CRITIQUE)
CSRF_COOKIE_DOMAIN = None
SESSION_COOKIE_DOMAIN = None

# Secure ABSOLU (TRUE obligatoire pour Railway)
CSRF_COOKIE_SECURE = True  # FORCÉ à True
SESSION_COOKIE_SECURE = True  # FORCÉ à True

# SameSite (Lax fonctionne mieux)
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'

# HTTPOnly (False pour permettre l'accès JS)
CSRF_COOKIE_HTTPONLY = False

# Autres paramètres CSFORCÉS
CSRF_USE_SESSIONS = False
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'
CSRF_COOKIE_PATH = '/'
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_AGE = 31449600

print(f"\n🍪 COOKIES FORCÉS POUR RAILWAY:")
print(f"   - Domain: {CSRF_COOKIE_DOMAIN} (CRITIQUE: None)")
print(f"   - Secure: {CSRF_COOKIE_SECURE} (FORCÉ: True)")
print(f"   - SameSite: {CSRF_COOKIE_SAMESITE}")
print(f"   - HTTPOnly: {CSRF_COOKIE_HTTPONLY}")

# ============================================================================
# 4. PROXY & SECURITY - FORCÉ POUR RAILWAY
# ============================================================================

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Sécurité HTTPS FORCÉE
SECURE_SSL_REDIRECT = True  # FORCÉ à True
SECURE_HSTS_SECONDS = 31536000  # FORCÉ à 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

print(f"\n🌐 PROXY CONFIGURÉ: {SECURE_PROXY_SSL_HEADER}")
print("🔒 HTTPS redirection: FORCÉE ACTIVÉE")
print("🔒 HSTS: FORCÉ ACTIVÉ (1 an)")

# ============================================================================
# 5. ALLOWED_HOSTS - FORCÉ POUR RAILWAY
# ============================================================================

ALLOWED_HOSTS = []

# Domaine Railway FORCÉ
if RAILWAY_DOMAIN:
    ALLOWED_HOSTS.append(RAILWAY_DOMAIN)

# Patterns Railway FORCÉS
ALLOWED_HOSTS.extend([
    '.railway.app',
    '*.railway.app',
    '.up.railway.app',
    '*.up.railway.app',
])

# Local FORCÉ
ALLOWED_HOSTS.extend([
    'localhost',
    '127.0.0.1',
    '[::1]',
])

# Environnement (déjà forcé)
env_hosts = os.environ.get('ALLOWED_HOSTS', '')
if env_hosts:
    ALLOWED_HOSTS.extend([h.strip() for h in env_hosts.split(',') if h.strip()])

# Debug (jamais en production)
if DEBUG:
    ALLOWED_HOSTS.append('*')

ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))

print(f"\n🌍 ALLOWED_HOSTS ({len(ALLOWED_HOSTS)} hôtes FORCÉS):")
for host in sorted(ALLOWED_HOSTS)[:8]:
    print(f"   - {host}")

# ============================================================================
# 6. CORS - CONFIGURÉ POUR RAILWAY
# ============================================================================

CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOW_CREDENTIALS = True

if not CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS.copy()
else:
    CORS_ALLOWED_ORIGINS = []

CORS_ALLOW_METHODS = [
    'DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization', 'content-type',
    'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with',
]

print(f"\n🔗 CORS: {'Toutes origines (DEBUG)' if CORS_ALLOW_ALL_ORIGINS else 'Origines restreintes'}")

# ============================================================================
# 7. APPLICATIONS
# ============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    
    # Vos apps
    'agents',
    'api',
    'assureur',
    'communication',
    'core',
    'ia_detection',
    'inscription',
    'medecin',
    'membres',
    'mutuelle_core',
    'notifications',
    'paiements',
    'pharmacie_public',
    'pharmacien',
    'relances',
    'scoring',
    'soins',
]

# ============================================================================
# 8. MIDDLEWARE (ORDRE CRITIQUE)
# ============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Position critique
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

print("\n🔧 MIDDLEWARE: CsrfViewMiddleware positionné après SessionMiddleware")

# ============================================================================
# 9. DATABASE
# ============================================================================

if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True
        )
    }
    db_engine = 'PostgreSQL'
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    db_engine = 'SQLite'

print(f"\n🗄️  Base de données: {db_engine}")

# ============================================================================
# 10. TEMPLATES & URLS
# ============================================================================

ROOT_URLCONF = 'mutuelle_core.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
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

# ============================================================================
# 11. AUTHENTICATION
# ============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================================================
# 12. INTERNATIONALIZATION
# ============================================================================

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ============================================================================
# 13. STATIC FILES
# ============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False

print(f"\n📁 Fichiers statiques: {STATIC_ROOT}")

# ============================================================================
# 14. REST FRAMEWORK
# ============================================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}

# ============================================================================
# 15. DEFAULT PRIMARY KEY
# ============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================================
# 16. LOGGING
# ============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ============================================================================
# 17. VÉRIFICATION FINALE ABSOLUE
# ============================================================================

print("\n" + "="*80)
print("✅ CONFIGURATION ULTIME FORCÉE POUR RAILWAY")
print("="*80)

# Vérification ABSOLUE
CSRF_VERIFIED = f'https://{RAILWAY_DOMAIN}' in CSRF_TRUSTED_ORIGINS
COOKIES_SECURE = CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE
HTTPS_ENABLED = SECURE_SSL_REDIRECT

print(f"🔍 VÉRIFICATION CSRF: {'✅ OUI' if CSRF_VERIFIED else '❌ NON'}")
print(f"🔍 Cookies Secure: {'✅ OUI' if COOKIES_SECURE else '❌ NON'}")
print(f"🔍 HTTPS Redirection: {'✅ OUI' if HTTPS_ENABLED else '❌ NON'}")

if not CSRF_VERIFIED:
    print(f"\n🚨 CRITIQUE: Ajout FORCÉ de https://{RAILWAY_DOMAIN}")
    CSRF_TRUSTED_ORIGINS.append(f'https://{RAILWAY_DOMAIN}')

print(f"\n📊 RÉSUMÉ FINAL:")
print(f"   • Domaine: {RAILWAY_DOMAIN}")
print(f"   • DEBUG: {DEBUG} (FORCÉ: false)")
print(f"   • CSRF origines: {len(CSRF_TRUSTED_ORIGINS)} (FORCÉES)")
print(f"   • Cookies Secure: {CSRF_COOKIE_SECURE} (FORCÉ: True)")
print(f"   • HTTPS: {SECURE_SSL_REDIRECT} (FORCÉ: True)")

print("\n" + "="*80)
print("🚀 CONFIGURATION ABSOLUMENT FORCÉE POUR RAILWAY")
print("="*80)

# ============================================================================
# 18. FONCTION DE DEBUG CSRF (utile pour diagnostiquer)
# ============================================================================

def debug_csrf_failure(request, reason=""):
    """Fonction de debug pour les échecs CSRF"""
    from django.http import HttpResponseForbidden
    import json
    
    debug_info = {
        'error': 'CSRF verification failed',
        'detail': reason,
        'host': request.get_host(),
        'origin': request.headers.get('Origin', 'Non spécifié'),
        'referer': request.headers.get('Referer', 'Non spécifié'),
        'trusted_origins': CSRF_TRUSTED_ORIGINS,
        'railway_domain': RAILWAY_DOMAIN,
        'in_list': f'https://{RAILWAY_DOMAIN}' in CSRF_TRUSTED_ORIGINS,
        'debug': DEBUG,
        'timestamp': str(datetime.now()),
    }
    
    print(f"\n🚨 DEBUG CSRF FAILURE:")
    for key, value in debug_info.items():
        print(f"   {key}: {value}")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return HttpResponseForbidden(
            json.dumps(debug_info),
            content_type='application/json'
        )
    
    from django.views.csrf import csrf_failure
    return csrf_failure(request, reason)

# Optionnel: activer le debug CSRF
# CSRF_FAILURE_VIEW = 'mutuelle_core.settings.debug_csrf_failure'

# ============================================================================
# 19. IMPORT POUR DATETIME (ajouté pour la fonction debug)
# ============================================================================
from datetime import datetime

print("\n" + "="*80)
print("✅ TOUTES LES CONFIGURATIONS SONT FORCÉES POUR RAILWAY")
print("="*80)