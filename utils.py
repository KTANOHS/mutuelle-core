"""
Utils pour l'application mutuelle_core
Fonctions utilitaires pour les vues et modèles
Version MISE À JOUR avec permissions fiables
"""
from django.contrib.auth.models import User, Group
from django.db.models import Sum, Count, Avg
from datetime import datetime, timedelta
from membres.models import Membre, Bon
from paiements.models import Paiement
import logging

# Configuration du logger
logger = logging.getLogger(__name__)

# Import des permissions fiables
try:
    from custom_permissions import is_medecin, is_membre, is_pharmacien, is_assureur
    logger.info("✅ Permissions personnalisées importées avec succès")
except ImportError as e:
    logger.error(f"❌ Erreur import permissions personnalisées: {e}")
    
    # Fallback vers les vérifications directes en base
    from membres.models import Membre
    from medecin.models import Medecin
    from pharmacien.models import Pharmacien
    from assureur.models import Assureur
from django.utils import timezone
    
    def is_medecin(user):
        """Vérifie si l'utilisateur est médecin (requête directe en base)"""
        if not user or not user.is_authenticated:
            return False
        return Medecin.objects.filter(user=user).exists()
    
    def is_membre(user):
        """Vérifie si l'utilisateur est membre (requête directe en base)"""
        if not user or not user.is_authenticated:
            return False
        return Membre.objects.filter(user=user).exists()
    
    def is_pharmacien(user):
        """Vérifie si l'utilisateur est pharmacien (requête directe en base)"""
        if not user or not user.is_authenticated:
            return False
        return Pharmacien.objects.filter(user=user).exists()
    
    def is_assureur(user):
        """Vérifie si l'utilisateur est assureur (requête directe en base)"""
        if not user or not user.is_authenticated:
            return False
        return Assureur.objects.filter(user=user).exists()

def get_user_redirect_url(user):
    """
    Détermine l'URL de redirection en fonction du profil de l'utilisateur
    Version COMPLÈTEMENT FIABLE avec vérifications en base
    """
    if not user.is_authenticated:
        return '/login/'
    
    logger.debug(f"get_user_redirect_url: User={user.username}, Superuser={user.is_superuser}")
    
    # Vérification FIABLE par requêtes directes en base
    if is_assureur(user):
        logger.debug(f"  -> Assureur détecté (vérification fiable)")
        return '/assureur-dashboard/'
    elif is_medecin(user):
        logger.debug(f"  -> Medecin détecté (vérification fiable)")
        return '/medecin-dashboard/'
    elif is_pharmacien(user):
        logger.debug(f"  -> Pharmacien détecté (vérification fiable)")
        return '/pharmacien-dashboard/'
    elif is_membre(user):
        logger.debug(f"  -> Membre détecté (vérification fiable)")
        return '/membre-dashboard/'
    
    # Fallback pour superuser sans profil spécifique
    elif user.is_superuser:
        logger.debug(f"  -> Superuser sans profil spécifique")
        return '/assureur-dashboard/'
    
    else:
        logger.debug(f"  -> Aucun profil détecté, redirection générique")
        return '/generic-dashboard/'

def get_user_type(user):
    """
    Retourne le type d'utilisateur sous forme de string
    Version FIABLE avec vérifications en base
    """
    if is_assureur(user):
        return 'assureur'
    elif is_medecin(user):
        return 'medecin'
    elif is_pharmacien(user):
        return 'pharmacien'
    elif is_membre(user):
        return 'membre'
    else:
        return 'generic'

def get_assureur_stats():
    """
    Récupère les statistiques pour le dashboard assureur
    """
    try:
        stats = {
            'total_membres': Membre.objects.count(),
            'membres_actifs': Membre.objects.filter(statut=Membre.StatutMembre.ACTIF).count(),
            'total_bons': Bon.objects.count(),
            'bons_valides': Bon.objects.filter(statut='VALIDE').count(),
            'bons_attente': Bon.objects.filter(statut='ATTENTE').count(),
            'montant_total_bons': Bon.objects.aggregate(total=Sum('montant_total'))['total'] or 0,
            'cout_total_valides': Bon.objects.filter(statut='VALIDE').aggregate(total=Sum('montant_total'))['total'] or 0,
            'paiements_total': Paiement.objects.count(),
            'paiements_payes': Paiement.objects.filter(statut='PAYE').count(),
            'paiements_attente': Paiement.objects.filter(statut='EN_ATTENTE').count(),
            'montant_paiements_payes': Paiement.objects.filter(statut='PAYE').aggregate(total=Sum('montant'))['total'] or 0,
            'taux_remboursement': Bon.objects.filter(statut='VALIDE').aggregate(avg_taux=Avg('taux_remboursement'))['avg_taux'] or 0,
        }
        
        # Derniers éléments
        stats['derniers_bons'] = Bon.objects.all().order_by('-date_creation')[:5]
        stats['derniers_paiements'] = Paiement.objects.all().order_by('-date_paiement')[:5]
        stats['derniers_soins'] = Bon.objects.all().order_by('-date_soins')[:5]
        
        return stats
        
    except Exception as e:
        logger.error(f"Erreur dans get_assureur_stats: {e}")
        return get_default_stats()

