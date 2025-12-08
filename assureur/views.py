"""
VUES ASSUREUR - Version avec diagnostic détaillé
"""
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import json
import csv
import traceback
from decimal import Decimal
from .forms import PaiementForm
from django.template.loader import render_to_string
import os
from django.db.models import Sum, Count, Avg, Q, F, ExpressionWrapper, DurationField
import logging

logger = logging.getLogger(__name__)

# Décorateur personnalisé (assurez-vous qu'il existe)
from .decorators import assureur_required
from .utils import get_assureur_from_request

# IMPORT CORRIGÉ : UN SEUL IMPORT Membre (agents.models)
from agents.models import Membre

# Import des modèles
from assureur.models import (
    Assureur, Bon, Soin, Paiement, Cotisation, 
    StatistiquesAssurance, ConfigurationAssurance, RapportAssureur
)
from medecin.models import Ordonnance
from django.contrib.auth.models import User, Group

# ==========================================================================
# DÉCORATEURS ET FONCTIONS UTILITAIRES - CORRIGÉES AVEC DIAGNOSTIC
# ==========================================================================

def is_assureur(user):
    """Vérifie si l'utilisateur est un assureur - Fonction pour user_passes_test"""
    print(f"🔍 DIAGNOSTIC is_assureur pour {user.username}")
    print(f"   - est authentifié: {user.is_authenticated}")
    print(f"   - est superuser: {user.is_superuser}")
    print(f"   - groupes: {[g.name for g in user.groups.all()]}")
    print(f"   - a assureur_profile: {hasattr(user, 'assureur_profile')}")
    
    return user.is_authenticated and (
        user.groups.filter(name__iexact='assureur').exists() or
        user.is_superuser or
        hasattr(user, 'assureur_profile')
    )

def get_assureur_from_request(request):
    """Récupère l'objet assureur à partir de la requête avec diagnostic détaillé"""
    print(f"🔍 DIAGNOSTIC get_assureur_from_request pour {request.user.username}")
    
    if not request.user.is_authenticated:
        print("   - utilisateur non authentifié")
        return None
    
    # 1. Vérifier si l'utilisateur a déjà un profil assureur
    if hasattr(request.user, 'assureur_profile'):
        print(f"   - a assureur_profile: OUI")
        try:
            assureur = request.user.assureur_profile
            print(f"   - profil trouvé: {assureur}")
            return assureur
        except Exception as e:
            print(f"   - erreur accès assureur_profile: {e}")
            return None
    else:
        print(f"   - a assureur_profile: NON")
    
    # 2. Vérifier si l'utilisateur est dans le groupe ASSUREUR
    if request.user.groups.filter(name__iexact='assureur').exists():
        print(f"   - est dans le groupe ASSUREUR: OUI")
        
        # 3. Essayer de trouver un profil Assureur par d'autres moyens
        try:
            # Vérifier si un profil Assureur existe déjà pour cet utilisateur
            assureur = Assureur.objects.filter(user=request.user).first()
            if assureur:
                print(f"   - profil Assureur trouvé dans la base: {assureur}")
                return assureur
            else:
                print(f"   - pas de profil Assureur trouvé dans la base")
                
                # Créer un profil Assureur
                print(f"   - tentative de création du profil Assureur...")
                try:
                    assureur = Assureur.objects.create(
                        user=request.user,
                        nom=request.user.get_full_name() or request.user.username,
                        email=request.user.email,
                        telephone='',
                        adresse='',
                        est_actif=True
                    )
                    print(f"   ✅ profil Assureur créé avec succès: {assureur}")
                    return assureur
                except Exception as e:
                    print(f"   ❌ erreur création profil Assureur: {e}")
                    print(f"   - traceback: {traceback.format_exc()}")
                    
                    # Si la création échoue, essayer de voir pourquoi
                    try:
                        # Vérifier les champs du modèle Assureur
                        print("   - vérification des champs obligatoires du modèle Assureur...")
                        from django.db import connection
                        with connection.cursor() as cursor:
                            cursor.execute("PRAGMA table_info(assureur_assureur)")
                            columns = cursor.fetchall()
                            print(f"   - colonnes de la table Assureur: {columns}")
                    except:
                        pass
                    
                    return None
        except Exception as e:
            print(f"   ❌ erreur générale recherche/creation profil: {e}")
            print(f"   - traceback: {traceback.format_exc()}")
            return None
    else:
        print(f"   - est dans le groupe ASSUREUR: NON")
    
    print(f"   - aucun profil Assureur trouvé ou créé")
    return None

# Décorateur personnalisé pour les vues assureur
def assureur_required(view_func):
    """
    Décorateur qui vérifie que l'utilisateur est un assureur
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        print(f"🔍 DIAGNOSTIC assureur_required pour {request.user.username}")
        
        # Vérifier si l'utilisateur est authentifié
        if not request.user.is_authenticated:
            print("   - utilisateur non authentifié, redirection vers login")
            return redirect('login')
        
        # Vérifier les conditions d'assureur
        is_assureur_user = (
            request.user.groups.filter(name__iexact='assureur').exists() or 
            request.user.is_superuser or
            hasattr(request.user, 'assureur_profile')
        )
        
        print(f"   - is_assureur_user: {is_assureur_user}")
        
        if not is_assureur_user:
            messages.error(request, "Accès réservé aux assureurs.")
            print("   - accès refusé, affichage page accès interdit")
            return render(request, 'assureur/acces_interdit.html', {
                'assureur': None
            })
        
        print(f"   - accès autorisé, appel de la vue")
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

# ==========================================================================
# VUE DASHBOARD - CORRIGÉE AVEC ASSUREUR DANS LE CONTEXTE
# ==========================================================================

@login_required
@assureur_required
def dashboard_assureur(request):
    """Dashboard principal de l'assureur - VERSION AVEC DIAGNOSTIC"""
    print(f"🎯 DIAGNOSTIC dashboard_assureur - Début")
    print(f"   - utilisateur: {request.user.username}")
    print(f"   - groupes: {[g.name for g in request.user.groups.all()]}")
    
    try:
        # 1. RÉCUPÉRATION DE L'ASSUREUR AVEC DIAGNOSTIC
        print(f"   - appel de get_assureur_from_request...")
        assureur = get_assureur_from_request(request)
        print(f"   - assureur récupéré: {assureur}")
        print(f"   - type assureur: {type(assureur)}")
        
        if not assureur:
            print(f"   ❌ aucun assureur trouvé, affichage page accès interdit")
            messages.error(request, "Vous n'avez pas de profil assureur associé.")
            return render(request, 'assureur/acces_interdit.html', {'assureur': None})
        
        # Vérifier si assureur est un dictionnaire (simulé) ou un objet
        if isinstance(assureur, dict):
            print(f"   ⚠️ assureur est un dictionnaire simulé")
        else:
            print(f"   ✅ assureur est un objet Assureur: id={assureur.id}, nom={assureur.nom}")
        
        # 2. Statistiques principales (avec gestion d'erreurs)
        print(f"   - calcul des statistiques...")
        try:
            total_membres = Membre.objects.filter(statut='actif').count()
            total_bons = Bon.objects.count()
            print(f"   - membres actifs: {total_membres}, total bons: {total_bons}")
        except Exception as e:
            print(f"   ⚠️ erreur calcul statistiques: {e}")
            total_membres = 0
            total_bons = 0
        
        # Continuer avec d'autres statistiques...
        
        # 3. Préparer le contexte
        context = {
            'assureur': assureur,
            'total_membres': total_membres,
            'total_bons': total_bons,
            'stats': {
                'membres_actifs': total_membres,
                'total_bons': total_bons,
                # Ajoutez d'autres stats ici...
            }
        }
        
        print(f"   ✅ dashboard prêt, rendu du template")
        return render(request, 'assureur/dashboard.html', context)
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE dans dashboard_assureur: {e}")
        print(f"   - traceback: {traceback.format_exc()}")
        messages.error(request, f"Erreur lors du chargement du dashboard: {str(e)}")
        assureur = get_assureur_from_request(request)
        return render(request, 'assureur/dashboard.html', {'assureur': assureur})

# ==========================================================================
# VUE D'ACCÈS INTERDIT - CORRIGÉE
# ==========================================================================

@login_required
def acces_interdit(request):
    """Vue pour les utilisateurs qui n'ont pas accès à l'assureur"""
    context = {
        'assureur': get_assureur_from_request(request),
    }
    return render(request, 'assureur/acces_interdit.html', context)

# ==========================================================================
# VUE DE DIAGNOSTIC AVANCÉ
# ==========================================================================

@login_required
def diagnostic_assureur(request):
    """Vue de diagnostic pour comprendre le problème"""
    print(f"🔬 DIAGNOSTIC COMPLET pour {request.user.username}")
    
    diagnostics = []
    
    # 1. Informations utilisateur
    diagnostics.append(f"Utilisateur: {request.user.username}")
    diagnostics.append(f"Email: {request.user.email}")
    diagnostics.append(f"Superutilisateur: {request.user.is_superuser}")
    
    # 2. Groupes
    groupes = [g.name for g in request.user.groups.all()]
    diagnostics.append(f"Groupes: {', '.join(groupes) if groupes else 'Aucun'}")
    
    # 3. Vérification profil Assureur
    if hasattr(request.user, 'assureur_profile'):
        try:
            assureur = request.user.assureur_profile
            diagnostics.append(f"Profil Assureur trouvé via assureur_profile: {assureur}")
            diagnostics.append(f"  - ID: {assureur.id}")
            diagnostics.append(f"  - Nom: {assureur.nom}")
            diagnostics.append(f"  - Email: {assureur.email}")
        except Exception as e:
            diagnostics.append(f"Erreur accès assureur_profile: {e}")
    else:
        diagnostics.append("Pas d'attribut 'assureur_profile' sur l'utilisateur")
    
    # 4. Recherche dans la base de données
    try:
        from assureur.models import Assureur
        assureur_db = Assureur.objects.filter(user=request.user).first()
        if assureur_db:
            diagnostics.append(f"Profil Assureur trouvé dans DB: {assureur_db}")
            diagnostics.append(f"  - ID: {assureur_db.id}")
            diagnostics.append(f"  - Nom: {assureur_db.nom}")
            diagnostics.append(f"  - User ID: {assureur_db.user_id}")
        else:
            diagnostics.append("Aucun profil Assureur trouvé dans la base de données")
            
            # Vérifier si on peut en créer un
            if request.user.groups.filter(name__iexact='assureur').exists():
                diagnostics.append("L'utilisateur est dans le groupe ASSUREUR, tentative de création...")
                try:
                    nouvel_assureur = Assureur.objects.create(
                        user=request.user,
                        nom=request.user.get_full_name() or request.user.username,
                        email=request.user.email,
                        telephone='',
                        adresse='',
                        est_actif=True
                    )
                    diagnostics.append(f"✅ Profil Assureur créé avec succès: {nouvel_assureur}")
                except Exception as e:
                    diagnostics.append(f"❌ Erreur création profil: {e}")
                    diagnostics.append(f"   Détails: {traceback.format_exc()}")
    except Exception as e:
        diagnostics.append(f"Erreur recherche Assureur: {e}")
    
    # 5. Vérification des permissions
    diagnostics.append(f"is_assureur(): {is_assureur(request.user)}")
    
    # Afficher les diagnostics
    html = "<h1>Diagnostic Assureur</h1>"
    for diagnostic in diagnostics:
        html += f"<p>{diagnostic}</p>"
    
    html += f"""
    <hr>
    <h2>Actions</h2>
    <ul>
        <li><a href="/assureur/">Retour au dashboard</a></li>
        <li><a href="/admin/auth/user/{request.user.id}/change/">Modifier l'utilisateur dans l'admin</a></li>
        <li><a href="/admin/assureur/assureur/">Voir tous les assureurs</a></li>
    </ul>
    """
    
    return HttpResponse(html)

