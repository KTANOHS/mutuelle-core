from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from pharmacien.decorators import pharmacien_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import date
import csv
from django.contrib.auth import logout
from django.db import transaction
from django.db.models import Q, Sum, Count, F
from datetime import datetime, timedelta
from core.utils import generer_numero_ordonnance, generer_numero_unique_verifie

# Décorateur de gestion d'erreurs
try:
    from core.utils import gerer_erreurs
except ImportError:
    def gerer_erreurs(view_func):
        """
        Décorateur pour gérer les erreurs dans les vues
        """
        from functools import wraps
        import logging
        logger = logging.getLogger(__name__)
        
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                return view_func(request, *args, **kwargs)
            except Exception as e:
                logger.error(f"Erreur dans {view_func.__name__}: {e}")
                from django.contrib import messages
                messages.error(request, "Une erreur est survenue.")
                # Essayer de rediriger vers le dashboard pharmacien
                try:
                    from django.urls import reverse
                    return redirect('pharmacien:dashboard')
                except:
                    return redirect('/')
        
        return _wrapped_view



import uuid

import random
import string

# --- Modèles ---
from soins.models import BonDeSoin
from pharmacien.models import Pharmacien, StockPharmacie
from communication.models import Notification, Conversation, Message

# --- Formulaires ---
from .forms import (
    ValiderOrdonnanceForm,
    RechercheOrdonnanceForm,
    FiltreOrdonnanceForm,
    PharmacienProfileForm
)

# --- Utilitaires ---
from core.utils import pharmacien_required, user_is_pharmacien, get_user_primary_group
from core.constants import UserGroups

# ---------------------------------------------------------------------
# DASHBOARD PHARMACIEN - VERSION CORRIGÉE
# ---------------------------------------------------------------------
@login_required
@pharmacien_required
def dashboard_pharmacien(request):
    """Affiche le tableau de bord principal du pharmacien."""
    try:
        # Récupérer le profil pharmacien
        pharmacien = get_object_or_404(Pharmacien, user=request.user)
        
        # Récupérer les données de communication
        notifications_non_lues = Notification.objects.filter(
            user=request.user, 
            est_lue=False
        )
        
        unread_count = notifications_non_lues.count()
        notifications_a_afficher = notifications_non_lues[:3]
        
        # CORRECTION: Utiliser le bon modèle Ordonnance (medecin.Ordonnance)
        from medecin.models import Ordonnance as MedecinOrdonnance
        
        # Statistiques des ordonnances
        ordonnances_attente = MedecinOrdonnance.objects.filter(statut="ACTIVE").count()
        ordonnances_aujourdhui = MedecinOrdonnance.objects.filter(
            date_creation__date=timezone.now().date(),
            statut="ACTIVE"
        ).count()

        # Dernières ordonnances en attente
        dernieres_ordonnances = (
            MedecinOrdonnance.objects.filter(statut="ACTIVE")
            .select_related("patient", "medecin")
            .order_by("-date_creation")[:5]
        )

        # CORRECTION: Récupérer les conversations avec prefetch pour optimiser
        conversations = Conversation.objects.filter(
            participants=request.user
        ).prefetch_related('participants').order_by('-date_modification')[:5]

        # Statistiques du stock
        stocks_alerte = StockPharmacie.objects.filter(
            pharmacie=pharmacien,
            quantite_stock__lte=F('seuil_alerte'),
            quantite_stock__gt=0
        ).count()
        
        stocks_rupture = StockPharmacie.objects.filter(
            pharmacie=pharmacien,
            quantite_stock=0
        ).count()

        context = {
            "pharmacien": pharmacien,
            "ordonnances_attente": ordonnances_attente,
            "ordonnances_aujourdhui": ordonnances_aujourdhui,
            "total_ordonnances": MedecinOrdonnance.objects.count(),
            "dernieres_ordonnances": dernieres_ordonnances,
            "notifications_non_lues": notifications_a_afficher,
            "unread_count": unread_count,
            "conversations": conversations,
            "stocks_alerte": stocks_alerte,
            "stocks_rupture": stocks_rupture,
            "date_aujourdhui": date.today().strftime("%d/%m/%Y"),
            "user_group": get_user_primary_group(request.user),
        }
        
        print(f"DEBUG Dashboard: {conversations.count()} conversations pour {request.user.username}")
        return render(request, "pharmacien/dashboard.html", context)

    except Exception as e:
        print(f"ERREUR Dashboard: {e}")
        messages.error(request, f"Erreur lors du chargement du tableau de bord : {e}")
        return render(request, "pharmacien/dashboard.html", {
            "ordonnances_attente": 0,
            "ordonnances_aujourdhui": 0,
            "total_ordonnances": 0,
            "dernieres_ordonnances": [],
            "notifications_non_lues": [],
            "unread_count": 0,
            "conversations": [],
            "stocks_alerte": 0,
            "stocks_rupture": 0,
            "date_aujourdhui": date.today().strftime("%d/%m/%Y"),
            "user_group": get_user_primary_group(request.user),
        })

# ---------------------------------------------------------------------
# LISTE ET DÉTAIL DES ORDONNANCES - VERSION CORRIGÉE
# ---------------------------------------------------------------------
@login_required
@pharmacien_required
def liste_ordonnances_attente(request):
    """Liste des ordonnances en attente de validation."""
    try:
        # CORRECTION: Utiliser le bon modèle
        from medecin.models import Ordonnance as MedecinOrdonnance
        
        ordonnances = MedecinOrdonnance.objects.filter(statut="ACTIVE")\
            .select_related("patient", "medecin")\
            .order_by("-date_creation")

        return render(request, "pharmacien/liste_ordonnances.html", {
            "ordonnances": ordonnances,  # Variable: ordonnances (pas ordonnances_en_attente)
            "total_en_attente": ordonnances.count(),
            "date_aujourdhui": date.today().strftime("%d/%m/%Y"),
            "user_group": get_user_primary_group(request.user),
        })
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement des ordonnances: {e}")
        return redirect('pharmacien:dashboard_pharmacien')

