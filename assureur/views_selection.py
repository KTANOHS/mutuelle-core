# views_selection.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db.models import Q
from .models import Membre
from .forms import RechercheMembreForm

@login_required
def selection_membre(request):
    """Vue pour la sélection interactive de membres"""
    form = RechercheMembreForm(request.GET or None)
    membres = Membre.objects.none()
    
    # Recherche rapide
    query = request.GET.get('q')
    if query:
        membres = Membre.objects.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(numero_membre__icontains=query)
        )[:10]  # Limiter à 10 résultats
    
    if form.is_valid():
        terme_recherche = form.cleaned_data['terme_recherche']
        champ_recherche = form.cleaned_data['champ_recherche']
        statut = form.cleaned_data['statut']
        
        if terme_recherche:
            filtres = Q()
            if champ_recherche == 'numero_membre':
                filtres &= Q(numero_membre__icontains=terme_recherche)
            elif champ_recherche == 'nom':
                filtres &= Q(nom__icontains=terme_recherche)
            elif champ_recherche == 'prenom':
                filtres &= Q(prenom__icontains=terme_recherche)
            elif champ_recherche == 'email':
                filtres &= Q(email__icontains=terme_recherche)
            elif champ_recherche == 'telephone':
                filtres &= Q(telephone__icontains=terme_recherche)
            elif champ_recherche == 'numero_contrat':
                filtres &= Q(numero_contrat__icontains=terme_recherche)
            
            if statut:
                filtres &= Q(statut=statut)
            
            membres = Membre.objects.filter(filtres)
    
    context = {
        'form': form,
        'membres': membres,
        'query': query,
    }
    
    # Si c'est une requête AJAX, retourner JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'id': membre.id,
                'numero_membre': membre.numero_membre,
                'nom_complet': f"{membre.prenom} {membre.nom}",
                'email': membre.email,
                'telephone': membre.telephone,
                'statut': membre.get_statut_display(),
            }
            for membre in membres
        ]
        return JsonResponse(data, safe=False)
    
    return render(request, 'assureur/selection/membre.html', context)