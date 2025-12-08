

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Paiement, Remboursement, HistoriquePaiement
from .forms import PaiementForm, RemboursementForm, PaiementFiltreForm
from assureur.models import BonPriseEnCharge


# Décorateur pour vérifier les rôles
def allowed_roles(roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if not hasattr(request.user, 'profile'):
                raise PermissionDenied("Profil utilisateur non trouvé")
            if request.user.profile.role not in roles:
                raise PermissionDenied("Vous n'avez pas accès à cette page")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


@login_required
@allowed_roles(['ASSUREUR', 'COMPTABLE'])
def liste_paiements(request):
    """Liste tous les paiements avec filtres"""
    paiements = Paiement.objects.all().select_related(
        'bon', 'bon__membre', 'bon__soin', 'created_by'
    ).order_by('-date_paiement')

    # Application des filtres
    form = PaiementFiltreForm(request.GET or None)
    
    if form.is_valid():
        statut = form.cleaned_data.get('statut')
        mode_paiement = form.cleaned_data.get('mode_paiement')
        date_debut = form.cleaned_data.get('date_debut')
        date_fin = form.cleaned_data.get('date_fin')
        reference = form.cleaned_data.get('reference')

        if statut:
            paiements = paiements.filter(statut=statut)
        if mode_paiement:
            paiements = paiements.filter(mode_paiement=mode_paiement)
        if date_debut:
            paiements = paiements.filter(date_paiement__date__gte=date_debut)
        if date_fin:
            paiements = paiements.filter(date_paiement__date__lte=date_fin)
        if reference:
            paiements = paiements.filter(reference__icontains=reference)

    # Statistiques
    total_paiements = paiements.count()
    total_montant = paiements.aggregate(total=Sum('montant'))['total'] or 0
    paiements_payes = paiements.filter(statut='PAYE').count()
    montant_paye = paiements.filter(statut='PAYE').aggregate(total=Sum('montant'))['total'] or 0

    context = {
        'paiements': paiements,
        'form': form,
        'total_paiements': total_paiements,
        'total_montant': total_montant,
        'paiements_payes': paiements_payes,
        'montant_paye': montant_paye,
        'user_role': request.user.profile.role,
    }
    
    return render(request, 'assureur/historique_paiements.html', context)


@login_required
@allowed_roles(['ASSUREUR', 'COMPTABLE'])
def creer_paiement(request):
    """Créer un nouveau paiement"""
    if request.method == 'POST':
        form = PaiementForm(request.POST, request.FILES)
        if form.is_valid():
            paiement = form.save(commit=False)
            paiement.created_by = request.user
            
            # Si le statut est PAYE, mettre à jour la date de paiement
            if paiement.statut == 'PAYE' and not paiement.date_paiement:
                paiement.date_paiement = timezone.now()
            
            paiement.save()
            
            # Créer une entrée d'historique
            HistoriquePaiement.objects.create(
                paiement=paiement,
                ancien_statut='NOUVEAU',
                nouveau_statut=paiement.statut,
                modifie_par=request.user,
                motif=f"Création du paiement"
            )
            
            messages.success(request, f"Paiement {paiement.reference} créé avec succès!")
            return redirect('paiements:liste_paiements')
    else:
        form = PaiementForm()

    # Récupérer les bons éligibles pour les statistiques
    bons_eligibles = BonPriseEnCharge.objects.filter(statut='VALIDE').count()
    montant_total_attendu = BonPriseEnCharge.objects.filter(
        statut='VALIDE'
    ).aggregate(total=Sum('montant_prise_en_charge'))['total'] or 0

    context = {
        'form': form,
        'bons_eligibles': bons_eligibles,
        'montant_total_attendu': montant_total_attendu,
        'user_role': request.user.profile.role,
    }
    return render(request, 'assureur/enregistrer_paiement.html', context)


@login_required
@allowed_roles(['ASSUREUR', 'COMPTABLE'])
def detail_paiement(request, paiement_id):
    """Détail d'un paiement"""
    paiement = get_object_or_404(
        Paiement.objects.select_related(
            'bon', 'bon__membre', 'bon__soin', 'created_by'
        ), 
        id=paiement_id
    )
    
    historique = paiement.historique.all().order_by('-date_modification')
    remboursement = getattr(paiement, 'remboursement', None)

    context = {
        'paiement': paiement,
        'historique': historique,
        'remboursement': remboursement,
        'user_role': request.user.profile.role,
    }
    return render(request, 'assureur/detail_paiement.html', context)


@login_required
@allowed_roles(['ASSUREUR', 'COMPTABLE'])
def modifier_paiement(request, paiement_id):
    """Modifier un paiement"""
    paiement = get_object_or_404(Paiement, id=paiement_id)
    ancien_statut = paiement.statut

    if request.method == 'POST':
        form = PaiementForm(request.POST, request.FILES, instance=paiement)
        if form.is_valid():
            paiement = form.save()
            
            # Créer une entrée d'historique si le statut a changé
            if paiement.statut != ancien_statut:
                HistoriquePaiement.objects.create(
                    paiement=paiement,
                    ancien_statut=ancien_statut,
                    nouveau_statut=paiement.statut,
                    modifie_par=request.user,
                    motif=request.POST.get('motif_modification', 'Modification')
                )
            
            messages.success(request, f"Paiement {paiement.reference} modifié avec succès!")
            return redirect('paiements:detail_paiement', paiement_id=paiement.id)
    else:
        form = PaiementForm(instance=paiement)

    context = {
        'form': form,
        'paiement': paiement,
        'user_role': request.user.profile.role,
    }
    return render(request, 'assureur/modifier_paiement.html', context)


@login_required
@allowed_roles(['ASSUREUR', 'COMPTABLE'])
def valider_paiement(request, paiement_id):
    """Valider un paiement (marquer comme payé)"""
    paiement = get_object_or_404(Paiement, id=paiement_id)
    
    if request.method == 'POST':
        ancien_statut = paiement.statut
        paiement.marquer_comme_paye()
        
        # Créer une entrée d'historique
        HistoriquePaiement.objects.create(
            paiement=paiement,
            ancien_statut=ancien_statut,
            nouveau_statut=paiement.statut,
            modifie_par=request.user,
            motif="Validation manuelle du paiement"
        )
        
        messages.success(request, f"Paiement {paiement.reference} validé avec succès!")
    
    return redirect('paiements:detail_paiement', paiement_id=paiement.id)


@login_required
@allowed_roles(['ASSUREUR', 'COMPTABLE'])
def annuler_paiement(request, paiement_id):
    """Annuler un paiement"""
    paiement = get_object_or_404(Paiement, id=paiement_id)
    
    if request.method == 'POST':
        ancien_statut = paiement.statut
        paiement.marquer_comme_annule()
        
        # Créer une entrée d'historique
        HistoriquePaiement.objects.create(
            paiement=paiement,
            ancien_statut=ancien_statut,
            nouveau_statut=paiement.statut,
            modifie_par=request.user,
            motif=request.POST.get('motif_annulation', 'Annulation manuelle')
        )
        
        messages.warning(request, f"Paiement {paiement.reference} annulé.")
    
    return redirect('paiements:detail_paiement', paiement_id=paiement.id)


@login_required
@allowed_roles(['ASSUREUR', 'COMPTABLE'])
def demander_remboursement(request, paiement_id):
    """Demander un remboursement pour un paiement"""
    paiement = get_object_or_404(Paiement, id=paiement_id)
    
    if hasattr(paiement, 'remboursement'):
        messages.error(request, "Un remboursement existe déjà pour ce paiement.")
        return redirect('paiements:detail_paiement', paiement_id=paiement.id)

    if request.method == 'POST':
        form = RemboursementForm(request.POST, paiement=paiement)
        if form.is_valid():
            remboursement = form.save(commit=False)
            remboursement.paiement = paiement
            remboursement.save()
            
            messages.success(request, "Demande de remboursement créée avec succès!")
            return redirect('paiements:detail_paiement', paiement_id=paiement.id)
    else:
        form = RemboursementForm(paiement=paiement)

    context = {
        'form': form,
        'paiement': paiement,
        'user_role': request.user.profile.role,
    }
    return render(request, 'assureur/demander_remboursement.html', context)


@login_required
@allowed_roles(['ASSUREUR'])
def statistiques_paiements(request):
    """Statistiques des paiements"""
    # Périodes
    aujourdhui = timezone.now().date()
    debut_mois = aujourdhui.replace(day=1)
    debut_annee = aujourdhui.replace(month=1, day=1)
    
    # Statistiques générales
    total_paiements = Paiement.objects.count()
    total_montant = Paiement.objects.aggregate(total=Sum('montant'))['total'] or 0
    
    # Statistiques du mois
    paiements_mois = Paiement.objects.filter(
        date_paiement__date__gte=debut_mois
    )
    montant_mois = paiements_mois.aggregate(total=Sum('montant'))['total'] or 0
    
    # Par statut
    par_statut = Paiement.objects.values('statut').annotate(
        count=Count('id'),
        total=Sum('montant')
    ).order_by('statut')
    
    # Par mode de paiement
    par_mode = Paiement.objects.values('mode_paiement').annotate(
        count=Count('id'),
        total=Sum('montant')
    ).order_by('mode_paiement')
    
    # Évolution mensuelle (6 derniers mois)
    evolution_data = []
    for i in range(5, -1, -1):
        mois = aujourdhui - timedelta(days=30*i)
        debut_mois_calc = mois.replace(day=1)
        if i == 0:
            fin_mois_calc = aujourdhui
        else:
            fin_mois_calc = (debut_mois_calc + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        paiements_mois_calc = Paiement.objects.filter(
            date_paiement__date__range=[debut_mois_calc, fin_mois_calc]
        )
        montant_mois_calc = paiements_mois_calc.aggregate(total=Sum('montant'))['total'] or 0
        
        evolution_data.append({
            'mois': debut_mois_calc.strftime('%Y-%m'),
            'label': debut_mois_calc.strftime('%b %Y'),
            'montant': montant_mois_calc,
            'count': paiements_mois_calc.count()
        })

    context = {
        'total_paiements': total_paiements,
        'total_montant': total_montant,
        'paiements_mois': paiements_mois.count(),
        'montant_mois': montant_mois,
        'par_statut': par_statut,
        'par_mode': par_mode,
        'evolution_data': evolution_data,
        'user_role': request.user.profile.role,
    }
    
    return render(request, 'assureur/statistiques_paiements.html', context)


# Vues API pour AJAX
@login_required
@allowed_roles(['ASSUREUR', 'COMPTABLE'])
def get_bon_info(request, bon_id):
    """Récupérer les informations d'un bon pour AJAX"""
    bon = get_object_or_404(BonPriseEnCharge, id=bon_id)
    
    data = {
        'membre': bon.membre.user.get_full_name(),
        'montant_attendu': float(bon.montant_prise_en_charge),
        'soin': str(bon.soin.type_soin) if bon.soin else 'N/A',
        'date_soin': bon.soin.date_realisation.strftime('%d/%m/%Y') if bon.soin else 'N/A',
    }
    
    return JsonResponse(data)


@login_required
def mes_paiements(request):
    """Vue pour les membres pour voir leurs paiements"""
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'MEMBRE':
        raise PermissionDenied("Accès réservé aux membres")
    
    paiements = Paiement.objects.filter(
        bon__membre__user=request.user
    ).select_related('bon', 'bon__soin').order_by('-date_paiement')
    
    context = {
        'paiements': paiements,
        'total_percus': paiements.filter(statut='PAYE').aggregate(
            total=Sum('montant')
        )['total'] or 0,
        'user_role': request.user.profile.role,
    }
    
    return render(request, 'membres/mes_paiements.html', context)


