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

# Détecter l'environnement Railway
RAILWAY = os.environ.get('RAILWAY') == 'true' or os.environ.get('RAILWAY') == 'True'
RAILWAY_PUBLIC_DOMAIN = os.environ.get('RAILWAY_STATIC_URL', '')

# Environnement simple
IS_PRODUCTION = RAILWAY or os.environ.get('DJANGO_ENV') == 'production'
IS_DEVELOPMENT = not IS_PRODUCTION

# DEBUG : False en production, True en développement
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true' if IS_DEVELOPMENT else False

# FORCER DEBUG=False en production
if IS_PRODUCTION:
    DEBUG = False
    print(f"⚙️ Mode PRODUCTION - DEBUG forcé à False")

# SECRET_KEY : gestion robuste
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if IS_PRODUCTION:
        # Générer une clé sécurisée pour Railway
        SECRET_KEY = get_random_secret_key()
        print(f"🔑 Clé secrète générée automatiquement pour Railway")
    else:
        # Clé de développement
        SECRET_KEY = 'django-dev-' + get_random_secret_key()
        print(f"🔑 Clé de développement générée automatiquement")

# =============================================================================
# ALLOWED_HOSTS - CONFIGURATION SÉCURISÉE
# =============================================================================
ALLOWED_HOSTS = []

# Mode développement local
if IS_DEVELOPMENT:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '[::1]', '0.0.0.0'])
    if DEBUG:
        ALLOWED_HOSTS.append('*')  # Pour faciliter le dev, retirer en prod
    print(f"🌐 Mode développement: localhost autorisé")

# Mode production sur Railway
if RAILWAY:
    # Domaine Railway principal
    railway_domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '')
    if railway_domain:
        ALLOWED_HOSTS.append(railway_domain)
    
    # Domaine générique Railway
    ALLOWED_HOSTS.append('.railway.app')
    
    print(f"🌐 Railway host détecté: {railway_domain or '.railway.app'}")

# Ajouter les hosts depuis l'environnement
env_hosts = os.environ.get('ALLOWED_HOSTS', '')
if env_hosts:
    ALLOWED_HOSTS.extend([host.strip() for host in env_hosts.split(',') if host.strip()])

# Éviter les doublons et nettoyer
ALLOWED_HOSTS = list(set([h for h in ALLOWED_HOSTS if h]))
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
    print(f"⚠️  Aucun host configuré, utilisation de hosts par défaut")

print(f"✅ ALLOWED_HOSTS configurés: {ALLOWED_HOSTS}")

# =============================================================================
# APPLICATION DEFINITION
# =============================================================================

INSTALLED_APPS = [
    # Django core
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
    'django_filters',
    'django_extensions',
    
    # Vos applications (dans l'ordre logique)
    'core',
    'membres',
    'inscription',
    'paiements',
    'soins',
    'notifications',
    'assureur',
    'medecin',
    'pharmacien',
    'pharmacie_public',
    'agents',
    'communication',
    'ia_detection',
    'scoring',
    'relances',
    'dashboard',
    'api',  # API REST doit être en dernier pour éviter les conflits d'import
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# =============================================================================
# MIDDLEWARE - ORDRE CRITIQUE
# =============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # CRITIQUE pour les fichiers statiques
    'corsheaders.middleware.CorsMiddleware',  # Après WhiteNoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'mutuelle_core.urls'

# =============================================================================
# TEMPLATES
# =============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'agents' / 'templates',
            BASE_DIR / 'core' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'core.context_processors.mutuelle_context',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'mutuelle_core.wsgi.application'

# =============================================================================
# BASE DE DONNÉES - CONFIGURATION RAILWAY
# =============================================================================

# Configuration par défaut (SQLite pour développement)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Utiliser PostgreSQL sur Railway via DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    try:
        # Configuration PostgreSQL pour Railway
        db_config = dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=IS_PRODUCTION,
        )
        
        # S'assurer que ENGINE est correct
        if 'ENGINE' in db_config:
            db_config['ENGINE'] = 'django.db.backends.postgresql'
        
        DATABASES['default'] = db_config
        print(f"✅ Base de données PostgreSQL configurée via DATABASE_URL")
    except Exception as e:
        print(f"⚠️  Erreur configuration PostgreSQL: {e}")
        print(f"⚠️  Utilisation de SQLite comme fallback")
