#!/bin/bash

echo "🎯 VÉRIFICATION ULTIME - DASHBOARD PHARMACIEN"
echo "=============================================="

# Vérification avec paramètres
python manage.py shell << 'PYTHONEOF'
from django.urls import reverse

print("🔍 URLs sans paramètres (doivent fonctionner):")
print("=" * 45)

urls_sans_params = [
    'pharmacien:dashboard_pharmacien',
    'pharmacien:liste_ordonnances_attente',
    'pharmacien:historique_validation',
    'pharmacien:rechercher_ordonnances',
    'pharmacien:filtrer_ordonnances',
    'pharmacien:profil_pharmacien',
    'pharmacien:stock',
]

for url_name in urls_sans_params:
    try:
        url = reverse(url_name)
        print(f"✅ {url_name:35} → {url}")
    except Exception as e:
        print(f"❌ {url_name:35} → {e}")

print("\n🔍 URLs avec paramètres (doivent échouer sans paramètre):")
print("=" * 55)

urls_avec_params = [
    'pharmacien:detail_ordonnance',
    'pharmacien:valider_ordonnance', 
    'pharmacien:refuser_ordonnance',
]

for url_name in urls_avec_params:
    try:
        # Essayer sans paramètre - DOIT échouer
        url = reverse(url_name)
        print(f"⚠️  {url_name:35} → {url} (DEVRAIT ÉCHOUER)")
    except Exception as e:
        print(f"✅ {url_name:35} → Échec normal: nécessite ordonnance_id")

print("\n🔍 Test avec paramètre (simulation):")
print("=" * 35)

try:
    url = reverse('pharmacien:detail_ordonnance', kwargs={'ordonnance_id': 1})
    print(f"✅ detail_ordonnance avec paramètre → {url}")
except Exception as e:
    print(f"❌ Même avec paramètre: {e}")

print("\n✨ Le dashboard devrait fonctionner maintenant!")
print("   Testez: http://127.0.0.1:8000/pharmacien/dashboard/")
PYTHONEOF

# Vérification des templates principaux
echo -e "\n📋 Vérification des templates principaux:"
echo "======================================"

check_template() {
    local template=$1
    if grep -q "pharmacien:dashboard" "$template"; then
        echo "❌ $template: contient encore 'pharmacien:dashboard'"
        return 1
    else
        echo "✅ $template: OK"
        return 0
    fi
}

check_template "templates/pharmacien/_sidebar_pharmacien.html"
check_template "templates/pharmacien/_sidebar_pharmacien_updated.html"
check_template "templates/pharmacien/_navbar_pharmacien.html"

echo -e "\n🚀 Pour tester: python manage.py runserver"
echo "🌐 Puis allez sur: http://127.0.0.1:8000/pharmacien/dashboard/"
