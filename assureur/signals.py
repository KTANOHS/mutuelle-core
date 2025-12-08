from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import BonDeSoin, HistoriqueActionAssureur
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=BonDeSoin)
def bon_soin_post_save(sender, instance, created, **kwargs):
    """Log les actions sur les bons de soin"""
    try:
        if created:
            action_type = HistoriqueActionAssureur.TypeAction.CREATION_BON
            description = f"Création du bon {instance.numero_bon} pour {instance.membre.nom_complet}"
        else:
            action_type = HistoriqueActionAssureur.TypeAction.MODIFICATION_BON
            description = f"Modification du bon {instance.numero_bon}"

        # Loguer l'action
        HistoriqueActionAssureur.logger_action(
            assureur=instance.assureur,
            type_action=action_type,
            description=description,
            bon=instance
        )
    except Exception as e:
        logger.error(f"Erreur lors du logging de l'action: {e}")

@receiver(pre_save, sender=BonDeSoin)
def bon_soin_pre_save(sender, instance, **kwargs):
    """Validation avant sauvegarde d'un bon"""
    if not instance.numero_bon:
        instance.numero_bon = instance._generer_numero_bon()