# ==========================================================================
# VUE FALLBACK SIMPLE POUR TEST
# ==========================================================================

@login_required
def dashboard_simple(request):
    """Dashboard simple pour tester l'accès"""
    print(f"🎯 dashboard_simple pour {request.user.username}")
    
    # Vérifier si l'utilisateur est dans le groupe ASSUREUR
    if not request.user.groups.filter(name__iexact='assureur').exists():
        return HttpResponse("Vous n'êtes pas dans le groupe ASSUREUR")
    
    # Créer un profil simulé si nécessaire
    assureur_info = {
        'nom': request.user.get_full_name() or request.user.username,
        'email': request.user.email,
        'est_simule': True
    }
    
    context = {
        'assureur': assureur_info,
        'message': "Dashboard simple - Accès autorisé"
    }
    
    return render(request, 'assureur/dashboard_simple.html', context)

# ==========================================================================
# COMMANDE DE CONSOLE POUR CORRIGER LE PROBLÈME
# ==========================================================================

"""
Pour exécuter cette commande depuis le shell Django :

python manage.py shell
>>> from assureur.views import corriger_probleme_assureur
>>> corriger_probleme_assureur()
"""

def corriger_probleme_assureur():
    """Corrige les problèmes d'assureur - à exécuter depuis le shell Django"""
    print("🔧 Correction des problèmes d'assureur...")
    
    # 1. Trouver tous les utilisateurs du groupe ASSUREUR
    try:
        groupe_assureur = Group.objects.filter(name__iexact='assureur').first()
        if not groupe_assureur:
            print("❌ Le groupe ASSUREUR n'existe pas")
            return
        
        utilisateurs_assureurs = groupe_assureur.user_set.all()
        print(f"✅ Trouvé {utilisateurs_assureurs.count()} utilisateurs dans le groupe ASSUREUR")
        
        # 2. Pour chaque utilisateur, vérifier/créer un profil Assureur
        for user in utilisateurs_assureurs:
            print(f"\n--- Traitement de {user.username} ---")
            
            # Vérifier si un profil Assureur existe déjà
            assureur_existant = Assureur.objects.filter(user=user).first()
            
            if assureur_existant:
                print(f"✅ Profil Assureur existe déjà: {assureur_existant}")
            else:
                print(f"⚠️  Pas de profil Assureur, création...")
                try:
                    nouvel_assureur = Assureur.objects.create(
                        user=user,
                        nom=user.get_full_name() or user.username,
                        email=user.email,
                        telephone='',
                        adresse='',
                        est_actif=True
                    )
                    print(f"✅ Profil créé: {nouvel_assureur}")
                except Exception as e:
                    print(f"❌ Erreur création: {e}")
        
        print("\n✅ Correction terminée")
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()

# ==========================================================================
# VUES GÉNÉRIQUES AVEC CONTEXTE ASSUREUR
# ==========================================================================

def assureur_view(template_name):
    """Décorateur pour les vues assureur qui ajoute automatiquement l'assureur au contexte"""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        @assureur_required
        def wrapper(request, *args, **kwargs):
            # Exécuter la vue originale
            result = view_func(request, *args, **kwargs)
            
            # Si c'est un HttpResponse avec un template, ajouter assureur au contexte
            if isinstance(result, dict):
                context = result
                # Ajouter assureur si pas déjà présent
                if 'assureur' not in context:
                    assureur = get_assureur_from_request(request)
                    context['assureur'] = assureur
                return render(request, template_name, context)
            return result
        return wrapper
    return decorator

# ==========================================================================
# VUES POUR LES MEMBRES
# ==========================================================================

