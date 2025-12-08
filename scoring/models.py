from django.db import models
from membres.models import Membre
from django.utils import timezone

class HistoriqueScore(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    niveau_risque = models.CharField(max_length=20)
    details_calcul = models.JSONField(default=dict)
    date_calcul = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Historique Score"
        verbose_name_plural = "Historiques Scores"
        ordering = ['-date_calcul']
    
    def __str__(self):
        return f"Score {self.score} - {self.membre}"

class RegleScoring(models.Model):
    nom = models.CharField(max_length=100)
    critere = models.CharField(max_length=200)
    poids = models.DecimalField(max_digits=4, decimal_places=2)
    est_active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Règle Scoring"
        verbose_name_plural = "Règles Scoring"
        ordering = ['-poids']
    
    def __str__(self):
        return f"{self.nom} (poids: {self.poids})"
