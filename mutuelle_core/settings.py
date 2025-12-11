"""
Django settings for mutuelle_core project.
Version optimisée pour Render.com + développement local
"""
import os
from pathlib import Path
from datetime import timedelta
import dj_database_url
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# CONFIGURATION ENVIRONNEMENT
# =============================================================================

# Détecter si on est sur Render
IS_RENDER = 'RENDER' in os.environ

# Environnement simple
IS_PRODUCTION = IS_RENDER or os.environ.get('DJANGO_ENV') == 'production'
IS_DEVELOPMENT = not IS_PRODUCTION

# DEBUG : False en production, True en développement
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# FORCER DEBUG=False en production
if IS_PRODUCTION:
    DEBUG = False
    print(f"⚙️ Mode PRODUCTION - DEBUG forcé à False")

# SECRET_KEY : gestion robuste
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if IS_PRODUCTION:
        # Générer une clé sécurisée pour Render
        SECRET_KEY = get_random_secret_key()
        print(f"🔑 Clé secrète générée automatiquement pour Render")
    else:
        # Clé de développement
        SECRET_KEY = 'django-dev-' + get_random_secret_key()
        print(f"🔑 Clé de développement générée automatiquement")

# =============================================================================
# ALLOWED_HOSTS - CONFIGURATION SÉCURISÉE
# =============================================================================
ALLOWED_HOSTS = []

# Toujours autoriser localhost pour le développement
if IS_DEVELOPMENT:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '[::1]'])
    print(f"🌐 Mode développement: localhost autorisé")

# Ajouter le host Render si présent
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    ALLOWED_HOSTS.append('.onrender.com')  # Tous les sous-domaines Render
    print(f"🌐 Render host détecté: {RENDER_EXTERNAL_HOSTNAME}")

# Ajouter les hosts depuis l'environnement
env_hosts = os.environ.get('ALLOWED_HOSTS', '')
if env_hosts:
    ALLOWED_HOSTS.extend([host.strip() for host in env_hosts.split(',') if host.strip()])

# Éviter les doublons et vérifier qu'on a au moins un host
ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('localhost')
    print(f"⚠️  Aucun host configuré, utilisation de 'localhost'")

print(f"✅ ALLOWED_HOSTS configurés: {ALLOWED_HOSTS}")

# =============================================================================
# SUITE DE LA CONFIGURATION
# =============================================================================

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Applications tierces
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'crispy_forms',
    'crispy_bootstrap5',
    'whitenoise.runserver_nostatic',
    
    # Vos applications
    'membres',
    'inscription',
    'paiements',
    'soins',
    'notifications',
    'api',
    'assureur',
    'medecin',
    'pharmacien',
    'core',
    'mutuelle_core',
    'pharmacie_public',
    'agents',
    'communication',
    'ia_detection',
    'scoring',
    'relances',
    'dashboard',
    
    'channels',
    'django_extensions',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Configuration de REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer' if DEBUG else None,
    ),
}

# Filtrer les renderers None
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    r for r in REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] if r is not None
]

# Configuration de JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Middleware - ORDRE CRITIQUE POUR RENDER
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # CRITIQUE: juste après SecurityMiddleware
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'membres.middleware.TrackingConnexionsMiddleware',  # Votre middleware personnalisé
]

ROOT_URLCONF = 'mutuelle_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'agents', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'agents.context_processors.agent_context',
                'core.utils.mutuelle_context',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'mutuelle_core.wsgi.application'
ASGI_APPLICATION = 'mutuelle_core.asgi.application'

# =============================================================================
# BASE DE DONNÉES
# =============================================================================

# Configuration par défaut (SQLite pour développement)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Sur Render.com ou si DATABASE_URL est défini, utiliser PostgreSQL
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    try:
        DATABASES['default'] = dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=IS_PRODUCTION,
        )
        print(f"✅ Base de données PostgreSQL configurée")
    except Exception as e:
        print(f"⚠️  Erreur configuration PostgreSQL: {e}")
        print(f"⚠️  Utilisation de SQLite comme fallback")
else:
    print(f"✅ Base de données SQLite configurée")

# =============================================================================
# FICHIERS STATIQUES - CONFIGURATION CRITIQUE POUR RENDER
# =============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'agents', 'static'),
]

# Configuration WhiteNoise optimisée pour Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuration WhiteNoise
WHITENOISE_USE_FINDERS = False  # Désactiver pour performance
WHITENOISE_AUTOREFRESH = DEBUG  # Auto-refresh seulement en développement
WHITENOISE_MAX_AGE = 31536000  # 1 an pour le cache

