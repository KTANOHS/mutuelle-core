#!/bin/bash

echo "🎯 VÉRIFICATION FINALE COMPLÈTE"
echo "================================"

# Vérifier que toutes les URLs sont résolvables
python manage.py shell << 'PYTHONEOF'
from django.urls import reverse

urls_a_verifier = [
    'pharmacien:dashboard_pharmacien',
    'pharmacien:liste_ordonnances_attente',
    'pharmacien:detail_ordonnance',
    'pharmacien:valider_ordonnance',
    'pharmacien:refuser_ordonnance',
    'pharmacien:historique_validation',
    'pharmacien:rechercher_ordonnances',
    'pharmacien:filtrer_ordonnances',
    'pharmacien:profil_pharmacien',
    'pharmacien:export_historique',
    'pharmacien:api_ordonnances_attente',
    'pharmacien:stock',
    'pharmacien:export_stock',
    'pharmacien:ajouter_stock',
    'pharmacien:importer_stock',
    'pharmacien:home',
    'pharmacien:logout',
]

print("🔍 Vérification de toutes les URLs:")
print("=" * 50)

for url_name in urls_a_verifier:
    try:
        url = reverse(url_name)
        print(f"✅ {url_name:35} → {url}")
    except Exception as e:
        print(f"❌ {url_name:35} → ERREUR: {e}")

print("\n✨ Toutes les URLs devraient maintenant être résolues !")
PYTHONEOF

# Vérifier les templates
echo -e "\n📋 Vérification des templates:"
echo "=============================="
grep -l "{% url" templates/pharmacien/*.html | while read template; do
    echo "🔍 $template:"
    grep -c "{% url" "$template" | xargs echo "  - Nombre de références d'URL:"
done

echo -e "\n🎉 VÉRIFICATION TERMINÉE !"
echo "Le dashboard pharmacien devrait maintenant fonctionner correctement."
