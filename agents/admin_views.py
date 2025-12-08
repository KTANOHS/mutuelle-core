from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Agent, BonSoin

@user_passes_test(lambda u: u.is_staff)
def toggle_agent(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    agent.est_actif = not agent.est_actif
    agent.save()
    
    action = "activé" if agent.est_actif else "désactivé"
    messages.success(request, f"Agent {agent.matricule} {action} avec succès.")
    
    return redirect('admin:agents_agent_changelist')

@user_passes_test(lambda u: u.is_staff)
def utiliser_bon_soin(request, bon_id):
    bon = get_object_or_404(BonSoin, id=bon_id)
    
    if bon.utiliser():
        messages.success(request, f"Bon de soin {bon.code} marqué comme utilisé.")
    else:
        messages.error(request, f"Impossible d'utiliser le bon de soin {bon.code}.")
    
    return redirect('admin:agents_bonsoin_changelist')