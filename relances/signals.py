from django.db.models.signals import post_save
from django.dispatch import receiver
from membres.models import Membre
from agents.models import VerificationCotisation
from relances.services import ServiceRelances

@receiver(post_save, sender=VerificationCotisation)
def verifier_relance_apres_verification(sender, instance, created, **kwargs):
    """Vérifie si une relance est nécessaire après mise à jour vérification"""
    if created or instance.jours_retard > 0:
        try:
            service = ServiceRelances()
            service.planifier_relances_automatiques()
        except Exception as e:
            print(f"❌ Erreur vérification relances: {e}")
