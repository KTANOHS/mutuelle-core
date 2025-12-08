# soins/models.py - VERSION COMPLÈTE CORRIGÉE
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class TypeSoin(models.Model):
    """Modèle pour les types de soins médicaux"""
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    prix_reference = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Type de soin"
        verbose_name_plural = "Types de soins"

class Soin(models.Model):
    """Modèle principal pour les soins médicaux"""
    STATUT_CHOICES = [
        ('attente', 'En attente'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
        ('termine', 'Terminé'),
    ]

    # Relations principales
    patient = models.ForeignKey('membres.Membre', on_delete=models.CASCADE, related_name='soins')
    type_soin = models.ForeignKey('TypeSoin', on_delete=models.PROTECT)
    medecin = models.ForeignKey(
        'auth.User', 
        on_delete=models.PROTECT, 
        limit_choices_to={'groups__name': 'Medecin'}
    )
    
    # Dates
    date_soin = models.DateTimeField(auto_now_add=True)
    date_realisation = models.DateField()
    
    # Informations médicales
    diagnostic = models.TextField()
    observations = models.TextField(blank=True)
    duree_sejour = models.PositiveIntegerField(
        default=0, 
        help_text="Durée en jours",
        blank=True,
        null=True
    )
    
    # Informations financières
    cout_estime = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True
    )
    cout_reel = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    taux_prise_charge = models.PositiveIntegerField(
        default=80,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Pourcentage pris en charge par l'assureur",
        blank=True,
        null=True
    )
    
    # Validation et statut
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='attente')
    valide_par = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='soins_valides',
        limit_choices_to={'groups__name': 'Assureur'}
    )
    date_validation = models.DateTimeField(null=True, blank=True)
    motif_refus = models.TextField(blank=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='soins_crees'
    )

    def __str__(self):
        return f"Soin {self.type_soin.nom} - {self.patient} - {self.date_realisation}"

    class Meta:
        verbose_name = "Soin"
        verbose_name_plural = "Soins"
        ordering = ['-date_realisation']

class Prescription(models.Model):
    """Modèle pour les prescriptions médicales"""
    soin = models.ForeignKey('Soin', on_delete=models.CASCADE, related_name='prescriptions')
    medicament = models.CharField(max_length=200)
    posologie = models.CharField(max_length=100)
    duree_traitement = models.PositiveIntegerField(help_text="Durée en jours")
    instructions = models.TextField(blank=True)
    date_prescription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicament} - {self.soin}"

    class Meta:
        verbose_name = "Prescription"
        verbose_name_plural = "Prescriptions"

class DocumentSoin(models.Model):
    """Modèle pour les documents associés aux soins"""
    TYPE_DOCUMENT_CHOICES = [
        ('ordonnance', 'Ordonnance'),
        ('resultat', 'Résultat d\'analyse'),
        ('compte_rendu', 'Compte-rendu'),
        ('facture', 'Facture'),
        ('autre', 'Autre'),
    ]

    soin = models.ForeignKey('Soin', on_delete=models.CASCADE, related_name='documents')
    type_document = models.CharField(max_length=20, choices=TYPE_DOCUMENT_CHOICES)
    fichier = models.FileField(upload_to='documents/soins/')
    nom = models.CharField(max_length=200)
    date_upload = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} - {self.soin}"

    class Meta:
        verbose_name = "Document de soin"
        verbose_name_plural = "Documents de soin"

class BonDeSoin(models.Model):
    """Modèle pour les bons de soin"""
    STATUT_CHOICES = [
        ('attente', 'En attente'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
    ]
    
    patient = models.ForeignKey(
        'membres.Membre', 
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    medecin = models.ForeignKey(
        'auth.User', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        limit_choices_to={'groups__name': 'Medecin'}
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_soin = models.DateField(default=timezone.now)
    symptomes = models.TextField(default="")
    diagnostic = models.TextField(default="")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='attente')
    montant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"Bon de soin {self.id} - {self.patient}"

    class Meta:
        verbose_name = "Bon de soin"
        verbose_name_plural = "Bons de soin"
        ordering = ['-date_creation']

class Ordonnance(models.Model):
    """Modèle pour les ordonnances médicales"""
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
        ('termine', 'Terminé'),
    ]
    
    bon_de_soin = models.ForeignKey(
        'BonDeSoin', 
        on_delete=models.CASCADE, 
        related_name='ordonnances',
        null=True,
        blank=True
    )
    medicament = models.CharField(max_length=200)
    posologie = models.CharField(max_length=100)
    duree = models.CharField(max_length=100, null=True, blank=True)
    instructions = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default='en_attente'
    )
    
    date_validation = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Ordonnance"
        verbose_name_plural = "Ordonnances"
        ordering = ['-date_creation']

    def __str__(self):
        return f"Ordonnance {self.id} - {self.medicament}"
    
    @property
    def patient(self):
        return self.bon_de_soin.patient if self.bon_de_soin else None
    
    @property
    def medecin(self):
        return self.bon_de_soin.medecin if self.bon_de_soin else None

