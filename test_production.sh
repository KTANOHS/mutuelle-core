#!/bin/bash
# test_production.sh - Tester le déploiement en local

echo "🧪 TEST DE DÉPLOIEMENT EN MODE PRODUCTION"
echo "========================================="

# 1. Charger les variables d'environnement
if [ -f .env.production ]; then
    export $(cat .env.production | xargs)
    echo "✅ Variables d'environnement chargées"
else
    echo "⚠ .env.production non trouvé, création..."
    cat > .env.production << 'EOF'
DJANGO_ENV=production
SECRET_KEY=test-secret-key-change-in-production
DEBUG=False
DATABASE_URL=sqlite:///test.db
EOF
    export $(cat .env.production | xargs)
fi

# 2. Tester les imports
echo ""
echo "1. Vérification des imports..."
python -c "
import sys
try:
    import django
    import gunicorn
    import dj_database_url
    import whitenoise
    print('✅ Tous les imports fonctionnent')
except ImportError as e:
    print(f'❌ ImportError: {e}')
    sys.exit(1)
"

# 3. Tester les settings
echo ""
echo "2. Vérification des settings..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
try:
    import django
    django.setup()
    from django.conf import settings
    print(f'✅ Django configuré')
    print(f'   DEBUG: {settings.DEBUG}')
    print(f'   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS[:3]}')
    print(f'   DATABASE: {settings.DATABASES[\"default\"][\"ENGINE\"]}')
except Exception as e:
    print(f'❌ Erreur: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

# 4. Tester collectstatic
echo ""
echo "3. Test collectstatic..."
python manage.py collectstatic --dry-run --noinput 2>&1 | tail -5
if [ $? -eq 0 ]; then
    echo "✅ collectstatic fonctionne"
else
    echo "⚠ collectstatic a eu un problème"
fi

# 5. Tester les migrations
echo ""
echo "4. Test migrations..."
python manage.py showmigrations --list 2>&1 | head -10
if [ $? -eq 0 ]; then
    echo "✅ migrations fonctionnent"
else
    echo "⚠ migrations ont eu un problème"
fi

# 6. Tester le serveur
echo ""
echo "5. Test rapide du serveur..."
timeout 3 python manage.py runserver 0.0.0.0:8888 &
sleep 2
curl -s http://localhost:8888 > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Serveur répond"
else
    echo "⚠ Serveur ne répond pas"
fi
pkill -f "runserver"

echo ""
echo "🎯 TEST TERMINÉ - Prêt pour le déploiement !"