@login_required
@pharmacien_required
def detail_ordonnance(request, ordonnance_id):
    """Affiche le détail d'une ordonnance."""
    try:
        # CORRECTION: Utiliser le bon modèle
        from medecin.models import Ordonnance as MedecinOrdonnance
        
        ordonnance = get_object_or_404(
            MedecinOrdonnance.objects.select_related("patient", "medecin"),
            id=ordonnance_id
        )

        return render(request, "pharmacien/detail_ordonnance.html", {
            "ordonnance": ordonnance,
            "est_deja_validee": ordonnance.statut == "valide",
            "date_aujourdhui": date.today().strftime("%d/%m/%Y"),
            "user_group": get_user_primary_group(request.user),
        })
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement de l'ordonnance: {e}")
        return redirect('pharmacien:liste_ordonnances_attente')

# ---------------------------------------------------------------------
# VALIDATION / REFUS D'ORDONNANCE - VERSION CORRIGÉE
# ---------------------------------------------------------------------
@login_required
@pharmacien_required
def valider_ordonnance(request, ordonnance_id):
    """Valide une ordonnance après vérification."""
    try:
        # CORRECTION: Utiliser le bon modèle
        from medecin.models import Ordonnance as MedecinOrdonnance
        
        ordonnance = get_object_or_404(
            MedecinOrdonnance.objects.select_related("patient", "medecin"),
            id=ordonnance_id
        )

        if ordonnance.statut == "valide":
            messages.info(request, f"L'ordonnance #{ordonnance.id} est déjà validée.")
            return redirect("pharmacien:detail_ordonnance", ordonnance_id=ordonnance.id)

        if request.method == "POST":
            form = ValiderOrdonnanceForm(request.POST, instance=ordonnance)
            if form.is_valid():
                with transaction.atomic():
                    ordonnance.statut = "valide"
                    ordonnance.date_validation = timezone.now()

                    if hasattr(ordonnance, "pharmacien_validateur"):
                        ordonnance.pharmacien_validateur = request.user

                    notes = form.cleaned_data.get("notes_pharmacien")
                    if notes and hasattr(ordonnance, "notes_pharmacien"):
                        ordonnance.notes_pharmacien = notes

                    ordonnance.save()
                    messages.success(request, f"Ordonnance #{ordonnance.id} validée avec succès.")
                    return redirect("pharmacien:liste_ordonnances_attente")
            else:
                messages.error(request, "Erreur dans le formulaire.")
        else:
            form = ValiderOrdonnanceForm(instance=ordonnance)

        return render(request, "pharmacien/valider_ordonnance.html", {
            "ordonnance": ordonnance,
            "form": form,
            "date_aujourdhui": date.today().strftime("%d/%m/%Y"),
            "user_group": get_user_primary_group(request.user),
        })
    except Exception as e:
        messages.error(request, f"Erreur lors de la validation: {e}")
        return redirect('pharmacien:detail_ordonnance', ordonnance_id=ordonnance_id)

@login_required
@pharmacien_required
def refuser_ordonnance(request, ordonnance_id):
    """Refuse une ordonnance avec un motif."""
    try:
        # CORRECTION: Utiliser le bon modèle
        from medecin.models import Ordonnance as MedecinOrdonnance
        
        ordonnance = get_object_or_404(
            MedecinOrdonnance.objects.select_related("patient", "medecin"),
            id=ordonnance_id
        )

        if ordonnance.statut == "refuse":
            messages.warning(request, f"L'ordonnance #{ordonnance.id} est déjà refusée.")
            return redirect("pharmacien:detail_ordonnance", ordonnance_id=ordonnance.id)

        if request.method == "POST":
            motif_refus = request.POST.get("motif_refus", "").strip()
            if not motif_refus:
                messages.error(request, "Veuillez fournir un motif de refus.")
                return render(request, "pharmacien/refuser_ordonnance.html", {
                    "ordonnance": ordonnance,
                    "date_aujourdhui": date.today().strftime("%d/%m/%Y"),
                    "user_group": get_user_primary_group(request.user),
                })

            with transaction.atomic():
                ordonnance.statut = "refuse"
                ordonnance.date_validation = timezone.now()
                if hasattr(ordonnance, "motif_refus"):
                    ordonnance.motif_refus = motif_refus
                elif hasattr(ordonnance, "notes_pharmacien"):
                    ordonnance.notes_pharmacien = f"Refusé - {motif_refus}"
                ordonnance.save()

            messages.warning(request, f"Ordonnance #{ordonnance.id} refusée.")
            return redirect("pharmacien:liste_ordonnances_attente")

        return render(request, "pharmacien/refuser_ordonnance.html", {
            "ordonnance": ordonnance,
            "date_aujourdhui": date.today().strftime("%d/%m/%Y"),
            "user_group": get_user_primary_group(request.user),
        })
    except Exception as e:
        messages.error(request, f"Erreur lors du refus: {e}")
        return redirect('pharmacien:detail_ordonnance', ordonnance_id=ordonnance_id)

# ---------------------------------------------------------------------
# HISTORIQUE ET EXPORT CSV - VERSION CORRIGÉE
# ---------------------------------------------------------------------




