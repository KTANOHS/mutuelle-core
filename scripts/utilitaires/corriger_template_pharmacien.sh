#!/bin/bash

echo "🔧 CORRECTION DU TEMPLATE PHARMACIEN"

# Remplacer 'dashboard' par 'dashboard_pharmacien' dans le template problématique
sed -i '' 's/{% url .pharmacien:dashboard. %}/{% url "pharmacien:dashboard_pharmacien" %}/g' templates/pharmacien/_sidebar_pharmacien.html

echo "✅ Template corrigé : 'dashboard' → 'dashboard_pharmacien'"

# Vérification
echo "📋 Vérification de la correction :"
grep -n "dashboard_pharmacien" templates/pharmacien/_sidebar_pharmacien.html
