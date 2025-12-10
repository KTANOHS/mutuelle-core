#!/bin/bash

echo "🚀 Démarrage de l'application Django en mode développement..."

# Variables d'environnement pour développement
export DEBUG="True"
export DJANGO_ENV="development"
export SECURE_SSL_REDIRECT="False"
export SECURE_PROXY_SSL_HEADER=""
export PYTHONUNBUFFERED="1"

# Démarrer le serveur de développement Django
echo "⚡ Démarrage du serveur de développement..."
python manage.py runserver 0.0.0.0:8000