#!/bin/bash
# fix_missing_functions.sh

echo "🔧 Ajout des fonctions manquantes dans core/utils.py..."

cat >> core/utils.py << 'EOF'

# ========================
# FONCTIONS DE COMPATIBILITÉ
# (Pour les applications qui utilisent les anciens noms)
# ========================

def user_is_pharmacien(user):
    """Vérifie si l'utilisateur est un pharmacien"""
    return get_user_primary_group(user) == 'PHARMACIEN'

def user_is_medecin(user):
    """Vérifie si l'utilisateur est un médecin"""
    return get_user_primary_group(user) == 'MEDECIN'

def user_is_agent(user):
    """Vérifie si l'utilisateur est un agent"""
    return get_user_primary_group(user) == 'AGENT'

def user_is_assureur(user):
    """Vérifie si l'utilisateur est un assureur"""
    return get_user_primary_group(user) == 'ASSUREUR'

def user_is_membre(user):
    """Vérifie si l'utilisateur est un membre"""
    return get_user_primary_group(user) == 'MEMBRE'

def user_is_admin(user):
    """Vérifie si l'utilisateur est un administrateur"""
    return user.is_superuser or get_user_primary_group(user) == 'ADMIN'

# Alias pour la rétrocompatibilité
is_pharmacien = user_is_pharmacien
is_medecin = user_is_medecin
is_agent = user_is_agent
is_assureur = user_is_assureur
is_membre = user_is_membre

print("✅ Fonctions de compatibilité chargées")
EOF

echo "✅ Fonctions ajoutées avec succès !"
echo "🎯 Test du serveur..."

python manage.py check