@login_required
@pharmacien_required
@gerer_erreurs
def historique_validation(request):
    """Affiche l'historique des ordonnances validées par le pharmacien"""
    try:
        # Importer les modèles nécessaires
        from pharmacien.models import OrdonnancePharmacien, Pharmacien
        from django.core.paginator import Paginator
        from django.utils import timezone
        from datetime import timedelta
        import logging
        
        logger = logging.getLogger(__name__)
        
        # 1. Obtenir le profil Pharmacien de l'utilisateur
        try:
            pharmacien_profile = Pharmacien.objects.get(user=request.user)
        except Pharmacien.DoesNotExist:
            logger.error(f"Profil pharmacien non trouvé pour {request.user.username}")
            from django.contrib import messages
            messages.error(request, "Profil pharmacien introuvable.")
            return redirect('pharmacien:dashboard')
        
        # 2. Récupérer l'historique des validations
        # CORRECTION: utiliser pharmacien_validateur (Foreign Key vers User)
        validations_qs = OrdonnancePharmacien.objects.filter(
            pharmacien_validateur=request.user,  # CHANGÉ ICI: pharmacien_validateur est un ForeignKey vers User
            date_validation__isnull=False
        ).select_related(
            'ordonnance_medecin__patient',
            'ordonnance_medecin__medecin'
        ).order_by('-date_validation')
        
        # 3. Adapter les données pour le template
        validations_list = []
        for validation in validations_qs:
            if hasattr(validation, 'ordonnance_medecin') and validation.ordonnance_medecin:
                ordonnance = validation.ordonnance_medecin
                validations_list.append({
                    'ordonnance': {
                        'id': ordonnance.id if hasattr(ordonnance, 'id') else validation.id,
                        'ordonnance_medecin': {
                            'patient': getattr(ordonnance, 'patient', None),
                            'medecin': getattr(ordonnance, 'medecin', None),
                            'date_prescription': getattr(ordonnance, 'date_prescription', None),
                        }
                    },
                    'date_validation': validation.date_validation,
                })
        
        # 4. Pagination
        paginator = Paginator(validations_list, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # 5. Statistiques
        stats = {
            'total': len(validations_list),
            'mois_courant': validations_qs.filter(
                date_validation__month=timezone.now().month,
                date_validation__year=timezone.now().year
            ).count(),
            'semaine_courante': validations_qs.filter(
                date_validation__gte=timezone.now() - timedelta(days=7)
            ).count(),
        }
        
        # 6. Contexte
        context = {
            'validations': page_obj,
            'stats': stats,
            'title': 'Historique des validations',
            'pharmacien_profile': pharmacien_profile,
        }
        return render(request, 'pharmacien/historique.html', context)
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erreur dans historique_validation : {e}")
        from django.contrib import messages
        messages.error(request, "Erreur lors du chargement de l'historique.")
        return redirect('pharmacien:dashboard')
@login_required
@pharmacien_required
def export_historique(request):
    """Exporte l'historique des validations au format CSV."""
    try:
        # CORRECTION: Utiliser le bon modèle
        from medecin.models import Ordonnance as MedecinOrdonnance
        
        date_debut = request.GET.get("date_debut")
        date_fin = request.GET.get("date_fin")

        validations = MedecinOrdonnance.objects.filter(statut="valide")
        if date_debut:
            validations = validations.filter(date_validation__gte=date_debut)
        if date_fin:
            validations = validations.filter(date_validation__lte=date_fin)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="historique_validations.csv"'

        writer = csv.writer(response)
        writer.writerow(["ID", "Patient", "Médecin", "Médicament", "Date Validation", "Statut"])

        for v in validations:
            patient = v.patient if v.patient else None
            medecin = v.medecin if v.medecin else None
            writer.writerow([
                v.id,
                f"{patient.first_name} {patient.last_name}" if patient else "N/A",
                f"{medecin.first_name} {medecin.last_name}" if medecin else "N/A",
                v.medicaments or "N/A",
                v.date_validation.strftime("%d/%m/%Y %H:%M") if v.date_validation else "N/A",
                v.statut,
            ])

        return response
    except Exception as e:
        messages.error(request, f"Erreur lors de l'export: {e}")
        return redirect('pharmacien:historique_validation')

# ---------------------------------------------------------------------
# PROFIL PHARMACIEN - VERSION CORRIGÉE
# ---------------------------------------------------------------------
@login_required
@pharmacien_required
def profil_pharmacien(request):
    """Affiche et met à jour le profil du pharmacien."""
    try:
        pharmacien, created = Pharmacien.objects.get_or_create(user=request.user)

        if request.method == "POST":
            form = PharmacienProfileForm(request.POST, instance=pharmacien)
            if form.is_valid():
                form.save()
                messages.success(request, "Profil mis à jour avec succès !")
                return redirect("pharmacien:dashboard_pharmacien")
            else:
                messages.error(request, "Erreur dans le formulaire.")
        else:
            # REQUÊTE GET - afficher le formulaire
            form = PharmacienProfileForm(instance=pharmacien)

        # TOUJOURS afficher le template avec le formulaire
        return render(request, "pharmacien/profil.html", {
            "form": form,
            "pharmacien": pharmacien,
            "date_aujourdhui": date.today().strftime("%d/%m/%Y"),
            "user_group": get_user_primary_group(request.user),
        })
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement du profil: {e}")
        # Même en cas d'erreur, afficher le template
        return render(request, "pharmacien/profil.html", {
            "form": PharmacienProfileForm(),
            "pharmacien": None,
            "date_aujourdhui": date.today().strftime("%d/%m/%Y"),
            "user_group": get_user_primary_group(request.user),
        })
# ---------------------------------------------------------------------
# RECHERCHE ET FILTRAGE - VERSION CORRIGÉE
# ---------------------------------------------------------------------
@login_required
@pharmacien_required
def rechercher_ordonnances(request):
    """Recherche avancée des ordonnances."""
    try:
        # CORRECTION: Utiliser le bon modèle
        from medecin.models import Ordonnance as MedecinOrdonnance
        
        form = RechercheOrdonnanceForm(request.GET or None)
        ordonnances = MedecinOrdonnance.objects.none()

        if form.is_valid():
            query = form.cleaned_data.get("query", "")
            statut = form.cleaned_data.get("statut", "")
            date_debut = form.cleaned_data.get("date_debut")
            date_fin = form.cleaned_data.get("date_fin")

            ordonnances = MedecinOrdonnance.objects.all()

            if query:
                ordonnances = ordonnances.filter(
                    Q(patient__first_name__icontains=query) |
                    Q(patient__last_name__icontains=query) |
                    Q(medecin__first_name__icontains=query) |
                    Q(medecin__last_name__icontains=query) |
                    Q(medicaments__icontains=query)
                )

            if statut:
                ordonnances = ordonnances.filter(statut=statut)
            if date_debut:
                ordonnances = ordonnances.filter(date_creation__gte=date_debut)
            if date_fin:
                ordonnances = ordonnances.filter(date_creation__lte=date_fin)

            ordonnances = ordonnances.select_related("patient", "medecin")

        return render(request, "pharmacien/recherche_ordonnances.html", {
            "form": form,
            "ordonnances": ordonnances,
            "total_resultats": ordonnances.count(),
            "user_group": get_user_primary_group(request.user),
        })
    except Exception as e:
        messages.error(request, f"Erreur lors de la recherche: {e}")
        return redirect('pharmacien:dashboard_pharmacien')

@login_required
@pharmacien_required
def filtrer_ordonnances(request):
    """Filtrage rapide des ordonnances."""
    try:
        # CORRECTION: Utiliser le bon modèle
        from medecin.models import Ordonnance as MedecinOrdonnance
        
        form = FiltreOrdonnanceForm(request.GET or None)
        tri = "-date_creation"
        items_par_page = 25

        if form.is_valid():
            tri = form.cleaned_data.get("tri", "-date_creation")
            items_par_page = int(form.cleaned_data.get("items_par_page", 25))

        ordonnances = (
            MedecinOrdonnance.objects.select_related("patient", "medecin")
            .order_by(tri)[:items_par_page]
        )

        return render(request, "pharmacien/filtre_ordonnances.html", {
            "form": form,
            "ordonnances": ordonnances,
            "tri_actuel": tri,
            "items_par_page": items_par_page,
            "user_group": get_user_primary_group(request.user),
        })
    except Exception as e:
        messages.error(request, f"Erreur lors du filtrage: {e}")
        return redirect('pharmacien:dashboard_pharmacien')

# ---------------------------------------------------------------------
# API JSON (AJAX DASHBOARD) - VERSION CORRIGÉE
# ---------------------------------------------------------------------
@login_required
@pharmacien_required
def api_ordonnances_attente(request):
    """Retourne le nombre d'ordonnances en attente (AJAX)."""
    try:
        # CORRECTION: Utiliser le bon modèle
        from medecin.models import Ordonnance as MedecinOrdonnance
        
        count = MedecinOrdonnance.objects.filter(statut="ACTIVE").count()
        return JsonResponse({"count": count})
    except Exception as e:
        return JsonResponse({"count": 0, "error": str(e)})

@login_required
@pharmacien_required
def api_statistiques_temps_reel(request):
    """Statistiques en temps réel (AJAX)."""
    try:
        # CORRECTION: Utiliser le bon modèle
        from medecin.models import Ordonnance as MedecinOrdonnance
        
        today = timezone.now().date()
        stats = {
            "attente": MedecinOrdonnance.objects.filter(statut="ACTIVE").count(),
            "validees_aujourdhui": MedecinOrdonnance.objects.filter(statut="valide", date_validation__date=today).count(),
            "validees_semaine": MedecinOrdonnance.objects.filter(statut="valide", date_validation__gte=today - timedelta(days=7)).count(),
            "validees_mois": MedecinOrdonnance.objects.filter(statut="valide", date_validation__month=today.month).count(),
        }
        return JsonResponse(stats)
    except Exception as e:
        return JsonResponse({"error": str(e)})

@login_required
@pharmacien_required
def api_statistiques_pharmacien(request):
    """Statistiques globales du pharmacien."""
    try:
        # CORRECTION: Utiliser le bon modèle
        from medecin.models import Ordonnance as MedecinOrdonnance
        
        total = MedecinOrdonnance.objects.count()
        validees = MedecinOrdonnance.objects.filter(statut="valide").count()
        taux = round((validees / total) * 100, 1) if total else 0

        data = {
            "ordonnances_attente": MedecinOrdonnance.objects.filter(statut="ACTIVE").count(),
            "total_ordonnances": total,
            "validations_mois": MedecinOrdonnance.objects.filter(statut="valide", date_validation__month=timezone.now().month).count(),
            "taux_validation": taux,
        }
        return JsonResponse({"status": "success", "data": data})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

# =============================================================================
# VUES POUR LA GESTION DU STOCK - VERSION COMPLÈTEMENT CORRIGÉE
# =============================================================================

@login_required
@pharmacien_required
def gestion_stock(request):
    """Page de gestion du stock - VERSION CORRIGÉE"""
    try:
        pharmacien = get_object_or_404(Pharmacien, user=request.user)
        stocks = StockPharmacie.objects.filter(pharmacie=pharmacien).order_by('-date_creation')
        
        # Filtres
        categorie_filter = request.GET.get('categorie', '')
        statut_filter = request.GET.get('statut', '')
        recherche = request.GET.get('recherche', '')
        
        if categorie_filter:
            stocks = stocks.filter(categorie=categorie_filter)
        
        if statut_filter:
            if statut_filter == 'normal':
                stocks = stocks.filter(quantite_stock__gt=F('seuil_alerte'))
            elif statut_filter == 'alerte':
                stocks = stocks.filter(quantite_stock__lte=F('seuil_alerte'), quantite_stock__gt=0)
            elif statut_filter == 'rupture':
                stocks = stocks.filter(quantite_stock=0)
            elif statut_filter == 'perime':
                stocks = stocks.filter(date_peremption__lt=timezone.now().date())
        
        if recherche:
            stocks = stocks.filter(
                Q(nom_medicament__icontains=recherche) |
                Q(code_medicament__icontains=recherche) |
                Q(categorie__icontains=recherche)
            )
        
        # Calcul des statistiques
        total_stocks = stocks.count()
        stocks_normal = stocks.filter(quantite_stock__gt=F('seuil_alerte')).count()
        stocks_alerte = stocks.filter(quantite_stock__lte=F('seuil_alerte'), quantite_stock__gt=0).count()
        stocks_rupture = stocks.filter(quantite_stock=0).count()
        stocks_perimes = stocks.filter(date_peremption__lt=timezone.now().date()).count()
        
        # Valeur totale du stock
        valeur_stock = stocks.aggregate(total_vente=Sum('prix_vente'))
        
        context = {
            'page_title': 'Gestion du Stock',
            'active_tab': 'stock',
            'user_group': get_user_primary_group(request.user),
            'stocks': stocks,
            'today': timezone.now().date(),
            'total_stocks': total_stocks,
            'stocks_normal': stocks_normal,
            'stocks_alerte': stocks_alerte,
            'stocks_rupture': stocks_rupture,
            'stocks_perimes': stocks_perimes,
            'valeur_stock': valeur_stock['total_vente'] or 0,
            'categories': StockPharmacie.CATEGORIE_MEDICAMENT,
            'recherche': recherche,
            'categorie_filter': categorie_filter,
            'statut_filter': statut_filter,
        }
        return render(request, 'pharmacien/stock.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement du stock: {str(e)}")
        return render(request, 'pharmacien/stock.html', {
            'page_title': 'Gestion du Stock',
            'active_tab': 'stock',
            'stocks': [],
            'total_stocks': 0,
            'stocks_normal': 0,
            'stocks_alerte': 0,
            'stocks_rupture': 0,
            'stocks_perimes': 0,
            'valeur_stock': 0,
        })

@login_required
@pharmacien_required
def export_stock(request):
    """Exporter le stock en CSV - VERSION COMPLÈTE"""
    try:
        pharmacien = get_object_or_404(Pharmacien, user=request.user)
        stocks = StockPharmacie.objects.filter(pharmacie=pharmacien)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="stock_pharmacie_{datetime.now().strftime("%Y%m%d_%H%M")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Nom Médicament', 'Code', 'Catégorie', 'Quantité Stock', 
            'Seuil Alerte', 'Prix Achat', 'Prix Vente', 'Marge',
            'Date Péremption', 'Jours Restants', 'Statut'
        ])
        
        for stock in stocks:
            jours_restants = stock.get_jours_avant_peremption() if stock.date_peremption else 'N/A'
            statut = stock.statut_stock
            
            writer.writerow([
                stock.nom_medicament,
                stock.code_medicament or '',
                stock.get_categorie_display(),
                stock.quantite_stock,
                stock.seuil_alerte,
                f"{stock.prix_achat:.2f}",
                f"{stock.prix_vente:.2f}",
                f"{stock.marge:.2f}",
                stock.date_peremption.strftime("%d/%m/%Y") if stock.date_peremption else '',
                jours_restants,
                statut
            ])
        
        return response
        
    except Exception as e:
        messages.error(request, f"Erreur lors de l'export: {str(e)}")
        return redirect('pharmacien:stock')

