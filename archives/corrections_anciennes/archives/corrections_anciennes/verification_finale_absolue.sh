#!/bin/bash

echo "🎯 VÉRIFICATION FINALE ABSOLUE"
echo "================================"

# Vérifier qu'aucun template ne contient pharmacien:dashboard (sans _pharmacien)
echo "📋 Recherche de 'pharmacien:dashboard' (sans _pharmacien):"
echo "=========================================================="

found_errors=0
for template in templates/pharmacien/*.html; do
    # Rechercher pharmacien:dashboard qui n'est PAS suivi de _pharmacien
    if grep -q "pharmacien:dashboard[^_]" "$template"; then
        echo "❌ $template: contient encore 'pharmacien:dashboard'"
        grep -n "pharmacien:dashboard[^_]" "$template"
        found_errors=1
    else
        echo "✅ $template: OK"
    fi
done

# Vérifier les URLs avec _pharmacien_pharmacien (duplication)
echo -e "\n📋 Recherche de duplications '_pharmacien_pharmacien':"
echo "======================================================"

found_duplicates=0
for template in templates/pharmacien/*.html; do
    if grep -q "pharmacien:dashboard_pharmacien_pharmacien" "$template"; then
        echo "❌ $template: contient une duplication"
        grep -n "pharmacien:dashboard_pharmacien_pharmacien" "$template"
        found_duplicates=1
    fi
done

if [ $found_errors -eq 0 ] && [ $found_duplicates -eq 0 ]; then
    echo -e "\n🎉 TOUS LES TEMPLATES SONT PARFAITEMENT CORRIGÉS !"
    echo "✨ L'erreur NoReverseMatch est RÉSOLUE"
else
    echo -e "\n⚠️  Il reste des corrections à faire"
    exit 1
fi

# Vérification finale des URLs critiques
echo -e "\n🔍 VÉRIFICATION ULTIME DES URLs:"
echo "================================="

python manage.py shell << 'PYTHONEOF'
from django.urls import reverse

print("URLs critiques pour le dashboard:")
critical_urls = [
    'pharmacien:dashboard_pharmacien',
    'pharmacien:liste_ordonnances_attente', 
    'pharmacien:historique_validation',
    'pharmacien:rechercher_ordonnances',
    'pharmacien:profil_pharmacien',
]

all_ok = True
for url_name in critical_urls:
    try:
        url = reverse(url_name)
        print(f"✅ {url_name:35} → {url}")
    except Exception as e:
        print(f"❌ {url_name:35} → {e}")
        all_ok = False

if all_ok:
    print("\n🚀 TOUTES LES URLs FONCTIONNENT !")
    print("🌐 Le dashboard pharmacien est OPÉRATIONNEL")
else:
    print("\n⚠️  Certaines URLs ont des problèmes")
PYTHONEOF

echo -e "\n🎊 VÉRIFICATION TERMINÉE !"
echo "Redémarrez le serveur et testez: http://127.0.0.1:8000/pharmacien/dashboard/"
