"""
Décorateurs pour les vues pharmacien
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from core.utils import est_pharmacien

def pharmacien_required(view_func):
    """
    Décorateur qui vérifie que l'utilisateur est un pharmacien
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not est_pharmacien(request.user):
            messages.error(request, "Accès réservé aux pharmaciens.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
