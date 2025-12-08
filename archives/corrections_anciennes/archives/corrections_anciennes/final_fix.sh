#!/bin/bash

echo "🔧 Correction finale pour mutuelle_core..."

# Active le virtualenv
source venv/bin/activate

# Corrige le problème User __str__
echo ""
echo "🔧 Correction du modèle User..."
python fix_user_str_issue.py

# Fait les migrations
echo ""
echo "🗃️ Création des migrations..."
python manage.py makemigrations mutuelle_core

echo ""
echo "🗃️ Application des migrations..."
python manage.py migrate

# Vérifie les corrections
echo ""
echo "🔍 Vérification finale..."
python updated_mutuelle_checklist.py

echo ""
echo "✅ Corrections finales terminées!"