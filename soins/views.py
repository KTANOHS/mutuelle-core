from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Soin, TypeSoin, Prescription
from .forms import SoinForm, PrescriptionForm
from .models import Soin
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Max, Min, Q
from datetime import timedelta
from decimal import Decimal



# Décorateur personnalisé pour vérifier les rôles autorisés
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

# Fonction utilitaire pour choisir le template selon le rôle
def get_template_by_role(base_template, user_role):
    templates = {
        'ASSUREUR': f'assureur/{base_template}',
        'MEDECIN': f'medecin/{base_template}', 
        'MEMBRE': f'soins/{base_template}',  # ou créer un dossier membre/ si besoin
    }
    return templates.get(user_role, f'soins/{base_template}')

@login_required
@allowed_roles(['ASSUREUR', 'MEDECIN', 'MEMBRE'])
def dashboard(request):
    role = request.user.profile.role
    
    # Logique différente selon le rôle
    if role == 'ASSUREUR':
        soins = Soin.objects.all()
        template = 'assureur/dashboard_soins.html'  # Template spécifique assureur
    elif role == 'MEDECIN':
        soins = Soin.objects.filter(bon_de_soin__medecin=request.user)
        template = 'medecin/dashboard_soins.html'  # Template spécifique médecin
    else:  # MEMBRE
        soins = Soin.objects.filter(patient=request.user)
        template = 'soins/dashboard.html'  # Template générique
    
    # Statistiques
    total_soins = soins.count()
    soins_valides = soins.filter(statut='valide').count()
    soins_attente = soins.filter(statut='attente').count()
    
    context = {
        'total_soins': total_soins,
        'soins_valides': soins_valides,
        'soins_attente': soins_attente,
        'user_role': role,
        'soins': soins.order_by('-date_realisation')[:5],
    }
    
    return render(request, template, context)

@login_required
@allowed_roles(['ASSUREUR', 'MEDECIN', 'MEMBRE'])
def liste_soins(request):
    role = request.user.profile.role
    
    # Filtrage selon le rôle
    if role == 'ASSUREUR':
        soins = Soin.objects.all()
        template = 'assureur/liste_soins.html'
    elif role == 'MEDECIN':
        soins = Soin.objects.filter(bon_de_soin__medecin=request.user)
        template = 'medecin/liste_soins.html'
    else:  # MEMBRE
        soins = Soin.objects.filter(patient=request.user)
        template = 'soins/liste_soins.html'
    
    # Filtres supplémentaires
    statut_filter = request.GET.get('statut')
    type_filter = request.GET.get('type')
    
    if statut_filter:
        soins = soins.filter(statut=statut_filter)
    if type_filter:
        soins = soins.filter(type_soin_id=type_filter)
    
    soins = soins.select_related('patient', 'type_soin', 'medecin').order_by('-date_realisation')
    types_soin = TypeSoin.objects.filter(actif=True)
    
    context = {
        'soins': soins,
        'types_soin': types_soin,
        'statut_filter': statut_filter,
        'type_filter': type_filter,
        'user_role': role,
    }
    return render(request, template, context)

@login_required
@allowed_roles(['MEDECIN'])
def creer_soin(request):
    if request.method == 'POST':
        form = SoinForm(request.POST)
        if form.is_valid():
            soin = form.save(commit=False)
            soin.medecin = request.user
            soin.created_by = request.user
            soin.save()
            messages.success(request, 'Soin créé avec succès!')
            return redirect('soins:detail_soin', soin_id=soin.id)
    else:
        form = SoinForm(initial={'medecin': request.user})
    
    return render(request, 'medecin/creer_soin.html', {'form': form})

