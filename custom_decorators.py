"""
Décorateurs de permission qui utilisent les vérifications directes en base
"""
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps
from custom_permissions import is_medecin, is_membre, is_pharmacien, is_assureur

def medecin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_medecin(request.user):
            return HttpResponseForbidden("Accès réservé aux médecins")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def membre_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_membre(request.user):
            return HttpResponseForbidden("Accès réservé aux membres")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def pharmacien_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_pharmacien(request.user):
            return HttpResponseForbidden("Accès réservé aux pharmaciens")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def assureur_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_assureur(request.user):
            return HttpResponseForbidden("Accès réservé aux assureurs")
        return view_func(request, *args, **kwargs)
    return _wrapped_view