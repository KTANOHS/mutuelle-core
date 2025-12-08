# assureur/services.py
import logging
from django.utils import timezone
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

class BonService:
    """
    Service pour la gestion des bons de soin
    Version robuste avec gestion d'erreurs complète
    """
    
    @staticmethod
    def creer_bon_soin(membre, user, type_soin, request=None, **kwargs):
        """
        Crée un nouveau bon de soin avec validation
        """
        try:
            # Import dans la méthode pour éviter les dépendances circulaires
            from soins.models import BonDeSoin
            from django.contrib import messages
            
            logger.info(f"Tentative création bon pour {membre.numero_unique} par {user.username}")
            
            # Validation des paramètres
            if not membre:
                error_msg = "Membre non spécifié"
                logger.error(error_msg)
                if request:
                    messages.error(request, error_msg)
                return False, error_msg, None
                
            if not type_soin:
                error_msg = "Le type de soin est obligatoire"
                logger.error(error_msg)
                if request:
                    messages.error(request, error_msg)
                return False, error_msg, None
            
            # Vérifier que le membre est à jour (si la méthode existe)
            if hasattr(membre, 'est_a_jour') and not membre.est_a_jour():
                error_msg = "Le membre n'est pas à jour de ses cotisations"
                logger.warning(error_msg)
                if request:
                    messages.error(request, error_msg)
                return False, error_msg, None
            
            # Préparer les données du bon
            bon_data = {
                'membre': membre,
                'assureur': user,
                'type_soin': type_soin,
                'date_emission': timezone.now(),
                'statut': 'EMIS',
            }
            
            # Ajouter les kwargs supplémentaires
            bon_data.update(kwargs)
            
            # Création du bon
            bon = BonDeSoin.objects.create(**bon_data)
            
            success_msg = f"Bon de soin {getattr(bon, 'numero_bon', 'N°' + str(bon.id))} créé avec succès!"
            logger.info(f"Bon {bon.id} créé avec succès pour {membre.nom_complet}")
            
            if request:
                messages.success(request, success_msg)
            
            return True, success_msg, bon
            
        except Exception as e:
            error_msg = f"Erreur lors de la création du bon: {str(e)}"
            logger.error(error_msg, exc_info=True)
            if request:
                from django.contrib import messages
                messages.error(request, error_msg)
            return False, error_msg, None
    
    @staticmethod
    def annuler_bon(bon_id, user, raison=""):
        """
        Annule un bon de soin avec vérification des permissions
        """
        try:
            from soins.models import BonDeSoin
            
            bon = BonDeSoin.objects.get(id=bon_id)
            
            # Vérification des permissions
            if bon.assureur != user and not user.is_superuser:
                logger.warning(f"Tentative d'annulation non autorisée par {user.username} sur le bon {bon_id}")
                return False, "Vous n'avez pas la permission d'annuler ce bon"
            
            # Vérifier que le bon peut être annulé
            if bon.statut not in ['EMIS', 'EN_ATTENTE']:
                return False, f"Impossible d'annuler un bon avec le statut '{bon.statut}'"
            
            # Annulation du bon
            ancien_statut = bon.statut
            bon.statut = 'ANNULE'
            
            if raison:
                observations = getattr(bon, 'observations', '')
                bon.observations = f"ANNULÉ le {timezone.now().strftime('%d/%m/%Y %H:%M')} - Raison: {raison}\n{observations}"
            
            bon.save()
            
            logger.info(f"Bon {bon_id} annulé par {user.username}. Ancien statut: {ancien_statut}")
            return True, f"Bon {getattr(bon, 'numero_bon', 'N°' + str(bon.id))} annulé avec succès"
            
        except BonDeSoin.DoesNotExist:
            error_msg = f"Bon avec l'ID {bon_id} non trouvé"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Erreur lors de l'annulation du bon: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return False, error_msg
    
    @staticmethod
    def get_bons_crees_ce_mois(user):
        """Retourne le nombre de bons créés ce mois par l'utilisateur"""
        try:
            from soins.models import BonDeSoin
            debut_mois = timezone.now().replace(day=1, hour=0, minute=0, second=0)
            return BonDeSoin.objects.filter(
                assureur=user,
                date_emission__gte=debut_mois
            ).count()
        except Exception as e:
            logger.error(f"Erreur get_bons_crees_ce_mois: {e}")
            return 0
    
    @staticmethod
    def get_derniers_bons(limit=5):
        """Retourne les derniers bons créés"""
        try:
            from soins.models import BonDeSoin
            return BonDeSoin.objects.select_related('membre').order_by('-date_emission')[:limit]
        except Exception as e:
            logger.error(f"Erreur get_derniers_bons: {e}")
            return []
    
    @staticmethod
    def get_bons_actifs_par_membre(membre):
        """Retourne le nombre de bons actifs d'un membre"""
        try:
            from soins.models import BonDeSoin
            return BonDeSoin.objects.filter(patient=membre, statut='EMIS').count()
        except Exception as e:
            logger.error(f"Erreur get_bons_actifs_par_membre: {e}")
            return 0
    
    @staticmethod
    def get_bons_utilises_par_membre(membre):
        """Retourne le nombre de bons utilisés d'un membre"""
        try:
            from soins.models import BonDeSoin
            return BonDeSoin.objects.filter(patient=membre, statut='UTILISE').count()
        except Exception as e:
            logger.error(f"Erreur get_bons_utilises_par_membre: {e}")
            return 0

class ResponseHandler:
    """
    Gestionnaire de réponses standardisées pour les vues
    """
    
    @staticmethod
    def handle_ajax_response(request, success, message, data=None, redirect_url=None):
        """
        Retourne une réponse JSON standardisée
        """
        response_data = {
            'success': success,
            'message': message,
            'data': data or {}
        }
        
        if redirect_url:
            response_data['redirect_url'] = redirect_url
            
        return response_data
    
    @staticmethod
    def handle_template_response(request, success, message, template, context, redirect_url=None):
        """
        Gère les réponses template avec messages
        """
        from django.contrib import messages
        from django.shortcuts import render, redirect
        
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
            
        if redirect_url:
            return redirect(redirect_url)
        else:
            return render(request, template, context)

# Test que le module se charge correctement
logger.info("Module assureur.services chargé avec succès")