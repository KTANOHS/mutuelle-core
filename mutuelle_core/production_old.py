"""
Configuration Django pour l'environnement de production
Optimisé pour déploiement sur Render.com
"""
import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key

# ==================== CONFIGURATION DE BASE ====================
# Détermine l'environnement
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'production')
IS_PRODUCTION = DJANGO_ENV == 'production'
IS_DEVELOPMENT = not IS_PRODUCTION

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ==================== SECRET KEY ====================
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if IS_PRODUCTION:
        # EN PRODUCTION: ÉCHEC SI PAS DE SECRET_KEY
        raise ValueError(
            "❌ ERREUR CRITIQUE: SECRET_KEY doit être définie en production!\n"
            "Définissez la variable d'environnement SECRET_KEY sur Render.com"
        )
    else:
        SECRET_KEY = 'django-insecure-developpement-local-seulement-changez-moi-en-production'

# ==================== DEBUG ====================
# CORRECTION CRITIQUE: DEBUG doit toujours être False en production
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Forcer DEBUG=False en production quelle que soit la variable d'environnement
if IS_PRODUCTION:
    DEBUG = False  # FORCÉ À FALSE EN PRODUCTION
    print("⚙️ DEBUG forcé à False pour la production")
elif IS_DEVELOPMENT and DEBUG:
    print("⚙️ Mode développement avec DEBUG=True")

# ==================== ALLOWED_HOSTS ====================
ALLOWED_HOSTS = []

# Ajouter les hôtes depuis l'environnement
env_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS')
if env_hosts:
    ALLOWED_HOSTS.extend(env_hosts.split(','))

# Ajouter les hôtes par défaut selon l'environnement
if IS_PRODUCTION:
    # En production: uniquement les hôtes spécifiques
    default_hosts = [
        '.onrender.com',  # Tous les sous-domaines Render
        '.vercel.app',    # Vercel (au cas où)
    ]
    
    # Ajouter un domaine spécifique si défini
    domain = os.environ.get('DOMAIN_NAME')
    if domain:
        ALLOWED_HOSTS.append(domain)
        ALLOWED_HOSTS.append(f'.{domain}')  # Tous les sous-domaines
        
    # N'AJOUTEZ PAS '*' EN PRODUCTION!
    
else:
    # En développement
    default_hosts = [
        'localhost',
        '127.0.0.1',
        '[::1]',
        '0.0.0.0',
    ]
    
    # Pour les tests locaux
    if DEBUG:
        ALLOWED_HOSTS.append('*')

# Ajouter les hôtes par défaut
for host in default_hosts:
    if host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(host)

# ==================== APPLICATIONS ====================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Applications tierces
    'rest_framework',
    'corsheaders',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_extensions',
    
    # Applications locales
    'core',
    'accounts',
    'assureur',
    'medecin',
    'pharmacien',
    'agents',
    'communication',
    'paiements',
    'bon_de_soin',
]

# ==================== MIDDLEWARE ====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise pour les fichiers statiques
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==================== BASE DE DONNÉES ====================
# Gestion robuste de dj-database-url
try:
    import dj_database_url
    DJ_DATABASE_URL_AVAILABLE = True
except ImportError:
    DJ_DATABASE_URL_AVAILABLE = False
    print("⚠ dj-database-url non installé, utilisation de PostgreSQL natif")

# Configuration des bases de données
if IS_PRODUCTION:
    # En production, utiliser DATABASE_URL de Render
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if DATABASE_URL and DJ_DATABASE_URL_AVAILABLE:
        DATABASES = {
            'default': dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=600,
                ssl_require=True
            )
        }
    else:
        # Fallback PostgreSQL natif
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('DB_NAME', 'mutuelle_prod'),
                'USER': os.environ.get('DB_USER', 'postgres'),
                'PASSWORD': os.environ.get('DB_PASSWORD', ''),
                'HOST': os.environ.get('DB_HOST', 'localhost'),
                'PORT': os.environ.get('DB_PORT', '5432'),
                'CONN_MAX_AGE': 600,
            }
        }
else:
    # En développement, utiliser SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ==================== FICHIERS STATIQUES ====================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_ALLOW_ALL_ORIGINS = True

