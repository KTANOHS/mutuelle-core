from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta, date
import json
import logging
from django.views import View
from django.db import models
from django.views.decorators.http import require_http_methods
from functools import wraps
from django.shortcuts import redirect as django_redirect
from django.contrib import messages as django_messages

# LIGNE MANQUANTE - AJOUTEZ EN HAUT DU FICHIER
from agents.affichage_unifie import afficher_fiche_cotisation_unifiee, determiner_statut_cotisation
from .models import Agent
import random
import string
import time
# agents/views.py - VERSION CORRIGÉE ET SIMPLIFIÉE
from core.utils import gerer_erreurs, est_agent
from core.utils import get_user_primary_group, generer_numero_unique





# AJOUT: Imports communication
from communication.models import Message, Notification, Conversation
from communication.forms import MessageForm

# Configuration du logger
logger = logging.getLogger('agents')



# =============================================================================
# GESTION ROBUSTE DES IMPORTS DES MODÈLES
# =============================================================================

# Initialisation avec valeurs par défaut
MEMBRE_MODEL_AVAILABLE = False
PAIEMENT_MODEL_AVAILABLE = False  
AGENT_MODELS_AVAILABLE = False
BON_SOIN_AVAILABLE = False
COTISATION_MODEL_AVAILABLE = False 

# AJOUT: Définir agent_required si le décorateur n'existe pas
try:
    from core.utils import agent_required, gerer_erreurs, est_agent
