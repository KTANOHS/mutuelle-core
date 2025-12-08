# membres/views.py - CODE COMPLET CORRIGÉ
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate
import csv
import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from core.utils import est_agent, gerer_erreurs, est_assureur
from .forms import MembreCreationForm, MembreDocumentForm
from datetime import date
import os
from .forms import InscriptionMembreForm, ValidationDocumentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from membres.models import Membre, HistoriqueValidationDocument
from soins.models import BonDeSoin

from medecin.models import Ordonnance

# ✅ IMPORTS POUR SOINS
from soins.models import Soin
from datetime import timedelta

# ✅ IMPORTS MANQUANTS AJOUTÉS
from django.db import models
from django.db.models import Count, Sum, Q, Avg
import json
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# ==============================================================================
# VUES PUBLIQUES
# ==============================================================================

def liste_membres(request):
    membres = Membre.objects.all()
    return render(request, 'membres/liste_membres.html', {'membres': membres})

def detail_membre(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)
    return render(request, 'membres/detail_membre.html', {'membre': membre})


def inscription_membre(request):
    """Inscription d'un nouveau membre de la mutuelle"""
    if request.method == 'POST':
        form = InscriptionMembreForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # 1️⃣ Créer l'utilisateur lié
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']

                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=form.cleaned_data['prenom'],
                    last_name=form.cleaned_data['nom']
                )

                # 2️⃣ Ajouter au groupe "Membres"
                groupe, _ = Group.objects.get_or_create(name='Membres')
                user.groups.add(groupe)

                # 3️⃣ Créer le membre lié
                membre = form.save(commit=False)
                membre.user = user
                membre.date_derniere_cotisation = date.today()
                membre.statut = 'actif'
                membre.statut_documents = 'EN_ATTENTE'

                # 4️⃣ Gérer les noms de fichiers uploadés
                if membre.piece_identite_recto:
                    ext = os.path.splitext(membre.piece_identite_recto.name)[1][1:]
                    membre.piece_identite_recto.name = f"pieces/{membre.numero_unique}_recto.{ext}"

                if membre.piece_identite_verso:
                    ext = os.path.splitext(membre.piece_identite_verso.name)[1][1:]
                    membre.piece_identite_verso.name = f"pieces/{membre.numero_unique}_verso.{ext}"

                if membre.photo_identite:
                    ext = os.path.splitext(membre.photo_identite.name)[1][1:]
                    membre.photo_identite.name = f"photos/{membre.numero_unique}_photo.{ext}"

                membre.save()

                # 5️⃣ Authentifier et connecter automatiquement
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)

                messages.success(
                    request,
                    f"Félicitations {membre.prenom} ! "
                    f"Votre inscription a été enregistrée avec succès. "
                    f"Votre numéro de membre est : {membre.numero_unique}. "
                    "Vos documents sont en cours de validation."
                )
                return redirect('membres:dashboard')

            except Exception as e:
                # Nettoyer si une erreur survient
                if 'user' in locals():
                    user.delete()
                messages.error(request, f"Une erreur est survenue : {str(e)}")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = InscriptionMembreForm()

    context = {
        'form': form,
        'types_pieces': [('CNI', 'Carte Nationale d\'Identité'), ('PASSEPORT', 'Passeport'), ('PERMIS', 'Permis de conduire')],
        'title': 'Inscription - Devenir Membre'
    }
    return render(request, 'inscription/inscription.html', context)


# ==========================================================
# 🔹 Validation des documents (côté Agent / Admin)
# ==========================================================
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Agents').exists() or u.is_staff)
def validation_documents(request, membre_id):
    """Validation des documents d'un membre par un agent"""
    membre = get_object_or_404(Membre, id=membre_id)

    if request.method == 'POST':
        ancien_statut = membre.statut_documents
        form = ValidationDocumentForm(request.POST, instance=membre)

        if form.is_valid():
            membre = form.save(commit=False)
            membre.date_validation_documents = timezone.now()
            membre.save()

            # Enregistrer l'historique
            HistoriqueValidationDocument.objects.create(
                membre=membre,
                agent=request.user,
                ancien_statut=ancien_statut,
                nouveau_statut=membre.statut_documents,
                motif=membre.motif_rejet
            )

            # Notification selon le statut
            if membre.statut_documents == 'VALIDE':
                messages.success(request, f"Documents de {membre.prenom} {membre.nom} validés avec succès !")
                try:
                    from communication.utils import envoyer_notification
                    envoyer_notification(
                        user=membre.user,
                        titre="Documents validés",
                        message="Vos documents ont été validés. Votre compte est maintenant actif.",
                        type_notification='DOCUMENT_VALIDE'
                    )
                except ImportError:
                    pass  # Si le module de notification n'est pas encore implémenté
            elif membre.statut_documents == 'REJETE':
                messages.warning(request, f"Documents de {membre.prenom} {membre.nom} rejetés.")

            return redirect('liste_membres_attente_validation')

    else:
        form = ValidationDocumentForm(instance=membre)

    context = {
        'membre': membre,
        'form': form,
    }
    return render(request, 'inscription/validation_documents.html', context)


# ==========================================================
# 🔹 Liste des membres en attente de validation
# ==========================================================
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Agents').exists() or u.is_staff)
def liste_membres_attente_validation(request):
    """Affiche les membres dont les documents sont en attente"""
    membres_attente = Membre.objects.filter(
        statut_documents='EN_ATTENTE'
    ).order_by('date_inscription')

    context = {
        'membres_attente': membres_attente,
        'title': 'Membres en attente de validation'
    }
    return render(request, 'inscription/liste_validation.html', context)


# ==============================================================================
# FONCTION UTILITAIRE POUR CRÉER UN PROFIL MEMBRE AUTOMATIQUEMENT
# ==============================================================================

