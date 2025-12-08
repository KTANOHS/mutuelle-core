# verification_urls_disponibles.sh
#!/bin/bash

echo "🌐 URLS DISPONIBLES DANS COMMUNICATION"

echo "1. URLs principales (namespace: communication):"
python manage.py show_urls | grep "communication:" | grep -v "communication_api" | head -10

echo ""
echo "2. URLs API (namespace: communication_api):"
python manage.py show_urls | grep "communication_api:" | head -10

echo ""
echo "3. Test de l'URL api_last_activity:"
if python manage.py show_urls | grep -q "communication_api:api_last_activity"; then
    echo "✅ communication_api:api_last_activity trouvée"
else
    echo "❌ communication_api:api_last_activity NON trouvée"
    echo "📋 URLs API disponibles:"
    python manage.py show_urls | grep "communication_api:" 
fi
EOF