def get_rapport_stats():
    """
    Récupère les statistiques pour les rapports
    """
    try:
        stats = {
            'total_membres': Membre.objects.count(),
            'membres_actifs': Membre.objects.filter(statut=Membre.StatutMembre.ACTIF).count(),
            'total_bons': Bon.objects.count(),
            'bons_valides': Bon.objects.filter(statut='VALIDE').count(),
            'total_cotisations': Paiement.objects.filter(
                type_paiement='COTISATION', 
                statut='VALIDE'
            ).aggregate(total=Sum('montant'))['total'] or 0,
            'total_remboursements': Bon.objects.filter(statut='REMBOURSE').aggregate(
                total=Sum('montant_rembourse')
            )['total'] or 0,
        }
        
        # Bons par statut
        stats['bons_par_statut'] = Bon.objects.values('statut').annotate(
            count=Count('id'),
            montant_total=Sum('montant_total')
        )
        
        # Membres par catégorie
        stats['membres_par_categorie'] = Membre.objects.values('categorie').annotate(
            count=Count('id')
        )
        
        # Évolution mensuelle (6 derniers mois)
        six_mois_avant = timezone.now() - timedelta(days=180)
        stats['cotisations_mensuelles'] = Paiement.objects.filter(
            date_paiement__gte=six_mois_avant,
            type_paiement='COTISATION',
            statut='VALIDE'
        ).extra({
            'mois': "strftime('%%Y-%%m', date_paiement)"
        }).values('mois').annotate(
            total=Sum('montant'),
            count=Count('id')
        ).order_by('mois')
        
        return stats
        
    except Exception as e:
        logger.error(f"Erreur dans get_rapport_stats: {e}")
        return get_default_rapport_stats()

def get_default_stats():
    """
    Retourne des statistiques par défaut en cas d'erreur
    """
    return {
        'total_membres': 0,
        'membres_actifs': 0,
        'total_bons': 0,
        'bons_valides': 0,
        'bons_attente': 0,
        'montant_total_bons': 0,
        'cout_total_valides': 0,
        'paiements_total': 0,
        'paiements_payes': 0,
        'paiements_attente': 0,
        'montant_paiements_payes': 0,
        'taux_remboursement': 0,
        'derniers_bons': [],
        'derniers_paiements': [],
        'derniers_soins': [],
    }

def get_default_rapport_stats():
    """
    Retourne des statistiques de rapport par défaut en cas d'erreur
    """
    return {
        'total_membres': 0,
        'membres_actifs': 0,
        'total_bons': 0,
        'bons_valides': 0,
        'total_cotisations': 0,
        'total_remboursements': 0,
        'bons_par_statut': [],
        'membres_par_categorie': [],
        'cotisations_mensuelles': [],
    }

def format_currency(amount):
    """
    Formate un montant en devise
    """
    try:
        return f"{amount:,.2f} €".replace(',', ' ').replace('.', ',')
    except (TypeError, ValueError):
        return "0,00 €"

def format_percentage(value):
    """
    Formate un pourcentage
    """
    try:
        return f"{float(value):.1f} %"
    except (TypeError, ValueError):
        return "0,0 %"

def get_date_range(days=30):
    """
    Retourne une plage de dates pour les filtres
    """
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date

def validate_user_access(user, required_type):
    """
    Valide l'accès d'un utilisateur selon le type requis
    Version FIABLE avec vérifications en base
    """
    type_functions = {
        'assureur': is_assureur,
        'medecin': is_medecin,
        'pharmacien': is_pharmacien,
        'membre': is_membre,
    }
    
    if required_type in type_functions:
        return type_functions[required_type](user)
    
    return False

def get_dashboard_context(user, user_type=None):
    """
    Retourne le contexte de base pour les dashboards
    """
    if not user_type:
        user_type = get_user_type(user)
    
    context = {
        'user': user,
        'user_type': user_type,
        'current_year': timezone.now().year,
        'app_name': 'Mutuelle Core',
    }
    
    # Ajouter des statistiques spécifiques selon le type
    if user_type == 'assureur':
        stats = get_assureur_stats()
        context.update(stats)
    
    return context

# Fonctions de compatibilité - NE PAS UTILISER (maintenues pour compatibilité)
def old_is_assureur(user):
    """ANCIENNE VERSION - NE PAS UTILISER (maintenue pour compatibilité)"""
    logger.warning(f"Utilisation de l'ancienne fonction is_assureur pour {user.username}")
    return (
        user.groups.filter(name='assureur').exists() or 
        user.is_superuser or
        hasattr(user, 'assureur')
    )

def old_is_medecin(user):
    """ANCIENNE VERSION - NE PAS UTILISER (maintenue pour compatibilité)"""
    logger.warning(f"Utilisation de l'ancienne fonction is_medecin pour {user.username}")
    return (
        user.groups.filter(name='medecin').exists() or 
        user.is_superuser or
        hasattr(user, 'medecin')
    )

def old_is_pharmacien(user):
    """ANCIENNE VERSION - NE PAS UTILISER (maintenue pour compatibilité)"""
    logger.warning(f"Utilisation de l'ancienne fonction is_pharmacien pour {user.username}")
    return (
        user.groups.filter(name='pharmacien').exists() or 
        user.is_superuser or
        hasattr(user, 'pharmacien')
    )

def old_is_membre(user):
    """ANCIENNE VERSION - NE PAS UTILISER (maintenue pour compatibilité)"""
    logger.warning(f"Utilisation de l'ancienne fonction is_membre pour {user.username}")
    return (
        user.groups.filter(name='membre').exists() or 
        user.is_superuser or
        hasattr(user, 'membre')
    )