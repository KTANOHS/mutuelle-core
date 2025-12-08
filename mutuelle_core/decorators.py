"""
Décorateurs personnalisés pour l'application mutuelle_core
"""
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from .utils import is_assureur, is_medecin, is_pharmacien, is_membre

def assureur_required(view_func):
    """
    Décorateur qui vérifie que l'utilisateur est un assureur
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_assureur(request.user):
            return HttpResponseForbidden("Accès réservé aux assureurs")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def medecin_required(view_func):
    """
    Décorateur qui vérifie que l'utilisateur est un médecin
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_medecin(request.user):
            return HttpResponseForbidden("Accès réservé aux médecins")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def pharmacien_required(view_func):
    """
    Décorateur qui vérifie que l'utilisateur est un pharmacien
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_pharmacien(request.user):
            return HttpResponseForbidden("Accès réservé aux pharmaciens")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def membre_required(view_func):
    """
    Décorateur qui vérifie que l'utilisateur est un membre
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_membre(request.user):
            return HttpResponseForbidden("Accès réservé aux membres")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Décorateurs compatibles avec user_passes_test
assureur_only = user_passes_test(is_assureur)
medecin_only = user_passes_test(is_medecin)
pharmacien_only = user_passes_test(is_pharmacien)
membre_only = user_passes_test(is_membre)