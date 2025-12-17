"""
SETTINGS ULTIME POUR RAILWAY - TOUT EN UN - VERSION CORRIGÉE
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================================
# 1. CONFIGURATION PRODUCTION
# ============================================================================

# A. DOMAINE RAILWAY CORRECT
RAILWAY_DOMAIN = os.environ.get('RAILWAY_DOMAIN', 'web-production-abe5.up.railway.app')

print("\n" + "="*80)
print("⚡ SETTINGS ULTIME ACTIVÉ")
print("="*80)

# B. DEBUG - CORRECTION CRITIQUE
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
print(f"🔧 DEBUG = {DEBUG}")

# C. SECRET KEY - Déjà bonne
SECRET_KEY = os.environ.get('SECRET_KEY', 'q3b&jf0=w%0(%4k+_nu%rhazl7mez)xh0grl6s^b#ta!^e#yop')

# ============================================================================
# 2. CSRF - CORRIGÉ
# ============================================================================

# Lecture depuis variables d'environnement
CSRF_TRUSTED_ORIGINS = []

# 1. Depuis variable d'environnement
env_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if env_csrf:
    CSRF_TRUSTED_ORIGINS.extend([x.strip() for x in env_csrf.split(',') if x.strip()])

# 2. Ajouter le domaine Railway
if f'https://{RAILWAY_DOMAIN}' not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RAILWAY_DOMAIN}')
    CSRF_TRUSTED_ORIGINS.append(f'http://{RAILWAY_DOMAIN}')

# 3. Ajouter les wildcards Railway
CSRF_TRUSTED_ORIGINS.append('https://*.railway.app')
CSRF_TRUSTED_ORIGINS.append('http://*.railway.app')

# 4. Filtrer (Django 4.0)
CSRF_TRUSTED_ORIGINS = [
    origin for origin in CSRF_TRUSTED_ORIGINS 
    if origin.startswith(('http://', 'https://'))
]
CSRF_TRUSTED_ORIGINS = list(set(CSRF_TRUSTED_ORIGINS))

print(f"\n🔐 CSRF_TRUSTED_ORIGINS ({len(CSRF_TRUSTED_ORIGINS)} origines):")
for origin in CSRF_TRUSTED_ORIGINS[:8]:
    print(f"   - {origin}")

# ============================================================================
# 3. PROXY RAILWAY
# ============================================================================
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# ============================================================================
# 4. COOKIES - PRODUCTION
# ============================================================================
CSRF_COOKIE_DOMAIN = None
SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'True').lower() == 'true'
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
CSRF_COOKIE_HTTPONLY = True  # ✅ Changé à True pour la sécurité
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SAMESITE = 'Lax'

print(f"\n🍪 COOKIES: SECURE={CSRF_COOKIE_SECURE}, HTTPONLY={CSRF_COOKIE_HTTPONLY}")

# ============================================================================
# 5. ALLOWED_HOSTS - PRODUCTION SÉCURISÉE
# ============================================================================
ALLOWED_HOSTS = []

# 1. Depuis variable d'environnement
env_hosts = os.environ.get('ALLOWED_HOSTS', '')
if env_hosts:
    ALLOWED_HOSTS.extend([x.strip() for x in env_hosts.split(',') if x.strip()])

# 2. Ajouter le domaine Railway
ALLOWED_HOSTS.append(RAILWAY_DOMAIN)
ALLOWED_HOSTS.append(f'.{RAILWAY_DOMAIN}')
ALLOWED_HOSTS.append('.railway.app')

# 3. Localhost pour développement
if DEBUG:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '[::1]'])

ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))

print(f"\n🌍 ALLOWED_HOSTS: {len(ALLOWED_HOSTS)} hosts")

# ============================================================================
# 6. CORS - PRODUCTION
# ============================================================================
CORS_ALLOW_ALL_ORIGINS = False  # ✅ Changé à False pour la sécurité
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    f'https://{RAILWAY_DOMAIN}',
    'https://*.railway.app',
]

# Ajouter depuis variable d'environnement
env_cors = os.environ.get('CORS_ALLOWED_ORIGINS', '')
if env_cors:
    CORS_ALLOWED_ORIGINS.extend([x.strip() for x in env_cors.split(',') if x.strip()])

print(f"\n🔗 CORS: {len(CORS_ALLOWED_ORIGINS)} origines autorisées")

# ============================================================================
# 7. APPLICATIONS INSTALLÉES (inchangé)
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
    'apps',
    'rapports_performance',
    'rapports_surveillance',
]

# ... [Le reste du fichier reste identique] ...

print("\n" + "="*80)
print("✅ CONFIGURATION PRODUCTION PRÊTE")
print("="*80)

if DEBUG:
    print("\n⚠️  ATTENTION: DEBUG est ACTIVÉ (mode développement)")
    print("   En production, assurez-vous que DEBUG=False")
else:
    print("\n✅ MODE PRODUCTION: DEBUG est DÉSACTIVÉ")

print(f"\n📊 RÉSUMÉ:")
print(f"   - Domaine: {RAILWAY_DOMAIN}")
print(f"   - DEBUG: {DEBUG}")
print(f"   - CSRF origines: {len(CSRF_TRUSTED_ORIGINS)}")
print(f"   - Hôtes autorisés: {len(ALLOWED_HOSTS)}")
print(f"   - Cookies secure: {CSRF_COOKIE_SECURE}")
print(f"   - CORS restrictif: {not CORS_ALLOW_ALL_ORIGINS}")

print("\n" + "="*80)
print("🚀 APPLICATION EN PRODUCTION")
print("="*80)