else:
    print(f"✅ Base de données SQLite configurée (développement local)")

# =============================================================================
# FICHIERS STATIQUES - CONFIGURATION RAILWAY
# =============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Dossiers où Django cherchera les fichiers statiques
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'core' / 'static',
    BASE_DIR / 'agents' / 'static',
]

# Configuration WhiteNoise optimisée pour Railway
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Options WhiteNoise
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG  # Auto-refresh seulement en développement
WHITENOISE_MAX_AGE = 31536000  # 1 an pour le cache

print(f"📁 WhiteNoise configuré pour les fichiers statiques")

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# VALIDATION DES MOTS DE PASSE
# =============================================================================

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

# =============================================================================
# INTERNATIONALISATION
# =============================================================================

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Abidjan'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'English'),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# CONFIGURATION AUTHENTIFICATION
# =============================================================================

LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = '/'

# =============================================================================
# REST FRAMEWORK CONFIGURATION
# =============================================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer' if DEBUG else None,
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}

# Filtrer les renderers None
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    r for r in REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] if r is not None
]

# =============================================================================
# SIMPLE JWT CONFIGURATION
# =============================================================================

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# =============================================================================
# SÉCURITÉ - CONFIGURATION POUR RAILWAY
# =============================================================================

# CSRF - Configuration pour Railway
CSRF_TRUSTED_ORIGINS = []

if RAILWAY:
    # En production sur Railway
    if RAILWAY_PUBLIC_DOMAIN:
        CSRF_TRUSTED_ORIGINS.append(f'https://{RAILWAY_PUBLIC_DOMAIN}')
    CSRF_TRUSTED_ORIGINS.extend([
        'https://*.railway.app',
        'https://web-production-*.up.railway.app',
    ])
else:
    # Développement local
    CSRF_TRUSTED_ORIGINS.extend([
        'http://localhost:8000',
        'http://127.0.0.1:8000',
        'http://0.0.0.0:8000',
    ])

# Cookies - Configuration pour Railway
if RAILWAY:
    # Production sur Railway : HTTPS obligatoire
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    print(f"🔒 Cookies sécurisés et HTTPS activés (Railway)")
else:
    # Développement local : HTTP seulement
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    print(f"🔓 Cookies non-sécurisés (développement local)")

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# =============================================================================
# CORS CONFIGURATION
# =============================================================================

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    print(f"🔓 CORS: toutes les origines autorisées (développement)")
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS.copy()
    print(f"🔒 CORS: {len(CORS_ALLOWED_ORIGINS)} origines autorisées")

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']

# =============================================================================
# SÉCURITÉ PRODUCTION
# =============================================================================

# Headers de sécurité (toujours actifs)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS - Seulement en production HTTPS
if RAILWAY:
    SECURE_HSTS_SECONDS = 31536000  # 1 an
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

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
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'mutuelle': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# =============================================================================
# CONFIGURATION PERSONNALISÉE
# =============================================================================

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

# =============================================================================
# CRÉATION DES DOSSIERS NÉCESSAIRES
# =============================================================================

# Créer les dossiers nécessaires pour Railway
for folder in ['staticfiles', 'media', 'logs']:
    folder_path = BASE_DIR / folder
    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Dossier créé: {folder_path}")

# =============================================================================
# CONFIGURATION FINALE
# =============================================================================

print(f"🚀 Configuration Django chargée avec succès")
print(f"   Environnement: {'PRODUCTION (Railway)' if RAILWAY else 'DÉVELOPPEMENT'}")
print(f"   DEBUG: {DEBUG}")
print(f"   Base de données: {'PostgreSQL' if DATABASE_URL else 'SQLite'}")
print(f"   Hosts autorisés: {', '.join(ALLOWED_HOSTS[:3])}{'...' if len(ALLOWED_HOSTS) > 3 else ''}")
print(f"   Fichiers statiques: {STATIC_ROOT}")