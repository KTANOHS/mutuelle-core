from django.db import models
from membres.models import Membre
from agents.models import VerificationCotisation
from django.utils import timezone

class ModeleIA(models.Model):
    nom = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    type_modele = models.CharField(
        max_length=50,
        choices=[
            ('detection_fraude', 'Détection de fraude'),
            ('scoring_risque', 'Scoring de risque'),
            ('prediction_retard', 'Prédiction de retard'),
        ]
    )
    fichier_modele = models.FileField(upload_to='modeles_ia/', null=True, blank=True)
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    date_entrainement = models.DateTimeField(default=timezone.now)
    est_actif = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Modèle IA"
        verbose_name_plural = "Modèles IA"
    
    def __str__(self):
        return f"{self.nom} v{self.version}"

class AnalyseIA(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    verification = models.ForeignKey(VerificationCotisation, on_delete=models.CASCADE, null=True, blank=True)
    type_analyse = models.CharField(max_length=50)
    score_confiance = models.DecimalField(max_digits=5, decimal_places=2)
    resultat = models.JSONField(default=dict)
    date_analyse = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Analyse IA"
        verbose_name_plural = "Analyses IA"
        ordering = ['-date_analyse']
    
    def __str__(self):
        return f"Analyse {self.type_analyse} - {self.membre}"