@login_required
@pharmacien_required
def ajouter_stock(request):
    """Ajouter un produit au stock - VERSION CORRIGÉE"""
    if request.method == 'POST':
        try:
            with transaction.atomic():
                pharmacien = get_object_or_404(Pharmacien, user=request.user)
                
                nom_medicament = request.POST.get('nom_medicament')
                code_medicament = request.POST.get('code_medicament', '')
                categorie = request.POST.get('categorie', 'AUTRE')
                quantite_stock = int(request.POST.get('quantite_stock', 0))
                seuil_alerte = int(request.POST.get('seuil_alerte', 10))
                prix_achat = float(request.POST.get('prix_achat', 0))
                prix_vente = float(request.POST.get('prix_vente', 0))
                date_peremption = request.POST.get('date_peremption')
                
                if not nom_medicament:
                    messages.error(request, 'Le nom du médicament est obligatoire')
                    return redirect('pharmacien:ajouter_stock')
                
                if prix_vente < prix_achat:
                    messages.error(request, 'Le prix de vente doit être supérieur au prix d\'achat')
                    return redirect('pharmacien:ajouter_stock')
                
                existing_stock = StockPharmacie.objects.filter(
                    pharmacie=pharmacien,
                    nom_medicament=nom_medicament,
                    code_medicament=code_medicament
                ).first()
                
                if existing_stock:
                    existing_stock.quantite_stock += quantite_stock
                    existing_stock.prix_achat = prix_achat
                    existing_stock.prix_vente = prix_vente
                    if date_peremption:
                        existing_stock.date_peremption = datetime.strptime(date_peremption, '%Y-%m-%d').date()
                    existing_stock.save()
                    message = f"Stock de {nom_medicament} mis à jour. Quantité totale: {existing_stock.quantite_stock}"
                else:
                    stock = StockPharmacie(
                        pharmacie=pharmacien,
                        nom_medicament=nom_medicament,
                        code_medicament=code_medicament,
                        categorie=categorie,
                        quantite_stock=quantite_stock,
                        seuil_alerte=seuil_alerte,
                        prix_achat=prix_achat,
                        prix_vente=prix_vente,
                        actif=True
                    )
                    
                    if date_peremption:
                        stock.date_peremption = datetime.strptime(date_peremption, '%Y-%m-%d').date()
                    
                    stock.save()
                    message = f"Médicament {nom_medicament} ajouté au stock avec succès"
                
                messages.success(request, message)
                return redirect('pharmacien:stock')
                
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'ajout: {str(e)}')
            return redirect('pharmacien:ajouter_stock')
    
    context = {
        'page_title': 'Ajouter un Médicament',
        'active_tab': 'stock',
        'user_group': get_user_primary_group(request.user),
        'categories': StockPharmacie.CATEGORIE_MEDICAMENT,
    }
    return render(request, 'pharmacien/ajouter_stock.html', context)

