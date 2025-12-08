#!/bin/bash

echo "🔧 Correction spécifique pour mutuelle_core..."

# Active le virtualenv
source venv/bin/activate

# Exécute le script de correction
python fix_mutuelle_issues.py

# Fait les migrations
echo ""
echo "🗃️ Création des migrations..."
python manage.py makemigrations

echo ""
echo "🗃️ Application des migrations..."
python manage.py migrate

# Vérifie les corrections
echo ""
echo "🔍 Vérification finale..."
python mutuelle_checklist.py

echo ""
echo "✅ Corrections terminées pour mutuelle_core!"