# ==================== MÉDIA FILES ====================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==================== TEMPLATES ====================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'core/templates',
            BASE_DIR / 'accounts/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.settings_context',
            ],
            'debug': DEBUG,  # Utiliser la variable DEBUG
        },
    },
]

# ==================== SÉCURITÉ ====================
# CORRECTION: Toujours activer ces paramètres en production
SECURE_SSL_REDIRECT = IS_PRODUCTION
SESSION_COOKIE_SECURE = IS_PRODUCTION
CSRF_COOKIE_SECURE = IS_PRODUCTION
CSRF_TRUSTED_ORIGINS = []

# Ajouter les origines de confiance
trusted_origins = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if trusted_origins:
    CSRF_TRUSTED_ORIGINS.extend(trusted_origins.split(','))

# Ajouter les origines Render par défaut
if IS_PRODUCTION:
    CSRF_TRUSTED_ORIGINS.extend([
        'https://*.onrender.com',
        'https://*.vercel.app',
    ])
    
    # Ajouter le domaine spécifique
    domain = os.environ.get('DOMAIN_NAME')
    if domain:
        CSRF_TRUSTED_ORIGINS.append(f'https://{domain}')
        CSRF_TRUSTED_ORIGINS.append(f'https://*.{domain}')

# HSTS - Important pour la sécurité
if IS_PRODUCTION:
    SECURE_HSTS_SECONDS = 31536000  # 1 an
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Proxy SSL - Important pour Render/Heroku
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ==================== CORS ====================
CORS_ALLOWED_ORIGINS = []
cors_origins = os.environ.get('CORS_ALLOWED_ORIGINS', '')
if cors_origins:
    CORS_ALLOWED_ORIGINS.extend(cors_origins.split(','))

if IS_DEVELOPMENT:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False  # IMPORTANT: Désactivé en production

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# En production, restreindre davantage
if IS_PRODUCTION:
    CORS_EXPOSE_HEADERS = []
    CORS_ALLOW_CREDENTIALS = False

# ==================== AUTHENTIFICATION ====================
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backends.EmailBackend',
]

AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/redirect-after-login/'
LOGOUT_REDIRECT_URL = '/'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ==================== INTERNATIONALISATION ====================
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==================== EMAIL ====================
if IS_PRODUCTION:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
    DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@mutuelle.com')
    SERVER_EMAIL = DEFAULT_FROM_EMAIL
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ==================== CACHE ====================
if IS_PRODUCTION:
    REDIS_URL = os.environ.get('REDIS_URL')
    if REDIS_URL:
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.redis.RedisCache',
                'LOCATION': REDIS_URL,
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                    'SSL': True,  # Important pour Redis Cloud
                },
                'KEY_PREFIX': 'mutuelle',
            }
        }
    else:
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake',
            }
        }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# ==================== REST FRAMEWORK ====================
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
    ] + (['rest_framework.renderers.BrowsableAPIRenderer'] if DEBUG else []),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# ==================== CRISPY FORMS ====================
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ==================== LOGGING ====================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {module} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
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
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'mutuelle': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ==================== CONFIGURATIONS SPÉCIFIQUES ====================
# Désactiver l'interface admin si nécessaire
ADMIN_ENABLED = os.environ.get('ADMIN_ENABLED', 'True') == 'True'
if not ADMIN_ENABLED:
    INSTALLED_APPS.remove('django.contrib.admin')

# Configuration pour tests
if os.environ.get('RUNNING_TESTS'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

# ==================== FIN DE CONFIGURATION ====================
print(f"🎯 Environnement: {'PRODUCTION' if IS_PRODUCTION else 'DÉVELOPPEMENT'}")
print(f"✅ Configuration chargée - DEBUG={DEBUG} - Hosts: {ALLOWED_HOSTS[:3]}")
print(f"📁 STATIC_ROOT: {STATIC_ROOT} - Existe: {STATIC_ROOT.exists()}")

# Avertissement sécurité
if IS_PRODUCTION and DEBUG:
    print("""
    ⚠️  ATTENTION: DEBUG=True en production!
    C'est une faille de sécurité grave.
    Vérifiez vos variables d'environnement.
    """)