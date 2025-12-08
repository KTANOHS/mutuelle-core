
# Exemple de views.py pour la messagerie multi-acteurs
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def messagerie_membre(request):
    return render(request, 'communication/messagerie_membre.html')

@login_required  
def messagerie_assureur(request):
    return render(request, 'communication/messagerie_assureur.html')

@login_required
def messagerie_medecin(request):
    return render(request, 'communication/messagerie_medecin.html')

@login_required
def messagerie_agent(request):
    return render(request, 'communication/messagerie_agent.html')
