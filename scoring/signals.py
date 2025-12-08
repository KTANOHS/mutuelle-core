from django.db.models.signals import post_save
from django.dispatch import receiver
from membres.models import Membre
from agents.models import VerificationCotisation
from scoring.calculators import CalculateurScoreMembre
# from ia_detection.services import analyser_verification_ia  # À décommenter après déploiement IA

@receiver(post_save, sender=VerificationCotisation)
def recalculer_score_apres_verification(sender, instance, created, **kwargs):
    """Recalcule le score après chaque nouvelle vérification"""
    try:
        if created:
            calculateur = CalculateurScoreMembre()
            calculateur.calculer_score_complet(instance.membre)
            
            # Analyser aussi avec l'IA
            analyser_verification_ia(instance)
    except Exception as e:
        print(f"❌ Erreur recalcul score: {e}")

@receiver(post_save, sender=Membre)
def initialiser_score_nouveau_membre(sender, instance, created, **kwargs):
    """Initialise le score pour un nouveau membre"""
    if created:
        try:
            calculateur = CalculateurScoreMembre()
            calculateur.calculer_score_complet(instance)
        except Exception as e:
            print(f"❌ Erreur initialisation score: {e}")
