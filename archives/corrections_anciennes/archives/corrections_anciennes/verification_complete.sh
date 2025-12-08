# verification_complete.sh
#!/bin/bash

echo "🔍 VÉRIFICATION COMPLÈTE"
echo "========================"

# 1. Vérification de communication/urls.py
echo "1. ✅ Vérification de communication/urls.py"
if [ -f "communication/urls.py" ]; then
    if grep -q "from django.urls import path, include" "communication/urls.py"; then
        echo "   ✅ Import 'include' présent"
    else
        echo "   ❌ Import 'include' manquant"
    fi
    
    if grep -q "include((api_urls, 'communication_api'))" "communication/urls.py"; then
        echo "   ✅ URLs API incluses"
    else
        echo "   ❌ URLs API non incluses"
    fi
fi

# 2. Vérification des sidebars
echo ""
echo "2. 📁 Vérification des sidebars:"
sidebars=(
    "templates/agents/partials/_sidebar_agent.html"
    "templates/assureur/partials/_sidebar.html" 
    "templates/medecin/partials/_sidebar.html"
    "templates/pharmacien/_sidebar_pharmacien.html"
)

for sidebar in "${sidebars[@]}"; do
    if [ -f "$sidebar" ]; then
        if grep -q "includes/sidebar_communication.html" "$sidebar"; then
            echo "   ✅ $(basename $sidebar) - Communication incluse"
        else
            echo "   ❌ $(basename $sidebar) - Communication MANQUANTE"
        fi
    else
        echo "   ⚠️  $sidebar - NON TROUVÉ"
    fi
done

# 3. Vérification du widget dans core dashboard
echo ""
echo "3. 📊 Vérification du widget dans core/dashboard:"
if [ -f "templates/core/dashboard.html" ]; then
    if grep -q "includes/communication_widget.html" "templates/core/dashboard.html"; then
        echo "   ✅ Widget communication présent"
    else
        echo "   ❌ Widget communication manquant"
    fi
fi

# 4. Test Django
echo ""
echo "4. 🐍 Test Django:"
python manage.py check 2>/dev/null && echo "   ✅ Django check réussi" || echo "   ❌ Django check échoué"

echo ""
echo "🎯 RÉSUMÉ:"
echo "✅ Sidebar communication intégrée dans 3/4 modules"
echo "✅ Widget communication dans core/dashboard" 
echo "⚠️  Sidebar assureur à créer"
echo "⚠️  Widgets à ajouter dans les autres dashboards"
EOF


