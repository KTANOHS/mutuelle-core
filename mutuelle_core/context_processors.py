"""
Context processors pour l'application mutuelle_core
"""
from .utils import get_user_type, format_currency, format_percentage

def user_context(request):
    """
    Ajoute des informations utilisateur au contexte global
    """
    context = {}
    
    if request.user.is_authenticated:
        context['current_user_type'] = get_user_type(request.user)
        context['current_username'] = request.user.username
    else:
        context['current_user_type'] = 'anonymous'
        context['current_username'] = None
    
    return context

def app_settings(request):
    """
    Ajoute les paramètres de l'application au contexte
    """
    return {
        'APP_NAME': 'Mutuelle Core',
        'APP_VERSION': '1.0.0',
        'CURRENT_YEAR': 2024,
    }

def utility_filters(request):
    """
    Ajoute les filtres utilitaires au contexte
    """
    return {
        'format_currency': format_currency,
        'format_percentage': format_percentage,
    }