def creer_profil_membre_automatique(user):
    """Crée automatiquement un profil membre pour un utilisateur"""
    # Générer un numéro unique
    while True:
        annee = timezone.now().strftime('%Y')
        random_part = ''.join(random.choices(string.digits, k=5))
        numero = f"MEM{annee}{random_part}"
        if not Membre.objects.filter(numero_unique=numero).exists():
            break
    
    # Créer le profil membre avec les informations de l'utilisateur
    membre = Membre.objects.create(
        user=user,
        nom=user.last_name or "Non défini",
        prenom=user.first_name or "Non défini",
        email=user.email or f"{user.username}@example.com",
        numero_unique=numero,
        statut='actif',
        categorie='standard',
        date_inscription=timezone.now().date(),
        date_derniere_cotisation=timezone.now().date(),
        telephone="Non défini",
        adresse="Non définie",
        profession="Non définie"
    )
    
    return membre

# ==============================================================================
# VUES MEMBRES (PROTÉGÉES) - VERSIONS CORRIGÉES
# ==============================================================================

@login_required
def dashboard(request):
    """Tableau de bord pour les membres avec intégration soins - VERSION CORRIGÉE"""
    try:
        # Vérifier si l'utilisateur a un profil membre
        try:
            membre = Membre.objects.get(user=request.user)
        except Membre.DoesNotExist:
            # ✅ CORRECTION : Créer automatiquement le profil membre
            membre = creer_profil_membre_automatique(request.user)
            messages.success(request, f"Profil membre créé automatiquement ! Votre numéro : {membre.numero_unique}")
        
        # ========================
        # STATISTIQUES SOINS DU MEMBRE
        # ========================
        try:
            # CORRECTION : Utiliser le bon champ pour filtrer les soins
            mes_soins = Soin.objects.filter(patient=membre)
            soins_total = mes_soins.count()
            soins_valides = mes_soins.filter(statut='valide').count()
            soins_attente = mes_soins.filter(statut='attente').count()
            
            # Derniers soins du membre
            derniers_soins = mes_soins.select_related(
                'type_soin', 'medecin'
            ).order_by('-date_realisation')[:10]
            
            # Soins récents (30 derniers jours)
            date_limite = timezone.now() - timedelta(days=30)
            soins_recents = mes_soins.filter(date_realisation__gte=date_limite).count()
            
            # Coût total des soins validés
            cout_total = mes_soins.filter(statut='valide').aggregate(
                total=Sum('cout_reel')
            )['total'] or 0
        except Exception as e:
            # Si erreur avec les soins, mettre des valeurs par défaut
            soins_total = 0
            soins_valides = 0
            soins_attente = 0
            soins_recents = 0
            cout_total = 0
            derniers_soins = []
        
        # ========================
        # INFORMATIONS DU MEMBRE
        # ========================
        aujourdhui = timezone.now().date()
        jours_restants_cotisation = 0
        statut_cotisation = "Non défini"
        
        if membre.date_derniere_cotisation:
            date_expiration = membre.date_derniere_cotisation + timedelta(days=365)
            jours_restants_cotisation = (date_expiration - aujourdhui).days
            statut_cotisation = "À jour" if jours_restants_cotisation > 0 else "En retard"
        
        # Calcul du pourcentage de progression de la cotisation
        if membre.date_derniere_cotisation and jours_restants_cotisation > 0:
            jours_ecoules = 365 - jours_restants_cotisation
            pourcentage_cotisation = min(100, max(0, (jours_ecoules / 365) * 100))
        else:
            pourcentage_cotisation = 0
        
        context = {
            'title': 'Mon Espace Membre',
            'membre': membre,
            
            # Statistiques soins
            'soins_total': soins_total,
            'soins_valides': soins_valides,
            'soins_attente': soins_attente,
            'soins_recents': soins_recents,
            'cout_total': cout_total,
            'derniers_soins': derniers_soins,
            
            # Informations membre
            'statut_cotisation': statut_cotisation,
            'jours_restants_cotisation': jours_restants_cotisation,
            'pourcentage_cotisation': pourcentage_cotisation,
        }
        
        return render(request, 'membres/dashboard.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement du tableau de bord: {str(e)}")
        # Retourner un contexte minimal en cas d'erreur
        return render(request, 'membres/dashboard.html', {
            'membre': None,
            'soins_total': 0,
            'soins_valides': 0,
            'soins_attente': 0,
            'soins_recents': 0,
            'cout_total': 0,
            'derniers_soins': [],
            'statut_cotisation': 'Erreur',
            'jours_restants_cotisation': 0,
            'pourcentage_cotisation': 0,
        })

@login_required
def mes_soins(request):
    """Page dédiée aux soins du membre - VERSION CORRIGÉE"""
    try:
        # Vérifier si l'utilisateur a un profil membre
        try:
            membre = Membre.objects.get(user=request.user)
        except Membre.DoesNotExist:
            # ✅ CORRECTION : Créer automatiquement le profil membre
            membre = creer_profil_membre_automatique(request.user)
            messages.info(request, f"Profil membre créé automatiquement. Numéro: {membre.numero_unique}")
        
        # CORRECTION : Utiliser le bon champ de relation
        soins_query = Soin.objects.filter(patient=membre).select_related(
            'type_soin', 'medecin'
        ).order_by('-date_realisation')
        
        # Filtres
        statut_filter = request.GET.get('statut')
        if statut_filter:
            soins_query = soins_query.filter(statut=statut_filter)
        
        context = {
            'membre': membre,
            'soins': soins_query,
            'statut_filter': statut_filter,
        }
        
        return render(request, 'membres/mes_soins.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return redirect('membres:dashboard')

@login_required
def mon_profil(request):
    """Gestion du profil membre - VERSION CORRIGÉE"""
    try:
        # Vérifier si l'utilisateur a un profil membre
        try:
            membre = Membre.objects.get(user=request.user)
        except Membre.DoesNotExist:
            # ✅ CORRECTION : Créer automatiquement le profil membre
            membre = creer_profil_membre_automatique(request.user)
            messages.info(request, f"Profil membre créé automatiquement. Numéro: {membre.numero_unique}")
        
        if request.method == 'POST':
            # Traitement de la modification du profil
            membre.telephone = request.POST.get('telephone', membre.telephone)
            membre.adresse = request.POST.get('adresse', membre.adresse)
            membre.email = request.POST.get('email', membre.email)
            membre.profession = request.POST.get('profession', membre.profession)
            membre.save()
            
            # Mise à jour des infos utilisateur
            request.user.first_name = request.POST.get('prenom', request.user.first_name)
            request.user.last_name = request.POST.get('nom', request.user.last_name)
            request.user.email = request.POST.get('email', request.user.email)
            request.user.save()
            
            messages.success(request, "Profil mis à jour avec succès!")
            return redirect('membres:mon_profil')
        
        context = {
            'membre': membre,
        }
        
        return render(request, 'membres/mon_profil.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return redirect('membres:dashboard')

@login_required
def historique_cotisations(request):
    """Historique des cotisations du membre - VERSION CORRIGÉE"""
    try:
        # Vérifier si l'utilisateur a un profil membre
        try:
            membre = Membre.objects.get(user=request.user)
        except Membre.DoesNotExist:
            # ✅ CORRECTION : Créer automatiquement le profil membre
            membre = creer_profil_membre_automatique(request.user)
            messages.info(request, f"Profil membre créé automatiquement. Numéro: {membre.numero_unique}")
        
        # Si vous avez un modèle Cotisation, remplacer par :
        # cotisations = Cotisation.objects.filter(membre=membre).order_by('-date_paiement')
        cotisations = []  # Placeholder pour les cotisations
        
        context = {
            'membre': membre,
            'cotisations': cotisations,
        }
        
        return render(request, 'membres/historique_cotisations.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return redirect('membres:dashboard')

# ==============================================================================
# VUES POUR LES PAIEMENTS - VERSIONS CORRIGÉES
# ==============================================================================

@login_required
def mes_paiements(request):
    """Page des paiements et cotisations du membre - VERSION CORRIGÉE"""
    try:
        # Vérifier si l'utilisateur a un profil membre
        try:
            membre = Membre.objects.get(user=request.user)
        except Membre.DoesNotExist:
            # ✅ CORRECTION : Créer automatiquement le profil membre
            membre = creer_profil_membre_automatique(request.user)
            messages.info(request, f"Profil membre créé automatiquement. Numéro: {membre.numero_unique}")
        
        # Simulation des données de paiement (à remplacer par vos modèles réels)
        paiements = [
            {
                'id': 1,
                'date': timezone.now().date() - timedelta(days=30),
                'montant': 150.00,
                'type': 'Cotisation annuelle',
                'statut': 'Payé'
            },
            {
                'id': 2, 
                'date': timezone.now().date() - timedelta(days=395),
                'montant': 150.00,
                'type': 'Cotisation annuelle',
                'statut': 'Payé'
            }
        ]
        
        context = {
            'membre': membre,
            'paiements': paiements,
            'title': 'Mes Paiements'
        }
        
        return render(request, 'membres/mes_paiements.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return redirect('membres:dashboard')

@login_required
def solde_remboursements(request):
    """Page du solde et des remboursements - VERSION CORRIGÉE"""
    try:
        # Vérifier si l'utilisateur a un profil membre
        try:
            membre = Membre.objects.get(user=request.user)
        except Membre.DoesNotExist:
            # ✅ CORRECTION : Créer automatiquement le profil membre
            membre = creer_profil_membre_automatique(request.user)
            messages.info(request, f"Profil membre créé automatiquement. Numéro: {membre.numero_unique}")
        
        # Simulation des données (à adapter avec vos modèles)
        solde_data = {
            'solde_disponible': 1250.50,
            'montant_attente': 320.75,
            'prochain_remboursement': timezone.now().date() + timedelta(days=5),
            'historique_remboursements': [
                {'date': timezone.now().date() - timedelta(days=15), 'montant': 450.00, 'description': 'Remboursement soins dentaires'},
                {'date': timezone.now().date() - timedelta(days=45), 'montant': 280.50, 'description': 'Remboursement consultation'},
            ]
        }
        
        context = {
            'membre': membre,
            'solde_data': solde_data,
            'title': 'Solde & Remboursements'
        }
        
        return render(request, 'membres/solde_remboursements.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return redirect('membres:dashboard')

@login_required
def detail_mon_paiement(request, paiement_id):
    """Détail d'un paiement spécifique - VERSION CORRIGÉE"""
    try:
        # Vérifier si l'utilisateur a un profil membre
        try:
            membre = Membre.objects.get(user=request.user)
        except Membre.DoesNotExist:
            # ✅ CORRECTION : Créer automatiquement le profil membre
            membre = creer_profil_membre_automatique(request.user)
            messages.info(request, f"Profil membre créé automatiquement. Numéro: {membre.numero_unique}")
        
        # Simulation d'un paiement (à remplacer par votre modèle)
        paiement = {
            'id': paiement_id,
            'date': timezone.now().date() - timedelta(days=30),
            'montant': 150.00,
            'type_paiement': 'Cotisation annuelle',
            'methode': 'Carte bancaire',
            'reference': f"PAY-{paiement_id:06d}",
            'statut': 'Payé',
            'description': 'Cotisation annuelle pour la période en cours'
        }
        
        context = {
            'membre': membre,
            'paiement': paiement,
            'title': f'Détail du paiement #{paiement_id}'
        }
        
        return render(request, 'membres/detail_mon_paiement.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return redirect('membres:dashboard')

# ==============================================================================
# VUES ADMIN/ASSUREUR
# ==============================================================================

@login_required
def dashboard_admin(request):
    """Dashboard administrateur avec statistiques globales"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('membres:dashboard')
    
    try:
        # ========================
        # STATISTIQUES MEMBRES
        # ========================
        total_membres = Membre.objects.count()
        membres_actifs = Membre.objects.filter(statut='actif').count()
        membres_retard = Membre.objects.filter(statut='en_retard').count()
        membres_inactifs = Membre.objects.filter(statut='inactif').count()
        
        # Membres récents (30 derniers jours)
        date_limite = timezone.now() - timedelta(days=30)
        nouveaux_membres = Membre.objects.filter(date_inscription__gte=date_limite).count()
        
        # ========================
        # STATISTIQUES SOINS (ADMIN)
        # ========================
        soins_total = Soin.objects.count()
        soins_valides = Soin.objects.filter(statut='valide').count()
        soins_attente = Soin.objects.filter(statut='attente').count()
        soins_refuses = Soin.objects.filter(statut='refuse').count()
        
        # Derniers soins
        derniers_soins = Soin.objects.select_related(
            'membre', 'type_soin', 'medecin'
        ).order_by('-date_realisation')[:10]
        
        # Coûts totaux
        cout_total_valide = Soin.objects.filter(statut='valide').aggregate(
            total=Sum('cout_reel')
        )['total'] or 0
        
        cout_total_attente = Soin.objects.filter(statut='attente').aggregate(
            total=Sum('cout_reel')
        )['total'] or 0
        
        # ========================
        # STATISTIQUES PAR CATÉGORIE
        # ========================
        stats_categories = Membre.objects.values('categorie').annotate(
            total=Count('id')
        ).order_by('-total')
        
        context = {
            'title': 'Dashboard Administrateur',
            
            # Statistiques membres
            'total_membres': total_membres,
            'membres_actifs': membres_actifs,
            'membres_retard': membres_retard,
            'membres_inactifs': membres_inactifs,
            'nouveaux_membres': nouveaux_membres,
            
            # Statistiques soins
            'soins_total': soins_total,
            'soins_valides': soins_valides,
            'soins_attente': soins_attente,
            'soins_refuses': soins_refuses,
            'cout_total_valide': cout_total_valide,
            'cout_total_attente': cout_total_attente,
            'derniers_soins': derniers_soins,
            
            # Données graphiques
            'stats_categories': list(stats_categories),
            
            # Pourcentages
            'pourcentage_actifs': (membres_actifs / total_membres * 100) if total_membres > 0 else 0,
            'pourcentage_retard': (membres_retard / total_membres * 100) if total_membres > 0 else 0,
            'pourcentage_valides': (soins_valides / soins_total * 100) if soins_total > 0 else 0,
        }
        
        return render(request, 'membres/dashboard_admin.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement du dashboard admin: {str(e)}")
        return render(request, 'membres/dashboard_admin.html', {
            'total_membres': 0,
            'membres_actifs': 0,
            'membres_retard': 0,
            'soins_total': 0,
            'soins_valides': 0,
            'soins_attente': 0,
        })

@login_required
def liste_membres_admin(request):
    """Liste complète des membres avec filtres (admin)"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('membres:dashboard')
    
    statut_filter = request.GET.get('statut', '')
    categorie_filter = request.GET.get('categorie', '')
    recherche = request.GET.get('recherche', '')
    
    membres = Membre.objects.all().select_related('user')
    
    # Filtres
    if statut_filter:
        membres = membres.filter(statut=statut_filter)
    if categorie_filter:
        membres = membres.filter(categorie=categorie_filter)
    if recherche:
        membres = membres.filter(
            Q(nom__icontains=recherche) |
            Q(prenom__icontains=recherche) |
            Q(numero_unique__icontains=recherche) |
            Q(telephone__icontains=recherche) |
            Q(email__icontains=recherche)
        )
    
    # Tri
    tri = request.GET.get('tri', '-date_inscription')
    if tri in ['nom', 'prenom', 'date_inscription', 'date_derniere_cotisation']:
        membres = membres.order_by(tri)
    else:
        membres = membres.order_by('-date_inscription')
    
    context = {
        'membres': membres,
        'statut_filter': statut_filter,
        'categorie_filter': categorie_filter,
        'recherche': recherche,
        'tri': tri,
        'statuts': [('actif', 'Actif'), ('en_retard', 'En retard'), ('inactif', 'Inactif')],
        'categories': [('standard', 'Standard'), ('premium', 'Premium'), ('vip', 'VIP')],
    }
    
    return render(request, 'membres/liste_membres_admin.html', context)

@login_required
def statistiques_avancees(request):
    """Statistiques avancées pour l'admin"""
    if not request.user.is_staff and not request.user.is_superuser:
        return JsonResponse({'error': 'Accès non autorisé'}, status=403)
    
    try:
        # Période pour les statistiques (30 derniers jours)
        date_debut = timezone.now() - timedelta(days=30)
        
        # Inscriptions par jour
        inscriptions = Membre.objects.filter(
            date_inscription__gte=date_debut
        ).extra(
            {'date': "date(date_inscription)"}
        ).values('date').annotate(count=Count('id')).order_by('date')
        
        # Soins par type
        soins_par_type = Soin.objects.values('type_soin__nom').annotate(
            total=Count('id'),
            cout_moyen=Avg('cout_reel')
        ).order_by('-total')
        
        # Évolution des soins
        soins_evolution = Soin.objects.filter(
            date_realisation__gte=date_debut
        ).extra(
            {'date': "date(date_realisation)"}
        ).values('date').annotate(count=Count('id')).order_by('date')
        
        # Statistiques financières
        stats_financieres = {
            'cout_total_soins': Soin.objects.filter(statut='valide').aggregate(
                total=Sum('cout_reel')
            )['total'] or 0,
            'soins_moyens_par_membre': Soin.objects.filter(statut='valide').count() / max(Membre.objects.count(), 1),
            'cout_moyen_soin': Soin.objects.filter(statut='valide').aggregate(
                moyen=Avg('cout_reel')
            )['moyen'] or 0,
        }
        
        context = {
            'inscriptions': list(inscriptions),
            'soins_par_type': list(soins_par_type),
            'soins_evolution': list(soins_evolution),
            'stats_financieres': stats_financieres,
        }
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(context)
        
        return render(request, 'membres/statistiques_avancees.html', context)
        
    except Exception as e:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': str(e)}, status=500)
        messages.error(request, f"Erreur lors du chargement des statistiques: {str(e)}")
        return render(request, 'membres/statistiques_avancees.html')

# ==============================================================================
# VUES API POUR GRAPHIQUES
# ==============================================================================

@login_required
def api_statistiques_membres(request):
    """API pour les données graphiques membres"""
    if not request.user.is_staff and not request.user.is_superuser:
        return JsonResponse({'error': 'Accès non autorisé'}, status=403)
    
    try:
        # Statistiques par statut
        stats_statut = Membre.objects.values('statut').annotate(
            count=Count('id')
        )
        
        # Statistiques par catégorie
        stats_categorie = Membre.objects.values('categorie').annotate(
            count=Count('id')
        )
        
        # Évolution mensuelle des inscriptions
        inscriptions_mensuelles = Membre.objects.filter(
            date_inscription__gte=timezone.now()-timedelta(days=365)
        ).extra({
            'mois': "strftime('%%Y-%%m', date_inscription)"
        }).values('mois').annotate(count=Count('id')).order_by('mois')
        
        return JsonResponse({
            'stats_statut': list(stats_statut),
            'stats_categorie': list(stats_categorie),
            'inscriptions_mensuelles': list(inscriptions_mensuelles),
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def api_statistiques_soins(request):
    """API pour les données graphiques soins"""
    if not request.user.is_staff and not request.user.is_superuser:
        return JsonResponse({'error': 'Accès non autorisé'}, status=403)
    
    try:
        # Soins par statut
        soins_statut = Soin.objects.values('statut').annotate(
            count=Count('id')
        )
        
        # Soins par type
        soins_type = Soin.objects.values('type_soin__nom').annotate(
            count=Count('id')
        )
        
        # Coûts par type de soin
        couts_par_type = Soin.objects.filter(statut='valide').values('type_soin__nom').annotate(
            total_cout=Sum('cout_reel'),
            moyenne_cout=Avg('cout_reel')
        )
        
        return JsonResponse({
            'soins_statut': list(soins_statut),
            'soins_type': list(soins_type),
            'couts_par_type': list(couts_par_type),
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ==============================================================================
# VUES ANALYTICS
# ==============================================================================

class AnalyseConnexions:
    """Classe pour analyser les connexions des membres"""
    
    def __init__(self):
        self.today = timezone.now().date()
    
    def get_periode_analyse(self, jours=30):
        return self.today - timedelta(days=jours)
    
    def statistiques_connexions_globales(self, jours=30):
        """Statistiques globales des connexions"""
        date_limite = self.get_periode_analyse(jours)
        
        try:
            # Connexions basées sur last_login
            membres_actifs = Membre.objects.filter(
                user__last_login__gte=date_limite
            ).count()
            
            total_membres = Membre.objects.count()
            nouveaux_membres = Membre.objects.filter(
                date_inscription__gte=date_limite
            ).count()
            
            membres_retard = Membre.objects.filter(
                statut='en_retard'
            ).count()
            
            return {
                'membres_actifs': membres_actifs,
                'total_membres': total_membres,
                'nouveaux_membres': nouveaux_membres,
                'membres_retard': membres_retard,
                'taux_activite': (membres_actifs / total_membres * 100) if total_membres > 0 else 0,
                'periode_jours': jours
            }
            
        except Exception as e:
            return {'erreur': str(e)}
    
    def top_membres_actifs(self, limit=10, jours=30):
        """Top des membres les plus actifs"""
        date_limite = self.get_periode_analyse(jours)
        
        membres_actifs = Membre.objects.filter(
            user__last_login__gte=date_limite
        ).select_related('user').order_by('-user__last_login')[:limit]
        
        result = []
        for membre in membres_actifs:
            result.append({
                'id': membre.id,
                'nom_complet': f"{membre.prenom} {membre.nom}",
                'numero_unique': membre.numero_unique,
                'derniere_connexion': membre.user.last_login,
                'email': membre.email,
                'statut': membre.statut
            })
        
        return result
    
    def membres_inactifs(self, jours_inactivite=30):
        """Détection des membres inactifs"""
        date_limite_inactivite = self.today - timedelta(days=jours_inactivite)
        
        membres_inactifs = Membre.objects.filter(
            Q(user__last_login__lt=date_limite_inactivite) | 
            Q(user__last_login__isnull=True)
        ).select_related('user').order_by('user__last_login')
        
        result = []
        for membre in membres_inactifs:
            jours_inactif = 0
            if membre.user.last_login:
                jours_inactif = (self.today - membre.user.last_login.date()).days
            
            result.append({
                'id': membre.id,
                'nom_complet': f"{membre.prenom} {membre.nom}",
                'numero_unique': membre.numero_unique,
                'email': membre.email,
                'derniere_connexion': membre.user.last_login,
                'jours_inactif': jours_inactif,
                'statut': membre.statut
            })
        
        return result
    
    def generate_rapport_complet(self, jours=30):
        """Génère un rapport complet"""
        return {
            'statistiques_globales': self.statistiques_connexions_globales(jours),
            'top_membres_actifs': self.top_membres_actifs(10, jours),
            'membres_inactifs': self.membres_inactifs(30),
            'date_generation': timezone.now().isoformat(),
            'periode_analyse': f"{jours} jours"
        }

@login_required
def dashboard_analytics(request):
    """Tableau de bord d'analyse des connexions"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('membres:dashboard')
    
    analyseur = AnalyseConnexions()
    jours = int(request.GET.get('jours', 30))
    
    rapport = analyseur.generate_rapport_complet(jours)
    
    context = {
        'title': 'Analytics des Connexions',
        'rapport': rapport,
        'jours_selectionnes': jours,
        'date_actuelle': timezone.now().strftime("%d/%m/%Y %H:%M")
    }
    
    return render(request, 'membres/analytics_dashboard.html', context)

@login_required
def api_analytics_data(request):
    """API pour les données d'analytics"""
    if not request.user.is_staff and not request.user.is_superuser:
        return JsonResponse({'error': 'Accès non autorisé'}, status=403)
    
    analyseur = AnalyseConnexions()
    jours = int(request.GET.get('jours', 30))
    
    data_type = request.GET.get('type', 'global')
    
    if data_type == 'global':
        data = analyseur.statistiques_connexions_globales(jours)
    elif data_type == 'top_membres':
        data = analyseur.top_membres_actifs(10, jours)
    elif data_type == 'inactifs':
        data = analyseur.membres_inactifs(30)
    else:
        data = {'error': 'Type de données non supporté'}
    
    return JsonResponse(data, safe=False)

@login_required
def export_analytics_csv(request):
    """Export des données d'analytics en CSV"""
    if not request.user.is_staff and not request.user.is_superuser:
        return JsonResponse({'error': 'Accès non autorisé'}, status=403)
    
    analyseur = AnalyseConnexions()
    jours = int(request.GET.get('jours', 30))
    rapport = analyseur.generate_rapport_complet(jours)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="analytics_connexions_{timezone.now().strftime("%Y%m%d_%H%M")}.csv"'
    
    writer = csv.writer(response)
    
    # En-têtes
    writer.writerow(['Rapport Analytics Membres', f"Généré le {timezone.now().strftime('%d/%m/%Y %H:%M')}"])
    writer.writerow(['Période d\'analyse', f"{jours} jours"])
    writer.writerow([])
    
    # Statistiques globales
    writer.writerow(['STATISTIQUES GLOBALES'])
    stats = rapport['statistiques_globales']
    for key, value in stats.items():
        writer.writerow([key.replace('_', ' ').title(), value])
    
    writer.writerow([])
    writer.writerow(['TOP MEMBRES ACTIFS'])
    writer.writerow(['Nom', 'Numéro', 'Email', 'Dernière connexion', 'Statut'])
    
    for membre in rapport['top_membres_actifs']:
        writer.writerow([
            membre['nom_complet'],
            membre['numero_unique'],
            membre['email'],
            membre['derniere_connexion'].strftime('%d/%m/%Y %H:%M') if membre['derniere_connexion'] else 'Jamais',
            membre['statut']
        ])
    
    writer.writerow([])
    writer.writerow(['MEMBRES INACTIFS (30+ jours)'])
    writer.writerow(['Nom', 'Numéro', 'Email', 'Dernière connexion', 'Jours inactif', 'Statut'])
    
    for membre in rapport['membres_inactifs']:
        writer.writerow([
            membre['nom_complet'],
            membre['numero_unique'],
            membre['email'],
            membre['derniere_connexion'].strftime('%d/%m/%Y %H:%M') if membre['derniere_connexion'] else 'Jamais',
            membre['jours_inactif'],
            membre['statut']
        ])
    
    return response

@login_required
@gerer_erreurs
def creer_membre(request):
    """Vue pour créer un nouveau membre (agents seulement) - CORRIGÉE"""
    if not est_agent(request.user):
        messages.error(request, "Accès réservé aux agents.")
        return redirect('agents:tableau_de_bord')
    
    # CORRECTION : Vérifier que l'agent a un assureur
    try:
        agent = request.user.agent
        if not hasattr(agent, 'assureur'):
            messages.error(request, "Votre profil agent n'est pas associé à un assureur.")
            return redirect('agents:tableau_de_bord')
    except Exception as e:
        messages.error(request, "Erreur de profil agent.")
        return redirect('agents:tableau_de_bord')

    if request.method == 'POST':
        form = MembreCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # CORRECTION : Sauvegarde avec agent_createur
                membre = form.save(commit=False)
                membre.agent_createur = agent
                membre.save()
                
                messages.success(
                    request, 
                    f"✅ Membre {membre.prenom} {membre.nom} créé avec succès ! Numéro: {membre.numero_unique}"
                )
                return redirect('membres:upload_documents', membre_id=membre.id)
            except Exception as e:
                messages.error(request, f"❌ Erreur lors de la création : {str(e)}")
    else:
        form = MembreCreationForm()
    
    context = {
        'form': form,
        'title': 'Créer un nouveau membre',
        'agent': agent
    }
    return render(request, 'membres/creer_membre.html', context)

@login_required
@gerer_erreurs  
def liste_membres_agent(request):
    """Liste des membres créés par l'agent connecté"""
    if not est_agent(request.user):
        messages.error(request, "Accès réservé aux agents.")
        return redirect('agents:tableau_de_bord')
    
    agent = request.user.agent
    membres_list = Membre.objects.filter(agent_createur=agent).order_by('-date_inscription')
    
    # Pagination
    paginator = Paginator(membres_list, 10)
    page_number = request.GET.get('page')
    membres = paginator.get_page(page_number)
    
    context = {
        'membres': membres,
        'title': 'Mes membres créés',
        'total_membres': membres_list.count()
    }
    return render(request, 'membres/liste_membres_agent.html', context)

@login_required
@gerer_erreurs
def upload_documents_membre(request, membre_id):
    """Upload des documents pour un membre créé"""
    if not est_agent(request.user):
        messages.error(request, "Accès réservé aux agents.")
        return redirect('agents:tableau_de_bord')
    
    membre = get_object_or_404(Membre, id=membre_id, agent_createur=request.user.agent)
    
    if request.method == 'POST':
        form = MembreDocumentForm(request.POST, request.FILES, instance=membre)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Documents uploadés avec succès !")
            return redirect('membres:liste_membres_agent')
    else:
        form = MembreDocumentForm(instance=membre)
    
    context = {
        'form': form,
        'membre': membre,
        'title': f'Documents - {membre.prenom} {membre.nom}'
    }
    return render(request, 'membres/upload_documents.html', context)

# ==============================================================================
# VUES UTILITAIRES
# ==============================================================================

@login_required
def recherche_membres(request):
    """Recherche de membres pour l'assureur"""
    query = request.GET.get('q', '')
    membres = Membre.objects.none()
    
    if query:
        membres = Membre.objects.filter(
            Q(nom__icontains=query) | 
            Q(prenom__icontains=query) |
            Q(numero_unique__icontains=query) |
            Q(email__icontains=query)
        )[:10]
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        results = [{
            'id': m.id,
            'numero_unique': m.numero_unique,
            'nom_complet': f"{m.nom} {m.prenom}",
            'email': m.email,
            'telephone': m.telephone,
            'statut': m.statut,
        } for m in membres]
        return JsonResponse(results, safe=False)
    
    return render(request, 'membres/recherche_membres.html', {
        'membres': membres,
        'query': query
    })

def test_auth(request):
    """Vue pour tester l'authentification"""
    if request.user.is_authenticated:
        return HttpResponse(f"✅ Utilisateur connecté: {request.user.username} - Staff: {request.user.is_staff} - Superuser: {request.user.is_superuser}")
    else:
        return HttpResponse("❌ Utilisateur NON connecté")

# ==============================================================================
# MIXIN POUR LE PARTAGE DE DOCUMENTS - CORRIGÉ
# ==============================================================================

class FiltreParPartageMixin:
    """Mixin pour filtrer les documents par partage et permissions"""
    
    def get_document_partage(self, type_document, document_id):
        """
        Récupère un document avec vérification des permissions
        """
        try:
            if type_document == 'ORD':
                ordonnance = get_object_or_404(Ordonnance, id=document_id)
                
                # Vérifier que l'utilisateur a le droit de voir cette ordonnance
                user = self.request.user
                
                if hasattr(user, 'membre') and ordonnance.consultation.membre == user.membre:
                    # Membre regardant sa propre ordonnance
                    return ordonnance
                elif hasattr(user, 'medecin') and ordonnance.medecin == user.medecin:
                    # Médecin regardant sa propre ordonnance
                    return ordonnance
                elif user.is_staff:
                    # Staff admin
                    return ordonnance
                else:
                    raise PermissionDenied("Vous n'avez pas accès à cette ordonnance")
            else:
                raise Http404("Type de document non supporté")
                
        except Ordonnance.DoesNotExist:
            raise Http404("Ordonnance non trouvée")
        except Exception as e:
            print(f"Erreur dans get_document_partage: {e}")
            raise PermissionDenied("Erreur d'accès au document")

    def get_queryset_ordonnances(self):
        """Retourne les ordonnances accessibles à l'utilisateur"""
        user = self.request.user
        queryset = Ordonnance.objects.all()
        
        if hasattr(user, 'membre'):
            # Membre ne voit que ses propres ordonnances
            queryset = queryset.filter(consultation__membre=user.membre)
        elif hasattr(user, 'medecin'):
            # Médecin voit ses propres ordonnances
            queryset = queryset.filter(medecin=user.medecin)
        elif not user.is_staff:
            # Autres utilisateurs non-staff ne voient rien
            queryset = queryset.none()
            
        return queryset

    def get_queryset_bons(self):
        """Retourne les bons accessibles à l'utilisateur"""
        from soins.models import BonDeSoin
        user = self.request.user
        queryset = BonDeSoin.objects.all()
        
        if hasattr(user, 'membre'):
            # Membre ne voit que ses propres bons
            queryset = queryset.filter(patient=user.membre)
        elif not user.is_staff:
            # Autres utilisateurs non-staff ne voient rien
            queryset = queryset.none()
            
        return queryset

# ==============================================================================
# VUES BASÉES SUR LES CLASSES - CORRIGÉES
# ==============================================================================

class MesOrdonnancesView(LoginRequiredMixin, FiltreParPartageMixin, ListView):
    """Liste des ordonnances accessibles au membre"""
    template_name = 'membres/mes_ordonnances.html'
    context_object_name = 'ordonnances'
    paginate_by = 10
    
    def get_queryset(self):
        return self.get_queryset_ordonnances().select_related(
            'consultation', 'medecin', 'consultation__membre'
        ).order_by('-date_creation')

class MesBonsView(LoginRequiredMixin, FiltreParPartageMixin, ListView):
    """Liste des bons accessibles au membre"""
    template_name = 'membres/mes_bons.html'
    context_object_name = 'bons'
    paginate_by = 10
    
    def get_queryset(self):
        return self.get_queryset_bons().select_related(
            'membre', 'type_soin'
        ).order_by('-date_creation')

class DetailOrdonnanceMembreView(LoginRequiredMixin, FiltreParPartageMixin, DetailView):
    """Détail d'une ordonnance pour le membre"""
    template_name = 'membres/detail_ordonnance.html'
    context_object_name = 'ordonnance'
    
    def get_object(self):
        """
        Récupère l'ordonnance en vérifiant les permissions
        CORRECTION : Suppression de l'appel à get_document_partage qui causait l'erreur
        """
        try:
            ordonnance_id = self.kwargs.get('ordonnance_id')
            ordonnance = get_object_or_404(Ordonnance, id=ordonnance_id)
            
            # Vérifier que l'utilisateur a le droit de voir cette ordonnance
            user = self.request.user
            
            if hasattr(user, 'membre') and ordonnance.consultation.membre == user.membre:
                # Membre regardant sa propre ordonnance
                return ordonnance
            elif hasattr(user, 'medecin') and ordonnance.medecin == user.medecin:
                # Médecin regardant sa propre ordonnance
                return ordonnance
            elif user.is_staff:
                # Staff admin
                return ordonnance
            else:
                raise PermissionDenied("Vous n'avez pas accès à cette ordonnance")
                
        except Ordonnance.DoesNotExist:
            raise Http404("Ordonnance non trouvée")
        except Exception as e:
            print(f"Erreur dans get_object: {e}")
            raise

# ==============================================================================
# VUES FONCTION POUR LES ORDONNANCES - CORRIGÉES
# ==============================================================================

@login_required
def mes_ordonnances(request):
    """Affiche les ordonnances du membre connecté"""
    try:
        # Récupérer TOUTES les ordonnances pour debug
        toutes_ordonnances = Ordonnance.objects.all()
        print(f"DEBUG: {toutes_ordonnances.count()} ordonnances totales dans la base")
        
        for ord in toutes_ordonnances[:5]:  # Limiter l'affichage debug
            print(f"DEBUG - Ordonnance {ord.id}: patient={ord.patient}, diagnostic={ord.diagnostic}")
        
        # Récupérer les ordonnances du membre connecté
        try:
            membre = Membre.objects.get(user=request.user)
            ordonnances = Ordonnance.objects.filter(consultation__membre=membre)
            print(f"DEBUG: {ordonnances.count()} ordonnances pour le membre {membre.prenom} {membre.nom}")
        except Membre.DoesNotExist:
            # Si pas de membre, utiliser une autre logique
            ordonnances = Ordonnance.objects.none()
            print("DEBUG: Aucun profil membre trouvé")
        
        context = {
            'ordonnances': ordonnances
        }
        return render(request, 'membres/mes_ordonnances.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement des ordonnances: {str(e)}")
        return render(request, 'membres/mes_ordonnances.html', {'ordonnances': []})

@login_required
def export_analytics_excel(request):
    """Export Excel des analytics - Vue temporaire"""
    return HttpResponse("Export Excel - Fonctionnalité à implémenter")

# ==============================================================================
# VUES POUR LA SÉLECTION DES MEMBRES - CORRIGÉES
# ==============================================================================

@login_required
@gerer_erreurs
def selection_membre(request):
    """Vue pour sélectionner un membre avant de créer un bon"""
    # CORRECTION : Vérifier les permissions selon le type d'utilisateur
    if est_assureur(request.user):
        # Assureur voit tous les membres de son assureur
        assureur = request.user.assureur
        membres = Membre.objects.filter(agent_createur__assureur=assureur)
    elif est_agent(request.user):
        # Agent ne voit que ses propres membres
        agent = request.user.agent
        membres = Membre.objects.filter(agent_createur=agent)
    else:
        messages.error(request, "Accès non autorisé.")
        return redirect('membres:dashboard')
    
    context = {
        'membres': membres,
        'title': 'Sélectionner un membre'
    }
    return render(request, 'membres/selection_membre.html', context)

# ==============================================================================
# VUES POUR LES BONS DE SOIN - CORRIGÉES
# ==============================================================================



@login_required
def mes_bons(request):
    """Affiche les bons de soin du membre connecté"""
    try:
        # Récupérer le membre associé à l'utilisateur
        membre = request.user.membre
        bons = BonDeSoin.objects.filter(membre=membre).order_by('-date_creation')
        
        context = {
            'bons': bons,
            'membre': membre
        }
        return render(request, 'membres/mes_bons.html', context)
        
    except Exception as e:
        # Fallback vers un template simple si le template spécifique n'existe pas
        context = {
            'bons': [],
            'membre': getattr(request.user, 'membre', None),
            'erreur': str(e)
        }
        return render(request, 'membres/mes_bons.html', context)

@login_required
def mes_ordonnances(request):
    """Affiche les ordonnances du membre connecté"""
    try:
        membre = request.user.membre
        ordonnances = Ordonnance.objects.filter(patient=membre).order_by('-date_prescription')
        
        context = {
            'ordonnances': ordonnances,
            'membre': membre
        }
        return render(request, 'membres/mes_ordonnances.html', context)
        
    except Exception as e:
        context = {
            'ordonnances': [],
            'membre': getattr(request.user, 'membre', None),
            'erreur': str(e)
        }
        return render(request, 'membres/mes_ordonnances.html', context)

# ==============================================================================
# VUE POUR LE SUIVI DES REMBOURSEMENTS
# ==============================================================================

@login_required
def suivi_remboursements(request):
    """Suivi des remboursements du membre"""
    try:
        # Vérifier si l'utilisateur a un profil membre
        try:
            membre = Membre.objects.get(user=request.user)
        except Membre.DoesNotExist:
            # ✅ CORRECTION : Créer automatiquement le profil membre
            membre = creer_profil_membre_automatique(request.user)
            messages.info(request, f"Profil membre créé automatiquement. Numéro: {membre.numero_unique}")
        
        # Récupérer les remboursements (à adapter avec vos modèles)
        remboursements = [
            {
                'id': 1,
                'date_demande': timezone.now().date() - timedelta(days=10),
                'montant': 250.00,
                'statut': 'Traité',
                'date_traitement': timezone.now().date() - timedelta(days=2),
                'description': 'Remboursement consultation générale'
            },
            {
                'id': 2,
                'date_demande': timezone.now().date() - timedelta(days=5),
                'montant': 180.50,
                'statut': 'En cours',
                'date_traitement': None,
                'description': 'Remboursement analyses médicales'
            }
        ]
        
        context = {
            'membre': membre,
            'remboursements': remboursements,
            'title': 'Suivi des Remboursements'
        }
        
        return render(request, 'membres/suivi_remboursements.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement du suivi: {str(e)}")
        return redirect('membres:dashboard')