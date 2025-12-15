#!/bin/bash
# LA SOLUTION LA PLUS SIMPLE
echo "🔄 REMPLACEMENT SIMPLE DU settings.py"

# Créez un settings.py ULTRA simple
cat > mutuelle_core/settings.py << 'SIMPLE'
import os
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
DEBUG = True
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://web-production-555c.up.railway.app', 'http://web-production-555c.up.railway.app']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_DOMAIN = None
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db.sqlite3'}}
INSTALLED_APPS = ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware']
ROOT_URLCONF = 'mutuelle_core.urls'
WSGI_APPLICATION = 'mutuelle_core.wsgi.application'
print("✅ Settings ultra simple chargé")
SIMPLE

echo "✅ Settings.py remplacé"
echo ""
echo "📝 Maintenant déployez:"
echo "git add ."
echo "git commit -m 'Ultra simple settings for Railway'"
echo "git push railway main"
echo ""
echo "🎯 Cela DEVRAIT résoudre le problème CSRF immédiatement."
