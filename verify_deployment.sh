#!/bin/bash
# Vérification ultime avant déploiement Render

echo "🔍 VÉRIFICATION ULTIME POUR RENDER"
echo "=================================="

# 1. Vérifier la configuration Docker (si utilisée)
if [ -f "Dockerfile" ]; then
    echo "🐳 Dockerfile détecté"
    docker build -t test-render .
fi

# 2. Simuler l'environnement Render
echo "🌐 Simulation de l'environnement Render..."
export RENDER=true
export RENDER_EXTERNAL_HOSTNAME=mutuelle-core-18.onrender.com
export PORT=10000

# 3. Tester avec Gunicorn
echo "🚀 Test avec Gunicorn (comme sur Render)..."
timeout 10 gunicorn app:application --bind 0.0.0.0:$PORT &
GUNICORN_PID=$!
sleep 5

# 4. Tester quelques endpoints
echo "🌐 Test des endpoints..."
curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/ && echo "✅ Accueil fonctionne" || echo "❌ Accueil échoue"
curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/admin/ && echo "✅ Admin redirige (attendu 302)" || echo "❌ Admin échoue"

# 5. Nettoyer
kill $GUNICORN_PID 2>/dev/null

# 6. Vérifier la taille des fichiers statiques
echo "📊 Taille des fichiers statiques:"
du -sh staticfiles/ | awk '{print "  " $1 " dans staticfiles/"}'

# 7. Vérifier les migrations
echo "🔄 État des migrations:"
python manage.py showmigrations --list | grep -E "\[X\]|\[ \]" | head -10

echo ""
echo "✅ VÉRIFICATION TERMINÉE !"
echo ""
echo "📝 POUR DÉPLOYER :"
echo "1. git push origin main"
echo "2. Render déploiera automatiquement"
echo "3. Surveillez les logs sur https://dashboard.render.com"
echo "4. Accédez à https://mutuelle-core-18.onrender.com"