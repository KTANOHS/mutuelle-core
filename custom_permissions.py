"""
Fichier de permissions personnalisées qui contourne les problèmes de relations OneToOne
À placer dans votre dossier de projet et à importer dans vos vues et décorateurs
"""

from django.contrib.auth.models import User
from membres.models import Membre
from medecin.models import Medecin
from pharmacien.models import Pharmacien
from assureur.models import Assureur

def is_medecin(user):
    """Vérifie si l'utilisateur est médecin (requête directe en base)"""
    if not user or not user.is_authenticated:
        return False
    return Medecin.objects.filter(user=user).exists()

def is_membre(user):
    """Vérifie si l'utilisateur est membre (requête directe en base)"""
    if not user or not user.is_authenticated:
        return False
    return Membre.objects.filter(user=user).exists()

def is_pharmacien(user):
    """Vérifie si l'utilisateur est pharmacien (requête directe en base)"""
    if not user or not user.is_authenticated:
        return False
    return Pharmacien.objects.filter(user=user).exists()

def is_assureur(user):
    """Vérifie si l'utilisateur est assureur (requête directe en base)"""
    if not user or not user.is_authenticated:
        return False
    return Assureur.objects.filter(user=user).exists()

def get_user_profile(user):
    """Retourne le type de profil de l'utilisateur"""
    if is_medecin(user):
        return 'medecin'
    elif is_membre(user):
        return 'membre'
    elif is_pharmacien(user):
        return 'pharmacien'
    elif is_assureur(user):
        return 'assureur'
    else:
        return None

def get_profile_instance(user):
    """Retourne l'instance du profil de l'utilisateur"""
    if is_medecin(user):
        return Medecin.objects.get(user=user)
    elif is_membre(user):
        return Membre.objects.get(user=user)
    elif is_pharmacien(user):
        return Pharmacien.objects.get(user=user)
    elif is_assureur(user):
        return Assureur.objects.get(user=user)
    return None