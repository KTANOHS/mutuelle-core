#!/bin/bash

echo "🔧 APPLICATION DES CORRECTIONS ET RETEST"
echo "========================================"

# Active l'environnement virtuel
source venv/bin/activate

# Applique les corrections
echo ""
echo "🔧 Application des corrections..."
python fix_identified_issues.py

# Fait les migrations si nécessaire
echo ""
echo "🗃️ Vérification des migrations..."
python manage.py makemigrations
python manage.py migrate

# Relance les tests
echo ""
echo "🔐 Relance des tests de connexion..."
python test_user_connections_fixed.py

echo ""
echo "========================================"
echo "✅ PROCESSUS TERMINÉ!"