@login_required
@pharmacien_required
def importer_stock(request):
    """Importer le stock depuis un fichier CSV - VERSION CORRIGÉE"""
    if request.method == 'POST' and request.FILES.get('fichier_csv'):
        try:
            pharmacien = get_object_or_404(Pharmacien, user=request.user)
            fichier = request.FILES['fichier_csv']
            
            if not fichier.name.endswith('.csv'):
                messages.error(request, 'Veuillez importer un fichier CSV')
                return redirect('pharmacien:importer_stock')
            
            decoded_file = fichier.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            produits_ajoutes = 0
            produits_modifies = 0
            erreurs = []
            
            with transaction.atomic():
                for ligne, row in enumerate(reader, start=2):
                    try:
                        nom_medicament = row.get('Nom Médicament', '').strip()
                        if not nom_medicament:
                            erreurs.append(f"Ligne {ligne}: Nom du médicament manquant")
                            continue
                        
                        code_medicament = row.get('Code', '').strip()
                        categorie = row.get('Catégorie', 'AUTRE').strip()
                        quantite = int(row.get('Quantité Stock', 0))
                        seuil = int(row.get('Seuil Alerte', 10))
                        prix_achat = float(row.get('Prix Achat', 0))
                        prix_vente = float(row.get('Prix Vente', 0))
                        
                        date_peremption_str = row.get('Date Péremption', '').strip()
                        date_peremption = None
                        if date_peremption_str:
                            try:
                                date_peremption = datetime.strptime(date_peremption_str, '%d/%m/%Y').date()
                            except ValueError:
                                try:
                                    date_peremption = datetime.strptime(date_peremption_str, '%Y-%m-%d').date()
                                except ValueError:
                                    erreurs.append(f"Ligne {ligne}: Format de date invalide")
                                    continue
                        
                        existing_stock = StockPharmacie.objects.filter(
                            pharmacie=pharmacien,
                            nom_medicament=nom_medicament,
                            code_medicament=code_medicament
                        ).first()
                        
                        if existing_stock:
                            existing_stock.quantite_stock += quantite
                            existing_stock.prix_achat = prix_achat
                            existing_stock.prix_vente = prix_vente
                            if date_peremption:
                                existing_stock.date_peremption = date_peremption
                            existing_stock.save()
                            produits_modifies += 1
                        else:
                            stock = StockPharmacie(
                                pharmacie=pharmacien,
                                nom_medicament=nom_medicament,
                                code_medicament=code_medicament,
                                categorie=categorie,
                                quantite_stock=quantite,
                                seuil_alerte=seuil,
                                prix_achat=prix_achat,
                                prix_vente=prix_vente,
                                date_peremption=date_peremption,
                                actif=True
                            )
                            stock.save()
                            produits_ajoutes += 1
                            
                    except Exception as e:
                        erreurs.append(f"Ligne {ligne}: {str(e)}")
                        continue
            
            message = f"Import terminé: {produits_ajoutes} ajoutés, {produits_modifies} modifiés"
            if erreurs:
                message += f". {len(erreurs)} erreur(s)"
            
            messages.success(request, message)
            return redirect('pharmacien:stock')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'import: {str(e)}')
            return redirect('pharmacien:importer_stock')
    
    context = {
        'page_title': 'Importer Stock',
        'active_tab': 'stock',
        'user_group': get_user_primary_group(request.user),
    }
    return render(request, 'pharmacien/importer_stock.html', context)

