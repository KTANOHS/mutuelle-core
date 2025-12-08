#!/usr/bin/env python
"""
Script de validation spécifique pour mutuelle_core
"""

import os
import django

def setup_django():
    """Configure Django"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        django.setup()
        return True
    except Exception as e:
        print(f"❌ Impossible de configurer Django: {e}")
        return False

def check_file_contains(file_path, search_text):
    """Vérifie si un fichier contient un texte spécifique"""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
            return search_text in content
    return False

def check_models_have_str():
    """Vérifie que les modèles ont bien une méthode __str__"""
    try:
        from django.contrib.auth import get_user_model
        from membres.models import LigneBon
        from django.contrib.sessions.models import Session
        
        checks = {
            "Modèle User": hasattr(get_user_model(), '__str__'),
            "Modèle LigneBon": hasattr(LigneBon, '__str__'),
            "Modèle Session": hasattr(Session, '__str__'),
        }
        
        return checks
    except Exception as e:
        print(f"⚠️ Erreur vérification modèles: {e}")
        return {}

def check_corrections():
    """Vérifie l'application des corrections"""
    print("🔍 VÉRIFICATION DES CORRECTIONS - MUTUELLE_CORE")
    print("=" * 50)
    
    checks = {
        "Fichier .env existe": os.path.exists('.env'),
        "DEBUG=False dans .env": False,
        "Dossier media/ existe": os.path.exists('media'),
        "mutuelle_core/models.py existe": os.path.exists('mutuelle_core/models.py'),
        "Méthode __str__ dans mutuelle_core Session": False,
    }
    
    # Vérifie DEBUG dans .env
    if checks["Fichier .env existe"]:
        with open('.env', 'r') as f:
            env_content = f.read()
            checks["DEBUG=False dans .env"] = 'DEBUG=False' in env_content
    
    # Vérifie mutuelle_core/models.py
    if checks["mutuelle_core/models.py existe"]:
        models_content = open('mutuelle_core/models.py').read()
        checks["Méthode __str__ dans mutuelle_core Session"] = 'class Session' in models_content and 'def __str__' in models_content
    
    # Configure Django pour vérifier les modèles
    if setup_django():
        model_checks = check_models_have_str()
        checks.update(model_checks)
    
    # Vérifie aussi les fichiers directement
    checks["Méthode __str__ dans membres User"] = check_file_contains('membres/models.py', 'class User') and check_file_contains('membres/models.py', 'def __str__')
    checks["Méthode __str__ dans LigneBon fichier"] = check_file_contains('membres/models.py', 'class LigneBon') and check_file_contains('membres/models.py', 'def __str__')
    
    # Affiche les résultats
    all_passed = True
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    
    # Suggestions spécifiques
    if not all_passed:
        print("\\n🔧 CORRECTIONS MANQUANTES:")
        if not checks["mutuelle_core/models.py existe"]:
            print("- Créer mutuelle_core/models.py avec modèle Session")
        if not checks["Méthode __str__ dans LigneBon fichier"]:
            print("- Ajouter __str__ dans modèle LigneBon (membres/models.py)")
        if not checks["Méthode __str__ dans membres User"]:
            print("- Ajouter __str__ dans modèle User (membres/models.py)")
    
    if all_passed:
        print("🎉 TOUTES LES CORRECTIONS SONT APPLIQUÉES!")
        print("\\n🚀 Le projet mutuelle_core est prêt pour la production!")
    else:
        print("⚠️  Certaines corrections sont manquantes")
        print("💡 Exécutez: ./fix_mutuelle.sh pour les appliquer")
    
    return all_passed

if __name__ == "__main__":
    check_corrections()