print(f"📁 WhiteNoise configuré pour les fichiers statiques")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Abidjan'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'English'),
]

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# CONFIGURATION SPÉCIFIQUE
# =============================================================================

LOGIN_REDIRECT_URL = '/redirect-after-login/'
LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = '/'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = 'mutuelle_sessionid'
SESSION_COOKIE_AGE = 1209600  # 2 semaines
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True

# =============================================================================
# SÉCURITÉ - CONFIGURATION POUR RENDER
# =============================================================================

# CSRF - Configuration pour Render
CSRF_TRUSTED_ORIGINS = []

if IS_PRODUCTION:
    # En production sur Render
    if RENDER_EXTERNAL_HOSTNAME:
        CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')
    CSRF_TRUSTED_ORIGINS.append('https://*.onrender.com')
    
    # Ajouter depuis l'environnement
    csrf_env = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
    if csrf_env:
        CSRF_TRUSTED_ORIGINS.extend([origin.strip() for origin in csrf_env.split(',') if origin.strip()])
else:
    # Développement local
    CSRF_TRUSTED_ORIGINS.extend([
        'http://localhost:8000',
        'http://127.0.0.1:8000',
        'http://localhost:3000',
    ])

# Cookies - Configuration pour Render
if IS_PRODUCTION and RENDER_EXTERNAL_HOSTNAME:
    # Production sur Render : HTTPS obligatoire
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Lax'  # 'None' si cross-domain, sinon 'Lax'
    CSRF_COOKIE_SAMESITE = 'Lax'
    print(f"🔒 Cookies sécurisés activés (HTTPS)")
else:
    # Développement local : HTTP seulement
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SAMESITE = 'Lax'
    print(f"🔓 Cookies non-sécurisés (HTTP)")

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # Doit être False pour AJAX

# CORS - Configuration simplifiée
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
    print(f"🔓 CORS: toutes les origines autorisées (développement)")
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOW_CREDENTIALS = True
    
    # Liste des origines autorisées en production
    CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS.copy()  # Mêmes que CSRF
    
    # S'assurer qu'il y a au moins une origine
    if not CORS_ALLOWED_ORIGINS:
        CORS_ALLOWED_ORIGINS.append('https://localhost')
    
    print(f"🔒 CORS: {len(CORS_ALLOWED_ORIGINS)} origines autorisées")

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@mutuelle.local'

# =============================================================================
# SÉCURITÉ PRODUCTION - CONFIGURATION POUR RENDER
# =============================================================================

if IS_PRODUCTION and RENDER_EXTERNAL_HOSTNAME:
    # Production sur Render : activer HTTPS
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    print(f"🔒 Redirection HTTPS activée")
else:
    # Développement local : DÉSACTIVER HTTPS
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = None
    print(f"🔓 Redirection HTTPS désactivée")

# Headers de sécurité (toujours actifs)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS - Seulement en production HTTPS
if IS_PRODUCTION and RENDER_EXTERNAL_HOSTNAME:
    SECURE_HSTS_SECONDS = 31536000  # 1 an
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_HSTS_SECONDS = 0

SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Logging simplifié pour Render
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {asctime} {module}: {message}',
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
        'mutuelle': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Configuration personnalisée
MUTUELLE_CONFIG = {
    'COTISATION_STANDARD': 5000,
    'COTISATION_FEMME_ENCEINTE': 7500,
    'FRAIS_CARTE': 2000,
    'AVANCE': 10000,
    'CMU_OPTION': 1000,
    'REVERSION_CLINIQUE': 2000,
    'REVERSION_PHARMACIE': 2000,
    'CAISSE_MUTUELLE': 1000,
    'LIMITE_BONS_QUOTIDIENNE': 10,
    'DUREE_VALIDITE_BON': 24,
}

# Channels (pour websockets si nécessaire)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# =============================================================================
# FIN DE LA CONFIGURATION
# =============================================================================

# Créer les dossiers nécessaires
for folder in ['logs', 'media', 'staticfiles']:
    folder_path = os.path.join(BASE_DIR, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

print(f"🚀 Configuration Django chargée")
print(f"   Environnement: {'PRODUCTION' if IS_PRODUCTION else 'DÉVELOPPEMENT'}")
print(f"   DEBUG: {DEBUG}")
print(f"   STATIC_ROOT: {STATIC_ROOT}")
print(f"   Base de données: {'PostgreSQL' if DATABASE_URL else 'SQLite'}")