@login_required
@pharmacien_required
def desactiver_stock(request, stock_id):
    """Désactiver un produit du stock - VERSION CORRIGÉE"""
    if request.method == 'POST':
        try:
            pharmacien = get_object_or_404(Pharmacien, user=request.user)
            stock = get_object_or_404(StockPharmacie, id=stock_id, pharmacie=pharmacien)
            
            stock.actif = False
            stock.save()
            
            messages.success(request, 'Produit désactivé avec succès')
            return redirect('pharmacien:stock')
            
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('pharmacien:stock')
    
    return redirect('pharmacien:stock')

@login_required
@pharmacien_required
def activer_stock(request, stock_id):
    """Activer un produit du stock - VERSION CORRIGÉE"""
    if request.method == 'POST':
        try:
            pharmacien = get_object_or_404(Pharmacien, user=request.user)
            stock = get_object_or_404(StockPharmacie, id=stock_id, pharmacie=pharmacien)
            
            stock.actif = True
            stock.save()
            
            messages.success(request, 'Produit activé avec succès')
            return redirect('pharmacien:stock')
            
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('pharmacien:stock')
    
    return redirect('pharmacien:stock')

@login_required
@pharmacien_required
def modifier_stock(request, stock_id):
    """Modifier un produit du stock - VERSION COMPLÈTE"""
    try:
        pharmacien = get_object_or_404(Pharmacien, user=request.user)
        stock = get_object_or_404(StockPharmacie, id=stock_id, pharmacie=pharmacien)
        
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    stock.nom_medicament = request.POST.get('nom_medicament', stock.nom_medicament)
                    stock.code_medicament = request.POST.get('code_medicament', stock.code_medicament)
                    stock.categorie = request.POST.get('categorie', stock.categorie)
                    stock.quantite_stock = int(request.POST.get('quantite_stock', stock.quantite_stock))
                    stock.seuil_alerte = int(request.POST.get('seuil_alerte', stock.seuil_alerte))
                    stock.prix_achat = float(request.POST.get('prix_achat', stock.prix_achat))
                    stock.prix_vente = float(request.POST.get('prix_vente', stock.prix_vente))
                    
                    date_peremption = request.POST.get('date_peremption')
                    if date_peremption:
                        stock.date_peremption = datetime.strptime(date_peremption, '%Y-%m-%d').date()
                    else:
                        stock.date_peremption = None
                    
                    if stock.prix_vente < stock.prix_achat:
                        messages.error(request, 'Le prix de vente doit être supérieur au prix d\'achat')
                        return redirect('pharmacien:modifier_stock', stock_id=stock_id)
                    
                    stock.save()
                    messages.success(request, 'Produit modifié avec succès')
                    return redirect('pharmacien:stock')
                    
            except Exception as e:
                messages.error(request, f'Erreur lors de la modification: {str(e)}')
                return redirect('pharmacien:modifier_stock', stock_id=stock_id)
        
        context = {
            'page_title': 'Modifier le Stock',
            'active_tab': 'stock',
            'user_group': get_user_primary_group(request.user),
            'stock': stock,
            'categories': StockPharmacie.CATEGORIE_MEDICAMENT,
        }
        return render(request, 'pharmacien/modifier_stock.html', context)
    except Exception as e:
        messages.error(request, f'Erreur: {str(e)}')
        return redirect('pharmacien:stock')

