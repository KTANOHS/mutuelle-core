# assureur/decorators.py
from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def assureur_required(user):
    """Vérifie si l'utilisateur est un assureur"""
    return user.is_authenticated and (
        user.groups.filter(name='assureur').exists() or 
        user.is_superuser or
        hasattr(user, 'assureur_profile')
    )

def assureur_required_decorator(view_func):
    """Décorateur pour vérifier si l'utilisateur est un assureur"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not assureur_required(request.user):
            messages.error(request, "Vous n'avez pas les permissions nécessaires pour accéder à cette page.")
            return redirect('admin:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def get_assureur_from_request(request):
    """Récupère l'objet assureur à partir de la requête"""
    if hasattr(request.user, 'assureur_profile'):
        return request.user.assureur_profile
    return None

def assureur_view(template_name):
    """Décorateur pour les vues assureur qui ajoute automatiquement l'assureur au contexte"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Importer render ici pour éviter les importations circulaires
            from django.shortcuts import render
            
            # Exécuter la vue originale
            result = view_func(request, *args, **kwargs)
            
            # Si c'est un dict (contexte), ajouter assureur
            if isinstance(result, dict):
                context = result
                # Ajouter assureur si pas déjà présent
                if 'assureur' not in context:
                    assureur = get_assureur_from_request(request)
                    context['assureur'] = assureur
                return render(request, template_name, context)
            return result
        return wrapper
    return decorator