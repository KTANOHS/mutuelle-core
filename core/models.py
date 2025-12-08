from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


# Modèle proxy pour Session avec méthode __str__
from django.contrib.sessions.models import Session as BaseSession

class Session(BaseSession):
    class Meta:
        proxy = True
        
    def __str__(self):
        return f"Session {self.session_key} - {self.expire_date.strftime('%Y-%m-%d %H:%M')}"




class PartageAutomatique(models.Model):
    """Gestion centralisée des permissions de partage - VERSION CORRIGÉE"""
    ORDONNANCE = 'ORD'
    BON = 'BON'
    TYPE_CHOICES = [
        (ORDONNANCE, 'Ordonnance'),
        (BON, 'Bon'),
    ]
    
    type_document = models.CharField(max_length=3, choices=TYPE_CHOICES)
    document_id = models.PositiveIntegerField()  # ID de l'ordonnance ou du bon
    
    # 🔥 CORRECTION : Retirer l'index sur ManyToManyField
    visible_par = models.ManyToManyField(User, related_name='documents_visibles')
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        # 🔥 CORRECTION : Supprimer l'index sur le ManyToManyField
        indexes = [
            models.Index(fields=['type_document', 'document_id']),
            # ❌ SUPPRIMER : models.Index(fields=['visible_par']),
        ]
        unique_together = ['type_document', 'document_id']
    
    def __str__(self):
        return f"Partage {self.type_document}-{self.document_id}"

class Notification(models.Model):
    """Système de notifications pour les nouveaux documents - VERSION CORRIGÉE"""
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    type_document = models.CharField(max_length=3, choices=PartageAutomatique.TYPE_CHOICES)
    document_id = models.PositiveIntegerField()
    lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['utilisateur', 'lu']),
            models.Index(fields=['type_document', 'document_id']),
        ]
    
    def __str__(self):
        return f"Notification pour {self.utilisateur}"