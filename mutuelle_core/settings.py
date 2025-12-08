"""
Django settings for mutuelle_core project.
Version optimisée pour Render.com + développement local
"""
import os
from pathlib import Path
from datetime import timedelta
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# CONFIGURATION ENVIRONNEMENT
# =============================================================================

# Détecter si on est sur Render
IS_RENDER = os.environ.get('RENDER', False)

# DEBUG : True par défaut en local, False sur Render
DEBUG = os.environ.get('DJANGO_DEBUG', 'True' if not IS_RENDER else 'False') == 'True'

# SECRET_KEY : développement par défaut, production sur Render
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 
    'django-insecure-dev-key-change-in-production' if DEBUG else 
    os.environ.get('SECRET_KEY', 'fallback-production-key')
)

# =============================================================================
# ALLOWED_HOSTS - CONFIGURATION INTELLIGENTE
# =============================================================================
ALLOWED_HOSTS = []

# Toujours autoriser localhost en développement
if DEBUG:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '[::1]'])

# Ajouter le host Render si présent
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Ajouter les hosts depuis l'environnement
env_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
if env_hosts:
    ALLOWED_HOSTS.extend([host.strip() for host in env_hosts.split(',') if host.strip()])

# En production, s'assurer qu'on a au moins un host
if not DEBUG and not ALLOWED_HOSTS:
    # Si pas DEBUG et pas de hosts, ajouter une valeur par défaut sécurisée
    if IS_RENDER:
        ALLOWED_HOSTS.append('.onrender.com')  # Tous les sous-domaines Render
    else:
        # En production non-Render, lever une erreur explicative
        print("⚠️  ATTENTION: DEBUG=False mais ALLOWED_HOSTS vide!")
        print("   Pour développement local, définissez DEBUG=True")
        print("   Pour production, définissez DJANGO_ALLOWED_HOSTS")
        # Autoriser temporairement localhost pour éviter l'erreur
        ALLOWED_HOSTS.append('localhost')

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
}

# Configuration de JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'membres.middleware.TrackingConnexionsMiddleware',
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
        },
    },
]

WSGI_APPLICATION = 'mutuelle_core.wsgi.application'

# =============================================================================
# BASE DE DONNÉES
# =============================================================================

# Par défaut SQLite pour le développement
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Sur Render.com, utiliser PostgreSQL
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )

# =============================================================================
# FICHIERS STATIQUES - CORRIGÉ
# =============================================================================

STATIC_URL = '/static/'

# ⚠️ CORRECTION IMPORTANTE : STATIC_ROOT TOUJOURS DÉFINI (même en développement)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'agents', 'static'),
]

# Configuration selon l'environnement
if DEBUG:
    # En développement : servir depuis STATICFILES_DIRS
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    # En production : utiliser WhiteNoise optimisé
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    # Optimisations WhiteNoise pour la production
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_MANIFEST_STRICT = False
    WHITENOISE_ALLOW_ALL_ORIGINS = True

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
SESSION_COOKIE_AGE = 1209600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True

# Sécurité ajustée selon l'environnement
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@mutuelle.local'

# =============================================================================
# SÉCURITÉ PRODUCTION
# =============================================================================

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}', 'style': '{'},
        'simple': {'format': '{levelname} {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'simple'},
        'file': {'level': 'INFO', 'class': 'logging.FileHandler', 'filename': os.path.join(BASE_DIR, 'logs', 'django.log'), 'formatter': 'verbose'},
    },
    'loggers': {
        'django': {'handlers': ['console', 'file'], 'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO')},
        'agents': {'handlers': ['console', 'file'], 'level': 'INFO', 'propagate': False},
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

# Channels
ASGI_APPLICATION = 'mutuelle_core.asgi.application'
CHANNEL_LAYERS = {
    'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'},
}

# =============================================================================
# FIN DE LA CONFIGURATION
# =============================================================================

# Créer les dossiers nécessaires
for folder in ['logs', 'media', 'staticfiles']:
    folder_path = os.path.join(BASE_DIR, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

print(f"✅ Configuration chargée - DEBUG={DEBUG} - Hosts: {ALLOWED_HOSTS}")
print(f"📁 STATIC_ROOT: {STATIC_ROOT} - Existe: {os.path.exists(STATIC_ROOT)}")