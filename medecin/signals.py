# medecin/signals.py - CRÉER CE FICHIER
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Medecin

@receiver(post_save, sender=User)
def assign_medecin_profile(sender, instance, created, **kwargs):
    """Attribue automatiquement un profil médecin"""
    if created and instance.groups.filter(name='medecin').exists():
        # Logique de création automatique
        pass