@login_required
@pharmacien_required
def reapprovisionner_stock(request, stock_id):
    """Réapprovisionner un produit - VERSION COMPLÈTE"""
    try:
        pharmacien = get_object_or_404(Pharmacien, user=request.user)
        stock = get_object_or_404(StockPharmacie, id=stock_id, pharmacie=pharmacien)
        
        if request.method == 'POST':
            try:
                quantite_ajoutee = int(request.POST.get('quantite', 0))
                nouveau_prix_achat = float(request.POST.get('nouveau_prix_achat', stock.prix_achat))
                nouveau_prix_vente = float(request.POST.get('nouveau_prix_vente', stock.prix_vente))
                date_peremption = request.POST.get('date_peremption')
                
                if quantite_ajoutee <= 0:
                    messages.error(request, 'La quantité doit être positive')
                    return redirect('pharmacien:reapprovisionner_stock', stock_id=stock_id)
                
                stock.quantite_stock += quantite_ajoutee
                stock.prix_achat = nouveau_prix_achat
                stock.prix_vente = nouveau_prix_vente
                
                if date_peremption:
                    stock.date_peremption = datetime.strptime(date_peremption, '%Y-%m-%d').date()
                
                if stock.prix_vente < stock.prix_achat:
                    messages.error(request, 'Le prix de vente doit être supérieur au prix d\'achat')
                    return redirect('pharmacien:reapprovisionner_stock', stock_id=stock_id)
                
                stock.save()
                
                messages.success(request, f'Stock réapprovisionné: {quantite_ajoutee} unités ajoutées')
                return redirect('pharmacien:stock')
                
            except Exception as e:
                messages.error(request, f'Erreur lors du réapprovisionnement: {str(e)}')
                return redirect('pharmacien:reapprovisionner_stock', stock_id=stock_id)
        
        context = {
            'page_title': 'Réapprovisionner le Stock',
            'active_tab': 'stock',
            'user_group': get_user_primary_group(request.user),
            'stock': stock,
        }
        return render(request, 'pharmacien/reapprovisionner_stock.html', context)
    except Exception as e:
        messages.error(request, f'Erreur: {str(e)}')
        return redirect('pharmacien:stock')

# =============================================================================
# VUES GÉNÉRIQUES - VERSION CORRIGÉE
# =============================================================================

@login_required
def home(request):
    """Page d'accueil - Redirige vers le dashboard pharmacien"""
    return redirect('pharmacien:dashboard_pharmacien')

@login_required
def logout_view(request):
    """Déconnexion de l'utilisateur"""
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('pharmacien:dashboard_pharmacien')

# =============================================================================
# VUES DE COMMUNICATION SPÉCIFIQUES PHARMACIEN
# =============================================================================

@login_required
@pharmacien_required
def creer_conversation_medecin(request, medecin_id):
    """Créer une conversation avec un médecin spécifique."""
    try:
        from medecin.models import Medecin
        medecin_user = get_object_or_404(Medecin, id=medecin_id).user
        
        # Vérifier si une conversation existe déjà
        existing_conversation = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=medecin_user
        ).first()
        
        if existing_conversation:
            messages.info(request, "Une conversation existe déjà avec ce médecin")
            return redirect('communication:detail_conversation', conversation_id=existing_conversation.id)
        
        # Créer une nouvelle conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, medecin_user)
        
        messages.success(request, "Conversation créée avec succès")
        return redirect('communication:detail_conversation', conversation_id=conversation.id)
        
    except Exception as e:
        messages.error(request, f"Erreur lors de la création de la conversation: {e}")
        return redirect('pharmacien:dashboard_pharmacien')