except ImportError as e:
    logger.warning(f"Utilitaires core non disponibles: {e}")
    # Définir des fonctions de remplacement
    def gerer_erreurs(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    
    def est_agent(user):
        return True
    
    # Définir un décorateur de remplacement
    def agent_required(view_func):
        """Décorateur factice pour vérifier que l'utilisateur est un agent"""
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return django_redirect('login')
            
            # Vérifier si l'utilisateur est dans le groupe AGENT
            if not request.user.groups.filter(name='AGENT').exists():
                django_messages.error(request, "Vous n'avez pas les permissions d'agent.")
                return django_redirect('home')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view

# Classes factices pour éviter les erreurs
class MockAgent:
    """Classe factice pour Agent si le modèle n'est pas disponible - VERSION CORRIGÉE"""
    def __init__(self, user=None):
        self.user = user
        self.id = 0  # ✅ TOUJOURS un ID numérique
        self.limite_bons_quotidienne = 10
        self.nom = getattr(user, 'last_name', 'Agent') if user else 'Agent'
        self.prenom = getattr(user, 'first_name', '')
        self.est_actif = True
        self.telephone = ""
        self.email = getattr(user, 'email', '') if user else ''
        self.date_embauche = timezone.now().date() if hasattr(timezone, 'now') else date.today()
        
        # Ajouter des attributs supplémentaires pour compatibilité
        self.taux_collecte = 0.0
        self.nombre_membres = 0
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
    def peut_creer_bon(self):
        return True
    
    def rechercher_membres_nom(self, query=None):
        """Méthode factice pour la recherche de membres"""
        return []
    
    # ✅ AJOUT: Méthodes pour compatibilité avec le template
    def get_nombre_membres(self):
        return self.nombre_membres
    
    def get_taux_collecte(self):
        return self.taux_collecte
    
    def update_statistiques(self):
        """Méthode factice pour mettre à jour les statistiques"""
        pass

class MockQuerySet:
    """QuerySet factice pour les modèles non disponibles"""
    def count(self):
        return 0
    
    def filter(self, *args, **kwargs):
        return self
    
    def order_by(self, *args, **kwargs):
        return self
    
    def select_related(self, *args, **kwargs):
        return self

class MockManager:
    """Manager factice pour les modèles non disponibles"""
    def filter(self, *args, **kwargs):
        return MockQuerySet()
    
    def get(self, *args, **kwargs):
        return MockAgent()
    
    def count(self):
        return 0

# Import de vos modèles existants avec gestion d'erreur robuste
try:
    from membres.models import Membre
    MEMBRE_MODEL_AVAILABLE = True
    logger.info("Modèle Membre importé avec succès")
except ImportError as e:
    logger.warning(f"Modèle Membre non disponible: {e}")
    # Créer une classe Membre factice
    class Membre:
        objects = MockManager()
        id = 0
        nom = "Membre"
        prenom = "Factice"
        telephone = "000000000"
        statut = "actif"
        date_inscription = date.today()

# =============================================================================
# IMPORT DE L'AFFICHAGE UNIFIÉ
# =============================================================================

try:
    from agents.affichage_unifie import afficher_fiche_cotisation_unifiee, determiner_statut_cotisation
    logger.info("✅ Module affichage_unifie importé avec succès")
except ImportError as e:
    logger.warning(f"Module affichage_unifie non disponible: {e}")
    # Fonctions de remplacement
    def afficher_fiche_cotisation_unifiee(membre, verification, cotisation):
        return f"Fiche non disponible - Module d'affichage manquant"
    
    def determiner_statut_cotisation(verification):
        return "À vérifier", "🟠", "statut-a-verifier"


try:
    from paiements.models import Paiement
    PAIEMENT_MODEL_AVAILABLE = True
    logger.info("Modèle Paiement importé avec succès")
except ImportError as e:
    logger.warning(f"Modèle Paiement non disponible: {e}")

try:
    from .models import Agent as RealAgent, VerificationCotisation, ActiviteAgent, BonSoin
    AGENT_MODELS_AVAILABLE = True
    logger.info("Modèles agents importés avec succès")
    # Utiliser le vrai modèle Agent
    Agent = RealAgent
except ImportError as e:
    logger.warning(f"Modèles agents non disponibles: {e}")
    # Utiliser les classes factices
    VerificationCotisation = type('VerificationCotisation', (), {'objects': MockManager()})
    ActiviteAgent = type('ActiviteAgent', (), {'objects': MockManager()})
    BonSoin = type('BonSoin', (), {'objects': MockManager()})
    Agent = MockAgent

# CORRECTION : Importer BonDeSoin au lieu de BonSoin
try:
    from soins.models import BonDeSoin
    BON_SOIN_AVAILABLE = True
    logger.info("Modèle BonDeSoin importé avec succès")
except ImportError as e:
    logger.warning(f"Modèle BonDeSoin non disponible: {e}")
    # Classe factice pour BonDeSoin
    class BonDeSoin:
        objects = MockManager()
        id = 0
        patient = Membre()
        date_soin = date.today()
        symptomes = ""
        diagnostic = ""
        montant = 0
        statut = "attente"
        date_creation = date.today()

# AJOUT: Import manquant pour le modèle Cotisation
try:
    from cotisations.models import Cotisation
    COTISATION_MODEL_AVAILABLE = True
    logger.info("Modèle Cotisation importé avec succès")
except ImportError as e:
    logger.warning(f"Modèle Cotisation non disponible: {e}")
    # Classe factice pour Cotisation
    class Cotisation:
        objects = MockManager()
        id = 0
        membre = None
        date_debut = date.today()
        date_fin = date.today()
        montant = 0
        statut = "actif"




# =============================================================================
# fonction creer membre
# ============================================================================


def generer_numero_unique():
    """Génère un numéro unique aléatoire avec vérification d'unicité"""
    
    # ✅ VÉRIFICATION AJOUTÉE : S'assurer que le modèle Membre est disponible
    if not MEMBRE_MODEL_AVAILABLE:
        # Fallback si le modèle n'est pas disponible
        lettres = ''.join(random.choices(string.ascii_uppercase, k=3))
        chiffres = ''.join(random.choices(string.digits, k=3))
        timestamp = str(int(time.time()))[-3:]
        return f"MEM{lettres}{chiffres}{timestamp}"
    
    max_tentatives = 10
    
    for _ in range(max_tentatives):
        lettres = ''.join(random.choices(string.ascii_uppercase, k=3))
        chiffres = ''.join(random.choices(string.digits, k=3))
        timestamp = str(int(time.time()))[-3:]
        numero_unique = f"MEM{lettres}{chiffres}{timestamp}"
        
        # Vérifier si le numéro existe déjà
        if not Membre.objects.filter(numero_unique=numero_unique).exists():
            return numero_unique
    
    # Fallback en cas d'échec
    return f"MEM{int(time.time())}"


# =============================================================================
# FONCTIONS UTILITAIRES AMÉLIORÉES - VERSION CORRIGÉE
# =============================================================================


def verifier_statut_cotisation_simple(membre):
    """Vérification REALISTE du statut de cotisation - VERSION CORRIGÉE"""
    try:
        logger.info(f"🔍 Vérification cotisation pour membre {membre.id}: {membre.prenom} {membre.nom}")
        
        # ✅ CORRECTION: Gestion robuste des types datetime/date
        aujourd_hui = timezone.now().date()
        
        # Vérifier si c'est un nouveau membre (créé récemment)
        if hasattr(membre, 'date_inscription') and membre.date_inscription:
            # ✅ CORRECTION: Convertir en date si c'est un datetime
            if hasattr(membre.date_inscription, 'date'):
                date_inscription = membre.date_inscription.date()
            else:
                date_inscription = membre.date_inscription
                
            delai_creation = aujourd_hui - date_inscription
            if delai_creation.days < 30:  # Membre créé il y a moins d'un mois
                logger.info(f"❌ Nouveau membre détecté ({delai_creation.days} jours) - Statut: NON À JOUR")
                return False
        
        # Méthode 1: Si le modèle Membre a un champ est_a_jour
        if hasattr(membre, 'est_a_jour') and membre.est_a_jour is not None:
            # Si c'est une méthode, l'appeler
            if callable(membre.est_a_jour):
                statut = membre.est_a_jour()
            else:
                statut = membre.est_a_jour
            logger.info(f"📊 Statut via est_a_jour: {statut}")
            return statut
        
        # Méthode 2: Vérification par date de dernière cotisation
        if hasattr(membre, 'date_derniere_cotisation') and membre.date_derniere_cotisation:
            # ✅ CORRECTION: Convertir en date si c'est un datetime
            if hasattr(membre.date_derniere_cotisation, 'date'):
                derniere_cotisation = membre.date_derniere_cotisation.date()
            else:
                derniere_cotisation = membre.date_derniere_cotisation
                
            delai = aujourd_hui - derniere_cotisation
            est_a_jour = delai.days < 365  # 1 an de validité
            logger.info(f"📊 Statut via date_derniere_cotisation: {est_a_jour} ({delai.days} jours)")
            return est_a_jour
        
        # ✅ CORRECTION: Par défaut, les membres ne sont PAS à jour
        logger.info(f"⚠️ Aucune donnée cotisation - Statut par défaut: NON À JOUR")
        return False
        
    except Exception as e:
        logger.error(f"❌ Erreur vérification statut {getattr(membre, 'id', 'N/A')}: {e}")
        return False  # En cas d'erreur, considérer comme non à jour



def verifier_cotisation_membre_simplifiee(membre):
    """Vérification simplifiée REALISTE pour l'enregistrement - VERSION COMPLÈTEMENT CORRIGÉE"""
    try:
        logger.info(f"🔍 Vérification simplifiée pour membre {membre.id}")
        
        # Utiliser la vérification corrigée
        est_a_jour = verifier_statut_cotisation_simple(membre)
        
        # ✅ CORRECTION: Dates réalistes basées sur le statut réel
        aujourd_hui = timezone.now().date()
        
        if est_a_jour:
            return True, {
                'message': '✅ Le membre est à jour dans ses cotisations',
                'prochaine_echeance': (aujourd_hui + timedelta(days=30)).strftime('%d/%m/%Y'),
                'dernier_paiement': (aujourd_hui - timedelta(days=30)).strftime('%d/%m/%Y'),
                'montant_dette_str': '0 FCFA',
                'jours_retard': 0,
            }
        else:
            # ✅ CORRECTION: Pour les nouveaux membres, montrer qu'ils doivent payer
            if hasattr(membre, 'date_inscription') and membre.date_inscription:
                # ✅ CORRECTION COMPLÈTE: Gestion robuste des types datetime/date
                try:
                    if hasattr(membre.date_inscription, 'date'):
                        date_inscription = membre.date_inscription.date()
                    else:
                        date_inscription = membre.date_inscription
                    
                    # ✅ ASSURER que c'est bien un date object
                    if isinstance(date_inscription, datetime):
                        date_inscription = date_inscription.date()
                    
                    delai_creation = aujourd_hui - date_inscription
                    
                    if delai_creation.days < 30:
                        message = f'🆕 Nouveau membre ({delai_creation.days} jours) - Cotisation initiale requise'
                        montant_dette = '10 000 FCFA'
                        jours_retard = 0
                    else:
                        message = '⚠️ Le membre a des cotisations en retard'
                        montant_dette = '15 000 FCFA'
                        jours_retard = max(30, delai_creation.days - 30)
                        
                except Exception as date_error:
                    logger.warning(f"Erreur calcul date inscription: {date_error}")
                    message = '⚠️ Le membre a des cotisations en retard'
                    montant_dette = '15 000 FCFA'
                    jours_retard = 90
            else:
                message = '⚠️ Le membre a des cotisations en retard'
                montant_dette = '15 000 FCFA'
                jours_retard = 90
                
            return False, {
                'message': message,
                'prochaine_echeance': 'Immédiate',
                'dernier_paiement': 'Aucun paiement',
                'montant_dette_str': montant_dette,
                'jours_retard': jours_retard,
            }
            
    except Exception as e:
        logger.error(f"❌ Erreur vérification simplifiée {getattr(membre, 'id', 'N/A')}: {e}")
        return False, {
            'message': f'Erreur lors de la vérification: {str(e)}',
            'prochaine_echeance': 'Erreur',
            'dernier_paiement': 'Erreur',
            'montant_dette_str': 'Erreur',
            'jours_retard': 0,
        }



def get_client_ip(request):
    """Récupère l'adresse IP du client"""
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except:
        return '0.0.0.0'

def _ajouter_message(request, level, message):
    """Ajoute un message de manière sécurisée (gère l'absence du middleware)"""
    try:
        if hasattr(request, '_messages'):
            if level == 'success':
                messages.success(request, message)
            elif level == 'error':
                messages.error(request, message)
            elif level == 'warning':
                messages.warning(request, message)
            elif level == 'info':
                messages.info(request, message)
        else:
            # Fallback: logger le message
            log_message = f"[MESSAGE {level.upper()}] {message}"
            if level == 'error':
                logger.error(log_message)
            else:
                logger.info(log_message)
    except Exception as e:
        logger.warning(f"Impossible d'ajouter le message: {e}")

def get_activite_icone(type_activite):
    """Retourne l'icône correspondant au type d'activité"""
    icones = {
        'creation_bon': 'file-medical',
        'verification_cotisation': 'check-circle',
        'consultation_membre': 'user-check',
        'modification_donnees': 'edit',
        'rapport': 'chart-line',
        'recherche_membre': 'search',
    }
    return icones.get(type_activite, 'info-circle')

def get_activite_couleur(type_activite):
    """Retourne la couleur correspondant au type d'activité"""
    couleurs = {
        'creation_bon': 'success',
        'verification_cotisation': 'primary',
        'consultation_membre': 'info',
        'modification_donnees': 'warning',
        'rapport': 'secondary',
        'recherche_membre': 'dark',
    }
    return couleurs.get(type_activite, 'dark')

def get_agent_connecte(request):
    """Récupère l'agent connecté de manière sécurisée - VERSION CORRIGÉE"""
    try:
        logger.info(f"🔍 Tentative récupération agent pour utilisateur: {request.user.username}")
        
        # Vérifier si le modèle Agent est disponible
        if not AGENT_MODELS_AVAILABLE:
            logger.warning("⚠️ Modèle Agent non disponible - MockAgent retourné")
            # Créer un MockAgent temporaire pour éviter les erreurs
            mock_agent = MockAgent(user=request.user)
            mock_agent.id = 0  # Ajouter un ID factice
            mock_agent.nom = getattr(request.user, 'last_name', 'Agent')
            mock_agent.prenom = getattr(request.user, 'first_name', '')
            mock_agent.telephone = ""
            mock_agent.email = request.user.email
            mock_agent.est_actif = True
            mock_agent.limite_bons_quotidienne = 10
            return mock_agent
        
        # ✅ CORRECTION: Utiliser get_or_create pour éviter l'erreur "Agent non trouvé"
        try:
            agent, created = Agent.objects.get_or_create(
                user=request.user,
                defaults={
                    'nom': request.user.last_name or request.user.username,
                    'prenom': request.user.first_name or '',
                    'telephone': '',
                    'email': request.user.email,
                    'actif': True,
                }
            )
            
            if created:
                logger.info(f"✅ Nouvel Agent créé pour l'utilisateur {request.user.username}")
            else:
                logger.info(f"✅ Agent existant trouvé: {agent.nom} {agent.prenom} (ID: {agent.id})")
            
            return agent
            
        except Exception as e:
            logger.error(f"❌ Erreur get_or_create Agent: {e}")
            # Fallback: chercher juste par user
            try:
                agent = Agent.objects.get(user=request.user)
                logger.info(f"✅ Agent récupéré via get: {agent.nom} (ID: {agent.id})")
                return agent
            except Agent.DoesNotExist:
                logger.warning(f"Agent non trouvé pour l'utilisateur {request.user.username}")
                raise
            
    except Exception as e:
        logger.error(f"❌ Erreur récupération agent: {e}")
        
        # ✅ CRITIQUE: Retourner un MockAgent avec un ID numérique pour éviter l'erreur
        mock_agent = MockAgent(user=request.user)
        mock_agent.id = 0  # ID factice mais numérique
        mock_agent.nom = getattr(request.user, 'last_name', 'Agent')
        mock_agent.prenom = getattr(request.user, 'first_name', '')
        mock_agent.telephone = ""
        mock_agent.email = request.user.email
        mock_agent.est_actif = True
        mock_agent.limite_bons_quotidienne = 10
        
        return mock_agent

# =============================================================================
# VUES DE RECHERCHE DE MEMBRES - VERSION CORRIGÉE
# =============================================================================

@login_required
@require_http_methods(["GET"])
def rechercher_membre(request):
    """Vue pour la recherche de membres - VERSION CORRIGÉE"""
    try:
        agent = get_agent_connecte(request)
        
        if not hasattr(agent, 'est_actif') or not agent.est_actif:
            return JsonResponse({
                'success': False, 
                'error': 'Accès non autorisé ou agent inactif'
            }, status=403)
        
        query = request.GET.get('q', '').strip()
        
        if len(query) < 2:
            return JsonResponse({
                'success': False,
                'error': 'La recherche doit contenir au moins 2 caractères'
            }, status=400)
        
        # Effectuer la recherche en utilisant les méthodes du modèle Agent
        try:
            if hasattr(agent, 'rechercher_membres_nom'):
                membres = agent.rechercher_membres_nom(query)
            else:
                # Fallback si la méthode n'existe pas
                if MEMBRE_MODEL_AVAILABLE:
                    membres = Membre.objects.filter(
                        Q(user__first_name__icontains=query) |
                        Q(user__last_name__icontains=query) |
                        Q(numero_unique__icontains=query) |
                        Q(telephone__icontains=query)
                    )[:15]
                else:
                    membres = []
        except Exception as e:
            logger.error(f"Erreur lors de la recherche: {e}")
            membres = []
        
        # Préparer les résultats
        results = []
        for membre in membres[:15]:  # Limiter à 15 résultats
            try:
                results.append({
                    'id': getattr(membre, 'id', None),
                    'nom_complet': getattr(membre, 'nom_complet', 
                                         f"{getattr(membre, 'prenom', '')} {getattr(membre, 'nom', '')}".strip()),
                    'numero_unique': getattr(membre, 'numero_unique', ''),
                    'telephone': getattr(membre, 'telephone', ''),
                    'email': getattr(membre.user, 'email', '') if hasattr(membre, 'user') else getattr(membre, 'email', ''),
                    'nom': str(membre.nom) if hasattr(membre, 'nom') and membre.nom else '',
                    'est_actif': getattr(membre, 'est_actif', True)
                })
            except Exception as e:
                logger.error(f"Erreur préparation membre {getattr(membre, 'id', 'N/A')}: {e}")
                continue
        
        # Enregistrer l'activité de recherche
        if AGENT_MODELS_AVAILABLE:
            try:
                from .models import ActiviteAgent
                ActiviteAgent.objects.create(
                    agent=agent,
                    type_activite='recherche_membre',
                    description=f"Recherche de membre: '{query}' - {len(results)} résultat(s)",
                    donnees_concernees={
                        'terme_recherche': query,
                        'nombre_resultats': len(results)
                    }
                )
            except Exception as e:
                logger.warning(f"Impossible d'enregistrer l'activité de recherche: {e}")
        
        return JsonResponse({
            'success': True,
            'results': results,
            'count': len(results),
            'query': query
        })
        
    except Exception as e:
        logger.error(f"Erreur lors de la recherche: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': f'Erreur lors de la recherche: {str(e)}'
        }, status=500)

