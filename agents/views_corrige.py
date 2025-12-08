# Vue corrigée pour CreerBonSoinView
from django.shortcuts import render
from django.views.generic import CreateView
from membres.models import Membre
from agents.models import Agent
from django.contrib.auth.mixins import LoginRequiredMixin

class CreerBonSoinViewCorrige(LoginRequiredMixin, CreateView):
    """Vue corrigée pour créer un bon de soin"""
    template_name = 'agents/creer_bon_soin.html'
    fields = ['type_soin', 'montant', 'description']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Utiliser le bon champ 'statut' au lieu de 'est_actif'
        context['membres'] = Membre.objects.filter(statut='ACTIF')
        context['agent'] = Agent.objects.get(user=self.request.user)
        return context
    
    def form_valid(self, form):
        form.instance.agent = Agent.objects.get(user=self.request.user)
        return super().form_valid(form)
