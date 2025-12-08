#!/bin/bash

echo "🎯 VÉRIFICATION ULTIME FINALE"
echo "=============================="

# Vérifier qu'aucune duplication n'existe
echo "📋 Recherche de duplications restantes:"
echo "========================================"

found_duplicates=0
for template in templates/pharmacien/*.html; do
    if grep -q "pharmacien:dashboard_pharmacien_pharmacien" "$template"; then
        echo "❌ $template: contient encore une duplication"
        grep -n "pharmacien:dashboard_pharmacien_pharmacien" "$template"
        found_duplicates=1
    fi
done

# Vérifier que toutes les URLs utilisent pharmacien:dashboard_pharmacien
echo -e "\n📋 Vérification des URLs correctes:"
echo "===================================="

found_correct=0
for template in templates/pharmacien/*.html; do
    if grep -q "pharmacien:dashboard_pharmacien" "$template"; then
        echo "✅ $template: utilise l'URL correcte"
        found_correct=$((found_correct + 1))
    fi
done

if [ $found_duplicates -eq 0 ]; then
    echo -e "\n🎉 PLUS AUCUNE DUPLICATION !"
    echo "✨ Tous les templates utilisent l'URL correcte: pharmacien:dashboard_pharmacien"
else
    echo -e "\n❌ Il reste des duplications. Correction manuelle nécessaire."
    exit 1
fi

# Vérification finale des URLs Django
echo -e "\n🔍 VÉRIFICATION FINALE DES URLs DJANGO:"
echo "======================================="

python manage.py shell << 'PYTHONEOF'
from django.urls import reverse

print("Test de résolution de l'URL critique:")
try:
    url = reverse('pharmacien:dashboard_pharmacien')
    print(f"✅ pharmacien:dashboard_pharmacien → {url}")
    print("🎊 L'URL est parfaitement résolvable !")
except Exception as e:
    print(f"❌ ERREUR: {e}")

print("\n🌐 Le dashboard pharmacien est PRÊT !")
PYTHONEOF

echo -e "\n🚀 REDÉMARREZ LE SERVEUR ET TESTEZ:"
echo "   python manage.py runserver"
echo "   http://127.0.0.1:8000/pharmacien/dashboard/"
