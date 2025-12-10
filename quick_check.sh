#!/usr/bin/env bash
# quick_check.sh - Vérification rapide pour développement

echo "🔍 Vérification rapide Django..."
echo "================================"

# Vérifications de base
echo "1. Python..."
python --version || { echo "❌ Python manquant"; exit 1; }

echo "2. Django..."
python -c "import django; print(f'✅ Django {django.__version__}')" || { echo "❌ Django manquant"; exit 1; }

echo "3. Base de données..."
python manage.py check --database default 2>/dev/null && echo "✅ BD OK" || echo "⚠️  Problème BD"

echo "4. Migrations..."
python manage.py showmigrations --list | grep -c "\[ \]" | xargs test 0 -eq && echo "✅ Toutes migrées" || echo "⚠️  Migrations en attente"

echo "5. Static files..."
ls -la static/ staticfiles/ 2>/dev/null | head -5 && echo "✅ Static présents" || echo "⚠️  Static manquants"

echo "6. Settings..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()
from django.conf import settings
print(f'✅ Settings: DEBUG={settings.DEBUG}, DB={settings.DATABASES[\"default\"][\"ENGINE\"]}')
"

echo "7. Test serveur..."
timeout 2 python manage.py runserver --noreload 0.0.0.0:8888 &
SERVER_PID=$!
sleep 1
curl -s http://localhost:8888 > /dev/null && echo "✅ Serveur OK" || echo "⚠️  Serveur échec"
kill $SERVER_PID 2>/dev/null

echo "8. Dépendances critiques..."
for dep in Django gunicorn psycopg2-binary whitenoise; do
    python -c "import ${dep//-/_}" 2>/dev/null && echo "  ✅ $dep" || echo "  ⚠️  $dep manquant"
done

echo "================================"
echo "🎯 Vérification terminée!"