@login_required
@allowed_roles(['ASSUREUR', 'MEDECIN', 'MEMBRE'])
def detail_soin(request, soin_id):
    soin = get_object_or_404(Soin.objects.select_related(
        'patient', 'type_soin', 'medecin', 'valide_par'
    ), id=soin_id)
    
    role = request.user.profile.role
    
    # Vérification des permissions spécifiques
    if role == 'MEDECIN' and soin.medecin != request.user:
        raise PermissionDenied("Vous n'avez pas accès à ce soin")
    elif role == 'MEMBRE' and soin.patient != request.user:
        raise PermissionDenied("Vous n'avez pas accès à ce soin")
    
    # Choix du template selon le rôle
    if role == 'ASSUREUR':
        template = 'assureur/detail_soin.html'
    elif role == 'MEDECIN':
        template = 'medecin/detail_soin.html'
    else:
        template = 'soins/detail_soin.html'
    
    prescriptions = soin.prescriptions.all()
    documents = soin.documents.all()
    
    context = {
        'soin': soin,
        'prescriptions': prescriptions,
        'documents': documents,
        'user_role': role,
        'can_edit': role in ['MEDECIN', 'ASSUREUR'],
        'can_validate': role == 'ASSUREUR' and soin.statut == 'attente',  # Seulement si en attente
        'can_reject': role == 'ASSUREUR' and soin.statut == 'attente',    # Seulement si en attente
    }
    return render(request, template, context)

@login_required
@allowed_roles(['ASSUREUR'])
def valider_soin(request, soin_id):
    """
    Vue pour valider un soin - accessible uniquement aux assureurs
    """
    soin = get_object_or_404(Soin.objects.select_related(
        'patient', 'type_soin', 'medecin'
    ), id=soin_id)
    
    # Vérification supplémentaire des permissions
    if request.user.profile.role != 'ASSUREUR':
        raise PermissionDenied("Seuls les assureurs peuvent valider les soins")
    
    if request.method == 'POST':
        # Validation du soin
        soin.statut = 'valide'
        soin.valide_par = request.user
        soin.date_validation = timezone.now()  # N'oubliez pas d'importer timezone
        soin.save()
        
        messages.success(request, f"Soin #{soin_id} a été validé avec succès.")
        
        # Redirection selon l'origine ou vers la liste des soins
        next_url = request.POST.get('next', 'soins:liste_soins')
        return redirect(next_url)
    
    # Si méthode GET, afficher la page de confirmation
    template = get_template_by_role('valider_soin.html', request.user.profile.role)
    
    context = {
        'soin': soin,
        'user_role': request.user.profile.role,
        'next': request.GET.get('next', 'soins:liste_soins'),
    }
    return render(request, template, context)

@login_required
@allowed_roles(['ASSUREUR'])
def rejeter_soin(request, soin_id):
    """
    Vue optionnelle pour rejeter un soin
    """
    soin = get_object_or_404(Soin, id=soin_id)
    
    if request.method == 'POST':
        soin.statut = 'rejete'
        soin.valide_par = request.user
        soin.date_validation = timezone.now()
        soin.motif_rejet = request.POST.get('motif_rejet', '')
        soin.save()
        
        messages.warning(request, f"Soin #{soin_id} a été rejeté.")
        return redirect('soins:liste_soins')
    
    template = get_template_by_role('rejeter_soin.html', request.user.profile.role)
    
    context = {
        'soin': soin,
        'user_role': request.user.profile.role,
    }
    return render(request, template, context)


