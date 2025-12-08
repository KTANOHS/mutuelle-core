# communication/services.py - VERSION FINALE
from django.db import transaction
from django.contrib.auth.models import User
from .models import Conversation, Message, Notification
from datetime import datetime
import logging

logger = logging.getLogger('communication')

class MessagerieService:
    """Service de gestion de la messagerie"""
    
    @staticmethod
    def envoyer_message(expediteur_id, destinataire_ids, contenu, titre="", type_message="MESSAGE"):
        """Envoyer un message à un ou plusieurs destinataires"""
        try:
            with transaction.atomic():
                expediteur = User.objects.get(id=expediteur_id)
                destinataires = User.objects.filter(id__in=destinataire_ids)
                
                # Créer une conversation
                conversation = Conversation.objects.create()
                conversation.participants.add(expediteur)
                for dest in destinataires:
                    conversation.participants.add(dest)
                
                # Créer le message pour chaque destinataire
                for destinataire in destinataires:
                    message = Message.objects.create(
                        expediteur=expediteur,
                        destinataire=destinataire,
                        conversation=conversation,
                        titre=titre,
                        contenu=contenu,
                        type_message=type_message
                    )
                
                logger.info(f"Message envoyé: {expediteur.username} -> {len(destinataires)} destinataire(s)")
                return message
                
        except Exception as e:
            logger.error(f"Erreur envoi message: {e}")
            return None

class NotificationService:
    """Service de gestion des notifications"""
    
    @staticmethod
    def creer_notification(utilisateur_id, titre, message, type_notification="INFO"):
        """Créer une notification"""
        try:
            utilisateur = User.objects.get(id=utilisateur_id)
            notification = Notification.objects.create(
                user=utilisateur,
                titre=titre,
                message=message,
                type_notification=type_notification
            )
            logger.info(f"Notification créée: {titre}")
            return notification
        except Exception as e:
            logger.error(f"Erreur création notification: {e}")
            return None