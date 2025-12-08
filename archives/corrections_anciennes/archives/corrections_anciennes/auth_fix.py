# CORRECTIF SYSTÈME AUTHENTIFICATION
# Ajoutez ceci dans settings.py

# Configuration d'authentification
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/redirect-after-login/'
LOGOUT_REDIRECT_URL = '/'

# OU pour un correctif temporaire, dans mutuelle_core/views.py :

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_simple(request):
    """Version simplifiée du dashboard"""
    return HttpResponse(f"""
    <h1>Dashboard de {request.user}</h1>
    <p>Bienvenue ! Cette page fonctionne.</p>
    <p><a href="/agents/dashboard/">Dashboard Agent</a></p>
    <p><a href="/assureur/dashboard/">Dashboard Assureur</a></p>
    <p><a href="/logout/">Déconnexion</a></p>
    """)

# Puis dans urls.py :
# path('dashboard/', dashboard_simple, name='dashboard'),