@login_required
@pharmacien_required
def envoyer_notification_ordonnance(request, ordonnance_id):
    """Envoyer une notification concernant une ordonnance."""
    try:
        from medecin.models import Ordonnance as MedecinOrdonnance
        ordonnance = get_object_or_404(MedecinOrdonnance, id=ordonnance_id)
        
        if request.method == 'POST':
            message = request.POST.get('message', '').strip()
            if not message:
                messages.error(request, "Veuillez saisir un message")
                return redirect('pharmacien:detail_ordonnance', ordonnance_id=ordonnance_id)
            
            # Créer la notification pour le médecin
            if ordonnance.medecin and ordonnance.medecin.user:
                Notification.objects.create(
                    user=ordonnance.medecin.user,
                    titre=f"Notification Pharmacien - Ordonnance #{ordonnance.id}",
                    message=message,
                    lien=f"/medecin/ordonnances/{ordonnance.id}/"
                )
                messages.success(request, "Notification envoyée au médecin")
            else:
                messages.warning(request, "Impossible de trouver le médecin associé")
            
            return redirect('pharmacien:detail_ordonnance', ordonnance_id=ordonnance_id)
        
        context = {
            'ordonnance': ordonnance,
            'user_group': get_user_primary_group(request.user),
        }
        return render(request, 'pharmacien/envoyer_notification.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur: {e}")
        return redirect('pharmacien:liste_ordonnances_attente')




# =============================================================================
# VUES DE DÉBOGAGE
# =============================================================================

@login_required
@pharmacien_required
def debug_conversations(request):
    """Vue de débogage pour les conversations."""
    try:
        # Récupérer toutes les conversations
        conversations = Conversation.objects.filter(
            participants=request.user
        ).prefetch_related('participants')
        
        # Vérifier les données brutes
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT cc.id, u.username 
                FROM communication_conversation cc
                JOIN communication_conversation_participants cp ON cc.id = cp.conversation_id
                JOIN auth_user u ON cp.user_id = u.id
                ORDER BY cc.id, u.username
            """)
            raw_data = cursor.fetchall()
        
        context = {
            'user': request.user,
            'conversations': conversations,
            'conversations_count': conversations.count(),
            'raw_data': raw_data,
            'user_group': get_user_primary_group(request.user),
        }
        
        return render(request, 'pharmacien/debug_conversations.html', context)
        
    except Exception as e:
        return HttpResponse(f"Erreur de débogage: {e}")

@login_required
@pharmacien_required
def creer_conversations_test(request):
    """Créer des conversations de test pour le débogage."""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Trouver d'autres utilisateurs
        autres_users = User.objects.exclude(id=request.user.id).exclude(is_superuser=True)[:2]
        
        conversations_creees = []
        
        for autre_user in autres_users:
            # Créer conversation
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, autre_user)
            
            # Ajouter messages
            Message.objects.create(
                conversation=conversation,
                expediteur=request.user,
                contenu=f"Bonjour {autre_user.username}, je vous contacte en tant que pharmacien."
            )
            
            Message.objects.create(
                conversation=conversation,
                expediteur=autre_user,
                contenu=f"Bonjour pharmacien, comment puis-je vous aider?"
            )
            
            conversations_creees.append(conversation)
        
        messages.success(request, f"{len(conversations_creees)} conversations de test créées")
        return redirect('pharmacien:debug_conversations')
        
    except Exception as e:
        messages.error(request, f"Erreur: {e}")
        return redirect('pharmacien:debug_conversations')




@login_required
def messagerie_pharmacien(request):
    """Vue spécifique pour les pharmaciens"""
    try:
        from django.utils import timezone
        from datetime import datetime, timedelta
        
        user = request.user
        
        # Récupérer les conversations
        conversations = Conversation.objects.filter(participants=user).annotate(
            nb_messages_non_lus=Count('messages', filter=Q(messages__est_lu=False) & ~Q(messages__expediteur=user)),
            derniere_activite=Max('messages__date_envoi')
        ).order_by('-derniere_activite')
        
        # Messages récents (24 dernières heures)
        aujourd_hui = timezone.now() - timedelta(hours=24)
        messages_recents = Message.objects.filter(
            Q(expediteur=user) | Q(destinataire=user),
            date_envoi__gte=aujourd_hui
        ).select_related('expediteur', 'destinataire').order_by('-date_envoi')[:20]
        
        # Messages urgents
        messages_urgents = Message.objects.filter(
            destinataire=user,
            type_message='URGENT',
            est_lu=False
        ).order_by('-date_envoi')
        
        # Statistiques
        total_messages = Message.objects.filter(
            Q(expediteur=user) | Q(destinataire=user)
        ).count()
        
        messages_non_lus = Message.objects.filter(
            destinataire=user,
            est_lu=False
        ).count()
        
        aujourd_hui_count = Message.objects.filter(
            Q(expediteur=user) | Q(destinataire=user),
            date_envoi__gte=aujourd_hui
        ).count()
        
        context = {
            'conversations': conversations,
            'messages_recents': messages_recents,
            'messages_urgents': messages_urgents,
            'total_messages': total_messages,
            'messages_non_lus': messages_non_lus,
            'total_conversations': conversations.count(),
            'aujourd_hui_count': aujourd_hui_count,
            'notifications_count': Notification.objects.filter(user=user, est_lue=False).count(),
            'page_title': 'Messagerie Pharmacien',
            'user_type': 'pharmacien'
        }
        
        return render(request, 'communication/messagerie_pharmacien.html', context)
        
    except Exception as e:
        context = {
            'error': str(e),
            'page_title': 'Messagerie Pharmacien',
            'user_type': 'pharmacien'
        }
        return render(request, 'communication/messagerie_pharmacien.html', context)

# =============================================================================
# VUE DE TEST SIMPLIFIÉE
# =============================================================================

@login_required
@pharmacien_required 
def test_affichage(request):
    """Vue de test simplifiée."""
    print(f"TEST: Utilisateur: {request.user.username}")
    print(f"TEST: Groups: {[g.name for g in request.user.groups.all()]}")
    
    # Test des conversations
    conversations = Conversation.objects.filter(participants=request.user)
    print(f"TEST: Conversations: {conversations.count()}")
    
    return HttpResponse(f"""
    <h1>Test Pharmacien</h1>
    <p>Utilisateur: {request.user.username}</p>
    <p>Groups: {[g.name for g in request.user.groups.all()]}</p>
    <p>Conversations: {conversations.count()}</p>
    <a href="/pharmacien/dashboard/">Retour au dashboard</a>
    """)

# =============================================================================
# VUE DE REDIRECTION APRÈS LOGIN
# =============================================================================

def redirect_after_login(request):
    """Redirection après connexion basée sur le groupe de l'utilisateur."""
    user = request.user
    print(f"🔍 Redirect after login - User: {user.username}")
    
    if user.groups.filter(name='PHARMACIEN').exists():
        return redirect('pharmacien:dashboard_pharmacien')
    elif user.groups.filter(name='MEDECIN').exists():
        return redirect('medecin:dashboard_medecin')
    elif user.groups.filter(name='AGENT').exists():
        return redirect('agents:tableau_de_bord')
    else:
        return redirect('login')

# =============================================================================
# VUE DE TEST PUBLIQUE (Sans authentification)
# =============================================================================

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def test_public(request):
    """Vue de test publique sans authentification."""
    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>✅ Test Public - Pharmacien</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                color: white;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                padding: 40px;
                border-radius: 15px;
                text-align: center;
                max-width: 600px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }
            h1 {
                margin-bottom: 20px;
                font-size: 2.5em;
            }
            .success {
                color: #4CAF50;
                font-size: 3em;
                margin-bottom: 20px;
            }
            .button {
                display: inline-block;
                background: white;
                color: #667eea;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                margin: 10px;
                transition: transform 0.3s;
            }
            .button:hover {
                transform: translateY(-3px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success">✅</div>
            <h1>Test Public Réussi!</h1>
            <p>Le serveur Django fonctionne correctement.</p>
            <p><strong>Module Pharmacien</strong> est opérationnel.</p>
            
            <div style="margin-top: 30px;">
                <a href="/accounts/login/" class="button">Tester l'authentification</a>
                <a href="/pharmacien/dashboard/" class="button">Dashboard Pharmacien</a>
            </div>
            
            <div style="margin-top: 30px; font-size: 0.9em; opacity: 0.8;">
                <p>Serveur: <strong>Django 5.2.7</strong></p>
                <p>URL: <code>/pharmacien/test-public/</code></p>
            </div>
        </div>
    </body>
    </html>
    """)


# Ajoutez dans pharmacien/views.py
@login_required
@pharmacien_required
def debug_data(request):
    """Page de debug pour vérifier les données."""
    from communication.models import Conversation, Notification
    
    conversations = Conversation.objects.filter(participants=request.user)
    notifications = Notification.objects.filter(user=request.user)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Debug Data</title></head>
    <body>
        <h1>🔍 Debug Data - {request.user.username}</h1>
        
        <h2>Conversations ({conversations.count()})</h2>
        <ul>
    """
    
    for conv in conversations:
        participants = [p.username for p in conv.participants.all()]
        html += f"<li>Conv {conv.id}: {participants} (Messages: {conv.messages.count()})</li>"
    
    html += """
        </ul>
        
        <h2>Notifications</h2>
        <ul>
    """
    
    for notif in notifications:
        html += f"<li>{notif.titre} - Lu: {notif.est_lue}</li>"
    
    html += f"""
        </ul>
        
        <p><a href="/pharmacien/dashboard/">Retour au dashboard</a></p>
    </body>
    </html>
    """
    
    return HttpResponse(html)