@login_required
@allowed_roles(['MEDECIN'])
def statistiques_soins(request):
    """
    Vue pour afficher les statistiques médicales avec données réelles
    """
    # Périodes de référence
    aujourdhui = timezone.now().date()
    date_30j = aujourdhui - timedelta(days=30)
    date_60j = aujourdhui - timedelta(days=60)
    date_90j = aujourdhui - timedelta(days=90)
    
    # Soins du médecin connecté
    soins_medecin = Soin.objects.filter(bon_de_soin__medecin=request.user)
    soins_30j = soins_medecin.filter(date_realisation__gte=date_30j)
    soins_60j = soins_medecin.filter(date_realisation__gte=date_60j, date_realisation__lt=date_30j)
    soins_90j = soins_medecin.filter(date_realisation__gte=date_90j)
    
    # === STATISTIQUES CONSULTATIONS ===
    consultations_30j = soins_30j.count()
    consultations_60j = soins_60j.count()
    
    # Évolution des consultations
    evolution_consultations = 0
    if consultations_60j > 0:
        evolution_consultations = ((consultations_30j - consultations_60j) / consultations_60j) * 100
    
    # === STATISTIQUES ORDONNANCES ===
    try:
        ordonnances_30j = Prescription.objects.filter(
            soin__in=soins_30j
        ).count()
        ordonnances_60j = Prescription.objects.filter(
            soin__in=soins_60j
        ).count()
    except:
        # Fallback si le modèle Prescription n'existe pas
        ordonnances_30j = soins_30j.count()
        ordonnances_60j = soins_60j.count()
    
    # Moyenne d'ordonnances par jour (sur 30 jours)
    moyenne_ordonnances_par_jour = round(ordonnances_30j / 30, 1) if ordonnances_30j > 0 else 0
    
    # === STATISTIQUES FINANCIÈRES ===
    revenus_30j = soins_30j.aggregate(total=Sum('cout'))['total'] or Decimal('0')
    revenus_60j = soins_60j.aggregate(total=Sum('cout'))['total'] or Decimal('0')
    
    consultations_payees = soins_30j.filter(statut='valide').count()
    total_consultations = consultations_30j
    
    # Taux de remboursement
    taux_remboursement = 0
    if total_consultations > 0:
        taux_remboursement = (consultations_payees / total_consultations) * 100
    
    # Coût moyen par consultation
    cout_moyen = soins_30j.aggregate(moyenne=Avg('cout'))['moyenne'] or Decimal('0')
    
    # === RÉPARTITION PAR TYPE DE SOIN ===
    repartition_types = soins_30j.values(
        'type_soin__nom', 
        'type_soin__id'
    ).annotate(
        count=Count('id'),
        cout_total=Sum('cout'),
        cout_moyen=Avg('cout')
    ).order_by('-count')
    
    # Ajout des couleurs pour l'affichage
    couleurs = ['primary', 'success', 'info', 'warning', 'danger', 'secondary']
    for i, type_data in enumerate(repartition_types):
        type_data['couleur'] = couleurs[i % len(couleurs)]
        type_data['pourcentage'] = round((type_data['count'] / total_consultations * 100), 1) if total_consultations > 0 else 0
    
    # === TOP PATIENTS ===
    top_patients_data = soins_90j.values(
        'patient__id', 
        'patient__first_name', 
        'patient__last_name',
        'patient__username',
        'patient__email'
    ).annotate(
        nb_consultations=Count('id'),
        derniere_visite=Max('date_realisation'),
        premiere_visite=Min('date_realisation'),
        total_depense=Sum('cout')
    ).order_by('-nb_consultations')[:8]
    
    top_patients = []
    for patient in top_patients_data:
        # Calcul de la fidélité (basé sur la régularité des visites)
        if patient['premiere_visite'] and patient['derniere_visite']:
            jours_fidelite = (patient['derniere_visite'] - patient['premiere_visite']).days
            if jours_fidelite > 0:
                fidelite = min(100, (patient['nb_consultations'] / (jours_fidelite / 30)) * 10)
            else:
                fidelite = min(100, patient['nb_consultations'] * 20)
        else:
            fidelite = min(100, patient['nb_consultations'] * 20)
        
        nom_complet = f"{patient['patient__first_name'] or ''} {patient['patient__last_name'] or ''}".strip()
        if not nom_complet:
            nom_complet = patient['patient__username']
            
        top_patients.append({
            'nom': nom_complet,
            'email': patient['patient__email'],
            'numero_membre': patient['patient__username'],
            'nb_consultations': patient['nb_consultations'],
            'derniere_visite': patient['derniere_visite'],
            'total_depense': patient['total_depense'] or Decimal('0'),
            'fidelite': round(fidelite, 1)
        })
    
    # === STATISTIQUES TEMPORELLES ===
    # Activité par jour de la semaine
    from django.db.models.functions import ExtractWeekDay
    activite_semaine = soins_30j.annotate(
        jour_semaine=ExtractWeekDay('date_realisation')
    ).values('jour_semaine').annotate(
        count=Count('id')
    ).order_by('jour_semaine')
    
    # Jours de la semaine en français
    jours_map = {1: 'Lundi', 2: 'Mardi', 3: 'Mercredi', 4: 'Jeudi', 5: 'Vendredi', 6: 'Samedi', 7: 'Dimanche'}
    activite_semaine_formate = []
    for activite in activite_semaine:
        activite_semaine_formate.append({
            'jour': jours_map.get(activite['jour_semaine'], 'Inconnu'),
            'count': activite['count']
        })
    
    # Créneau horaire le plus populaire (basé sur l'heure de création)
    from django.db.models.functions import ExtractHour
    creneaux_horaires = soins_30j.annotate(
        heure=ExtractHour('date_creation')
    ).values('heure').annotate(
        count=Count('id')
    ).order_by('-count')
    
    creneau_populaire = "Non disponible"
    if creneaux_horaires:
        heure_populaire = creneaux_horaires[0]['heure']
        creneau_populaire = f"{heure_populaire}h-{heure_populaire+1}h"
    
    # Taux d'occupation (estimation basée sur la charge moyenne)
    jours_ouvrables = 22  # Jours ouvrables dans le mois
    consultations_par_jour = consultations_30j / jours_ouvrables if jours_ouvrables > 0 else 0
    capacite_journaliere = 8  # Capacité estimée de consultations par jour
    taux_occupation = min(100, (consultations_par_jour / capacite_journaliere) * 100) if capacite_journaliere > 0 else 0
    
    # Taux d'annulation (soins rejetés)
    annulations_30j = soins_30j.filter(statut='rejete').count()
    taux_annulation = (annulations_30j / total_consultations * 100) if total_consultations > 0 else 0
    
    # === STATISTIQUES AVANCÉES ===
    # Durée moyenne entre les consultations
    if soins_30j.count() > 1:
        dates_consultations = soins_30j.order_by('date_realisation').values_list('date_realisation', flat=True)
        differences = []
        for i in range(1, len(dates_consultations)):
            diff = (dates_consultations[i] - dates_consultations[i-1]).days
            differences.append(diff)
        if differences:
            duree_moyenne_entre_consultations = sum(differences) / len(differences)
        else:
            duree_moyenne_entre_consultations = 0
    else:
        duree_moyenne_entre_consultations = 0
    
    # Types de soins les plus rentables
    soins_rentables = soins_30j.values('type_soin__nom').annotate(
        rentabilite=Avg('cout')
    ).order_by('-rentabilite')[:3]
    
    # === PRÉPARATION DU CONTEXTE ===
    context = {
        'stats': {
            # Consultations
            'consultations_30j': consultations_30j,
            'evolution_consultations': round(evolution_consultations, 1),
            
            # Ordonnances
            'ordonnances_30j': ordonnances_30j,
            'moyenne_ordonnances_par_jour': moyenne_ordonnances_par_jour,
            
            # Finances
            'revenus_30j': f"{revenus_30j:,.0f}".replace(',', ' '),
            'revenus_60j': f"{revenus_60j:,.0f}".replace(',', ' '),
            'consultations_payees': consultations_payees,
            'total_consultations': total_consultations,
            'taux_remboursement': round(taux_remboursement, 1),
            'cout_moyen': round(cout_moyen, 2),
            
            # Répartition
            'repartition_types': repartition_types,
            'top_patients': top_patients,
            
            # Planning et occupation
            'creneau_populaire': creneau_populaire,
            'taux_occupation': round(taux_occupation, 1),
            'annulations': round(taux_annulation, 1),
            'activite_semaine': activite_semaine_formate,
            
            # Statistiques avancées
            'duree_moyenne_consultations': round(duree_moyenne_entre_consultations, 1),
            'soins_rentables': soins_rentables,
            
            # Données simulées (si nécessaire)
            'taux_satisfaction': 85,  # À remplacer par des données réelles si disponible
            'nombre_avis': max(consultations_30j, 10),
        }
    }
    
    return render(request, 'medecin/statistiques.html', context)

@login_required
def dashboard_soins(request):
    """Tableau de bord soins"""
    context = {
        'title': 'Dashboard Soins',
        'user': request.user
    }
    return render(request, 'soins/dashboard.html', context)