@login_required
@assureur_required
def liste_membres(request):
    """Liste tous les membres avec filtres et pagination - VERSION AVEC DEBUG DÉTAILLÉ"""
    try:
        print(f"=== DEBUG DÉTAILLÉ liste_membres ===")
        print(f"Utilisateur: {request.user.username}")
        print(f"GET params: {dict(request.GET)}")
        
        # Utiliser le bon modèle Membre (agents.models) et ses champs
        membres = Membre.objects.select_related('user').order_by('-date_inscription')
        print(f"1. Total membres en base: {membres.count()}")
        
        # Filtres
        statut = request.GET.get('statut', '')
        search = request.GET.get('q', '')
        
        print(f"2. Filtre statut: '{statut}'")
        print(f"3. Filtre recherche: '{search}'")
        
        if statut:
            membres = membres.filter(statut=statut)
            print(f"4. Après filtre statut: {membres.count()}")
        
        if search:
            membres = membres.filter(
                Q(nom__icontains=search) |
                Q(prenom__icontains=search) |
                Q(numero_unique__icontains=search) |
                Q(email__icontains=search) |
                Q(telephone__icontains=search)
            )
            print(f"5. Après filtre recherche '{search}': {membres.count()}")
            
            # Afficher les membres trouvés
            for m in membres[:5]:
                print(f"   → {m.id}: {m.prenom} {m.nom} - {m.numero_unique}")
        
        # Pagination
        paginator = Paginator(membres, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        print(f"6. Pagination: page {page_obj.number}/{page_obj.paginator.num_pages}")
        print(f"7. Éléments dans page_obj: {len(page_obj)}")
        
        # Statistiques pour les filtres
        stats_membres = {
            'total': Membre.objects.count(),
            'actifs': Membre.objects.filter(statut='actif').count(),
            'en_retard': Membre.objects.filter(statut='en_retard').count(),
        }
        
        print(f"8. Stats: {stats_membres}")
        
        # Choix pour les filtres
        statut_choices = [
            ('', 'Tous les statuts'),
            ('actif', 'Actif'),
            ('en_retard', 'En retard'),
        ]
        
        context = {
            'assureur': get_assureur_from_request(request),
            'page_obj': page_obj,
            'stats_membres': stats_membres,
            'statut_choices': statut_choices,
            'filters': {
                'statut': statut,
                'search': search,
            }
        }
        
        print(f"9. Contexte préparé, page_obj: {len(page_obj) if page_obj else 0} éléments")
        print("=== FIN DEBUG ===")
        
        return render(request, 'assureur/liste_membres.html', context)
        
    except Exception as e:
        print(f"=== ERREUR CRITIQUE liste_membres ===")
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()
        print("=========================")
        
        messages.error(request, f"Erreur lors du chargement des membres: {str(e)}")
        context = {'assureur': get_assureur_from_request(request)}
        return render(request, 'assureur/liste_membres.html', context)

@login_required
@assureur_required
def detail_membre(request, membre_id):
    """Détails complets d'un membre - VERSION COMPLÈTEMENT CORRIGÉE"""
    try:
        # CORRECTION: Importer correctement le modèle Membre
        from agents.models import Membre
        membre = get_object_or_404(Membre, id=membre_id)
        
        print(f"DEBUG: Membre trouvé: {membre.id} - {membre.nom} {membre.prenom}")
        print(f"DEBUG: Type membre: {type(membre)}")
        print(f"DEBUG: Classe membre: {membre.__class__.__name__}")
        
        # CORRECTION: Récupérer les bons AVEC LE BON FILTRE
        try:
            # Vérifier si le modèle Bon existe dans assureur.models
            from assureur.models import Bon
            bons = Bon.objects.filter(membre=membre).order_by('-date_creation')
            print(f"DEBUG: Bons trouvés: {bons.count()}")
        except Exception as e:
            print(f"DEBUG: Erreur récupération bons: {e}")
            bons = []
        
        # CORRECTION: Récupérer les soins
        try:
            from assureur.models import Soin
            soins = Soin.objects.filter(membre=membre).order_by('-date_soumission')
        except Exception as e:
            print(f"DEBUG: Erreur récupération soins: {e}")
            soins = []
        
        # CORRECTION: Récupérer les paiements
        try:
            from assureur.models import Paiement
            paiements = Paiement.objects.filter(membre=membre).order_by('-date_paiement')
        except Exception:
            paiements = []
        
        # CORRECTION: Récupérer les cotisations
        try:
            from assureur.models import Cotisation
            cotisations = Cotisation.objects.filter(membre=membre).order_by('-periode')
        except Exception:
            cotisations = []
        
        # Statistiques du membre
        stats_membre = {
            'total_bons': len(bons),
            'bons_valides': len([b for b in bons if hasattr(b, 'statut') and b.statut == 'valide']),
            'bons_utilises': len([b for b in bons if hasattr(b, 'statut') and b.statut == 'utilise']),
            'total_soins': len(soins),
            'soins_valides': len([s for s in soins if hasattr(s, 'statut') and s.statut == 'valide']),
            'total_paiements': len(paiements),
            'montant_total_paye': sum([p.montant for p in paiements if hasattr(p, 'montant')]),
            'cotisations_en_retard': len([c for c in cotisations if hasattr(c, 'statut') and c.statut in ['en_retard', 'due']]),
            'montant_dette': sum([c.montant for c in cotisations if hasattr(c, 'montant') and hasattr(c, 'statut') and c.statut in ['due', 'en_retard']]),
        }
        
        context = {
            'assureur': get_assureur_from_request(request),
            'membre': membre,
            'bons': bons[:10],
            'soins': soins[:10],
            'paiements': paiements[:10],
            'cotisations': cotisations,
            'stats_membre': stats_membre,
        }
        
        return render(request, 'assureur/detail_membre.html', context)
        
    except Exception as e:
        print(f"ERREUR COMPLÈTE detail_membre {membre_id}: {e}")
        import traceback
        traceback.print_exc()
        messages.error(request, f"Erreur lors du chargement du membre: {str(e)}")
        return redirect('liste_membres')

@login_required
@assureur_required
def creer_membre(request):
    """Création d'un nouveau membre - VERSION CORRIGÉE POUR agents.models.Membre"""
    if request.method == 'POST':
        try:
            data = request.POST
            
            # Vérifier si l'agent_createur est fourni
            agent_createur_id = data.get('agent_createur')
            agent_createur = None
            if agent_createur_id:
                try:
                    from agents.models import Agent
                    agent_createur = Agent.objects.get(id=agent_createur_id)
                except:
                    pass
            
            # Création du membre avec les BONS CHAMPS (agents.models.Membre)
            membre = Membre.objects.create(
                nom=data.get('nom', ''),
                prenom=data.get('prenom', ''),
                date_naissance=datetime.strptime(data.get('date_naissance'), '%Y-%m-%d').date() if data.get('date_naissance') else timezone.now().date(),
                email=data.get('email', ''),
                telephone=data.get('telephone', ''),
                adresse=data.get('adresse', ''),
                profession=data.get('profession', ''),
                agent_createur=agent_createur,
                numero_unique=data.get('numero_unique', f"MEM{timezone.now().strftime('%Y%m%d%H%M%S')}"),
                type_piece_identite=data.get('type_piece_identite', 'cni'),
                numero_piece_identite=data.get('numero_piece_identite', ''),
                date_expiration_piece=datetime.strptime(data.get('date_expiration_piece'), '%Y-%m-%d').date() if data.get('date_expiration_piece') else None,
                statut='actif',
                date_inscription=timezone.now(),
                niveau_risque=data.get('niveau_risque', 'faible'),
                cmu_option=data.get('cmu_option') == 'on',
            )
            
            messages.success(request, f"Membre {membre.prenom} {membre.nom} créé avec succès")
            return redirect('assureur:detail_membre', membre_id=membre.id)
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la création du membre: {str(e)}")
    
    # Récupérer les agents pour le formulaire
    try:
        from agents.models import Agent
        agents = Agent.objects.all()
    except:
        agents = []
    
    context = {
        'assureur': get_assureur_from_request(request),
        'agents': agents,
    }
    return render(request, 'assureur/creer_membre.html', context)

# ==========================================================================
# VUES POUR LES BONS
# ==========================================================================

@login_required
@assureur_required
def liste_bons(request):
    """Liste tous les bons avec filtres avancés"""
    try:
        # CORRECTION: Retirer 'ordonnance' qui n'existe pas dans le modèle Bon
        bons = Bon.objects.select_related('membre', 'valide_par').order_by('-date_creation')
        
        # Filtres
        statut = request.GET.get('statut')
        type_soin = request.GET.get('type_soin')
        date_debut = request.GET.get('date_debut')
        date_fin = request.GET.get('date_fin')
        search = request.GET.get('search')
        
        if statut:
            bons = bons.filter(statut=statut)
        if type_soin:
            bons = bons.filter(type_soin=type_soin)
        if date_debut:
            bons = bons.filter(date_creation__gte=date_debut)
        if date_fin:
            bons = bons.filter(date_creation__lte=date_fin)
        if search:
            bons = bons.filter(
                Q(numero_bon__icontains=search) |
                Q(membre__nom__icontains=search) |
                Q(membre__prenom__icontains=search) |
                Q(nom_medecin__icontains=search)
            )
        
        # Pagination
        paginator = Paginator(bons, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Statistiques
        stats_bons = {
            'total': Bon.objects.count(),
            'en_attente': Bon.objects.filter(statut='en_attente').count(),
            'valides': Bon.objects.filter(statut='valide').count(),
            'utilises': Bon.objects.filter(statut='utilise').count(),
            'expires': Bon.objects.filter(statut='expire').count(),
            'refuses': Bon.objects.filter(statut='refuse').count(),
            'annules': Bon.objects.filter(statut='annule').count(),
            'montant_total': Bon.objects.aggregate(total=Sum('montant_total'))['total'] or 0,
            'montant_prise_charge': Bon.objects.aggregate(total=Sum('montant_prise_charge'))['total'] or 0,
        }
        
        # Choix pour les filtres
        statut_choices = [
            ('', 'Tous les statuts'),
            ('en_attente', 'En attente'),
            ('valide', 'Validé'),
            ('utilise', 'Utilisé'),
            ('expire', 'Expiré'),
            ('refuse', 'Refusé'),
            ('annule', 'Annulé'),
        ]
        
        # Récupérer les types de soins uniques depuis la base
        type_soin_choices = [('', 'Tous les types')]
        try:
            types = Bon.objects.values_list('type_soin', flat=True).distinct().order_by('type_soin')
            for t in types:
                if t:  # Éviter les valeurs vides
                    type_soin_choices.append((t, t))
        except:
            # Valeurs par défaut
            type_soin_choices.extend([
                ('consultation', 'Consultation'),
                ('analyse', 'Analyse'),
                ('pharmacie', 'Pharmacie'),
                ('hospitalisation', 'Hospitalisation'),
                ('chirurgie', 'Chirurgie'),
            ])
        
        context = {
            'assureur': get_assureur_from_request(request),
            'page_obj': page_obj,
            'stats_bons': stats_bons,
            'statut_choices': statut_choices,
            'type_soin_choices': type_soin_choices,
            'filters': {
                'statut': statut,
                'type_soin': type_soin,
                'date_debut': date_debut,
                'date_fin': date_fin,
                'search': search,
            }
        }
        
        return render(request, 'assureur/liste_bons.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement des bons: {str(e)}")
        import traceback
        traceback.print_exc()
        # Retourner un contexte minimal
        context = {
            'assureur': get_assureur_from_request(request),
            'page_obj': None,
            'stats_bons': {},
            'statut_choices': [('', 'Tous les statuts')],
            'type_soin_choices': [('', 'Tous les types')],
            'filters': {}
        }
        return render(request, 'assureur/liste_bons.html', context)

@login_required
@assureur_required
def detail_bon(request, bon_id):
    """Détails d'un bon spécifique"""
    try:
        bon = get_object_or_404(Bon, id=bon_id)
        
        # Soins associés
        soins_associes = Soin.objects.filter(bon=bon)
        
        context = {
            'assureur': get_assureur_from_request(request),
            'bon': bon,
            'soins_associes': soins_associes,
        }
        
        return render(request, 'assureur/detail_bon.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement du bon: {str(e)}")
        return redirect('assureur:liste_bons')

@login_required
@assureur_required
def creer_bon(request):
    """Création d'un nouveau bon de prise en charge"""
    if request.method == 'POST':
        try:
            data = request.POST
            
            # Validation du membre
            membre_id = data.get('membre_id')
            try:
                membre = Membre.objects.get(id=membre_id)
            except Membre.DoesNotExist:
                messages.error(request, "Membre non trouvé")
                return redirect('assureur:creer_bon')
            
            # Vérification de l'éligibilité du membre
            if membre.statut != 'actif':
                messages.error(request, "Le membre n'est pas actif")
                return redirect('assureur:creer_bon')
            
            # Création du bon
            bon = Bon.objects.create(
                membre=membre,
                type_soin=data.get('type_soin'),
                description=data.get('description', ''),
                montant_total=float(data.get('montant_total', 0)),
                montant_prise_charge=float(data.get('montant_prise_charge', 0)),
                date_expiration=datetime.strptime(data.get('date_expiration'), '%Y-%m-%d').date(),
                date_soin=datetime.strptime(data.get('date_soin'), '%Y-%m-%d').date(),
                nom_medecin=data.get('nom_medecin', ''),
                specialite=data.get('specialite', ''),
                statut='en_attente',
                created_by=request.user
            )
            
            # Validation automatique si demandé
            if data.get('valider_immediatement') == 'on':
                bon.statut = 'valide'
                bon.valide_par = request.user
                bon.date_validation = timezone.now()
                bon.save()
                messages.success(request, f"Bon {bon.numero_bon} créé et validé avec succès")
            else:
                messages.success(request, f"Bon {bon.numero_bon} créé avec succès (en attente de validation)")
            
            return redirect('assureur:detail_bon', bon_id=bon.id)
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la création du bon: {str(e)}")
    
    # Récupération des membres actifs pour le formulaire
    membres_actifs = Membre.objects.filter(statut='actif')
    
    context = {
        'assureur': get_assureur_from_request(request),
        'membres': membres_actifs,
    }
    
    return render(request, 'assureur/creer_bon.html', context)

@login_required
@assureur_required
def creer_bon_pour_membre(request, membre_id):
    """Créer un bon pour un membre spécifique - Redirige vers la création de bon"""
    from django.shortcuts import redirect, get_object_or_404
    
    try:
        from agents.models import Membre
        membre = get_object_or_404(Membre, id=membre_id)
        
        # Log pour débogage
        print(f"DEBUG creer_bon_pour_membre: Membre {membre_id} - {membre.nom} {membre.prenom}")
        
        # Rediriger vers la page de création de bon avec paramètre membre
        return redirect(f'/assureur/bons/creer/?membre={membre_id}')
        
    except Exception as e:
        # Gestion d'erreur robuste
        import traceback
        error_details = traceback.format_exc()
        print(f"ERREUR creer_bon_pour_membre: {str(e)}\n{error_details}")
        messages.error(request, f"Erreur lors de la création du bon: {str(e)}")
        return redirect('assureur:detail_membre', membre_id=membre_id)

@login_required
@assureur_required
def valider_bon(request, bon_id):
    """Validation d'un bon par l'assureur"""
    try:
        bon = get_object_or_404(Bon, id=bon_id)
        
        if bon.statut != 'en_attente':
            messages.warning(request, f"Le bon {bon.numero_bon} n'est pas en attente de validation")
            return redirect('assureur:detail_bon', bon_id=bon.id)
        
        bon.statut = 'valide'
        bon.valide_par = request.user
        bon.date_validation = timezone.now()
        bon.save()
        messages.success(request, f"Bon {bon.numero_bon} validé avec succès")
        
        return redirect('assureur:detail_bon', bon_id=bon.id)
        
    except Exception as e:
        messages.error(request, f"Erreur lors de la validation du bon: {str(e)}")
        return redirect('assureur:liste_bons')

@login_required
@assureur_required
def rejeter_bon(request, bon_id):
    """Rejet d'un bon par l'assureur"""
    if request.method == 'POST':
        try:
            bon = get_object_or_404(Bon, id=bon_id)
            
            if bon.statut == 'en_attente':
                bon.statut = 'refuse'
                bon.valide_par = request.user
                bon.date_validation = timezone.now()
                bon.save()
                
                messages.success(request, f"Bon {bon.numero_bon} rejeté avec succès")
            else:
                messages.warning(request, f"Le bon {bon.numero_bon} ne peut pas être rejeté")
            
            return redirect('assureur:detail_bon', bon_id=bon.id)
            
        except Exception as e:
            messages.error(request, f"Erreur lors du rejet du bon: {str(e)}")
    
    return redirect('assureur:liste_bons')

# ==========================================================================
# VUES POUR LES COTISATIONS
# ==========================================================================

@login_required
@assureur_required
def liste_cotisations(request):
    """Affiche la liste des cotisations"""
    try:
        # Obtenir le filtre de période si présent
        periode_filter = request.GET.get('periode', '')
        
        # Récupérer toutes les cotisations
        cotisations = Cotisation.objects.select_related('membre').order_by('-periode', '-created_at')
        
        # Filtrer par période si spécifiée
        if periode_filter:
            cotisations = cotisations.filter(periode=periode_filter)
        
        # Compter par statut
        total = cotisations.count()
        generees = cotisations.filter(statut='generee').count()
        payees = cotisations.filter(statut='payee').count()
        
        context = {
            'assureur': get_assureur_from_request(request),
            'cotisations': cotisations,
            'total': total,
            'generees': generees,
            'payees': payees,
            'periode_filter': periode_filter,
        }
        
        return render(request, 'assureur/liste_cotisations.html', context)
        
    except Exception as e:
        print(f"ERROR dans liste_cotisations: {e}")
        messages.error(request, f"Erreur lors du chargement de la liste: {str(e)}")
        return render(request, 'assureur/liste_cotisations.html', {'cotisations': []})

def normaliser_periode(periode_input):
    """
    Normalise la période au format 'YYYY-MM'
    """
    if not periode_input:
        return timezone.now().strftime('%Y-%m')
    
    # Format YYYY-MM (input month)
    if '-' in periode_input and len(periode_input) == 7:
        try:
            datetime.strptime(periode_input, '%Y-%m')
            return periode_input
        except:
            pass
    
    # Format dd/mm/yyyy
    if '/' in periode_input:
        try:
            if len(periode_input.split('/')) == 3:
                date_obj = datetime.strptime(periode_input, '%d/%m/%Y')
                return date_obj.strftime('%Y-%m')
            elif len(periode_input.split('/')) == 2:
                date_obj = datetime.strptime(periode_input, '%m/%Y')
                return date_obj.strftime('%Y-%m')
        except:
            pass
    
    return timezone.now().strftime('%Y-%m')

@login_required
@assureur_required
def generer_cotisations(request):
    """Vue COMPLÈTEMENT corrigée pour générer des cotisations"""
    
    try:
        # Récupérer les membres actifs
        membres_actifs = Membre.objects.filter(statut='actif')
        membres_actifs_count = membres_actifs.count()
        
        # Compter les cotisations du mois en cours
        mois_courant = timezone.now().strftime('%Y-%m')
        cotisations_mois_count = Cotisation.objects.filter(periode=mois_courant).count()
        a_generer_count = max(0, membres_actifs_count - cotisations_mois_count)
        
        if request.method == 'POST':
            periode_input = request.POST.get('periode', mois_courant)
            periode = normaliser_periode(periode_input)
            
            print(f"DEBUG: Génération pour la période: {periode}")
            print(f"DEBUG: Membres actifs: {membres_actifs_count}")
            print(f"DEBUG: Cotisations existantes pour {periode}: {Cotisation.objects.filter(periode=periode).count()}")
            
            # Générer les cotisations pour les membres sans cotisation pour cette période
            membres_sans_cotisation = []
            for membre in membres_actifs:
                if not Cotisation.objects.filter(membre=membre, periode=periode).exists():
                    membres_sans_cotisation.append(membre)
            
            created_count = 0
            errors = []
            
            for membre in membres_sans_cotisation:
                try:
                    # Calculer les dates
                    date_emission = datetime.now().date()
                    
                    # Calculer la date d'échéance (fin du mois de la période)
                    if len(periode) == 7:
                        try:
                            year, month = map(int, periode.split('-'))
                            # Premier jour du mois suivant
                            if month == 12:
                                next_month = datetime(year+1, 1, 1)
                            else:
                                next_month = datetime(year, month+1, 1)
                            # Dernier jour du mois courant
                            date_echeance = (next_month - timedelta(days=1)).date()
                        except:
                            # Fallback: échéance dans 30 jours
                            date_echeance = date_emission + timedelta(days=30)
                    else:
                        date_echeance = date_emission + timedelta(days=30)
                    
                    # Déterminer le type de cotisation et le montant
                    # CORRECTION: Utiliser cmu_option au lieu de est_femme_enceinte
                    if hasattr(membre, 'cmu_option') and membre.cmu_option:
                        type_cotisation = 'femme_enceinte'
                        montant = Decimal('7500.00')
                    else:
                        type_cotisation = 'normale'
                        montant = Decimal('5000.00')
                    
                    # Créer la référence - CORRECTION: Utiliser numero_unique
                    ref_mois = periode.replace('-', '')
                    reference = f"COT-{membre.numero_unique}-{ref_mois}"
                    
                    # Créer la cotisation
                    cotisation = Cotisation(
                        membre=membre,
                        periode=periode,
                        montant=montant,
                        statut='due',
                        date_emission=date_emission,
                        date_echeance=date_echeance,
                        type_cotisation=type_cotisation,
                        reference=reference,
                        enregistre_par=request.user if request.user.is_authenticated else None,
                        notes='Générée automatiquement',
                        # Champs obligatoires avec valeurs par défaut
                        montant_clinique=Decimal('0.00'),
                        montant_pharmacie=Decimal('0.00'),
                        montant_charges_mutuelle=Decimal('0.00'),
                    )
                    
                    # Sauvegarder
                    cotisation.save()
                    
                    print(f"DEBUG: Cotisation créée - Réf: {reference}, Membre: {membre.nom}, Type: {type_cotisation}, Montant: {montant}")
                    created_count += 1
                    
                except Exception as e:
                    error_msg = f"Erreur pour {membre.nom}: {str(e)}"
                    errors.append(error_msg)
                    print(f"DEBUG: {error_msg}")
                    traceback.print_exc()
                    continue
            
            if errors:
                messages.warning(request, f"Génération partielle. {created_count} cotisation(s) créée(s), {len(errors)} erreur(s).")
                for error in errors[:3]:
                    messages.warning(request, error)
            else:
                messages.success(request, f'{created_count} cotisation(s) générée(s) pour {periode}')
            
            return redirect('assureur:liste_cotisations')
        
        # GET : Afficher le formulaire
        return render(request, 'assureur/generer_cotisations.html', {
            'assureur': get_assureur_from_request(request),
            'membres_actifs_count': membres_actifs_count,
            'cotisations_mois_count': cotisations_mois_count,
            'a_generer_count': a_generer_count,
            'current_month': timezone.now(),
        })
        
    except Exception as e:
        print(f"ERREUR GRAVE dans generer_cotisations: {e}")
        traceback.print_exc()
        messages.error(request, f'Erreur lors de la génération: {str(e)}')
        return redirect('assureur:dashboard')

@login_required
@assureur_required
def preview_generation(request):
    """Prévisualisation simplifiée"""
    periode_input = request.GET.get('periode', timezone.now().strftime('%Y-%m'))
    periode = normaliser_periode(periode_input)
    
    # Récupérer les membres actifs sans cotisation pour cette période
    membres_a_generer = []
    for membre in Membre.objects.filter(statut='actif'):
        if not Cotisation.objects.filter(membre=membre, periode=periode).exists():
            membres_a_generer.append(membre)
    
    data = {
        'periode': periode,
        'total_membres_actifs': Membre.objects.filter(statut='actif').count(),
        'cotisations_existantes': Cotisation.objects.filter(periode=periode).count(),
        'total_a_generer': len(membres_a_generer),
        'membres_a_generer': membres_a_generer,
    }
    
    return render(request, 'assureur/includes/preview_content.html', data)

@login_required
@assureur_required
def enregistrer_paiement_cotisation(request, cotisation_id):
    """Enregistrement du paiement d'une cotisation"""
    if request.method == 'POST':
        try:
            cotisation = get_object_or_404(Cotisation, id=cotisation_id)
            
            if cotisation.statut in ['due', 'en_retard']:
                cotisation.statut = 'payee'
                cotisation.date_paiement = datetime.strptime(request.POST.get('date_paiement'), '%Y-%m-%d').date() if request.POST.get('date_paiement') else timezone.now().date()
                cotisation.enregistre_par = request.user
                cotisation.save()
                
                messages.success(request, f"Paiement de la cotisation {cotisation.reference} enregistré avec succès")
            else:
                messages.warning(request, "Cette cotisation ne peut pas être payée")
            
            return redirect('assureur:liste_cotisations')
            
        except Exception as e:
            messages.error(request, f"Erreur lors de l'enregistrement du paiement: {str(e)}")
    
    return redirect('assureur:liste_cotisations')

@login_required
@assureur_required
def creer_cotisation_membre(request, membre_id=None):
    """Créer une cotisation manuelle pour un membre spécifique"""
    try:
        membre = None
        if membre_id:
            membre = get_object_or_404(Membre, id=membre_id)
        
        if request.method == 'POST':
            # Récupérer les données du formulaire
            periode_input = request.POST.get('periode', '')
            montant = Decimal(request.POST.get('montant', '0'))
            type_cotisation = request.POST.get('type_cotisation', 'normale')
            notes = request.POST.get('notes', '')
            
            # Normaliser la période
            periode = normaliser_periode(periode_input)
            
            # Vérifier si une cotisation existe déjà pour cette période
            if Cotisation.objects.filter(membre=membre, periode=periode).exists():
                messages.error(request, f"Une cotisation existe déjà pour {membre.get_full_name()} pour la période {periode}")
                return redirect('assureur:liste_cotisations')
            
            # Calculer les dates
            date_emission = timezone.now().date()
            
            # Calculer la date d'échéance (fin du mois de la période)
            if len(periode) == 7:
                try:
                    year, month = map(int, periode.split('-'))
                    if month == 12:
                        next_month = datetime(year+1, 1, 1)
                    else:
                        next_month = datetime(year, month+1, 1)
                    date_echeance = (next_month - timedelta(days=1)).date()
                except:
                    date_echeance = date_emission + timedelta(days=30)
            else:
                date_echeance = date_emission + timedelta(days=30)
            
            # Créer la référence
            ref_mois = periode.replace('-', '')
            reference = f"COT-MAN-{membre.numero_unique}-{ref_mois}"
            
            # Créer la cotisation
            cotisation = Cotisation.objects.create(
                membre=membre,
                periode=periode,
                montant=montant,
                statut='due',
                date_emission=date_emission,
                date_echeance=date_echeance,
                type_cotisation=type_cotisation,
                reference=reference,
                enregistre_par=request.user,
                notes=notes,
                # Champs obligatoires avec valeurs par défaut
                montant_clinique=Decimal('0.00'),
                montant_pharmacie=Decimal('0.00'),
                montant_charges_mutuelle=Decimal('0.00'),
            )
            
            messages.success(request, f"Cotisation créée avec succès pour {membre.get_full_name()}")
            return redirect('assureur:detail_membre', membre_id=membre.id)
        
        # Pour GET : afficher le formulaire
        # Liste des mois disponibles (6 derniers mois)
        mois_liste = []
        aujourd_hui = datetime.now()
        for i in range(6):
            mois = aujourd_hui - timedelta(days=30*i)
            mois_liste.append(mois.strftime('%Y-%m'))
        
        context = {
            'assureur': get_assureur_from_request(request),
            'membre': membre,
            'mois_liste': mois_liste,
            'aujourd_hui': timezone.now().strftime('%Y-%m'),
        }
        
        return render(request, 'assureur/creer_cotisation_membre.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors de la création de la cotisation: {str(e)}")
        traceback.print_exc()
        return redirect('assureur:liste_membres')

@login_required
@assureur_required
def editer_cotisation(request, cotisation_id):
    """Éditer une cotisation existante"""
    try:
        cotisation = get_object_or_404(Cotisation, id=cotisation_id)
        
        if request.method == 'POST':
            # Mettre à jour les données
            cotisation.montant = Decimal(request.POST.get('montant', '0'))
            cotisation.type_cotisation = request.POST.get('type_cotisation', 'normale')
            cotisation.statut = request.POST.get('statut', 'due')
            cotisation.notes = request.POST.get('notes', '')
            
            # Mettre à jour la date d'échéance si fournie
            date_echeance = request.POST.get('date_echeance')
            if date_echeance:
                cotisation.date_echeance = datetime.strptime(date_echeance, '%Y-%m-%d').date()
            
            cotisation.save()
            
            messages.success(request, f"Cotisation {cotisation.reference} mise à jour")
            return redirect('assureur:liste_cotisations')
        
        context = {
            'assureur': get_assureur_from_request(request),
            'cotisation': cotisation,
            'statuts_choices': [
                ('due', 'Due'),
                ('payee', 'Payée'),
                ('en_retard', 'En retard'),
                ('annulee', 'Annulée'),
            ],
            'types_choices': [
                ('normale', 'Normale'),
                ('femme_enceinte', 'Femme enceinte'),
                ('reduction', 'Réduction'),
                ('exceptionnelle', 'Exceptionnelle'),
            ],
        }
        
        return render(request, 'assureur/editer_cotisation.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors de l'édition: {str(e)}")
        return redirect('assureur:liste_cotisations')

@login_required
@assureur_required
def supprimer_cotisation(request, cotisation_id):
    """Supprimer une cotisation (si non payée)"""
    try:
        cotisation = get_object_or_404(Cotisation, id=cotisation_id)
        
        if cotisation.statut == 'payee':
            messages.error(request, "Impossible de supprimer une cotisation déjà payée")
            return redirect('assureur:liste_cotisations')
        
        if request.method == 'POST':
            reference = cotisation.reference
            cotisation.delete()
            messages.success(request, f"Cotisation {reference} supprimée")
            return redirect('assureur:liste_cotisations')
        
        context = {
            'assureur': get_assureur_from_request(request),
            'cotisation': cotisation,
        }
        
        return render(request, 'assureur/supprimer_cotisation.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors de la suppression: {str(e)}")
        return redirect('assureur:liste_cotisations')

# ==========================================================================
# VUES POUR LES SOINS
# ==========================================================================

@login_required
@assureur_required
def liste_soins(request):
    """Liste tous les soins avec filtres"""
    try:
        soins = Soin.objects.select_related('membre', 'bon', 'traite_par').order_by('-date_soumission')
        
        # Filtres
        statut = request.GET.get('statut')
        date_debut = request.GET.get('date_debut')
        date_fin = request.GET.get('date_fin')
        search = request.GET.get('search')
        
        if statut:
            soins = soins.filter(statut=statut)
        if date_debut:
            soins = soins.filter(date_soin__gte=date_debut)
        if date_fin:
            soins = soins.filter(date_soin__lte=date_fin)
        if search:
            soins = soins.filter(
                Q(membre__nom__icontains=search) |
                Q(membre__prenom__icontains=search) |
                Q(type_soin__icontains=search) |
                Q(description__icontains=search)
            )
        
        # Pagination
        paginator = Paginator(soins, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Statistiques
        stats_soins = {
            'total': Soin.objects.count(),
            'soumis': Soin.objects.filter(statut='soumis').count(),
            'en_cours': Soin.objects.filter(statut='en_cours').count(),
            'valides': Soin.objects.filter(statut='valide').count(),
            'refuses': Soin.objects.filter(statut='refuse').count(),
            'payes': Soin.objects.filter(statut='paye').count(),
            'montant_facture': Soin.objects.aggregate(total=Sum('montant_facture'))['total'] or 0,
            'montant_rembourse': Soin.objects.aggregate(total=Sum('montant_rembourse'))['total'] or 0,
        }
        
        context = {
            'assureur': get_assureur_from_request(request),
            'page_obj': page_obj,
            'stats_soins': stats_soins,
            'filters': {
                'statut': statut,
                'date_debut': date_debut,
                'date_fin': date_fin,
                'search': search,
            }
        }
        
        return render(request, 'assureur/liste_soins.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement des soins: {str(e)}")
        context = {'assureur': get_assureur_from_request(request)}
        return render(request, 'assureur/liste_soins.html', context)

@login_required
@assureur_required
def detail_soin(request, soin_id):
    """Détails d'un soin spécifique"""
    try:
        soin = get_object_or_404(Soin, id=soin_id)
        
        context = {
            'assureur': get_assureur_from_request(request),
            'soin': soin,
        }
        
        return render(request, 'assureur/detail_soin.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement du soin: {str(e)}")
        return redirect('assureur:liste_soins')

@login_required
@assureur_required
def valider_soin(request, soin_id):
    """Validation d'un soin"""
    try:
        soin = get_object_or_404(Soin, id=soin_id)
        
        if soin.statut in ['soumis', 'en_cours']:
            soin.statut = 'valide'
            soin.traite_par = request.user
            soin.date_traitement = timezone.now()
            soin.save()
            
            messages.success(request, f"Soin validé avec succès")
        else:
            messages.warning(request, "Ce soin ne peut pas être validé")
        
        return redirect('assureur:detail_soin', soin_id=soin.id)
        
    except Exception as e:
        messages.error(request, f"Erreur lors de la validation du soin: {str(e)}")
        return redirect('assureur:liste_soins')

@login_required
@assureur_required
def rejeter_soin(request, soin_id):
    """Rejet d'un soin avec motif"""
    if request.method == 'POST':
        try:
            soin = get_object_or_404(Soin, id=soin_id)
            motif_refus = request.POST.get('motif_refus', '')
            
            if soin.statut in ['soumis', 'en_cours']:
                soin.statut = 'refuse'
                soin.motif_refus = motif_refus
                soin.traite_par = request.user
                soin.date_traitement = timezone.now()
                soin.save()
                
                messages.success(request, f"Soin rejeté avec succès")
            else:
                messages.warning(request, "Ce soin ne peut pas être rejeté")
            
            return redirect('assureur:detail_soin', soin_id=soin.id)
            
        except Exception as e:
            messages.error(request, f"Erreur lors du rejet du soin: {str(e)}")
    
    return redirect('assureur:liste_soins')

# ==========================================================================
# VUES POUR LES PAIEMENTS
# ==========================================================================


@login_required
@csrf_exempt
def api_soins_par_membre(request, membre_id):
    """API pour récupérer les soins d'un membre"""
    try:
        from agents.models import Membre
        from assureur.models import Soin
        
        membre = Membre.objects.get(id=membre_id)
        soins = Soin.objects.filter(membre=membre, statut='valide').order_by('-date_soin')
        
        data = []
        for soin in soins:
            data.append({
                'id': soin.id,
                'code': soin.code or f'SOIN-{soin.id}',
                'type_soin': soin.type_soin,
                'description': soin.description or '',
                'montant_facture': float(soin.montant_facture) if soin.montant_facture else 0,
                'montant_restant': float(soin.montant_restant) if soin.montant_restant else 0,
                'date_soin': soin.date_soin.strftime('%d/%m/%Y') if soin.date_soin else '',
                'statut': soin.statut,
            })
        
        return JsonResponse(data, safe=False)
        
    except Membre.DoesNotExist:
        return JsonResponse({'error': 'Membre non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@assureur_required
def liste_paiements(request):
    """Liste tous les paiements"""
    try:
        paiements = Paiement.objects.select_related(
            'membre', 'soin', 'valide_par', 'created_by'
        ).order_by('-date_paiement')
        
        # Filtres
        statut = request.GET.get('statut')
        mode_paiement = request.GET.get('mode_paiement')
        date_debut = request.GET.get('date_debut')
        date_fin = request.GET.get('date_fin')
        search = request.GET.get('search')
        
        if statut:
            paiements = paiements.filter(statut=statut)
        if mode_paiement:
            paiements = paiements.filter(mode_paiement=mode_paiement)
        if date_debut:
            paiements = paiements.filter(date_paiement__gte=date_debut)
        if date_fin:
            paiements = paiements.filter(date_paiement__lte=date_fin)
        if search:
            paiements = paiements.filter(
                Q(membre__nom__icontains=search) |
                Q(membre__prenom__icontains=search) |
                Q(reference__icontains=search) |
                Q(notes__icontains=search)
            )
        
        # Pagination
        paginator = Paginator(paiements, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Statistiques
        stats_paiements = {
            'total': Paiement.objects.count(),
            'initie': Paiement.objects.filter(statut='initie').count(),
            'valide': Paiement.objects.filter(statut='valide').count(),
            'annule': Paiement.objects.filter(statut='annule').count(),
            'montant_total': Paiement.objects.aggregate(total=Sum('montant'))['total'] or 0,
            'montant_valide': Paiement.objects.filter(statut='valide').aggregate(total=Sum('montant'))['total'] or 0,
        }
        
        context = {
            'assureur': get_assureur_from_request(request),
            'page_obj': page_obj,
            'stats_paiements': stats_paiements,
            'filters': {
                'statut': statut,
                'mode_paiement': mode_paiement,
                'date_debut': date_debut,
                'date_fin': date_fin,
                'search': search,
            }
        }
        
        return render(request, 'assureur/liste_paiements.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement des paiements: {str(e)}")
        context = {'assureur': get_assureur_from_request(request)}
        return render(request, 'assureur/liste_paiements.html', context)

@login_required
@assureur_required
def creer_paiement(request):
    """Création d'un nouveau paiement avec formulaire - VERSION COMPLÈTE"""
    # Vérifier si un bon_id est passé en paramètre
    bon_id = request.GET.get('bon_id')
    bon = None
    
    if bon_id:
        try:
            bon = Bon.objects.get(id=bon_id)
        except Bon.DoesNotExist:
            messages.warning(request, "Le bon spécifié n'existe pas")
    
    if request.method == 'POST':
        form = PaiementForm(request.POST, bon=bon)
        if form.is_valid():
            try:
                paiement = form.save(commit=False)
                paiement.created_by = request.user
                
                # Si le statut est 'valide', définir les infos de validation
                if paiement.statut == 'valide':
                    paiement.valide_par = request.user
                    paiement.date_validation = timezone.now()
                
                # Sauvegarder le paiement
                paiement.save()
                
                messages.success(request, f"Paiement {paiement.reference} créé avec succès")
                
                # Rediriger vers la liste des paiements
                return redirect('assureur:liste_paiements')
                
            except Exception as e:
                messages.error(request, f"Erreur lors de la création du paiement: {str(e)}")
                print(f"Erreur création paiement: {e}")
                import traceback
                traceback.print_exc()
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        # Initialiser le formulaire
        initial_data = {}
        if bon:
            initial_data = {
                'membre': bon.membre,
                'montant': bon.montant_total,
                'notes': f"Paiement pour le bon {bon.numero_bon}"
            }
        form = PaiementForm(initial=initial_data, bon=bon)
    
    context = {
        'form': form,
        'assureur': get_assureur_from_request(request),
        'bon': bon,
    }
    
    return render(request, 'assureur/creer_paiement.html', context)


@login_required
@assureur_required
def detail_paiement(request, paiement_id):
    """Détails d'un paiement spécifique"""
    try:
        paiement = get_object_or_404(Paiement, id=paiement_id)
        
        context = {
            'assureur': get_assureur_from_request(request),
            'paiement': paiement,
        }
        
        return render(request, 'assureur/detail_paiement.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement du paiement: {str(e)}")
        return redirect('assureur:liste_paiements')

@login_required
@assureur_required
def valider_paiement(request, paiement_id):
    """Validation d'un paiement"""
    try:
        paiement = get_object_or_404(Paiement, id=paiement_id)
        
        if paiement.statut == 'initie':
            paiement.statut = 'valide'
            paiement.valide_par = request.user
            paiement.date_validation = timezone.now()
            paiement.save()
            
            messages.success(request, f"Paiement {paiement.reference} validé avec succès")
        else:
            messages.warning(request, f"Le paiement {paiement.reference} ne peut pas être validé")
        
        return redirect('assureur:detail_paiement', paiement_id=paiement.id)
        
    except Exception as e:
        messages.error(request, f"Erreur lors de la validation du paiement: {str(e)}")
        return redirect('assureur:liste_paiements')

@login_required
@assureur_required
def annuler_paiement(request, paiement_id):
    """Annulation d'un paiement"""
    if request.method == 'POST':
        try:
            paiement = get_object_or_404(Paiement, id=paiement_id)
            motif = request.POST.get('motif', '')
            
            if paiement.statut in ['initie', 'valide']:
                paiement.statut = 'annule'
                paiement.notes = f"{paiement.notes}\n\nANNULÉ - Motif: {motif}"
                paiement.save()
                
                messages.success(request, f"Paiement {paiement.reference} annulé avec succès")
            else:
                messages.warning(request, f"Le paiement {paiement.reference} ne peut pas être annulé")
            
            return redirect('assureur:detail_paiement', paiement_id=paiement.id)
            
        except Exception as e:
            messages.error(request, f"Erreur lors de l'annulation du paiement: {str(e)}")
    
    return redirect('assureur:liste_paiements')


def debug_paiement(request):
    """Vue de débogage pour le formulaire de paiement"""
    from assureur.forms import PaiementForm
    from assureur.models import Membre
    
    membre = Membre.objects.first()
    
    if request.method == 'POST':
        form = PaiementForm(request.POST)
        
        print("=== DÉBOGAGE POST ===")
        print("Données POST:", request.POST)
        print("Mode paiement:", request.POST.get('mode_paiement'))
        print("Formulaire valide:", form.is_valid())
        if not form.is_valid():
            print("Erreurs:", form.errors)
        
    else:
        # Pré-remplir avec un membre pour faciliter le test
        initial = {}
        if membre:
            initial['membre'] = membre.id
        form = PaiementForm(initial=initial)
    
    return render(request, 'assureur/debug_paiement.html', {
        'form': form,
        'debug': True
    })

# ==========================================================================
# VUES POUR LES STATISTIQUES ET RAPPORTS
# ==========================================================================


from django.core.exceptions import FieldError

@login_required
@assureur_required
def statistiques_assureur(request):
    """Version simplifiée et robuste des statistiques"""
    try:
        assureur = get_assureur_from_request(request)
        
        # Périodes
        today = timezone.now().date()
        one_year_ago = today - timedelta(days=365)
        one_month_ago = today - timedelta(days=30)
        
        # 1. Statistiques de base (robuste)
        stats = {
            'membres': {
                'total': Membre.objects.count(),
                'actifs': Membre.objects.filter(statut='actif').count(),
                'inactifs': Membre.objects.filter(statut='inactif').count(),
                'nouveaux_mois': Membre.objects.filter(
                    date_inscription__gte=one_month_ago
                ).count(),
            },
            'financier': {
                'cotisations_total': Cotisation.objects.filter(
                    date_emission__gte=one_year_ago
                ).aggregate(total=Sum('montant'))['total'] or 0,
                'cotisations_mois': Cotisation.objects.filter(
                    date_emission__month=today.month,
                    date_emission__year=today.year
                ).aggregate(total=Sum('montant'))['total'] or 0,
                'paiements_total': Paiement.objects.filter(
                    date_paiement__gte=one_year_ago,
                    statut='valide'
                ).aggregate(total=Sum('montant'))['total'] or 0,
                'bons_total': Bon.objects.filter(
                    date_creation__gte=one_year_ago
                ).aggregate(total=Sum('montant_total'))['total'] or 0,
            },
            'traitement': {
                'soins_total': Soin.objects.count(),
                'soins_valides': Soin.objects.filter(statut='valide').count(),
                'soins_en_cours': Soin.objects.filter(statut='en_cours').count(),
                'soins_soumis': Soin.objects.filter(statut='soumis').count(),
            }
        }
        
        # 2. Calculs sécurisés
        # Taux de validation
        if stats['traitement']['soins_total'] > 0:
            stats['traitement']['taux_validation'] = round(
                (stats['traitement']['soins_valides'] / stats['traitement']['soins_total']) * 100, 1
            )
        else:
            stats['traitement']['taux_validation'] = 0
            
        # Taux de recouvrement
        if stats['financier']['cotisations_total'] > 0:
            cotisations_payees = Cotisation.objects.filter(
                date_emission__gte=one_year_ago,
                statut='payee'
            ).aggregate(total=Sum('montant'))['total'] or 0
            stats['financier']['taux_recouvrement'] = round(
                (cotisations_payees / stats['financier']['cotisations_total']) * 100, 1
            )
        else:
            stats['financier']['taux_recouvrement'] = 0
        
        # 3. Membres avec cotisations (avec vérification)
        try:
            # Vérifier si la relation 'cotisations' existe
            membres_avec_cot = Membre.objects.filter(
                cotisations__isnull=False
            ).distinct().count()
            stats['membres']['avec_cotisations'] = membres_avec_cot
        except FieldError:
            # Alternative: compter via le modèle Cotisation
            membres_avec_cot = Cotisation.objects.values('membre').distinct().count()
            stats['membres']['avec_cotisations'] = membres_avec_cot
        
        # 4. Top 5 cotisants
        try:
            top_cotisants = Cotisation.objects.values(
                'membre__nom', 'membre__prenom'
            ).annotate(
                total=Sum('montant'),
                count=Count('id')
            ).order_by('-total')[:5]
            stats['top_cotisants'] = list(top_cotisants)
        except Exception as e:
            logger.error(f"Erreur top cotisants: {e}")
            stats['top_cotisants'] = []
        
        # 5. Évolution des 6 derniers mois
        evolution = []
        for i in range(6):
            mois = today.month - i
            annee = today.year
            
            while mois <= 0:
                mois += 12
                annee -= 1
            
            mois_debut = datetime(annee, mois, 1).date()
            if mois == 12:
                mois_fin = datetime(annee + 1, 1, 1).date() - timedelta(days=1)
            else:
                mois_fin = datetime(annee, mois + 1, 1).date() - timedelta(days=1)
            
            mois_stats = {
                'mois': mois_debut.strftime('%b %Y'),
                'cotisations': Cotisation.objects.filter(
                    date_emission__gte=mois_debut,
                    date_emission__lte=mois_fin
                ).aggregate(total=Sum('montant'))['total'] or 0,
                'membres': Membre.objects.filter(
                    date_inscription__gte=mois_debut,
                    date_inscription__lte=mois_fin
                ).count(),
                'paiements': Paiement.objects.filter(
                    date_paiement__gte=mois_debut,
                    date_paiement__lte=mois_fin,
                    statut='valide'
                ).aggregate(total=Sum('montant'))['total'] or 0,
            }
            evolution.append(mois_stats)
        
        evolution.reverse()  # Du plus ancien au plus récent
        
        context = {
            'assureur': assureur,
            'stats': stats,
            'evolution': evolution,
            'periode': f"{one_year_ago.strftime('%d/%m/%Y')} - {today.strftime('%d/%m/%Y')}",
        }
        
        return render(request, 'assureur/statistiques_simple.html', context)
        
    except Exception as e:
        logger.error(f"Erreur statistiques simplifiées: {e}", exc_info=True)
        return render(request, 'assureur/statistiques_simple.html', {
            'assureur': get_assureur_from_request(request),
            'error': str(e),
            'stats': {
                'membres': {'total': 0, 'actifs': 0, 'inactifs': 0, 'nouveaux_mois': 0},
                'financier': {'cotisations_total': 0, 'cotisations_mois': 0, 'paiements_total': 0, 'bons_total': 0},
                'traitement': {'soins_total': 0, 'soins_valides': 0, 'soins_en_cours': 0, 'soins_soumis': 0}
            }
        })

@login_required
@assureur_required
@csrf_exempt
def api_statistiques(request):
    """API pour récupérer les statistiques en temps réel (AJAX)"""
    try:
        assureur = get_assureur_from_request(request)
        
        # Filtre par assureur si applicable
        # NOTE: Adaptez selon vos relations de modèle
        filtres = {}
        # if assureur:
        #     filtres['assureur'] = assureur
        
        # Statistiques en temps réel
        stats = {
            'membres_actifs': Membre.objects.filter(statut='actif', **filtres).count(),
            'membres_total': Membre.objects.filter(**filtres).count(),
            'bons_en_attente': Bon.objects.filter(statut='en_attente', **filtres).count(),
            'bons_valides': Bon.objects.filter(statut='valide', **filtres).count(),
            'cotisations_en_retard': Cotisation.objects.filter(
                statut='en_retard', 
                date_echeance__lt=timezone.now().date(),
                **filtres
            ).count(),
            'cotisations_payees_mois': Cotisation.objects.filter(
                statut='payee',
                date_emission__month=timezone.now().month,
                date_emission__year=timezone.now().year,
                **filtres
            ).aggregate(total=Sum('montant'))['total'] or 0,
            'montant_total_bons': Bon.objects.filter(**filtres).aggregate(
                total=Sum('montant_total')
            )['total'] or 0,
            'montant_total_cotisations': Cotisation.objects.filter(**filtres).aggregate(
                total=Sum('montant')
            )['total'] or 0,
            'soins_en_cours': Soin.objects.filter(statut='en_cours', **filtres).count(),
        }
        
        # Ajouter des timestamps pour le rafraîchissement
        return JsonResponse({
            'success': True,
            'stats': stats,
            'timestamp': timezone.now().isoformat(),
            'mise_a_jour': timezone.now().strftime('%H:%M:%S')
        })
        
    except Exception as e:
        logger.error(f"Erreur API statistiques: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=500)

# ==========================================================================
# VUES POUR LA CONFIGURATION
# ==========================================================================

@login_required
@assureur_required
def configuration_assureur(request):
    """Configuration du système"""
    try:
        config = ConfigurationAssurance.objects.first()
        
        if request.method == 'POST':
            if not config:
                config = ConfigurationAssurance.objects.create()
            
            config.nom_assureur = request.POST.get('nom_assureur')
            config.taux_couverture_defaut = float(request.POST.get('taux_couverture_defaut', 80))
            config.delai_validite_bon = int(request.POST.get('delai_validite_bon', 30))
            config.montant_plafond_annuel = float(request.POST.get('montant_plafond_annuel', 10000))
            config.seuil_alerte_montant = float(request.POST.get('seuil_alerte_montant', 5000))
            config.updated_by = request.user
            config.save()
            
            messages.success(request, "Configuration mise à jour avec succès")
            return redirect('assureur:configuration')
        
        context = {
            'assureur': get_assureur_from_request(request),
            'config': config,
        }
        
        return render(request, 'assureur/configuration.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors de la configuration: {str(e)}")
        context = {'assureur': get_assureur_from_request(request)}
        return render(request, 'assureur/configuration.html', context)

# ==========================================================================
# VUES POUR LA RECHERCHE
# ==========================================================================

@login_required
@assureur_required
def recherche_membre(request):
    """Recherche avancée de membres - VERSION CORRIGÉE"""
    search = request.GET.get('q', '')
    
    if search:
        membres = Membre.objects.filter(
            Q(nom__icontains=search) |
            Q(prenom__icontains=search) |
            Q(numero_unique__icontains=search) |  # numero_unique, pas numero_membre
            Q(email__icontains=search) |
            Q(telephone__icontains=search) |
            Q(numero_piece_identite__icontains=search)  # numero_piece_identite, pas numero_contrat
        ).order_by('nom', 'prenom')[:20]
    else:
        membres = []
    
    context = {
        'assureur': get_assureur_from_request(request),
        'membres': membres,
        'search_term': search,
    }
    
    return render(request, 'assureur/recherche_membre.html', context)

# ==========================================================================
# VUES POUR LES RAPPORTS
# ==========================================================================

@login_required
@assureur_required
def rapports(request):
    """Gestion des rapports"""
    rapports_list = RapportAssureur.objects.filter(assureur=request.user).order_by('-date_generation')[:10]
    
    context = {
        'assureur': get_assureur_from_request(request),
        'rapports': rapports_list,
    }
    
    return render(request, 'assureur/rapports.html', context)

@login_required
@assureur_required
def generer_rapport(request):
    """Génération d'un rapport personnalisé"""
    if request.method == 'POST':
        try:
            data = request.POST
            
            rapport = RapportAssureur.objects.create(
                titre=data.get('titre', f"Rapport {timezone.now().strftime('%Y-%m-%d')}"),
                assureur=request.user,
                type_rapport=data.get('type_rapport', 'MENSUEL'),
                periode_debut=datetime.strptime(data.get('periode_debut'), '%Y-%m-%d').date() if data.get('periode_debut') else timezone.now().date() - timedelta(days=30),
                periode_fin=datetime.strptime(data.get('periode_fin'), '%Y-%m-%d').date() if data.get('periode_fin') else timezone.now().date(),
                description=data.get('description', ''),
            )
            
            messages.success(request, f"Rapport '{rapport.titre}' généré avec succès")
            return redirect('assureur:detail_rapport', rapport_id=rapport.id)
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la génération du rapport: {str(e)}")
    
    context = {
        'assureur': get_assureur_from_request(request),
    }
    return render(request, 'assureur/generer_rapport.html', context)

@login_required
@assureur_required
def detail_rapport(request, rapport_id):
    """Détails d'un rapport"""
    try:
        rapport = get_object_or_404(RapportAssureur, id=rapport_id, assureur=request.user)
        
        context = {
            'assureur': get_assureur_from_request(request),
            'rapport': rapport,
        }
        
        return render(request, 'assureur/detail_rapport.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement du rapport: {str(e)}")
        return redirect('assureur:rapports')

@login_required
@assureur_required
def export_rapport(request, rapport_id):
    """Export d'un rapport en CSV"""
    try:
        rapport = get_object_or_404(RapportAssureur, id=rapport_id, assureur=request.user)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="rapport_{rapport.titre}_{timezone.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Rapport', rapport.titre])
        writer.writerow(['Période', f'{rapport.periode_debut} au {rapport.periode_fin}'])
        writer.writerow(['Généré le', rapport.date_generation.strftime('%d/%m/%Y %H:%M')])
        
        return response
        
    except Exception as e:
        messages.error(request, f"Erreur lors de l'export du rapport: {str(e)}")
        return redirect('assureur:detail_rapport', rapport_id=rapport_id)

# ==========================================================================
# VUES POUR L'EXPORT DE DONNÉES
# ==========================================================================



def export_csv(fields, data_rows, filename):
    """Export en CSV"""
    try:
        from django.http import HttpResponse
        import csv
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        
        # Créer le writer CSV avec encodage UTF-8
        writer = csv.writer(response, delimiter=';')
        
        # Écrire les en-têtes
        headers = []
        for field in fields:
            # Formater les noms de colonnes
            header_name = field.replace('__', ' - ').replace('_', ' ').title()
            headers.append(header_name)
        writer.writerow(headers)
        
        # Écrire les données
        for row in data_rows:
            csv_row = []
            for field in fields:
                value = row.get(field, '')
                csv_row.append(value)
            writer.writerow(csv_row)
        
        return response
        
    except Exception as e:
        # En cas d'erreur, retourner une réponse CSV simple
        import traceback
        traceback.print_exc()
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}_error.csv"'
        writer = csv.writer(response)
        writer.writerow(['Erreur lors de l\'export'])
        writer.writerow([str(e)])
        return response


def export_pdf(request, titre, fields, data_rows, filename, template_name='assureur/export_pdf_template.html'):
    """Export en PDF avec template spécifique"""
    try:
        # Vérifier si WeasyPrint est installé
        try:
            from weasyprint import HTML
            from weasyprint.text.fonts import FontConfiguration
        except ImportError:
            # Rediriger vers la page d'export CSV si PDF non disponible
            messages.error(request, "Export PDF non disponible. Utilisez le format CSV ou installez WeasyPrint.")
            return export_csv(fields, data_rows, filename)
        
        # Préparer les en-têtes pour l'affichage
        headers = []
        for field in fields:
            header_name = field.replace('__', ' - ').replace('_', ' ').title()
            headers.append(header_name)
        
        # Préparer les données pour le template
        table_data = []
        for row in data_rows:
            table_row = []
            for field in fields:
                table_row.append(row.get(field, ''))
            table_data.append(table_row)
        
        # Contexte pour le template
        context = {
            'titre': titre,
            'headers': headers,
            'data': table_data,
            'date_export': timezone.now().strftime('%d/%m/%Y %H:%M'),
            'total_items': len(table_data),
            'assureur': get_assureur_from_request(request),
        }
        
        # Rendre le template HTML
        html_string = render_to_string(template_name, context)
        
        # Générer le PDF
        font_config = FontConfiguration()
        html = HTML(string=html_string)
        pdf_file = html.write_pdf(font_config=font_config)
        
        # Créer la réponse
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
        
        return response
        
    except Exception as e:
        # Fallback vers CSV en cas d'erreur PDF
        import traceback
        traceback.print_exc()
        return export_csv(fields, data_rows, filename)


@login_required
@assureur_required
def export_donnees(request, type_donnees):
    """Export des données en CSV ou PDF - VERSION ADAPTÉE À VOTRE STRUCTURE"""
    try:
        # Vérifier le format demandé
        export_format = request.GET.get('format', 'csv')  # Par défaut CSV
        
        # Préparer les données selon le type
        if type_donnees == 'membres':
            queryset = Membre.objects.all().order_by('nom', 'prenom')
            filename = f'membres_{timezone.now().strftime("%Y%m%d_%H%M%S")}'
            fields = ['numero_unique', 'nom', 'prenom', 'email', 'telephone', 'statut', 'date_inscription']
            titre = "Liste des membres"
            template_pdf = 'assureur/export_pdf_template.html'  # Template générique
            
        elif type_donnees == 'bons':
            queryset = Bon.objects.select_related('membre').all().order_by('-date_creation')
            filename = f'bons_{timezone.now().strftime("%Y%m%d_%H%M%S")}'
            fields = ['numero_bon', 'membre__nom', 'membre__prenom', 'type_soin', 'montant_total', 'montant_prise_charge', 'statut', 'date_creation']
            titre = "Liste des bons de prise en charge"
            template_pdf = 'assureur/export_bons_pdf.html'  # Template spécifique aux bons
            
        elif type_donnees == 'cotisations':
            queryset = Cotisation.objects.select_related('membre').all().order_by('-periode')
            filename = f'cotisations_{timezone.now().strftime("%Y%m%d_%H%M%S")}'
            fields = ['reference', 'membre__nom', 'membre__prenom', 'periode', 'montant', 'statut', 'date_emission', 'date_echeance']
            titre = "Liste des cotisations"
            template_pdf = 'assureur/export_pdf_template.html'
            
        elif type_donnees == 'paiements':
            queryset = Paiement.objects.select_related('membre').all().order_by('-date_paiement')
            filename = f'paiements_{timezone.now().strftime("%Y%m%d_%H%M%S")}'
            fields = ['reference', 'membre__nom', 'membre__prenom', 'montant', 'mode_paiement', 'statut', 'date_paiement']
            titre = "Liste des paiements"
            template_pdf = 'assureur/export_pdf_template.html'
            
        elif type_donnees == 'soins':
            queryset = Soin.objects.select_related('membre').all().order_by('-date_soin')
            filename = f'soins_{timezone.now().strftime("%Y%m%d_%H%M%S")}'
            fields = ['code', 'membre__nom', 'membre__prenom', 'type_soin', 'montant_facture', 'montant_rembourse', 'statut', 'date_soin']
            titre = "Liste des soins"
            template_pdf = 'assureur/export_pdf_template.html'
            
        else:
            messages.error(request, "Type de données non supporté")
            return redirect('assureur:dashboard')
        
        # Préparer les données pour l'export
        data_rows = []
        for obj in queryset:
            row = {}
            for field in fields:
                if '__' in field:
                    parts = field.split('__')
                    value = obj
                    for part in parts:
                        if value:
                            value = getattr(value, part, '')
                        else:
                            value = ''
                    row[field] = str(value) if value is not None else ''
                else:
                    row[field] = str(getattr(obj, field, '')) if getattr(obj, field, None) is not None else ''
            data_rows.append(row)
        
        # Gérer l'export selon le format
        if export_format.lower() == 'pdf':
            return export_pdf(request, titre, fields, data_rows, filename, template_pdf)
        else:  # CSV par défaut
            return export_csv(fields, data_rows, filename)
            
    except Exception as e:
        messages.error(request, f"Erreur lors de l'export: {str(e)}")
        import traceback
        traceback.print_exc()
        return redirect('assureur:dashboard')

# ==========================================================================
# VUES POUR LA COMMUNICATION
# ==========================================================================

@login_required
@assureur_required
def messagerie_assureur(request):
    """Messagerie pour l'assureur"""
    try:
        # Essayer d'importer le modèle Message de l'application communication
        from communication.models import Message
        
        # Récupérer les messages
        messages_recus = Message.objects.filter(
            destinataire=request.user
        ).select_related('expediteur').order_by('-date_envoi')[:20]
        
        messages_envoyes = Message.objects.filter(
            expediteur=request.user
        ).select_related('destinataire').order_by('-date_envoi')[:20]
        
    except ImportError:
        # Si l'application communication n'existe pas
        messages_recus = []
        messages_envoyes = []
    
    context = {
        'assureur': get_assureur_from_request(request),
        'messages_recus': messages_recus,
        'messages_envoyes': messages_envoyes,
    }
    return render(request, 'assureur/communication/messagerie.html', context)

@login_required
@assureur_required
def envoyer_message_assureur(request):
    """Envoi de message depuis l'assureur"""
    if request.method == 'POST':
        try:
            from communication.models import Message
            from django.contrib.auth import get_user_model
            
            User = get_user_model()
            
            # Récupérer les données
            destinataire_id = request.POST.get('destinataire')
            objet = request.POST.get('objet', '')
            contenu = request.POST.get('contenu', '')
            
            if destinataire_id and contenu:
                destinataire = User.objects.get(id=destinataire_id)
                
                # Créer le message
                Message.objects.create(
                    expediteur=request.user,
                    destinataire=destinataire,
                    objet=objet,
                    contenu=contenu
                )
                
                messages.success(request, "Message envoyé avec succès")
                return redirect('assureur:messagerie_assureur')
            else:
                messages.error(request, "Veuillez remplir tous les champs obligatoires")
                
        except Exception as e:
            messages.error(request, f"Erreur lors de l'envoi du message: {str(e)}")
    
    # Pour GET: afficher le formulaire
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Liste des utilisateurs possibles
    destinataires_possibles = User.objects.exclude(id=request.user.id).order_by('username')
    
    context = {
        'assureur': get_assureur_from_request(request),
        'destinataires_possibles': destinataires_possibles,
    }
    return render(request, 'assureur/communication/envoyer_message.html', context)

# ==========================================================================
# VUES API POUR AJAX
# ==========================================================================



@login_required
@csrf_exempt
def api_recherche_membre(request):
    """API de recherche de membres (AJAX) - VERSION CORRIGÉE"""
    search = request.GET.get('q', '')
    
    if search:
        membres = Membre.objects.filter(
            Q(nom__icontains=search) |
            Q(prenom__icontains=search) |
            Q(numero_unique__icontains=search) |  # CORRIGÉ: numero_unique
            Q(email__icontains=search)
        ).values('id', 'nom', 'prenom', 'numero_unique', 'email')[:10]  # CORRIGÉ: numero_unique
        
        membres_list = list(membres)
    else:
        membres_list = []
    
    return JsonResponse({
        'success': True,
        'membres': membres_list
    })

@login_required
@csrf_exempt
def api_creer_bon(request, membre_id):
    """API pour créer un bon (AJAX)"""
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            membre = get_object_or_404(Membre, id=membre_id)
            
            bon = Bon.objects.create(
                membre=membre,
                type_soin=data.get('type_soin', 'consultation'),
                montant_total=float(data.get('montant_total', 0)),
                montant_prise_charge=float(data.get('montant_prise_charge', 0)),
                date_expiration=timezone.now().date() + timedelta(days=30),
                date_soin=timezone.now().date(),
                statut='en_attente',
                created_by=request.user
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Bon créé',
                'bon_id': bon.id,
                'numero_bon': bon.numero_bon
            })
        
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@require_GET
@csrf_exempt
def get_soins_par_membre(request, membre_id):
    """API pour récupérer les soins d'un membre"""
    try:
        membre = Membre.objects.get(id=membre_id)
        # Adaptez cette ligne selon vos relations
        soins = Soin.objects.filter(membre=membre)  # Ou la relation appropriée
        
        data = [{
            'id': soin.id,
            'code': getattr(soin, 'code', f'Soin #{soin.id}'),
            'montant_facture': getattr(soin, 'montant_facture', 0),
            'description': getattr(soin, 'description', ''),
        } for soin in soins]
        
        return JsonResponse(data, safe=False)
    except Membre.DoesNotExist:
        return JsonResponse([], safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@csrf_exempt
def api_valider_bon(request, bon_id):
    """API pour valider un bon (AJAX)"""
    try:
        bon = get_object_or_404(Bon, id=bon_id)
        
        if bon.statut == 'en_attente':
            bon.statut = 'valide'
            bon.valide_par = request.user
            bon.date_validation = timezone.now()
            bon.save()
            return JsonResponse({
                'success': True,
                'message': f'Bon {bon.numero_bon} validé'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': f'Impossible de valider le bon {bon.numero_bon}'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)



# ==========================================================================
# VUE DE TEST
# ==========================================================================

@login_required
def test_assureur(request):
    """Vue de test pour vérifier l'accès et les permissions"""
    assureur = get_assureur_from_request(request)
    
    return HttpResponse(f"""
    <h1>Test Assureur</h1>
    <p>Utilisateur: {request.user.username}</p>
    <p>Est assureur: {is_assureur(request.user)}</p>
    <p>Assureur dans contexte: {'OUI' if assureur else 'NON'}</p>
    <p>Assureur nom: {assureur.nom if assureur else 'N/A'}</p>
    <p>Assureur email: {assureur.email if assureur else 'N/A'}</p>
    <hr>
    <h2>Navigation</h2>
    <ul>
        <li><a href="/assureur/">Dashboard</a></li>
        <li><a href="/assureur/membres/">Membres</a></li>
        <li><a href="/assureur/bons/">Bons</a></li>
        <li><a href="/assureur/soins/">Soins</a></li>
        <li><a href="/assureur/paiements/">Paiements</a></li>
        <li><a href="/assureur/cotisations/">Cotisations</a></li>
        <li><a href="/assureur/statistiques/">Statistiques</a></li>
        <li><a href="/admin/">Admin Django</a></li>
    </ul>
    """)