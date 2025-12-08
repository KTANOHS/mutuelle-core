
# CORRECTIF RAPIDE PUR /dashboard/
# Ajoutez ceci temporairement dans mutuelle_core/views.py

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required  
def dashboard_fixed(request):
    """Version fixée du dashboard"""
    return HttpResponse(f"""
    <h1>Dashboard Fixé</h1>
    <p>User: {request.user}</p>
    <p>Path: {request.path}</p>
    <p>Cette page fonctionne !</p>
    <hr>
    <p><a href="/agents/dashboard/">Aller au dashboard agent</a></p>
    <p><a href="/assureur/dashboard/">Aller au dashboard assureur</a></p>
    """)

# Puis dans urls.py, remplacez temporairement :
# path('dashboard/', dashboard_fixed, name='dashboard'),
