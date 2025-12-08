from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class Paiement(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('PAYE', 'Payé'),
        ('ANNULE', 'Annulé'),
        ('ECHEC', 'Échec'),
        ('REMBOURSE', 'Remboursé'),
    ]
    
    MODE_PAIEMENT_CHOICES = [
        ('VIREMENT', 'Virement bancaire'),
        ('CHEQUE', 'Chèque'),
        ('ESPECES', 'Espèces'),
        ('CARTE', 'Carte bancaire'),
        ('MOBILE', 'Paiement mobile'),
        ('AUTRE', 'Autre'),
    ]

    # Relations
    bon = models.ForeignKey(
        'assureur.BonPriseEnCharge', 
        on_delete=models.CASCADE,
        related_name='paiements',
        verbose_name="Bon de prise en charge"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='paiements_crees',
        verbose_name="Créé par"
    )

    # Informations de paiement
    montant = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Montant payé"
    )
    date_paiement = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date du paiement"
    )
    mode_paiement = models.CharField(
        max_length=20,
        choices=MODE_PAIEMENT_CHOICES,
        default='VIREMENT',
        verbose_name="Mode de paiement"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='EN_ATTENTE',
        verbose_name="Statut du paiement"
    )

    # Références et métadonnées
    reference = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Référence du paiement"
    )
    numero_transaction = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Numéro de transaction"
    )
    banque = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Banque émettrice"
    )
    date_valeur = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date de valeur"
    )

    # Informations supplémentaires
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes internes"
    )
    preuve_paiement = models.FileField(
        upload_to='paiements/preuves/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Preuve de paiement"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ['-date_paiement']
        indexes = [
            models.Index(fields=['statut']),
            models.Index(fields=['date_paiement']),
            models.Index(fields=['reference']),
        ]

    def __str__(self):
        return f"Paiement {self.reference} - {self.montant} FCFA"

    def save(self, *args, **kwargs):
        if not self.reference:
            # Générer une référence automatique
            annee = timezone.now().year
            dernier_paiement = Paiement.objects.filter(
                date_creation__year=annee
            ).count() + 1
            self.reference = f"PAY-{annee}-{dernier_paiement:06d}"
        
        super().save(*args, **kwargs)

    def marquer_comme_paye(self):
        """Marquer le paiement comme payé"""
        self.statut = 'PAYE'
        self.date_paiement = timezone.now()
        self.save()

    def marquer_comme_annule(self):
        """Annuler le paiement"""
        self.statut = 'ANNULE'
        self.save()

    @property
    def est_paye(self):
        return self.statut == 'PAYE'

    @property
    def est_en_attente(self):
        return self.statut == 'EN_ATTENTE'

    @property
    def beneficiaire(self):
        """Retourne le bénéficiaire du paiement"""
        return self.bon.membre.user.get_full_name()

    @property
    def montant_attendu(self):
        """Retourne le montant attendu selon le bon"""
        return self.bon.montant_prise_en_charge


class Remboursement(models.Model):
    STATUT_REMBOURSEMENT = [
        ('DEMANDE', 'Demandé'),
        ('VALIDEE', 'Validée'),
        ('REJETEE', 'Rejetée'),
        ('PAYEE', 'Payée'),
    ]

    paiement = models.OneToOneField(
        Paiement,
        on_delete=models.CASCADE,
        related_name='remboursement'
    )
    montant_rembourse = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Montant remboursé"
    )
    motif = models.TextField(
        verbose_name="Motif du remboursement"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_REMBOURSEMENT,
        default='DEMANDE'
    )
    date_demande = models.DateTimeField(auto_now_add=True)
    date_traitement = models.DateTimeField(blank=True, null=True)
    traite_par = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='remboursements_traites'
    )

    class Meta:
        verbose_name = "Remboursement"
        verbose_name_plural = "Remboursements"

    def __str__(self):
        return f"Remboursement {self.paiement.reference}"


class HistoriquePaiement(models.Model):
    """Historique des modifications des paiements"""
    paiement = models.ForeignKey(
        Paiement,
        on_delete=models.CASCADE,
        related_name='historique'
    )
    ancien_statut = models.CharField(max_length=20)
    nouveau_statut = models.CharField(max_length=20)
    modifie_par = models.ForeignKey(User, on_delete=models.CASCADE)
    date_modification = models.DateTimeField(auto_now_add=True)
    motif = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Historique de paiement"
        verbose_name_plural = "Historiques de paiements"
        ordering = ['-date_modification']

    def __str__(self):
        return f"Historique {self.paiement.reference}"