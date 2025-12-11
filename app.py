# app.py - Fichier corrigé
import os
import sys

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Essayer d'importer l'application WSGI
    from mutuelle_core.wsgi import application
    app = application
    print("✅ Application WSGI Django chargée avec succès")
except ImportError as e:
    print(f"⚠️ Erreur d'import WSGI: {e}")
    # Fallback pour éviter l'erreur
    app = None

if __name__ == "__main__":
    if app:
        print("🚀 Application prête")
    else:
        print("❌ Application non chargée")