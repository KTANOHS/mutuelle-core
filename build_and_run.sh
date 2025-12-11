#!/bin/bash
# build_and_run.sh - Script corrigé pour Render
set -e

echo "========================================"
echo "🚀 DÉPLOIEMENT DJANGO SUR RENDER"
echo "========================================"

# Vérifications
if [ ! -f "manage.py" ]; then
    echo "❌ ERREUR: manage.py non trouvé"
    exit 1
fi

# Dependencies
echo "📦 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# Static files
echo "📁 Fichiers statiques..."
python manage.py collectstatic --noinput

# Database
echo "🗄️  Migrations..."
python manage.py migrate --noinput

# Superuser
echo "👤 Superutilisateur..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@mutuelle.local', 'Admin123!')
    print('✅ Superutilisateur: admin / Admin123!')
else:
    print('✅ Superutilisateur existe déjà')
"

# Définir PORT par défaut si non défini
if [ -z "$PORT" ]; then
    PORT=10000
    echo "⚠️  PORT non défini, utilisation de la valeur par défaut: $PORT"
fi

# Afficher les informations
echo ""
echo "📊 INFORMATIONS DU PROJET"
echo "----------------------------------------"
echo "📁 Répertoire: $(pwd)"
echo "🐍 Python: $(python --version)"
echo "🎯 Django: $(python -c 'import django; print(django.get_version())')"
echo "🌐 Port: $PORT"
echo "🔧 DEBUG: $(python -c 'import os; print(os.environ.get(\"DEBUG\", \"False\"))')"

# Start server
echo ""
echo "6️⃣ DÉMARRAGE DU SERVEUR"
echo "========================================"
echo "🚀 Lancement de Gunicorn..."
echo "📢 L'application sera disponible sur: http://0.0.0.0:$PORT"
echo "========================================"

# Démarrer Gunicorn avec le port correct
exec gunicorn mutuelle_core.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile -