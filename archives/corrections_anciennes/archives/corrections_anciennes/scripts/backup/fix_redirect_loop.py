#!/usr/bin/env python
"""
CORRECTION RAPIDE DE LA BOUCLE DE REDIRECTION
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def fix_constants_file():
    """Corrige le fichier constants.py"""
    print("🔧 Correction de core/constants.py...")
    
    constants_path = BASE_DIR / 'core' / 'constants.py'
    
    with open(constants_path, 'r') as f:
        content = f.read()
    
    # Remplacer le mapping problématique
    old_mapping = """    # Mapping groupe -> URL de redirection
    REDIRECT_MAPPING = {
        ASSUREUR: "assureur:dashboard",
        MEDECIN: "medecin:dashboard",
        PHARMACIEN: "pharmacien:dashboard",
        ADMIN: "admin:index",
    }"""
    
    new_mapping = """    # Mapping groupe -> URL de redirection (URLs absolues)
    REDIRECT_MAPPING = {
        ASSUREUR: "/assureur/dashboard/",
        MEDECIN: "/medecin/dashboard/",
        PHARMACIEN: "/pharmacien/dashboard/", 
        ADMIN: "/admin/",
    }"""
    
    content = content.replace(old_mapping, new_mapping)
    
    with open(constants_path, 'w') as f:
        f.write(content)
    
    print("✅ constants.py corrigé")

def fix_utils_file():
    """Corrige le fichier utils.py"""
    print("🔧 Correction de core/utils.py...")
    
    utils_path = BASE_DIR / 'core' / 'utils.py'
    
    # Nouvelle version sécurisée de get_user_redirect_url
    new_function = """def get_user_redirect_url(user):
    \"""
    Retourne l'URL de redirection basée sur le groupe de l'utilisateur
    VERSION SÉCURISÉE avec URLs absolues
    \"""
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
    return "/dashboard/"  # URL absolue garantie"""

    with open(utils_path, 'r') as f:
        content = f.read()
    
    # Remplacer l'ancienne fonction
    lines = content.split('\n')
    new_lines = []
    in_function = False
    replaced = False
    
    for line in lines:
        if line.strip().startswith('def get_user_redirect_url(user):'):
            in_function = True
            if not replaced:
                new_lines.append(new_function)
                replaced = True
            continue
        
        if in_function:
            if line.strip() and not line.startswith(' ') and not line.startswith('def'):
                in_function = False
                if not replaced:
                    new_lines.append(line)
            continue
        else:
            new_lines.append(line)
    
    with open(utils_path, 'w') as f:
        f.write('\n'.join(new_lines))
    
    print("✅ utils.py corrigé")

if __name__ == "__main__":
    print("🔄 Correction de la boucle de redirection...")
    fix_constants_file()
    fix_utils_file()
    print("🎉 Correction terminée ! Redémarrez le serveur.")