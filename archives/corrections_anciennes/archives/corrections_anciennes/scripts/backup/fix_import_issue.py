#!/usr/bin/env python
"""
CORRECTION ULTIME DE L'IMPORTATION ET DE LA BOUCLE
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def fix_utils_completely():
    """Corrige complètement le fichier utils.py"""
    print("🔧 Correction complète de core/utils.py...")
    
    utils_content = '''"""
Fonctions utilitaires pour la gestion des utilisateurs et permissions
Version corrigée avec gestion robuste des erreurs
"""
from django.urls import reverse
from django.http import HttpResponseForbidden
from functools import wraps
from .constants import UserGroups, Permissions

def get_user_redirect_url(user):
    """
    Retourne l'URL de redirection basée sur le groupe de l'utilisateur
    VERSION SÉCURISÉE avec URLs absolues
    """
    if not user or not user.is_authenticated:
        return "/accounts/login/"  # URL absolue sécurisée
    
    if user.is_superuser:
        return "/admin/"  # URL absolue
    
    # Vérifier chaque groupe avec URLs absolues
    redirect_mapping = {
        UserGroups.ASSUREUR: "/assureur/dashboard/",
        UserGroups.MEDECIN: "/medecin/dashboard/", 
        UserGroups.PHARMACIEN: "/pharmacien/dashboard/",
        UserGroups.ADMIN: "/admin/",
    }
    
    for group_name, absolute_url in redirect_mapping.items():
        if user.groups.filter(name=group_name).exists():
            return absolute_url
    
    # Fallback sécurisé
    return "/dashboard/"  # URL absolue garantie

def get_user_primary_group(user):
    """Retourne le groupe principal de l'utilisateur"""
    if not user or not user.is_authenticated:
        return None
        
    for group_name in UserGroups.REDIRECT_MAPPING.keys():
        if user.groups.filter(name=group_name).exists():
            return group_name
    return None

def user_has_group(user, group_name):
    """Vérifie si l'utilisateur appartient à un groupe spécifique"""
    return user.groups.filter(name=group_name).exists()

def user_is_assureur(user):
    return user_has_group(user, UserGroups.ASSUREUR)

def user_is_medecin(user):
    return user_has_group(user, UserGroups.MEDECIN)

def user_is_pharmacien(user):
    return user_has_group(user, UserGroups.PHARMACIEN)

# ==============================================================================
# PERMISSIONS SPÉCIFIQUES (MEMBRES)
# ==============================================================================
def user_can_view_membres(user):
    """Vérifie si l'utilisateur peut voir les membres"""
    return user.has_perm(Permissions.VIEW_MEMBRES) or user_is_assureur(user)

def user_can_edit_membre(user):
    """Vérifie si l'utilisateur peut modifier un membre"""
    return user.has_perm(Permissions.CHANGE_MEMBRE) or user_is_assureur(user)

def user_can_create_membre(user):
    """Vérifie si l'utilisateur peut créer un membre"""
    return user.has_perm(Permissions.ADD_MEMBRE) or user_is_assureur(user)

# ==============================================================================
# DÉCORATEURS AVEC PERMISSIONS SPÉCIFIQUES
# ==============================================================================
def group_required(group_name):
    """Décorateur pour vérifier l'appartenance à un groupe"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.shortcuts import redirect
                return redirect('home')
            
            if not user_has_group(request.user, group_name):
                return HttpResponseForbidden("Accès non autorisé")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def permission_required(permission):
    """Décorateur pour vérifier une permission spécifique"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.shortcuts import redirect
                return redirect('home')
            
            if not request.user.has_perm(permission):
                return HttpResponseForbidden("Permission insuffisante")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Décorateurs spécifiques pour chaque groupe
def assureur_required(view_func):
    return group_required(UserGroups.ASSUREUR)(view_func)

def medecin_required(view_func):
    return group_required(UserGroups.MEDECIN)(view_func)

def pharmacien_required(view_func):
    return group_required(UserGroups.PHARMACIEN)(view_func)

# Décorateurs avec permissions spécifiques MEMBRES
def can_view_membres_required(view_func):
    """Décorateur pour la vue des membres"""
    return permission_required(Permissions.VIEW_MEMBRES)(view_func)
'''

    utils_path = BASE_DIR / 'core' / 'utils.py'
    
    with open(utils_path, 'w') as f:
        f.write(utils_content)
    
    print("✅ utils.py complètement corrigé")

def fix_constants_completely():
    """Corrige complètement le fichier constants.py"""
    print("🔧 Correction complète de core/constants.py...")
    
    constants_path = BASE_DIR / 'core' / 'constants.py'
    
    with open(constants_path, 'r') as f:
        content = f.read()
    
    # S'assurer que le REDIRECT_MAPPING est correct
    if 'assureur:dashboard' in content:
        print("❌ Ancien mapping détecté, correction en cours...")
        content = content.replace('"assureur:dashboard"', '"/assureur/dashboard/"')
        content = content.replace('"medecin:dashboard"', '"/medecin/dashboard/"')
        content = content.replace('"pharmacien:dashboard"', '"/pharmacien/dashboard/"')
        content = content.replace('"admin:index"', '"/admin/"')
    
    with open(constants_path, 'w') as f:
        f.write(content)
    
    print("✅ constants.py vérifié et corrigé")

def verify_fixes():
    """Vérifie que les corrections sont appliquées"""
    print("\n🔍 Vérification des corrections...")
    
    # Vérifier utils.py
    utils_path = BASE_DIR / 'core' / 'utils.py'
    with open(utils_path, 'r') as f:
        utils_content = f.read()
    
    if 'get_user_primary_group' in utils_content:
        print("✅ get_user_primary_group présente dans utils.py")
    else:
        print("❌ get_user_primary_group manquante dans utils.py")
    
    # Vérifier constants.py
    constants_path = BASE_DIR / 'core' / 'constants.py'
    with open(constants_path, 'r') as f:
        constants_content = f.read()
    
    if '"/assureur/dashboard/"' in constants_content:
        print("✅ URLs absolues dans constants.py")
    else:
        print("❌ Problème avec les URLs dans constants.py")

if __name__ == "__main__":
    print("🔄 Correction ultime des fichiers...")
    fix_utils_completely()
    fix_constants_completely()
    verify_fixes()
    print("🎉 Correction terminée ! Redémarrez le serveur.")