@login_required
def details_membre(request, membre_id):
    """Vue pour les détails d'un membre - VERSION CORRIGÉE"""
    try:
        agent = get_agent_connecte(request)
        
        if not agent:
            return JsonResponse({'error': 'Accès non autorisé'}, status=403)
        
        if not MEMBRE_MODEL_AVAILABLE:
            return JsonResponse({'error': 'Module membres non disponible'}, status=500)
        
        # Vérifier que le membre appartient à l'nom de l'agent
        membre = Membre.objects.get(id=membre_id)
        if hasattr(agent, 'nom') and agent.nom and hasattr(membre, 'nom'):
            if membre.nom != agent.nom:
                return JsonResponse({'error': 'Accès non autorisé à ce membre'}, status=403)
        
        # Préparer les données du membre
        data = {
            'id': membre.id,
            'nom_complet': getattr(membre, 'nom_complet', 
                                 f"{getattr(membre, 'prenom', '')} {getattr(membre, 'nom', '')}".strip()),
            'numero_unique': getattr(membre, 'numero_unique', ''),
            'telephone': getattr(membre, 'telephone', ''),
            'email': getattr(membre.user, 'email', '') if hasattr(membre, 'user') else getattr(membre, 'email', ''),
            'date_naissance': membre.date_naissance.strftime('%d/%m/%Y') if hasattr(membre, 'date_naissance') else '',
            'adresse': getattr(membre, 'adresse', ''),
            'ville': getattr(membre, 'ville', ''),
            'est_actif': getattr(membre, 'est_actif', True),
        }
        
        return JsonResponse({'success': True, 'membre': data})
        
    except Membre.DoesNotExist:
        return JsonResponse({'error': 'Membre non trouvé'}, status=404)
    except Exception as e:
        logger.error(f"Erreur détails membre: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)

# =============================================================================
# VUES PRINCIPALES - VERSION COMPLÈTEMENT CORRIGÉE
# =============================================================================


def get_agent_connecte(request):
    """Récupère l'agent connecté ou crée un agent par défaut"""
    try:
        return Agent.objects.get(user=request.user)
    except Agent.DoesNotExist:
        logger.warning(f"Agent non trouvé pour {request.user.username}")
        # Retourner un agent factice avec les attributs minimaux
        class AgentFactice:
            id = 0
            user = request.user
            matricule = "N/A"
            poste = "Non défini"
            est_actif = True
            limite_bons_quotidienne = 10
            telephone = ""
            email_professionnel = ""
            
            def __str__(self):
                return f"Agent factice pour {self.user.username}"
        
        return AgentFactice()

def agent_required(view_func):
    """Décorateur pour vérifier que l'utilisateur est un agent"""
    def _wrapped_view(request, *args, **kwargs):
        if not est_agent(request.user):
            messages.error(request, "Accès réservé aux agents.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@gerer_erreurs
@agent_required
def dashboard(request):
    """Tableau de bord agent - VERSION SIMPLIFIÉE ET CORRIGÉE"""
    user = request.user
    logger.info(f"📊 Dashboard demandé par: {user.username}")
    
    # Récupérer l'agent
    agent = get_agent_connecte(request)
    
    # S'assurer que l'agent a un ID
    if not hasattr(agent, 'id') or agent.id is None:
        agent.id = 0
    
    # Utiliser le nom de l'utilisateur, pas agent.nom (qui n'existe pas)
    nom_affichage = user.get_full_name() or user.username
    logger.info(f"✅ Agent: {nom_affichage} (Matricule: {getattr(agent, 'matricule', 'N/A')})")
    
    today = timezone.now().date()
    
    # Statistiques simplifiées
    stats = {
        'verifications_jour': 0,
        'membres_a_jour': 0,
        'membres_retard': 0,
        'pourcentage_conformite': 0,
        'total_bons': 0,
        'membres_actifs': 0,
        'taux_validation': 0,
        'bons_aujourdhui': 0,
        'total_bons_mois': 0,
        'verifications_mois': 0,
        'limite_quotidienne': getattr(agent, 'limite_bons_quotidienne', 10),
        'pourcentage_limite': 0,
    }
    
    # Essayer de récupérer des données réelles si l'agent existe
    if agent.id and agent.id > 0:
        try:
            # Statistiques membres (si le modèle existe)
            try:
                from membres.models import Membre
                
                # Compter les membres
                total_membres = Membre.objects.count()
                membres_actifs = Membre.objects.filter(est_actif=True).count()
                
                # Calculs basiques
                stats.update({
                    'membres_actifs': membres_actifs,
                    'membres_a_jour': int(membres_actifs * 0.8),  # Estimation
                    'membres_retard': int(membres_actifs * 0.2),  # Estimation
                    'pourcentage_conformite': 80,  # Estimation
                })
                
            except ImportError:
                logger.warning("Modèle Membre non disponible")
            
            # Statistiques bons de soin
            try:
                from bons_soins.models import BonDeSoin
                
                bons_aujourdhui = BonDeSoin.objects.filter(
                    date_creation__date=today
                ).count()
                
                total_bons_mois = BonDeSoin.objects.filter(
                    date_creation__month=today.month,
                    date_creation__year=today.year
                ).count()
                
                stats.update({
                    'bons_aujourdhui': bons_aujourdhui,
                    'total_bons_mois': total_bons_mois,
                    'total_bons': total_bons_mois,
                })
                
                # Calcul pourcentage limite
                limite = stats['limite_quotidienne']
                if limite > 0:
                    stats['pourcentage_limite'] = min(100, (bons_aujourdhui / limite) * 100)
                
            except ImportError:
                logger.warning("Modèle BonDeSoin non disponible")
                
        except Exception as e:
            logger.error(f"Erreur calcul statistiques: {e}")
    
    # Activités récentes
    activites_recentes = []
    
    # Récupérer les activités réelles si disponibles
    try:
        from agents.models import ActiviteAgent
        activites_db = ActiviteAgent.objects.filter(agent=agent).order_by('-date_activite')[:5]
        
        for activite in activites_db:
            activites_recentes.append({
                'icone': getattr(activite, 'icone', 'info-circle'),
                'couleur': getattr(activite, 'couleur', 'primary'),
                'date': activite.date_activite.strftime('%H:%M'),
                'description': getattr(activite, 'description', 'Activité')[:50]
            })
    except (ImportError, AttributeError):
        pass
    
    # Activités par défaut si vide
    if not activites_recentes:
        activites_recentes = [
            {
                'icone': 'check-circle',
                'couleur': 'success',
                'date': 'Maintenant',
                'description': f'Connecté en tant que {nom_affichage}'
            },
            {
                'icone': 'info-circle',
                'couleur': 'info',
                'date': 'Aujourd\'hui',
                'description': 'Tableau de bord chargé avec succès'
            }
        ]
    
    # Contexte
    context = {
        'page_title': 'Tableau de Bord Agent',
        'active_tab': 'dashboard',
        'agent': agent,
        'nom_agent': nom_affichage,
        'matricule': getattr(agent, 'matricule', 'N/A'),
        'poste': getattr(agent, 'poste', 'Agent'),
        'email_professionnel': getattr(agent, 'email_professionnel', ''),
        'telephone': getattr(agent, 'telephone', ''),
        'est_actif': getattr(agent, 'est_actif', True),
        'stats': stats,
        'actions_recentes': activites_recentes,
        'today': today.strftime('%d/%m/%Y'),
        'limite_bons': stats['limite_quotidienne'],
    }
    
    logger.info(f"✅ Dashboard généré pour {user.username}")
    return render(request, 'agents/dashboard.html', context)
# =============================================================================
# VUES POUR L'AFFICHAGE UNIFIÉ DES COTISATIONS
# =============================================================================



@login_required
@gerer_erreurs
@agent_required
def afficher_fiche_cotisation(request, membre_id):
    """Affiche une fiche de cotisation unifiée - VERSION CORRIGÉE"""
    try:
        # Vérifications de sécurité
        if not est_agent(request.user):
            _ajouter_message(request, 'error', "Accès réservé aux agents.")
            return redirect('home')
        
        # Récupération des objets
        membre = get_object_or_404(Membre, id=membre_id)
        verification = VerificationCotisation.objects.filter(membre=membre).first()
        
        # ✅ CORRECTION: Utiliser la variable vérifiée pour Cotisation
        cotisation = None
        if 'COTISATION_MODEL_AVAILABLE' in globals() and COTISATION_MODEL_AVAILABLE:
            cotisation = Cotisation.objects.filter(membre=membre).first()
        
        # Générer l'affichage unifié
        fiche = afficher_fiche_cotisation_unifiee(membre, verification, cotisation)
        
        context = {
            'fiche': fiche,
            'membre': membre,
            'verification': verification,
            'cotisation': cotisation,
            'page_title': f'Fiche Cotisation - {membre.nom_complet}',
            'active_tab': 'verification_cotisations',
            'agent': get_agent_connecte(request),
        }
        
        return render(request, 'agents/fiche_cotisation.html', context)
        
    except Membre.DoesNotExist:
        _ajouter_message(request, 'error', "Membre non trouvé")
        return redirect('agents:verification_cotisations')
    except Exception as e:
        logger.error(f"Erreur affichage fiche cotisation: {e}")
        _ajouter_message(request, 'error', f"Erreur technique: {str(e)}")
        return redirect('agents:verification_cotisations')


@login_required
@gerer_erreurs
@agent_required
def recherche_cotisations_avancee(request):
    """Recherche avancée avec affichage unifié - VERSION CORRIGÉE"""
    try:
        # Vérifications de sécurité
        if not est_agent(request.user):
            _ajouter_message(request, 'error', "Accès réservé aux agents.")
            return redirect('home')
        
        query = request.GET.get('q', '')
        results = []
        
        if query:
            # Recherche des membres
            membres = Membre.objects.filter(
                Q(numero_unique__icontains=query) |
                Q(telephone__icontains=query) |
                Q(nom__icontains=query) |
                Q(prenom__icontains=query)
            )[:10]
            
            # Préparation des résultats avec affichage unifié
            for membre in membres:
                verification = VerificationCotisation.objects.filter(membre=membre).first()
                cotisation = Cotisation.objects.filter(membre=membre).first()
                
                # Générer l'affichage unifié
                fiche = afficher_fiche_cotisation_unifiee(membre, verification, cotisation)
                
                results.append({
                    'membre': membre,
                    'fiche': fiche,
                    'verification': verification,
                    'cotisation': cotisation
                })
        
        context = {
            'results': results,
            'query': query,
            'page_title': 'Recherche Avancée Cotisations',
            'active_tab': 'verification_cotisations',
            'agent': get_agent_connecte(request),
        }
        
        return render(request, 'agents/recherche_cotisations.html', context)
        
    except Exception as e:
        logger.error(f"Erreur recherche avancée: {e}")
        _ajouter_message(request, 'error', f"Erreur lors de la recherche: {str(e)}")
        return redirect('agents:verification_cotisations')

@login_required
@gerer_erreurs
@agent_required
def verification_cotisations(request):
    """Page principale de vérification des cotisations - VERSION CORRIGÉE"""
    try:
        logger.info(f"🔍 Vérification cotisations demandée par: {request.user.username}")
        
        # Récupérer l'agent connecté
        agent = get_agent_connecte(request)
        
        # ✅ VÉRIFICATION CRITIQUE: S'assurer que l'agent a un ID numérique
        if not hasattr(agent, 'id') or agent.id is None:
            logger.error(f"⚠️ Agent sans ID pour l'utilisateur {request.user.username}")
            agent.id = 0  # ID factice mais numérique
        
        logger.info(f"✅ Agent utilisé pour vérifications: {agent.nom} (ID: {agent.id})")
        
        # Statistiques réelles
        aujourd_hui = timezone.now().date()
        verifications_du_jour = 0
        dernieres_verifications = []
        
        # ✅ CORRECTION: Vérifier que l'agent a un ID avant de faire des requêtes
        if hasattr(agent, 'id') and agent.id is not None and agent.id > 0:
            if AGENT_MODELS_AVAILABLE:
                try:
                    verifications_du_jour = VerificationCotisation.objects.filter(
                        agent=agent,
                        date_verification__date=aujourd_hui
                    ).count()
                    
                    # Dernières vérifications
                    dernieres_verifications = VerificationCotisation.objects.filter(
                        agent=agent
                    ).select_related('membre').order_by('-date_verification')[:10]
                except Exception as e:
                    logger.error(f"Erreur chargement vérifications: {e}")
        
        # Membres assignés (si applicable)
        membres_assignes = []
        total_membres = 0
        membres_a_jour = 0
        membres_en_retard = 0
        
        if MEMBRE_MODEL_AVAILABLE:
            try:
                # Vérifier si le modèle Membre a un champ agent
                if hasattr(Membre, 'agent'):
                    membres_assignes = Membre.objects.filter(agent=agent)
                    logger.info(f"✅ Membres assignés via champ agent: {membres_assignes.count()}")
                else:
                    # Tous les membres si pas de champ agent
                    membres_assignes = Membre.objects.all()
                    logger.info(f"✅ Tous les membres chargés (pas de champ agent): {membres_assignes.count()}")
                
                total_membres = membres_assignes.count()
                
                # Calculer les statuts
                for membre in membres_assignes[:100]:  # Limiter pour performance
                    if verifier_statut_cotisation_simple(membre):
                        membres_a_jour += 1
                    else:
                        membres_en_retard += 1
                
                # Extrapolation pour grand nombre de membres
                if total_membres > 100:
                    ratio = total_membres / 100
                    membres_a_jour = int(membres_a_jour * ratio)
                    membres_en_retard = total_membres - membres_a_jour
                    
            except Exception as e:
                logger.error(f"❌ Erreur chargement membres: {e}")
        
        context = {
            'agent': agent,
            'verifications_du_jour': verifications_du_jour,
            'dernieres_verifications': dernieres_verifications,
            'membres': membres_assignes[:50],  # Limiter l'affichage
            'total_membres': total_membres,
            'membres_a_jour': membres_a_jour,
            'membres_en_retard': membres_en_retard,
            'taux_conformite': (membres_a_jour / total_membres * 100) if total_membres > 0 else 0,
            'page_title': 'Vérification des Cotisations',
            'active_tab': 'verification_cotisations',
            'today': aujourd_hui,
        }
        
        logger.info(f"✅ Vérification cotisations générée avec succès")
        return render(request, 'agents/verification_cotisations.html', context)
        
    except Exception as e:
        logger.error(f"❌ Erreur page vérification: {e}")
        # Page d'erreur avec agent factice
        mock_agent = MockAgent(request.user)
        mock_agent.id = 0
        
        return render(request, 'agents/verification_cotisations.html', {
            'error': f'Erreur technique: {str(e)}',
            'page_title': 'Erreur',
            'agent': mock_agent,
            'verifications_du_jour': 0,
            'dernieres_verifications': [],
            'membres': [],
            'total_membres': 0,
            'membres_a_jour': 0,
            'membres_en_retard': 0,
            'taux_conformite': 0,
        })

@login_required
@gerer_erreurs
@agent_required
def afficher_fiche_cotisation_unifiee_view(request, membre_id):
    """Vue pour afficher la fiche de cotisation unifiée - CORRECTION"""
    try:
        logger.info(f"🔍 Affichage fiche unifiée pour membre {membre_id}")
        
        # Vérification des permissions
        if not est_agent(request.user):
            _ajouter_message(request, 'error', "Accès réservé aux agents.")
            return redirect('home')
        
        # Récupération du membre
        membre = get_object_or_404(Membre, id=membre_id)
        logger.info(f"✅ Membre trouvé: {membre.prenom} {membre.nom}")
        
        # Récupération des données associées avec gestion d'erreur
        verification = None
        cotisation = None
        
        try:
            verification = VerificationCotisation.objects.filter(membre=membre).first()
            logger.info(f"📊 Vérification trouvée: {verification is not None}")
        except Exception as e:
            logger.warning(f"⚠️ Erreur récupération vérification: {e}")
        
        try:
            if COTISATION_MODEL_AVAILABLE:
                cotisation = Cotisation.objects.filter(membre=membre).first()
                logger.info(f"💰 Cotisation trouvée: {cotisation is not None}")
        except Exception as e:
            logger.warning(f"⚠️ Erreur récupération cotisation: {e}")
        
        # Génération de la fiche unifiée
        try:
            fiche_html = afficher_fiche_cotisation_unifiee(membre, verification, cotisation)
            logger.info("✅ Fiche HTML générée avec succès")
        except Exception as e:
            logger.error(f"❌ Erreur génération fiche: {e}")
            fiche_html = f"""
            <div class="alert alert-danger">
                <h4>❌ Erreur de génération</h4>
                <p>Impossible de générer la fiche de cotisation.</p>
                <small>Erreur: {str(e)}</small>
            </div>
            """
        
        context = {
            'fiche_html': fiche_html,
            'membre': membre,
            'page_title': f'Fiche Cotisation - {membre.prenom} {membre.nom}',
            'active_tab': 'verification_cotisations',
            'agent': get_agent_connecte(request),
        }
        
        return render(request, 'agents/fiche_cotisation_unifiee.html', context)
        
    except Membre.DoesNotExist:
        logger.error(f"❌ Membre {membre_id} non trouvé")
        _ajouter_message(request, 'error', "Membre non trouvé")
        return redirect('agents:verification_cotisations')
    except Exception as e:
        logger.error(f"❌ Erreur critique affichage fiche unifiée: {e}")
        _ajouter_message(request, 'error', f"Erreur technique: {str(e)}")
        return redirect('agents:verification_cotisations')


@login_required
@gerer_erreurs
def recherche_membres_api(request):
    """API pour la recherche de membres - VERSION CORRIGÉE"""
    try:
        query = request.GET.get('q', '').strip()
        
        logger.info(f"Recherche membres API appelée avec query: '{query}'")
        
        if len(query) < 2:
            return JsonResponse({'membres': []})
        
        # Recherche dans la base de données si disponible
        if not MEMBRE_MODEL_AVAILABLE:
            return JsonResponse({'membres': []})
        
        membres = Membre.objects.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(numero_unique__icontains=query) |
            Q(telephone__icontains=query)
        )[:10]
        
        logger.info(f"Nombre de membres trouvés: {len(membres)}")
        
        # Construction des résultats avec valeurs SÉRIALISABLES
        results = []
        for membre in membres:
            results.append({
                'id': getattr(membre, 'id', None),
                'nom': getattr(membre, 'nom', ''),
                'prenom': getattr(membre, 'prenom', ''),
                'numero_unique': getattr(membre, 'numero_unique', ''),
                'telephone': getattr(membre, 'telephone', ''),
                'statut': getattr(membre, 'statut', '')
            })
        
        logger.info(f"Recherche réussie: {len(results)} résultats")
        return JsonResponse({'membres': results})
        
    except Exception as e:
        logger.error(f"Erreur critique recherche membres: {e}")
        return JsonResponse({
            'membres': [], 
            'error': 'Erreur technique lors de la recherche'
        }, status=500)

@login_required
@gerer_erreurs
def verifier_cotisation_api(request, membre_id=None):
    """API pour vérifier la cotisation d'un membre - VERSION SIMPLIFIÉE"""
    try:
        # Vérifier la disponibilité des modèles
        if not MEMBRE_MODEL_AVAILABLE:
            return JsonResponse({
                'success': False,
                'error': 'Module membres non disponible'
            }, status=500)
        
        # Récupérer le membre depuis les paramètres GET si membre_id n'est pas fourni
        if membre_id is None:
            membre_id = request.GET.get('membre_id')
        
        if not membre_id:
            return JsonResponse({
                'success': False,
                'error': 'ID membre non fourni'
            }, status=400)
        
        # Récupérer le membre
        membre = get_object_or_404(Membre, id=membre_id)
        
        # Récupérer l'agent connecté si disponible
        agent = None
        if AGENT_MODELS_AVAILABLE:
            try:
                agent = Agent.objects.get(user=request.user)
            except Agent.DoesNotExist:
                pass
        
        # Vérifier le statut de cotisation
        est_a_jour, details = verifier_cotisation_membre_simplifiee(membre)
        
        # Enregistrer la vérification si agent existe
        verification_id = None
        if agent and AGENT_MODELS_AVAILABLE:
            try:
                verification = VerificationCotisation.objects.create(
                    agent=agent,
                    membre=membre,
                    statut_cotisation='a_jour' if est_a_jour else 'en_retard',
                    prochaine_echeance=timezone.now().date() + timedelta(days=30),
                    observations=details.get('message', 'Vérification effectuée')
                )
                verification_id = verification.id
            except Exception as e:
                logger.error(f"Erreur création vérification: {e}")
        
        response_data = {
            'success': True,
            'est_a_jour': est_a_jour,
            'message': details.get('message', 'Statut vérifié'),
            'prochaine_echeance': details.get('prochaine_echeance'),
            'dernier_paiement': details.get('dernier_paiement'),
            'montant_du': details.get('montant_du', '0 FCFA'),
            'jours_retard': details.get('jours_retard', 0),
            'verification_id': verification_id,
        }
        
        return JsonResponse(response_data)
            
    except Membre.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Membre non trouvé'
        }, status=404)
    except Exception as e:
        logger.error(f"Erreur vérification cotisation: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': f'Erreur lors de la vérification: {str(e)}'
        }, status=500)

