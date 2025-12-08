#!/bin/bash

echo "🚀 Démarrage des corrections rapides..."

# Vérifie que nous sommes dans le bon dossier
if [ ! -f "manage.py" ]; then
    echo "❌ Erreur: Exécutez ce script depuis la racine du projet Django"
    exit 1
fi

# Crée le virtualenv s'il n'existe pas
if [ ! -d "venv" ]; then
    echo "📦 Création du virtualenv..."
    python3 -m venv venv
fi

# Active le virtualenv
echo "🔧 Activation du virtualenv..."
source venv/bin/activate

# Installe les requirements
if [ -f "requirements.txt" ]; then
    echo "📥 Installation des dépendances..."
    pip install -r requirements.txt
fi

# Exécute le script de correction
echo "🔨 Application des corrections..."
python fix_project_issues.py

# Lance les migrations
echo "🗃️ Application des migrations..."
python manage.py makemigrations
python manage.py migrate

# Crée un superutilisateur si demandé
read -p "Créer un superutilisateur? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

echo "✅ Corrections terminées! Lancez: python manage.py runserver"