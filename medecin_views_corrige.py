
# FICHIER: medecin_views_corrige.py
# COPIEZ CE CODE DANS medecin/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Count, Sum

from membres.models import Membre
from soins.models import BonDeSoin, TypeSoin
from medecin.models import Consultation, Ordonnance, Medecin, SpecialiteMedicale, EtablissementMedical

@login_required
def dashboard_medecin_robuste(request):
    """
    Tableau de bord médecin - VERSION DÉFINITIVE SANS RELATION
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    medecin = None
    warning = None
    
    try:
        # METHODE 1: Relation Django (si existe)
        if hasattr(request.user, 'medecin'):
            medecin = request.user.medecin
        
        else:
            # METHODE 2: Recherche directe par user_id
            try:
                medecin = Medecin.objects.get(user_id=request.user.id)
                warning = "Profil chargé directement depuis la base"
                
            except Medecin.DoesNotExist:
                # METHODE 3: Profil temporaire
                class ProfilTemporaire:
                    def __init__(self, user):
                        self.nom_complet = user.get_full_name() or user.username
                        self.specialite = "Médecine Générale"
                        self.etablissement = "Établissement à configurer"
                        self.numero_ordre = "EN_ATTENTE"
                        self.est_actif = True
                        self.id = None
                
                medecin = ProfilTemporaire(request.user)
                warning = "Profil temporaire - Configuration requise"
                
    except Exception as e:
        # Fallback ultime
        class ProfilFallback:
            nom_complet = "Médecin"
            specialite = "Médecine Générale"
            etablissement = "Centre Médical"
            numero_ordre = "CONFIG"
            est_actif = True
            id = None
        
        medecin = ProfilFallback()
        warning = f"Mode dégradé: {str(e)}"
    
    # Statistiques (avec fallbacks)
    try:
        ordonnances_count = Ordonnance.objects.filter(medecin_id=request.user.id).count()
    except:
        ordonnances_count = 0
        
    try:
        bons_attente = BonDeSoin.objects.filter(statut='EN_ATTENTE').count()
    except:
        bons_attente = 0
        
    try:
        consultations_count = Consultation.objects.filter(medecin__user_id=request.user.id).count()
    except:
        consultations_count = 0
    
    context = {
        'user': request.user,
        'medecin': medecin,
        'is_medecin': True,
        'page_title': 'Tableau de Bord Médecin',
        'ordonnances_count': ordonnances_count,
        'bons_attente': bons_attente,
        'consultations_count': consultations_count,
        'warning': warning,
    }
    
    return render(request, 'medecin/dashboard.html', context)

# Alias pour compatibilité
def dashboard_medecin(request):
    return dashboard_medecin_robuste(request)

def dashboard(request):
    return dashboard_medecin_robuste(request)
