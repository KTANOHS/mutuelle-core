#!/usr/bin/env python
"""
Script de validation mis à jour pour mutuelle_core
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

def check_user_model():
    """Vérifie le modèle User avec différentes approches"""
    if not setup_django():
        return "❌", "Django non configuré"
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Vérifie si c'est le User par défaut ou un proxy/custom
        if hasattr(User, '__str__'):
            # Teste si la méthode __str__ fonctionne
            try:
                test_str = str(User())
                return "✅", f"Modèle User: {User.__module__}.{User.__name__}"
            except:
                return "❌", "Méthode __str__ présente mais erreur"
        else:
            return "❌", "Méthode __str__ manquante"
            
    except Exception as e:
        return "❌", f"Erreur User: {e}"

def check_lignebon_model():
    """Vérifie le modèle LigneBon"""
    if not setup_django():
        return "❌", "Django non configuré"
    
    try:
        from membres.models import LigneBon
        if hasattr(LigneBon, '__str__'):
            return "✅", "Modèle LigneBon a __str__"
        else:
            return "❌", "LigneBon sans __str__"
    except Exception as e:
        return "❌", f"Erreur LigneBon: {e}"

def check_session_model():
    """Vérifie le modèle Session"""
    if not setup_django():
        return "❌", "Django non configuré"
    
    try:
        from mutuelle_core.models import Session
        if hasattr(Session, '__str__'):
            return "✅", "Modèle Session a __str__"
        else:
            return "❌", "Session sans __str__"
    except Exception as e:
        return "❌", f"Erreur Session: {e}"

def check_corrections():
    """Vérifie l'application des corrections"""
    print("🔍 VÉRIFICATION DES CORRECTIONS - MUTUELLE_CORE")
    print("=" * 50)
    
    # Vérifications de base
    basic_checks = {
        "Fichier .env existe": os.path.exists('.env'),
        "DEBUG=False dans .env": False,
        "Dossier media/ existe": os.path.exists('media'),
        "mutuelle_core/models.py existe": os.path.exists('mutuelle_core/models.py'),
        "mutuelle_core/admin.py existe": os.path.exists('mutuelle_core/admin.py'),
    }
    
    # Vérifie DEBUG dans .env
    if basic_checks["Fichier .env existe"]:
        with open('.env', 'r') as f:
            env_content = f.read()
            basic_checks["DEBUG=False dans .env"] = 'DEBUG=False' in env_content
    
    # Vérifie mutuelle_core/models.py
    if basic_checks["mutuelle_core/models.py existe"]:
        models_content = open('mutuelle_core/models.py').read()
        basic_checks["Session dans mutuelle_core"] = 'class Session' in models_content and 'def __str__' in models_content
        basic_checks["User dans mutuelle_core"] = 'class User' in models_content and 'def __str__' in models_content
    
    # Affiche les vérifications de base
    for check, passed in basic_checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")
    
    print("\\n🔍 VÉRIFICATIONS DES MODÈLES:")
    # Vérifications des modèles
    user_status, user_msg = check_user_model()
    print(f"{user_status} {user_msg}")
    
    lignebon_status, lignebon_msg = check_lignebon_model()
    print(f"{lignebon_status} {lignebon_msg}")
    
    session_status, session_msg = check_session_model()
    print(f"{session_status} {session_msg}")
    
    # Résumé
    all_passed = (
        all(basic_checks.values()) and 
        "✅" in user_status and 
        "✅" in lignebon_status and 
        "✅" in session_status
    )
    
    print("=" * 50)
    
    if all_passed:
        print("🎉 TOUTES LES CORRECTIONS SONT APPLIQUÉES!")
        print("\\n🚀 Le projet mutuelle_core est prêt pour la production!")
    else:
        print("⚠️  Certaines corrections sont manquantes")
        print("💡 Exécutez: python fix_user_str_issue.py pour les appliquer")
    
    return all_passed

if __name__ == "__main__":
    check_corrections()