#!/bin/bash
# SCRIPT DE DÉMARRAGE ULTIME POUR RENDER
set -e  # Arrêter en cas d'erreur

echo "🚀 DÉMARRAGE SUR RENDER - MUTUELLE CORE"
echo "======================================="

# Vérifier l'environnement
echo "🌐 Environnement:"
echo "   RENDER: $RENDER"
echo "   PORT: $PORT"
echo "   PWD: $(pwd)"
echo "   Python: $(python --version)"

# Afficher les fichiers
echo "📁 Fichiers présents:"
ls -la

# Appliquer les migrations FORCÉES
echo "🔄 APPLICATION DES MIGRATIONS (FORCÉ)..."
python manage.py migrate --noinput

# Vérifier les migrations
echo "📊 ÉTAT DES MIGRATIONS:"
python manage.py showmigrations --list 2>/dev/null || echo "⚠️ Impossible d'afficher les migrations"

# Collecter les statiques (au cas où)
echo "📁 COLLECTE DES FICHIERS STATIQUES..."
python manage.py collectstatic --noinput

# Vérifier que l'application Django fonctionne
echo "🧪 TEST DE L'APPLICATION DJANGO..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()
print('✅ Django chargé avec succès!')
from django.conf import settings
print(f'   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
print(f'   DEBUG: {settings.DEBUG}')
"

# Démarrer Gunicorn
echo "🚀 DÉMARRAGE DE GUNICORN..."
echo "   Port: $PORT"
echo "   Application: app:application"
echo "   Workers: ${WEB_CONCURRENCY:-1}"

exec gunicorn app:application \
    --bind 0.0.0.0:$PORT \
    --workers ${WEB_CONCURRENCY:-1} \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info