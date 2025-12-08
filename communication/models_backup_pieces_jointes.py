# communication/models.py - VERSION FINALE CORRIGÉE
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Conversation(models.Model):
    """Modèle pour gérer les conversations entre utilisateurs"""
    participants = models.ManyToManyField(User, related_name='conversations')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_modification']
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
    
    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    """Modèle pour les messages entre utilisateurs"""
    TYPE_MESSAGE = [
        ('NOTIFICATION', 'Notification'),
        ('ALERTE', 'Alerte'), 
        ('MESSAGE', 'Message'),
        ('BON_SOIN', 'Bon de Soin'),
        ('DOCUMENT', 'Document'),
    ]
    
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_recus')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    titre = models.CharField(max_length=200, blank=True)
    contenu = models.TextField()
    type_message = models.CharField(max_length=20, choices=TYPE_MESSAGE, default='MESSAGE')
    date_envoi = models.DateTimeField(auto_now_add=True)
    est_lu = models.BooleanField(default=False)
    date_lecture = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date_envoi']
        verbose_name = "Message"
        verbose_name_plural = "Messages"
    
    def __str__(self):
        return f"Message {self.id}"

class Notification(models.Model):
    """Modèle pour les notifications système"""
    TYPE_NOTIFICATION = [
        ('INFO', 'Information'),
        ('ALERTE', 'Alerte'),
        ('SUCCES', 'Succès'), 
        ('ERREUR', 'Erreur'),
        ('BON_SOIN', 'Bon de Soin'),
        ('RDV', 'Rendez-vous'),
        ('PAIEMENT', 'Paiement'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    titre = models.CharField(max_length=200)
    message = models.TextField()
    type_notification = models.CharField(max_length=50, choices=TYPE_NOTIFICATION, default='INFO')
    est_lue = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_lecture = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
    
    def __str__(self):
        return f"Notification {self.id}"
class PieceJointe(models.Model):
    """Modèle pour gérer les pièces jointes des messages"""
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='pieces_jointes')
    fichier = models.FileField(upload_to='pieces_jointes/')
    nom_original = models.CharField(max_length=255)
    date_upload = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Pièce jointe"
        verbose_name_plural = "Pièces jointes"
    
    def __str__(self):
        return self.nom_original
