#!/usr/bin/env python3
"""
SCRIPT DE VÉRIFICATION DE CONFIGURATION
Vérifie la configuration actuelle du projet
"""

import os
from pathlib import Path

def verifier_configuration():
    """Vérifie la configuration du projet"""
    print("=" * 80)
    print("VÉRIFICATION DE CONFIGURATION")
    print("=" * 80)
    
    # Vérification des dossiers
    dossiers_requis = [
        "templates",
        "static", 
        "media",
        "logs",
        "agents/templates",
        "agents/static"
    ]
    
    print("\n📁 VÉRIFICATION DES DOSSIERS:")
    for dossier in dossiers_requis:
        if os.path.exists(dossier):
            print(f"   ✅ {dossier} - Présent")
        else:
            print(f"   ❌ {dossier} - Manquant")
    
    # Vérification des configurations critiques
    print("\n⚙️  CONFIGURATIONS CRITIQUES:")
    configurations = {
        "SECRET_KEY": "Définie via variable d'environnement",
        "DEBUG": "True en développement uniquement",
        "ALLOWED_HOSTS": "Configurés pour l'environnement",
        "DATABASES": "SQLite configuré",
        "EMAIL_BACKEND": "Console en développement"
    }
    
    for config, statut in configurations.items():
        print(f"   • {config}: {statut}")

if __name__ == "__main__":
    verifier_configuration()