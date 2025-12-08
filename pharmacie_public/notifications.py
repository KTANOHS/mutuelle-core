# pharmacie_public/notifications.py
from django.core.mail import send_mail
from django.conf import settings

def envoyer_notification_commande(commande):
    """Envoie une notification pour une nouvelle commande"""
    sujet = f"Nouvelle commande #{commande.numero_commande}"
    message = f"""
    Nouvelle commande reçue !
    
    Numéro: {commande.numero_commande}
    Client: {commande.client.get_full_name() or commande.client.username}
    Montant: {commande.montant_total} €
    
    Connectez-vous pour traiter la commande.
    """
    
    send_mail(
        sujet,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [commande.pharmacie.user.email],
        fail_silently=False,
    )

def envoyer_confirmation_commande(commande):
    """Envoie une confirmation au client"""
    sujet = f"Confirmation de commande #{commande.numero_commande}"
    message = f"""
    Votre commande a été confirmée !
    
    Numéro: {commande.numero_commande}
    Pharmacie: {commande.pharmacie.nom_pharmacie}
    Statut: {commande.get_statut_display()}
    
    Merci pour votre confiance.
    """
    
    send_mail(
        sujet,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [commande.client.email],
        fail_silently=False,
    )