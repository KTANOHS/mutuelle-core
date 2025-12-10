#!/bin/bash
echo "🧪 Test Gunicorn avec configuration optimisée..."
echo "---------------------------------------------"

# Tuer tout processus Gunicorn existant
pkill -f gunicorn || true
sleep 2

# Tester avec différentes configurations
echo "1. Test avec worker sync (par défaut)..."
timeout 30 gunicorn mutuelle_core.wsgi:application \
    --bind 0.0.0.0:8001 \
    --workers 1 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug &
PID1=$!

sleep 5
echo "🔗 Test requête HTTP..."
curl -s -o /dev/null -w "Code: %{http_code}\n" http://localhost:8001/ || true
kill $PID1 2>/dev/null || true

echo ""
echo "2. Test avec gevent (async)..."
pip install gevent==24.8.1 2>/dev/null || true

timeout 30 gunicorn mutuelle_core.wsgi:application \
    --bind 0.0.0.0:8002 \
    --workers 1 \
    --worker-class gevent \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - &
PID2=$!

sleep 5
echo "🔗 Test requête HTTP..."
curl -s -o /dev/null -w "Code: %{http_code}\n" http://localhost:8002/ || true
kill $PID2 2>/dev/null || true

echo ""
echo "✅ Tests terminés. Utilisez './start_prod.sh' pour démarrer en production."