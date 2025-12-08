# test_deploy.sh - Script bash pour tester le déploiement
#!/bin/bash

echo "🧪 TEST DE DÉPLOIEMENT EN MODE PRODUCTION"
echo "========================================="

# 1. Créer un environnement de test
echo "1. Préparation de l'environnement de test..."
export DJANGO_ENV=production
export SECRET_KEY="test-secret-key-123456-change-me"
export DEBUG="False"
export DATABASE_URL="sqlite:///test_production.db"

# 2. Tester les imports critiques
echo ""
echo "2. Vérification des imports critiques..."
python3 -c "
try:
    import django
    print('✅ Django importé')
except ImportError:
    print('❌ Django non installé')
    exit(1)

try:
    import gunicorn
    print('✅ Gunicorn importé')
except ImportError:
    print('❌ Gunicorn non installé')

try:
    import dj_database_url
    print('✅ dj-database-url importé')
except ImportError:
    print('❌ dj-database-url non installé')
    exit(1)

try:
    import whitenoise
    print('✅ whitenoise importé')
except ImportError:
    print('❌ whitenoise non installé')

print('')
print('🎯 Tous les imports critiques vérifiés')
"

# 3. Tester la configuration Django
echo ""
echo "3. Vérification de la configuration Django..."
python3 -c "
import os
import sys

# Forcer l'environnement de production
os.environ['DJANGO_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'test-key'
os.environ['DEBUG'] = 'False'
os.environ['DATABASE_URL'] = 'sqlite:///test.db'

try:
    # Essayer d'importer les settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    
    import django
    django.setup()
    
    from django.conf import settings
    print('✅ Django configuré avec succès')
    print(f'   • DEBUG: {settings.DEBUG}')
    print(f'   • SECRET_KEY: {settings.SECRET_KEY[:10]}...')
    print(f'   • ALLOWED_HOSTS: {settings.ALLOWED_HOSTS[:2]}')
    print(f'   • DATABASE: {settings.DATABASES[\"default\"][\"ENGINE\"]}')
    
except Exception as e:
    print(f'❌ Erreur de configuration: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

# 4. Tester collectstatic
echo ""
echo "4. Test de collectstatic..."
python3 manage.py collectstatic --dry-run --noinput 2>&1 | grep -E "(static files|Copying|collected)" || echo "⚠ collectstatic avec des avertissements"

# 5. Tester les migrations
echo ""
echo "5. Test des migrations..."
python3 manage.py makemigrations --check --dry-run 2>&1 | grep -E "(No changes|Migrations)" && echo "✅ Migrations OK"

# 6. Tester le serveur de développement
echo ""
echo "6. Test rapide du serveur..."
timeout 3 python3 manage.py runserver 0.0.0.0:9999 > /tmp/django_test.log 2>&1 &
SERVER_PID=$!
sleep 2

if curl -s http://localhost:9999 > /dev/null 2>&1; then
    echo "✅ Serveur Django répond"
else
    echo "⚠ Serveur ne répond pas, vérifiez les logs:"
    tail -10 /tmp/django_test.log
fi

# Nettoyer
kill $SERVER_PID 2>/dev/null || true

echo ""
echo "🎯 TEST TERMINÉ !"
echo "Si aucune erreur critique, votre application est prête pour Render."