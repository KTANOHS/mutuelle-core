# test_final_complet.sh
#!/bin/bash

echo "🎯 TEST FINAL COMPLET"
echo "====================="

# 1. Vérification des imports
echo "1. 🔧 Vérification des imports dans communication/urls.py"
if grep -q "from django.urls import path, include" "communication/urls.py"; then
    echo "   ✅ Import 'include' présent"
else
    echo "   ❌ Import 'include' manquant - Correction nécessaire"
    # Correction automatique
    sed -i '' 's/from django.urls import path/from django.urls import path, include/g' communication/urls.py
    echo "   🔧 Correction appliquée automatiquement"
fi

# 2. Vérification Django
echo ""
echo "2. 🐍 Test Django complet"
if python manage.py check > /dev/null 2>&1; then
    echo "   ✅ Django check: SUCCÈS"
    echo ""
    echo "3. 🌐 Test du serveur (CTRL+C pour arrêter)"
    python manage.py runserver
else
    echo "   ❌ Django check: ÉCHEC"
    echo "   📋 Détails de l'erreur:"
    python manage.py check
fi
EOF


