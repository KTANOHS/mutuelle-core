#!/bin/bash
set -o errexit

echo "🔧 Démarrage de l'application Django..."

# Activer l'environnement si nécessaire
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Appliquer les migrations
echo "🗄️  Application des migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

# Démarrer Gunicorn avec configuration optimisée
echo "🚀 Démarrage de Gunicorn..."
exec gunicorn mutuelle_core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 1 \
    --threads 2 \
    --timeout 60 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --access-logfile - \
    --error-logfile - \
    --log-level info