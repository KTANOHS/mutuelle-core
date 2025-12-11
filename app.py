# app.py - Fichier temporaire pour contourner le bug Render
"""
Ce fichier est uniquement pour contourner le bug de Render
qui cherche par défaut 'app:app'
"""

import os
import sys

# Ajouter le chemin du projet
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importez l'application WSGI de Django
from mutuelle_core.wsgi import application

# L'application est directement accessible
app = application

if __name__ == "__main__":
    print("⚠️  Ce fichier est seulement pour Render, utilisez gunicorn mutuelle_core.wsgi:application")