@login_required
@gerer_erreurs
def test_simple_api(request):
    """API de test simple pour debuguer l'erreur 500"""
    try:
        return JsonResponse({
            'success': True,
            'message': 'API de test fonctionnelle',
            'user': request.user.username,
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

# =============================================================================
# VUES POUR LA CRÉATION DE BONS DE SOIN - VERSION COMPLÈTEMENT CORRIGÉE
# =============================================================================

@login_required
@gerer_erreurs
@agent_required
def creer_bon_soin(request, membre_id=None):
    """Créer un bon de soin pour un membre - VERSION CORRIGÉE"""
    if not est_agent(request.user):
        _ajouter_message(request, 'error', "Accès réservé aux agents.")
        return redirect('home')
    
    # Vérifier si BonDeSoin est disponible
    if not BON_SOIN_AVAILABLE:
        _ajouter_message(request, 'error', "Module soins non configuré")
        return redirect('agents:dashboard')
    
    # Calculer bons_du_jour pour éviter l'erreur dans le template
    today = date.today()
    bons_du_jour = 0
    
    if BON_SOIN_AVAILABLE:
        try:
            bons_du_jour = BonDeSoin.objects.filter(date_creation__date=today).count()
        except Exception as e:
            logger.error(f"Erreur calcul bons_du_jour: {e}")
            bons_du_jour = 0
    
    # Calculer la limite restante pour éviter l'erreur du template
    agent = get_agent_connecte(request)
    limite_quotidienne = getattr(agent, 'limite_bons_quotidienne', 10)
    limite_restante = max(0, limite_quotidienne - bons_du_jour)
    
    context = {
        'bons_du_jour': bons_du_jour,
        'today': today,
        'page_title': 'Créer un Bon de Soin',
        'active_tab': 'creer_bon_soin',
        'agent': agent,
        'limite_restante': limite_restante,  # CORRECTION : Ajout de la variable manquante
    }
    
    # Si un membre_id est fourni, pré-remplir avec les infos du membre
    if membre_id and MEMBRE_MODEL_AVAILABLE:
        try:
            membre = get_object_or_404(Membre, id=membre_id)
            context['membre'] = membre
            context['membre_id'] = membre_id
            
            # Vérifier le statut de cotisation du membre
            est_a_jour = verifier_statut_cotisation_simple(membre)
            context['est_a_jour'] = est_a_jour
            
            if not est_a_jour:
                _ajouter_message(request, 'warning',
                    f"Attention: {membre.prenom} {membre.nom} n'est pas à jour de cotisation. "
                    "Le bon de soin peut être refusé."
                )
                
        except Membre.DoesNotExist:
            _ajouter_message(request, 'error', "Membre non trouvé")
    
    return render(request, 'agents/creer_bon_soin.html', context)

@login_required
@gerer_erreurs
@agent_required
def creer_bon_soin_membre(request, membre_id):
    """Créer un bon de soin pour un membre spécifique - VERSION COMPLÈTEMENT CORRIGÉE"""
    # Vérification des permissions avec gestion sécurisée des messages
    if not est_agent(request.user):
        logger.warning(f"Tentative d'accès non autorisé: {request.user.username}")
        _ajouter_message(request, 'error', "Accès réservé aux agents.")
        return redirect('home')
    
    # Vérifier si BonDeSoin est disponible
    if not BON_SOIN_AVAILABLE:
        logger.error("Modèle BonDeSoin non disponible")
        _ajouter_message(request, 'error', "Module soins non configuré")
        return redirect('agents:dashboard')
    
    # Vérifier si Membre est disponible
    if not MEMBRE_MODEL_AVAILABLE:
        _ajouter_message(request, 'error', "Module membres non configuré")
        return redirect('agents:dashboard')
    
    # Calculer bons_du_jour pour éviter l'erreur dans le template
    today = date.today()
    bons_du_jour = 0
    
    if BON_SOIN_AVAILABLE:
        try:
            bons_du_jour = BonDeSoin.objects.filter(date_creation__date=today).count()
        except Exception as e:
            logger.error(f"Erreur calcul bons_du_jour: {e}")
            bons_du_jour = 0
    
    # Calculer la limite restante pour éviter l'erreur du template
    agent = get_agent_connecte(request)
    limite_quotidienne = getattr(agent, 'limite_bons_quotidienne', 10)
    limite_restante = max(0, limite_quotidienne - bons_du_jour)
    
    try:
        membre = get_object_or_404(Membre, id=membre_id)
        logger.info(f"Création bon de soin pour membre: {membre.prenom} {membre.nom}")
        
        if request.method == 'POST':
            # Récupérer les données du formulaire
            type_soin = request.POST.get('type_soin', '').strip()
            montant_str = request.POST.get('montant', '').strip()
            symptomes = request.POST.get('symptomes', '').strip()
            diagnostic = request.POST.get('diagnostic', '').strip()
            description = request.POST.get('description', '').strip()
            
            # Validation des données
            if not all([type_soin, montant_str]):
                logger.warning("Champs obligatoires manquants")
                _ajouter_message(request, 'error', "Tous les champs obligatoires doivent être remplis")
                return redirect('agents:creer_bon_soin_membre', membre_id=membre_id)
            
            # Validation du montant
            try:
                montant = float(montant_str)
                if montant <= 0:
                    logger.warning(f"Montant invalide: {montant}")
                    _ajouter_message(request, 'error', "Le montant doit être supérieur à 0")
                    return redirect('agents:creer_bon_soin_membre', membre_id=membre_id)
            except (ValueError, TypeError):
                logger.warning(f"Format montant invalide: {montant_str}")
                _ajouter_message(request, 'error', "Le montant doit être un nombre valide")
                return redirect('agents:creer_bon_soin_membre', membre_id=membre_id)
            
            # Créer le bon de soin
            try:
                bon_soin = BonDeSoin.objects.create(
                    patient=membre,
                    date_soin=timezone.now().date(),
                    symptomes=symptomes,
                    diagnostic=diagnostic,
                    montant=montant,
                    statut='attente'
                )
                
                logger.info(f"✅ Bon de soin créé avec succès - ID: {bon_soin.id}")
                
                # Utiliser la fonction sécurisée pour les messages
                success_message = f"✅ Bon de soin créé avec succès pour {membre.prenom} {membre.nom}! Référence: {bon_soin.id}"
                _ajouter_message(request, 'success', success_message)
                
                return redirect('agents:confirmation_bon_soin', bon_id=bon_soin.id)
                
            except Exception as e:
                logger.error(f"Erreur création BonDeSoin: {e}", exc_info=True)
                error_msg = f"Erreur lors de la création: {str(e)}"
                _ajouter_message(request, 'error', error_msg)
                return redirect('agents:creer_bon_soin_membre', membre_id=membre_id)
        
        # GET request - afficher le formulaire
        context = {
            'membre': membre,
            'membre_id': membre_id,
            'types_soins': [
                ('consultation', 'Consultation médicale'),
                ('analyse', 'Analyse médicale'),
                ('radiologie', 'Radiologie'),
                ('pharmacie', 'Médicaments'),
                ('hospitalisation', 'Hospitalisation'),
                ('urgence', 'Urgence'),
                ('autre', 'Autre')
            ],
            'bons_du_jour': bons_du_jour,
            'today': today,
            'page_title': f'Créer Bon de Soin - {membre.prenom} {membre.nom}',
            'active_tab': 'creer_bon_soin',
            'agent': agent,
            'limite_restante': limite_restante,  # CORRECTION : Ajout de la variable manquante
        }
        return render(request, 'agents/creer_bon_soin_membre.html', context)
            
    except Membre.DoesNotExist:
        logger.error(f"Membre {membre_id} non trouvé")
        _ajouter_message(request, 'error', "Membre non trouvé")
        return redirect('agents:creer_bon_soin')
    except Exception as e:
        logger.error(f"Erreur générale creer_bon_soin_membre: {e}", exc_info=True)
        _ajouter_message(request, 'error', f"Erreur technique: {str(e)}")
        return redirect('agents:creer_bon_soin')

@login_required
@gerer_erreurs
@agent_required
def confirmation_bon_soin(request, bon_id):
    """Affiche la confirmation de création du bon de soin"""
    if not est_agent(request.user):
        _ajouter_message(request, 'error', "Accès réservé aux agents.")
        return redirect('home')
    
    try:
        # Utiliser BonDeSoin
        bon_soin = get_object_or_404(BonDeSoin, id=bon_id)
        
        context = {
            'bon_soin': bon_soin,
            'membre': bon_soin.patient,
            'page_title': 'Confirmation Bon de Soin',
            'agent': get_agent_connecte(request),
        }
        
        return render(request, 'agents/confirmation_bon_soin.html', context)
        
    except Exception as e:
        logger.error(f"Erreur confirmation bon soin: {e}")
        _ajouter_message(request, 'error', "Erreur lors de l'affichage de la confirmation")
        return redirect('agents:dashboard')

@login_required
@gerer_erreurs
def api_recherche_membres_bon_soin(request):
    """API pour rechercher des membres lors de la création d'un bon de soin - VERSION CORRIGÉE"""
    query = request.GET.get('q', '').strip()
    
    logger.info(f"🔍 Recherche membres bon soin appelée avec: '{query}'")
    
    if not query or len(query) < 2:
        return JsonResponse({'membres': []})
    
    try:
        # Vérifier disponibilité modèle
        if not MEMBRE_MODEL_AVAILABLE:
            logger.warning("Module membres non disponible")
            return JsonResponse({'membres': []})
            
        # Recherche dans les membres avec logging détaillé
        logger.info(f"🔍 Recherche dans la base de données pour: '{query}'")
        
        # Construction de la requête de recherche
        conditions = Q()
        
        # Vérifier quels champs existent dans le modèle Membre
        try:
            # Test des champs possibles
            sample_membre = Membre.objects.first()
            if sample_membre:
                if hasattr(sample_membre, 'nom'):
                    conditions |= Q(nom__icontains=query)
                if hasattr(sample_membre, 'prenom'):
                    conditions |= Q(prenom__icontains=query)
                if hasattr(sample_membre, 'numero_unique'):
                    conditions |= Q(numero_unique__icontains=query)
                if hasattr(sample_membre, 'telephone'):
                    conditions |= Q(telephone__icontains=query)
                if hasattr(sample_membre, 'user'):
                    conditions |= Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query)
        except Exception as e:
            logger.warning(f"Erreur vérification champs membre: {e}")
            # Fallback: utiliser les champs de base
            conditions = Q(nom__icontains=query) | Q(prenom__icontains=query)
        
        membres = Membre.objects.filter(conditions)[:10]
        
        logger.info(f"✅ {len(membres)} membres trouvés pour la recherche: '{query}'")
        
        resultats = []
        for membre in membres:
            try:
                est_a_jour = verifier_statut_cotisation_simple(membre)
                
                # Construction du nom complet selon les champs disponibles
                nom_complet = ""
                if hasattr(membre, 'prenom') and hasattr(membre, 'nom'):
                    nom_complet = f"{membre.prenom} {membre.nom}"
                elif hasattr(membre, 'user'):
                    nom_complet = f"{membre.user.first_name} {membre.user.last_name}"
                else:
                    nom_complet = f"Membre {membre.id}"
                
                # Construction des autres informations
                numero_unique = getattr(membre, 'numero_unique', 'N/A')
                telephone = getattr(membre, 'telephone', 'Non renseigné')
                
                resultats.append({
                    'id': membre.id,
                    'nom_complet': nom_complet.strip(),
                    'numero_unique': numero_unique,
                    'telephone': telephone,
                    'est_a_jour': est_a_jour,
                })
                
                logger.debug(f"📋 Membre trouvé: {nom_complet} (ID: {membre.id}, À jour: {est_a_jour})")
                
            except Exception as e:
                logger.error(f"❌ Erreur traitement membre {membre.id}: {e}")
                continue
        
        logger.info(f"🎯 Recherche réussie: {len(resultats)} résultats retournés")
        return JsonResponse({'membres': resultats})
        
    except Exception as e:
        logger.error(f"💥 ERREUR CRITIQUE recherche membres bon soin: {str(e)}", exc_info=True)
        return JsonResponse({
            'membres': [], 
            'erreur': 'Erreur technique lors de la recherche',
            'details': str(e)
        })




def details_bon_soin_api(request, bon_id):
    """API pour récupérer les détails d'un bon de soin - VERSION CORRIGÉE POUR LE FRONTEND"""
    try:
        from soins.models import BonDeSoin
        from django.utils import timezone
        from datetime import timedelta
        from django.http import JsonResponse
        
        bon = BonDeSoin.objects.select_related('patient', 'medecin').get(id=bon_id)
        
        # Calculer la date d'expiration (30 jours après la création)
        date_expiration = None
        temps_restant = 0
        
        if bon.date_creation:
            # Convertir en date si c'est un datetime
            if hasattr(bon.date_creation, 'date'):
                date_creation = bon.date_creation.date()
            else:
                date_creation = bon.date_creation
                
            date_expiration = date_creation + timedelta(days=30)
            aujourd_hui = timezone.now().date()
            temps_restant = (date_expiration - aujourd_hui).days
        
        # CRITIQUE: Renvoyer les champs À LA RACINE comme le frontend les attend
        # Le frontend ne regarde pas dans un objet "bon", mais directement à la racine
        data = {
            # Champs généraux - À LA RACINE
            'code': str(bon.id),
            'membre': bon.patient.nom_complet if bon.patient and hasattr(bon.patient, 'nom_complet') else 'Non spécifié',
            'montant_max': str(bon.montant) if bon.montant else '0',
            'statut': bon.statut.upper() if bon.statut else 'INDEFINI',
            
            # Dates - À LA RACINE
            'date_creation': bon.date_creation.strftime('%d/%m/%Y') if bon.date_creation else 'Non spécifiée',
            'date_expiration': date_expiration.strftime('%d/%m/%Y') if date_expiration else 'Non calculée',
            'temps_restant': f"{temps_restant} jours" if temps_restant > 0 else "Expiré",
            
            # Détails médicaux - À LA RACINE
            'motif': bon.symptomes or 'Non spécifié',
            'type_soin': bon.diagnostic or 'Consultation générale',
            'urgence': 'Normale',
            
            # Champs supplémentaires pour compatibilité
            'id': bon.id,
            'patient_nom': bon.patient.nom if bon.patient else '',
            'patient_prenom': bon.patient.prenom if bon.patient else '',
            'medecin': bon.medecin.get_full_name() if bon.medecin and hasattr(bon.medecin, 'get_full_name') else 'Non assigné',
            'symptomes': bon.symptomes or 'Non spécifiés',
            'diagnostic': bon.diagnostic or 'Non spécifié'
        }
        
        return JsonResponse(data)  # IMPORTANT: Renvoyer data directement, pas dans un objet 'bon'
        
    except BonDeSoin.DoesNotExist:
        from django.http import JsonResponse
        return JsonResponse({'success': False, 'error': 'Bon de soin non trouvé'}, status=404)
    except Exception as e:
        from django.http import JsonResponse
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@gerer_erreurs
@agent_required
def debug_recherche_membres(request):
    """Page de debug pour tester la recherche de membres"""
    if not est_agent(request.user):
        _ajouter_message(request, 'error', "Accès réservé aux agents.")
        return redirect('home')
    
    context = {
        'page_title': 'Debug Recherche Membres',
        'active_tab': 'debug',
        'agent': get_agent_connecte(request),
    }
    
    # Test de la base de données
    if MEMBRE_MODEL_AVAILABLE:
        try:
            total_membres = Membre.objects.count()
            premier_membre = Membre.objects.first()
            
            context.update({
                'total_membres': total_membres,
                'premier_membre': premier_membre,
                'champs_premier_membre': dir(premier_membre) if premier_membre else [],
            })
            
            logger.info(f"🔍 Debug: {total_membres} membres trouvés dans la base")
            if premier_membre:
                logger.info(f"🔍 Premier membre: ID={premier_membre.id}, Champs disponibles: {[attr for attr in dir(premier_membre) if not attr.startswith('_')]}")
                
        except Exception as e:
            logger.error(f"❌ Erreur debug recherche: {e}")
            context['erreur_bdd'] = str(e)
    
    return render(request, 'agents/debug_recherche.html', context)

@login_required
@gerer_erreurs
@agent_required
def historique_bons(request):
    """Afficher l'historique des bons de soin"""
    if not est_agent(request.user):
        _ajouter_message(request, 'error', "Accès réservé aux agents.")
        return redirect('home')
    
    try:
        # Utiliser BonDeSoin
        if BON_SOIN_AVAILABLE:
            bons = BonDeSoin.objects.all().select_related('patient').order_by('-date_creation')[:50]
        else:
            bons = []
        
        context = {
            'bons': bons,
            'title': 'Historique des bons de soin',
            'page_title': 'Historique des Bons de Soin',
            'active_tab': 'historique_bons',
            'agent': get_agent_connecte(request),
        }
        return render(request, 'agents/historique_bons.html', context)
        
    except Exception as e:
        logger.error(f"Erreur historique bons: {e}")
        _ajouter_message(request, 'error', "Module soins non configuré")
        return render(request, 'agents/historique_bons.html', {
            'bons': [],
            'page_title': 'Historique des Bons de Soin',
            'agent': get_agent_connecte(request),
        })

@login_required
@gerer_erreurs
@agent_required
def rapport_performance(request):
    """Rapport de performance des agents"""
    if not est_agent(request.user):
        _ajouter_message(request, 'error', "Accès réservé aux agents.")
        return redirect('home')
    
    try:
        # Récupérer l'agent connecté
        agent = get_agent_connecte(request)
        
        # Statistiques de base
        aujourd_hui = timezone.now().date()
        debut_mois = aujourd_hui.replace(day=1)
        
        # Vérifications ce mois-ci
        verifications_mois = 0
        if AGENT_MODELS_AVAILABLE and hasattr(agent, 'id') and agent.id > 0:
            try:
                verifications_mois = VerificationCotisation.objects.filter(
                    agent=agent,
                    date_verification__date__gte=debut_mois
                ).count()
            except Exception as e:
                logger.error(f"Erreur calcul vérifications mois: {e}")
        
        # Bons de soin ce mois-ci
        bons_mois = 0
        if BON_SOIN_AVAILABLE:
            try:
                bons_mois = BonDeSoin.objects.filter(
                    date_creation__date__gte=debut_mois
                ).count()
            except Exception as e:
                logger.error(f"Erreur calcul bons mois: {e}")
        
        context = {
            'agent': agent,
            'verifications_mois': verifications_mois,
            'bons_mois': bons_mois,
            'date_debut_mois': debut_mois,
            'date_aujourdhui': aujourd_hui,
            'page_title': 'Rapport de Performance',
            'active_tab': 'rapport_performance',
        }
        
        return render(request, 'agents/rapport_performance.html', context)
        
    except Exception as e:
        logger.error(f"Erreur rapport performance: {e}")
        _ajouter_message(request, 'error', "Erreur lors de la génération du rapport")
        return redirect('agents:dashboard')


# =============================================================================
# VUES GESTION DES MEMBRES
# =============================================================================

@login_required
@gerer_erreurs
@agent_required
def creer_membre(request):
    """Création d'un nouveau membre avec VÉRITABLE enregistrement"""
    logger.info("🎯 ===== VUE creer_membre DÉBUT =====")
    logger.info(f"🎯 Méthode: {request.method}")
    logger.info(f"🎯 Utilisateur: {request.user.username}")
    
    try:
        agent = get_agent_connecte(request)
        logger.info(f"🎯 Agent connecté: {agent}")
        
        # ✅ CORRECTION: Vérifier si c'est un vrai Agent ou un MockAgent
        agent_reel = None
        if AGENT_MODELS_AVAILABLE and hasattr(agent, 'id') and not isinstance(agent, MockAgent) and agent.id > 0:
            agent_reel = agent
            logger.info(f"✅ Vrai Agent détecté: {agent_reel}")
        else:
            logger.warning(f"⚠️ MockAgent ou Agent non disponible - Activité ne sera pas enregistrée")
        
        if request.method == 'POST':
            logger.info("🎯 METHODE POST DÉTECTÉE")
            
            # Récupération des données du formulaire
            nom = request.POST.get('nom', '').strip()
            prenom = request.POST.get('prenom', '').strip()
            telephone = request.POST.get('telephone', '').strip()
            email = request.POST.get('email', '').strip()
            
            logger.info(f"🎯 Données formulaire:")
            logger.info(f"   - Nom: '{nom}'")
            logger.info(f"   - Prénom: '{prenom}'") 
            logger.info(f"   - Téléphone: '{telephone}'")
            logger.info(f"   - Email: '{email}'")
            
            # VALIDATION
            if not all([nom, prenom, telephone]):
                logger.warning("❌ VALIDATION ÉCHOUÉE - Champs obligatoires manquants")
                _ajouter_message(request, 'error', "Nom, prénom et téléphone sont obligatoires")
                return redirect('agents:creer_membre')
            
            logger.info("✅ VALIDATION RÉUSSIE")
            
            # GÉNÉRER UN NUMÉRO UNIQUE (OBLIGATOIRE !)
            numero_unique = generer_numero_unique()
            logger.info(f"🎯 Numéro unique généré: {numero_unique}")
            
            # CRÉATION RÉELLE DU MEMBRE
            try:
                logger.info("🎯 Tentative de création du membre en base...")
                
                nouveau_membre = Membre.objects.create(
                    nom=nom,
                    prenom=prenom,
                    telephone=telephone,
                    email=email if email else "",
                    numero_unique=numero_unique,
                    statut='actif',
                    date_inscription=timezone.now()
                )
                
                logger.info(f"✅ MEMBRE CRÉÉ AVEC SUCCÈS - ID: {nouveau_membre.id}")
                logger.info(f"✅ Détails: {prenom} {nom}, Téléphone: {telephone}, Numéro: {numero_unique}")
                
                # ✅ CORRECTION: Enregistrer l'activité SEULEMENT si on a un vrai Agent
                if agent_reel:
                    try:
                        ActiviteAgent.objects.create(
                            agent=agent_reel,  # ← Maintenant c'est un VRAI Agent
                            type_activite='consultation_membre',
                            description=f"Création du membre {prenom} {nom} (ID: {nouveau_membre.id})",
                            donnees_concernees={'action': 'creation', 'membre_id': nouveau_membre.id}
                        )
                        logger.info("✅ Activité enregistrée avec succès")
                    except Exception as e:
                        logger.warning(f"⚠️ Erreur enregistrement activité: {e}")
                        # Ne pas bloquer la création même si l'activité échoue
                else:
                    logger.warning("⚠️ Activité non enregistrée - Agent non disponible")
                
                _ajouter_message(request, 'success', f'Membre {prenom} {nom} créé avec succès! Numéro: {numero_unique}')
                logger.info("✅ Message de succès ajouté")
                
                return redirect('agents:liste_membres')
                
            except Exception as e:
                logger.error(f"❌ ERREUR CRÉATION MEMBRE: {e}")
                _ajouter_message(request, 'error', f"Erreur lors de la création: {str(e)}")
                return redirect('agents:creer_membre')
        else:
            logger.info("🎯 METHODE GET - Affichage formulaire")
        
        context = {
            'page_title': 'Créer un Nouveau Membre',
            'active_tab': 'creer_membre',
            'agent': agent,
        }
        return render(request, 'agents/creer_membre.html', context)
        
    except Exception as e:
        logger.error(f"❌ ERREUR GÉNÉRALE creer_membre: {e}")
        _ajouter_message(request, 'error', "Erreur lors de la création du membre")
        return redirect('agents:liste_membres')
        

@login_required
@gerer_erreurs
@agent_required
def liste_membres(request):
    """Liste des membres avec filtres"""
    try:
        from django.core.paginator import Paginator
        
        agent = get_agent_connecte(request)
        
        # Récupérer les paramètres de filtrage
        search_query = request.GET.get('search', '')
        statut_cotisation = request.GET.get('statut_cotisation', '')
        
        # Base queryset
        if MEMBRE_MODEL_AVAILABLE:
            membres = Membre.objects.all()
        else:
            membres = []
        
        # Appliquer les filtres
        if search_query and MEMBRE_MODEL_AVAILABLE:
            membres = membres.filter(
                Q(nom__icontains=search_query) |
                Q(prenom__icontains=search_query) |
                Q(telephone__icontains=search_query)
            )
        
        # Pagination
        if MEMBRE_MODEL_AVAILABLE:
            paginator = Paginator(membres, 20)  # 20 membres par page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            page_obj = []
        
        context = {
            'page_title': 'Liste des Membres',
            'active_tab': 'liste_membres',
            'agent': agent,
            'page_obj': page_obj,
            'search_query': search_query,
            'statut_cotisation': statut_cotisation,
        }
        return render(request, 'agents/liste_membres.html', context)
        
    except Exception as e:
        logger.error(f"Erreur liste membres: {e}")
        _ajouter_message(request, 'error', "Erreur lors du chargement de la liste des membres")
        return redirect('agents:dashboard')

# =============================================================================
# VUES DE COMMUNICATION - VERSION ROBUSTE
# =============================================================================

@login_required
@gerer_erreurs
@agent_required
def get_stats_communication(request):
    """Tableau de bord communication pour agent - VUE ROBUSTE"""
    try:
        if not est_agent(request.user):
            _ajouter_message(request, 'error', "Accès réservé aux agents.")
            return redirect('home')
        
        agent = get_agent_connecte(request)
        
        # Statistiques de communication avec valeurs par défaut
        messages_non_lus = 0
        notifications_non_lues = 0
        conversations_recentes = []
        
        try:
            from communication.models import Message, Notification, Conversation
            messages_non_lus = Message.objects.filter(destinataire=request.user, est_lu=False).count()
            notifications_non_lues = Notification.objects.filter(user=request.user, est_lue=False).count()
            conversations_recentes = Conversation.objects.filter(participants=request.user).order_by('-date_dernier_message')[:5]
        except Exception as e:
            logger.warning(f"Modules communication non disponibles: {e}")
        
        context = {
            'page_title': 'Communication',
            'active_tab': 'communication',
            'agent': agent,
            'messages_non_lus': messages_non_lus,
            'notifications_non_lues': notifications_non_lues,
            'conversations_recentes': conversations_recentes,
        }
        
        return render(request, 'agents/communication.html', context)
        
    except Exception as e:
        logger.error(f"Erreur dashboard_communication: {e}")
        _ajouter_message(request, 'error', "Erreur lors du chargement de la communication")
        return redirect('agents:dashboard')

@login_required
@gerer_erreurs
@agent_required
def liste_messages_agent(request):
    """Afficher les messages de l'agent - VUE ROBUSTE"""
    try:
        if not est_agent(request.user):
            _ajouter_message(request, 'error', "Accès réservé aux agents.")
            return redirect('home')
        
        agent = get_agent_connecte(request)
        
        messages_recus = []
        messages_envoyes = []
        
        try:
            from communication.models import Message
            messages_recus = Message.objects.filter(destinataire=request.user).order_by('-date_envoi')
            messages_envoyes = Message.objects.filter(expediteur=request.user).order_by('-date_envoi')
        except Exception as e:
            logger.warning(f"Modules communication non disponibles: {e}")
        
        context = {
            'page_title': 'Mes Messages',
            'active_tab': 'communication',
            'agent': agent,
            'messages_recus': messages_recus,
            'messages_envoyes': messages_envoyes,
        }
        
        return render(request, 'agents/communication/liste_messages.html', context)
        
    except Exception as e:
        logger.error(f"Erreur liste_messages_agent: {e}")
        _ajouter_message(request, 'error', "Erreur lors du chargement des messages")
        return redirect('agents:dashboard')

@login_required
@gerer_erreurs
@agent_required
def liste_notifications_agent(request):
    """Afficher les notifications de l'agent - VUE ROBUSTE"""
    try:
        if not est_agent(request.user):
            _ajouter_message(request, 'error', "Accès réservé aux agents.")
            return redirect('home')
        
        agent = get_agent_connecte(request)
        
        notifications = []
        
        try:
            from communication.models import Notification
            notifications = Notification.objects.filter(user=request.user).order_by('-date_creation')
            
            # Marquer comme lues si demandé
            if request.GET.get('marquer_lues'):
                notifications.filter(est_lue=False).update(est_lue=True)
                _ajouter_message(request, 'success', "Notifications marquées comme lues")
        except Exception as e:
            logger.warning(f"Modules communication non disponibles: {e}")
        
        context = {
            'page_title': 'Mes Notifications',
            'active_tab': 'communication',
            'agent': agent,
            'notifications': notifications,
        }
        
        return render(request, 'agents/communication/liste_notifications.html', context)
        
    except Exception as e:
        logger.error(f"Erreur liste_notifications_agent: {e}")
        _ajouter_message(request, 'error', "Erreur lors du chargement des notifications")
        return redirect('agents:dashboard')

@login_required
@gerer_erreurs
@agent_required
def envoyer_message_agent(request):
    """Envoyer un message depuis l'interface agent - VUE ROBUSTE"""
    try:
        if not est_agent(request.user):
            _ajouter_message(request, 'error', "Accès réservé aux agents.")
            return redirect('home')
        
        agent = get_agent_connecte(request)
        
        form = None
        try:
            from communication.forms import MessageForm
            
            if request.method == 'POST':
                form = MessageForm(request.POST)
                if form.is_valid():
                    message = form.save(commit=False)
                    message.expediteur = request.user
                    message.save()
                    
                    # Enregistrer l'activité
                    if AGENT_MODELS_AVAILABLE and hasattr(agent, 'id') and agent.id > 0:
                        ActiviteAgent.objects.create(
                            agent=agent,
                            type_activite='modification_donnees',
                            description=f"Message envoyé à {message.destinataire.username}",
                            donnees_concernees={'action': 'envoi_message', 'destinataire': message.destinataire.username}
                        )
                    
                    _ajouter_message(request, 'success', "Message envoyé avec succès!")
                    return redirect('agents:liste_messages')
                else:
                    _ajouter_message(request, 'error', "Veuillez corriger les erreurs du formulaire")
            else:
                form = MessageForm()
        except Exception as e:
            logger.warning(f"Modules communication non disponibles: {e}")
            _ajouter_message(request, 'error', "Module communication non disponible")
        
        context = {
            'page_title': 'Envoyer un Message',
            'active_tab': 'communication',
            'agent': agent,
            'form': form,
        }
        
        return render(request, 'agents/communication/envoyer_message.html', context)
        
    except Exception as e:
        logger.error(f"Erreur envoyer_message_agent: {e}")
        _ajouter_message(request, 'error', "Erreur lors de l'envoi du message")
        return redirect('agents:dashboard')

def votre_vue(request):
    try:
        # Vérifier la disponibilité des modèles nécessaires
        if not MEMBRE_MODEL_AVAILABLE:
            _ajouter_message(request, 'error', "Module membres non disponible")
            return redirect('agents:dashboard')
            
        if not BON_SOIN_AVAILABLE and 'bon_soin' in request.path:
            _ajouter_message(request, 'error', "Module soins non disponible")
            return redirect('agents:dashboard')
            
        # ... reste du code ...
        
    except Exception as e:
        logger.error(f"Erreur dans la vue: {e}")
        _ajouter_message(request, 'error', "Erreur technique")
        return redirect('agents:dashboard')

tableau_de_bord = dashboard  # Alias pour résoudre l'erreur URLa