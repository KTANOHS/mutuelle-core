# core/context_processors.py - VERSION OPTIMISÉE
"""
Context processors pour la mutuelle de santé
"""
from django.conf import settings
from django.utils import timezone

def mutuelle_context(request):
    """Context processor principal pour la mutuelle"""
    try:
        current_year = timezone.now().year
    except:
        current_year = 2024
    
    return {
        # Informations de la mutuelle
        'MUTUELLE_NAME': getattr(settings, 'MUTUELLE_NAME', 'Mutuelle de Santé'),
        'MUTUELLE_SLOGAN': getattr(settings, 'MUTUELLE_SLOGAN', 'Votre santé, notre priorité'),
        'MUTUELLE_PHONE': getattr(settings, 'MUTUELLE_PHONE', '01 23 45 67 89'),
        'MUTUELLE_EMAIL': getattr(settings, 'MUTUELLE_EMAIL', 'contact@mutuelle.com'),
        'MUTUELLE_ADDRESS': getattr(settings, 'MUTUELLE_ADDRESS', '123 Rue de la Santé, 75000 Paris'),
        'MUTUELLE_WEBSITE': getattr(settings, 'MUTUELLE_WEBSITE', 'https://www.mutuelle.com'),
        
        # Configuration
        'MUTUELLE_CONFIG': getattr(settings, 'MUTUELLE_CONFIG', {}),
        
        # Site
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'Mutuelle de Santé'),
        'SITE_URL': getattr(settings, 'SITE_URL', ''),
        'CONTACT_EMAIL': getattr(settings, 'CONTACT_EMAIL', 'contact@mutuelle.com'),
        'VERSION': getattr(settings, 'VERSION', '1.0.0'),
        
        # Année courante (sans dépendre de settings)
        'CURRENT_YEAR': current_year,
        
        # Environnement
        'DEBUG': getattr(settings, 'DEBUG', False),
        'IS_PRODUCTION': getattr(settings, 'IS_PRODUCTION', False),
        'IS_DEVELOPMENT': getattr(settings, 'IS_DEVELOPMENT', True),
    }

# Alias pour compatibilité
def settings_context(request):
    return mutuelle_context(request)

def user_context(request):
    """Contexte utilisateur"""
    context = {}
    if hasattr(request, 'user') and request.user.is_authenticated:
        context['current_user'] = request.user
        # Ajoutez d'autres infos utilisateur au besoin
    return context

def navigation_context(request):
    """Navigation principale"""
    return {
        'nav_items': [
            {'name': 'Accueil', 'url': '/', 'icon': 'home'},
            {'name': 'Dashboard', 'url': '/dashboard/', 'icon': 'dashboard'},
            {'name': 'Soins', 'url': '/soins/', 'icon': 'medical_services'},
            {'name': 'Membres', 'url': '/membres/', 'icon': 'people'},
            {'name': 'Bons', 'url': '/bons/', 'icon': 'receipt'},
            {'name': 'Paiements', 'url': '/paiements/', 'icon': 'payments'},
            {'name': 'API', 'url': '/api/', 'icon': 'api'},
            {'name': 'Admin', 'url': '/admin/', 'icon': 'admin_panel_settings'},
        ],
        'current_path': request.path if hasattr(request, 'path') else '/',
    }