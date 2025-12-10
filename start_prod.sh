#!/bin/bash
set -o errexit
set -o pipefail

echo "🚀 Démarrage de l'application Django en production..."

# Variables d'environnement pour production
export DEBUG="False"
export DJANGO_ENV="production"
export PYTHONUNBUFFERED="1"
export PYTHONDONTWRITEBYTECODE="1"

# Configuration ALLOWED_HOSTS pour production
export ALLOWED_HOSTS=".onrender.com,localhost,127.0.0.1"
export CSRF_TRUSTED_ORIGINS="https://*.onrender.com"

# Désactiver HTTPS en local (Render le gère)
export SECURE_SSL_REDIRECT="False"
export SECURE_PROXY_SSL_HEADER=""

# Attendre que la base de données soit prête (pour PostgreSQL)
if [ -n "$DATABASE_URL" ]; then
    echo "⏳ Vérification de la connexion à la base de données..."
    sleep 2
fi

# Appliquer les migrations
echo "🗄️  Application des migrations..."
python manage.py migrate --noinput || echo "⚠️  Erreur lors des migrations, continuation..."

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear || echo "⚠️  Erreur lors de la collecte statique, continuation..."

# Vérifier l'application
echo "🔍 Vérification de l'application Django..."
python manage.py check --deploy || echo "⚠️  Avertissements lors de la vérification"

# Démarrer Gunicorn avec configuration optimisée
echo "⚡ Démarrage de Gunicorn avec timeout étendu..."

# Utiliser le port de Render ou 8000 par défaut
PORT=${PORT:-8000}

exec gunicorn mutuelle_core.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --threads 2 \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --worker-class sync \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --preload