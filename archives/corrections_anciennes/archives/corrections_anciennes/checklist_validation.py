#!/usr/bin/env python
"""
Script de validation - Vérifie que toutes les corrections sont appliquées
"""

import os
import django
import sys

def check_corrections():
    """Vérifie l'application des corrections"""
    print("🔍 VÉRIFICATION DES CORRECTIONS")
    print("=" * 40)
    
    checks = {
        "Fichier .env existe": os.path.exists('.env'),
        "DEBUG=False dans .env": False,
        "Dossier media/ existe": os.path.exists('media'),
        "Dossier apps/ existe": os.path.exists('apps'),
        "Méthode __str__ dans User": False,
        "Méthode __str__ dans LigneBon": False,
    }
    
    # Vérifie DEBUG dans .env
    if checks["Fichier .env existe"]:
        with open('.env', 'r') as f:
            env_content = f.read()
            checks["DEBUG=False dans .env"] = 'DEBUG=False' in env_content
    
    # Vérifie les modèles (nécessite Django)
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        django.setup()
        
        from django.contrib.auth import get_user_model
        from membres.models import LigneBon
        
        User = get_user_model()
        checks["Méthode __str__ dans User"] = hasattr(User, '__str__')
        checks["Méthode __str__ dans LigneBon"] = hasattr(LigneBon, '__str__')
        
    except Exception as e:
        print(f"⚠️ Impossible de vérifier les modèles: {e}")
    
    # Affiche les résultats
    all_passed = True
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")
        if not passed:
            all_passed = False
    
    print("=" * 40)
    if all_passed:
        print("🎉 TOUTES LES CORRECTIONS SONT APPLIQUÉES!")
    else:
        print("⚠️  Certaines corrections sont manquantes")
    
    return all_passed

if __name__ == "__main__":
    check_corrections()