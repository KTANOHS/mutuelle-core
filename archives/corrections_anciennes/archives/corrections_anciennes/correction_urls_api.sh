# correction_urls_api.sh
#!/bin/bash

echo "🔧 CORRECTION DES URLs API MANQUANTES"

# Vérifier si les URLs API sont bien incluses
if grep -q "include((api_urls, 'communication_api'))" "communication/urls.py"; then
    echo "✅ URLs API incluses dans communication/urls.py"
else
    echo "❌ URLs API non incluses - Correction nécessaire"
    # Ajouter la ligne manquante
    echo "path('', include((api_urls, 'communication_api')))," >> communication/urls.py
    echo "✅ URLs API ajoutées"
fi

# Vérifier le contenu de urls_api.py
echo ""
echo "📄 Contenu de communication/urls_api.py:"
cat communication/urls_api.py

# Vérifier que api_last_activity est bien définie
echo ""
echo "🔍 Vérification de la vue api_last_activity:"
if grep -q "api_last_activity" "communication/api_views.py"; then
    echo "✅ Vue api_last_activity trouvée dans api_views.py"
else
    echo "❌ Vue api_last_activity non trouvée"
fi

# Test Django
echo ""
echo "🧪 Test Django:"
python manage.py check
EOF


