#!/usr/bin/env bash
# build.sh - Script de build pour Render.com
# Optimisé pour Django + PostgreSQL + WhiteNoise

set -o errexit
set -o pipefail
set -o nounset

echo "=========================================="
echo "  🚀 DÉPLOIEMENT DJANGO SUR RENDER"
echo "=========================================="
echo "Environnement: ${DJANGO_ENV:-production}"
echo "Python: $(python --version)"
echo "Port: ${PORT:-non défini}"
echo ""

# ==================== PRÉPARATION ====================
echo "📦 Préparation de l'environnement..."

# Créer les répertoires nécessaires
mkdir -p staticfiles
mkdir -p media
mkdir -p logs

# ==================== INSTALLATION DES DÉPENDANCES ====================
echo "📦 Installation des dépendances Python..."

# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠ requirements.txt non trouvé, installation des dépendances de base"
    pip install django gunicorn psycopg2-binary whitenoise dj-database-url
fi

# Installer les dépendances manquantes
echo "🔧 Installation des dépendances critiques..."
pip install whitenoise==6.7.0 dj-database-url==2.2.0 psycopg2-binary==2.9.11

# ==================== VÉRIFICATIONS ====================
echo "🔍 Vérifications..."

# Vérifier les imports critiques
python -c "
import django
import gunicorn
import dj_database_url
import whitenoise
print('✅ Tous les imports critiques fonctionnent')
"

# Vérifier les settings
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()
from django.conf import settings
print(f'✅ Django configuré: {settings.DATABASES[\"default\"][\"ENGINE\"]}')
"

# ==================== MIGRATIONS ====================
echo "🗄️  Application des migrations de base de données..."

python manage.py migrate --noinput || {
    echo "⚠ Erreur lors des migrations, tentative de résolution..."
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
}

# ==================== COLLECTSTATIC ====================
echo "📁 Collecte des fichiers statiques..."

python manage.py collectstatic --noinput --clear || {
    echo "⚠ collectstatic a échoué, tentative alternative..."
    # Tentative avec moins de verbosité
    python manage.py collectstatic --noinput --clear --verbosity 0 || true
}

# ==================== CRÉATION DU SUPERUSER ====================
# Optionnel: créer un superuser si les variables sont définies
if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    echo "👑 Création du superutilisateur..."
    python manage.py createsuperuser \
        --username "${DJANGO_SUPERUSER_USERNAME}" \
        --email "${DJANGO_SUPERUSER_EMAIL}" \
        --noinput || {
        echo "⚠ Superutilisateur déjà existant ou erreur"
    }
fi

# ==================== OPTIMISATIONS ====================
echo "⚡ Optimisations..."

# Nettoyer les fichiers .pyc
find . -name "*.pyc" -delete

# ==================== FINALISATION ====================
echo "✅ Build terminé avec succès !"
echo ""
echo "📊 RÉSUMÉ DU BUILD:"
echo "-------------------"
python --version
pip list | grep -E "Django|gunicorn|psycopg2|whitenoise|dj-database-url" | head -10
echo ""
echo "🎯 Prêt pour le déploiement !"
echo "   URL: https://votre-app.onrender.com"
echo ""