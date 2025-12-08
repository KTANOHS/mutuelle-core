
# VUES SIMPLIFIÉES POUR LE DASHBOARD AGENT
# Ajoutez ceci dans agents/views.py si les vues n'existent pas

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def creer_bon_soin(request):
    """Vue simplifiée pour créer un bon de soin"""
    return render(request, 'agents/creer_bon.html', {'title': 'Créer bon de soin'})

@login_required
def liste_membres(request):
    """Vue simplifiée pour lister les membres"""
    return render(request, 'agents/liste_membres.html', {'title': 'Liste des membres'})

@login_required
def verification_cotisation(request):
    """Vue simplifiée pour vérifier les cotisations"""
    return render(request, 'agents/verification_cotisation.html', {'title': 'Vérification cotisations'})

@login_required
def historique_bons_soin(request):
    """Vue simplifiée pour l'historique des bons"""
    return render(request, 'agents/historique_bons.html', {'title': 'Historique des bons'})

@login_required
def agents_notifications(request):
    """Vue simplifiée pour les notifications"""
    return render(request, 'agents/notifications.html', {'title': 'Notifications'})

@login_required
def rapport_performance(request):
    """Vue simplifiée pour les rapports"""
    return render(request, 'agents/rapports.html', {'title': 'Rapports de performance'})
