# notifications/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Notification(models.Model):
    TYPE_CHOICES = [
        ('INFO', 'Information'),
        ('ALERT', 'Alerte'), 
        ('SUCCESS', 'Succès'),
        ('WARNING', 'Avertissement'),
        ('SYSTEM', 'Système'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications')
    titre = models.CharField(max_length=200)
    message = models.TextField()
    type_notification = models.CharField(max_length=10, choices=TYPE_CHOICES, default='INFO')
    lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_lu = models.DateTimeField(null=True, blank=True)
    lien = models.URLField(blank=True, null=True)
    data_json = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['user', 'lu']),
            models.Index(fields=['date_creation']),
            models.Index(fields=['type_notification']),
        ]
    
    def __str__(self):
        return f"{self.titre} - {self.user.username}"
    
    def marquer_comme_lu(self):
        if not self.lu:
            self.lu = True
            self.date_lu = timezone.now()
            self.save()

class PreferenceNotification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_preferences_notifications')
    email_actif = models.BooleanField(default=True)
    push_actif = models.BooleanField(default=True)
    sms_actif = models.BooleanField(default=False)
    notifications_systeme = models.BooleanField(default=True)
    notifications_soins = models.BooleanField(default=True)
    notifications_paiements = models.BooleanField(default=True)
    notifications_alertes = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Préférences de {self.user.username}"