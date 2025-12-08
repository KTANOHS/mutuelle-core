"""
Vues de correction pour les redirections
"""

from django.shortcuts import redirect

def redirect_to_dashboard(request):
    """Redirige vers le vrai dashboard assureur"""
    return redirect('assureur:dashboard')
