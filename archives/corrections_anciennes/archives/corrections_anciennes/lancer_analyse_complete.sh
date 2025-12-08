#!/bin/bash

echo "🚀 LANCEMENT DE L'ANALYSE COMPLÈTE MEMBRE"
echo "=========================================="

# Vérification de l'environnement
if [ ! -f "manage.py" ]; then
    echo "❌ Erreur: Must be run from Django project root"
    exit 1
fi

# Création du dossier de rapports
mkdir -p rapports_analyse

echo "📊 Analyse principale..."
python scripts/analyse_membre_complet.py > rapports_analyse/rapport_principal.txt

echo "📝 Analyse des formulaires..."
python scripts/analyse_formulaires_membre.py > rapports_analyse/rapport_formulaires.txt

echo "🔍 Vérification compatibilité..."
python scripts/verifier_compatibilite_membre.py > rapports_analyse/rapport_compatibilite.txt

echo "📋 Génération du rapport consolidé..."
cat rapports_analyse/rapport_principal.txt > rapports_analyse/rapport_consolide.txt
echo "" >> rapports_analyse/rapport_consolide.txt
echo "=== FORMULAIRES ===" >> rapports_analyse/rapport_consolide.txt
cat rapports_analyse/rapport_formulaires.txt >> rapports_analyse/rapport_consolide.txt
echo "" >> rapports_analyse/rapport_consolide.txt
echo "=== COMPATIBILITÉ ===" >> rapports_analyse/rapport_consolide.txt
cat rapports_analyse/rapport_compatibilite.txt >> rapports_analyse/rapport_consolide.txt

echo "✅ Analyse terminée!"
echo "📁 Rapports disponibles dans: rapports_analyse/"