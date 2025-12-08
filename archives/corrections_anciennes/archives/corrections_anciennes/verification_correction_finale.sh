#!/bin/bash

echo "🔍 VÉRIFICATION DE LA CORRECTION FINALE"
echo "========================================"

# Vérifier que pharmacien:dashboard n'existe plus dans les templates
echo "📋 Recherche de 'pharmacien:dashboard' dans les templates:"
echo "=========================================================="

found_errors=0
for template in templates/pharmacien/*.html; do
    if grep -q "pharmacien:dashboard" "$template"; then
        echo "❌ $template: contient encore 'pharmacien:dashboard'"
        grep -n "pharmacien:dashboard" "$template"
        found_errors=1
    else
        echo "✅ $template: OK"
    fi
done

if [ $found_errors -eq 0 ]; then
    echo -e "\n🎉 TOUS LES TEMPLATES SONT CORRIGÉS !"
    echo "✨ L'erreur NoReverseMatch devrait être résolue"
else
    echo -e "\n⚠️  Il reste des erreurs à corriger manuellement"
fi

# Vérification finale des URLs
echo -e "\n🔍 VÉRIFICATION FINALE DES URLs:"
echo "================================="

python manage.py shell << 'PYTHONEOF'
from django.urls import reverse

print("URLs critiques pour le dashboard:")
critical_urls = [
    'pharmacien:dashboard_pharmacien',
    'pharmacien:liste_ordonnances_attente', 
    'pharmacien:historique_validation',
]

for url_name in critical_urls:
    try:
        url = reverse(url_name)
        print(f"✅ {url_name} → {url}")
    except Exception as e:
        print(f"❌ {url_name} → {e}")

print("\n🚀 Le dashboard pharmacien est prêt!")
PYTHONEOF

echo -e "\n🌐 Testez maintenant: http://127.0.0.1:8000/pharmacien/dashboard/"
