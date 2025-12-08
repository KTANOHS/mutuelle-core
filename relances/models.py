from django.db import models
from membres.models import Membre
from django.utils import timezone

class TemplateRelance(models.Model):
    nom = models.CharField(max_length=100)
    type_relance = models.CharField(
        max_length=50,
        choices=[
            ('premier_rappel', 'Premier rappel'),
            ('relance_urgente', 'Relance urgente'),
            ('suspension_imminente', 'Suspension imminente'),
        ]
    )
    sujet = models.CharField(max_length=200)
    template_html = models.TextField()
    template_texte = models.TextField()
    delai_jours = models.IntegerField(default=7)
    
    class Meta:
        verbose_name = "Template Relance"
        verbose_name_plural = "Templates Relance"
    
    def __str__(self):
        return f"{self.nom} ({self.type_relance})"

class RelanceProgrammee(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    template = models.ForeignKey(TemplateRelance, on_delete=models.CASCADE)
    date_programmation = models.DateTimeField(default=timezone.now)
    date_envoi = models.DateTimeField(null=True, blank=True)
    envoyee = models.BooleanField(default=False)
    statut = models.CharField(
        max_length=20,
        choices=[
            ('programmee', 'Programmée'),
            ('envoyee', 'Envoyée'),
            ('erreur', 'Erreur'),
            ('annulee', 'Annulée'),
        ],
        default='programmee'
    )
    
    class Meta:
        verbose_name = "Relance Programmee"
        verbose_name_plural = "Relances Programmees"
        ordering = ['-date_programmation']
    
    def __str__(self):
        return f"Relance {self.template.nom} - {self.membre}"
