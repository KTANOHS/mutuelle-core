"""
assureur/models.py - VERSION DÉFINITIVE CORRIGÉE
Utilise le modèle Membre d'agents.models sans créer de doublon
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import date, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
import logging
import uuid

logger = logging.getLogger(__name__)

# ==========================================================================
# IMPORT UNIQUE : Utiliser le Membre d'agents.models
# ==========================================================================

# IMPORT CRITIQUE : NE PAS créer de modèle Membre ici, utiliser celui d'agents
from agents.models import Membre

# ==========================================================================
# MODÈLE ASSUREUR (employés de l'assurance)
# ==========================================================================

class Assureur(models.Model):
    """Modèle pour les employés de l'assurance"""
    
    DEPARTEMENT_CHOICES = [
        ('gestion', 'Gestion des membres'),
        ('claims', 'Traitement des réclamations'),
        ('paiements', 'Service des paiements'),
        ('admin', 'Administration'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='assureur_profile'
    )
    
    numero_employe = models.CharField(max_length=20, unique=True)
    departement = models.CharField(max_length=100, choices=DEPARTEMENT_CHOICES)
    date_embauche = models.DateField(default=date.today)
    est_actif = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Assureur"
        verbose_name_plural = "Assureurs"
        ordering = ['user__last_name', 'user__first_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.numero_employe})"
    
    @property
    def nom(self):
        """Retourne le nom complet de l'utilisateur"""
        return self.user.get_full_name() or self.user.username
    
    @property
    def email(self):
        """Retourne l'email de l'utilisateur"""
        return self.user.email
    
    @property
    def prenom(self):
        """Retourne le prénom de l'utilisateur"""
        return self.user.first_name
    
    @property
    def nom_famille(self):
        """Retourne le nom de famille de l'utilisateur"""
        return self.user.last_name
    
    def nom_complet(self):
        """Méthode alternative pour compatibilité"""
        return self.nom
    
    def anciennete(self):
        """Calcule l'ancienneté en années"""
        today = date.today()
        return today.year - self.date_embauche.year - (
            (today.month, today.day) < 
            (self.date_embauche.month, self.date_embauche.day)
        )


# ==========================================================================
# MODÈLES PRINCIPAUX - UTILISENT agents.models.Membre
# ==========================================================================

class Bon(models.Model):
    """Bons de prise en charge"""
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
        ('utilise', 'Utilisé'),
        ('expire', 'Expiré'),
    ]

    TYPE_SOIN_CHOICES = [
        ('consultation', 'Consultation médicale'),
        ('analyse', 'Analyse médicale'),
        ('imagerie', 'Imagerie médicale'),
        ('hospitalisation', 'Hospitalisation'),
        ('pharmacie', 'Pharmacie'),
        ('dentaire', 'Soins dentaires'),
        ('optique', 'Soins optiques'),
        ('autre', 'Autre'),
    ]

    # CRITIQUE : Utiliser directement agents.models.Membre (sans chaîne)
    membre = models.ForeignKey(
        Membre,  # ← IMPORTANT : Utiliser l'objet importé, pas une chaîne
        on_delete=models.CASCADE, 
        related_name='bons_assureur',
        verbose_name="Membre"
    )
    
    numero_bon = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Numéro de bon"
    )
    
    type_soin = models.CharField(
        max_length=50, 
        choices=TYPE_SOIN_CHOICES,
        verbose_name="Type de soin"
    )
    
    description = models.TextField(
        blank=True, 
        verbose_name="Description des soins"
    )
    
    # Montants
    montant_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Montant total"
    )
    
    montant_prise_charge = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Montant pris en charge"
    )
    
    montant_restant = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Montant restant à charge"
    )
    
    # Dates
    date_creation = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(null=True, blank=True)
    date_expiration = models.DateField()
    date_soin = models.DateField(verbose_name="Date des soins")
    
    # Statut et validation
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default='en_attente'
    )
    
    valide_par = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='bons_valides_assureur'
    )
    
    # Informations du professionnel de santé
    nom_medecin = models.CharField(
        max_length=200, 
        verbose_name="Nom du médecin/établissement"
    )
    
    specialite = models.CharField(max_length=100, blank=True)
    
    # Métadonnées
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='bons_crees_assureur'
    )
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bon de prise en charge"
        verbose_name_plural = "Bons de prise en charge"
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['numero_bon']),
            models.Index(fields=['membre', 'statut']),
            models.Index(fields=['date_soin']),
            models.Index(fields=['statut']),
        ]

    def __str__(self):
        return f"Bon {self.numero_bon} - {self.membre}"

    def save(self, *args, **kwargs):
        # Génération automatique du numéro de bon
        if not self.numero_bon:
            date_str = timezone.now().strftime('%Y%m%d')
            last_bon = Bon.objects.filter(
                numero_bon__startswith=f'BON{date_str}'
            ).count()
            self.numero_bon = f'BON{date_str}{last_bon + 1:04d}'
        
        # Calcul automatique du montant restant
        if not self.montant_restant:
            self.montant_restant = self.montant_total - self.montant_prise_charge
        
        super().save(*args, **kwargs)

    def est_valide(self):
        """Vérifie si le bon est valide"""
        return self.statut == 'valide' and self.date_expiration >= timezone.now().date()


class Soin(models.Model):
    """Soins médicaux"""
    
    STATUT_CHOICES = [
        ('soumis', 'Soumis'),
        ('en_cours', 'En cours de traitement'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
        ('paye', 'Payé'),
    ]

    # CRITIQUE : Utiliser directement agents.models.Membre
    membre = models.ForeignKey(
        Membre,  # ← IMPORTANT : Utiliser l'objet importé
        on_delete=models.CASCADE, 
        related_name='soins_assureur'
    )
    
    bon = models.ForeignKey(
        Bon, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='soins'
    )
    
    type_soin = models.CharField(max_length=100, verbose_name="Type de soin")
    description = models.TextField(verbose_name="Description détaillée")
    
    # Montants
    montant_facture = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Montant facturé"
    )
    
    montant_rembourse = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name="Montant remboursé"
    )
    
    # Dates
    date_soin = models.DateField(verbose_name="Date des soins")
    date_soumission = models.DateTimeField(auto_now_add=True)
    date_traitement = models.DateTimeField(null=True, blank=True)
    
    # Statut
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default='soumis'
    )
    
    traite_par = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assureur_soins_traites'
    )
    
    # Métadonnées
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='assureur_soins_soumis'
    )
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Soin"
        verbose_name_plural = "Soins"
        ordering = ['-date_soumission']

    def __str__(self):
        return f"Soin {self.type_soin} - {self.membre}"


class Paiement(models.Model):
    """Paiements et remboursements"""
    
    MODE_PAIEMENT_CHOICES = [
        ('virement', 'Virement bancaire'),
        ('cheque', 'Chèque'),
        ('espece', 'Espèces'),
        ('carte', 'Carte bancaire'),
        ('mobile_money', 'Paiement mobile'),
        ('autre', 'Autre'),
        
    ]

    STATUT_CHOICES = [
        ('initie', 'Initié'),
        ('valide', 'Validé'),
        ('annule', 'Annulé'),
        ('echec', 'Échec'),
        ('rembourse', 'Remboursé'),
    ]

    # CRITIQUE : Utiliser directement agents.models.Membre
    membre = models.ForeignKey(
        Membre,  # ← IMPORTANT : Utiliser l'objet importé
        on_delete=models.CASCADE, 
        related_name='paiements_assureur'
    )
    
    soin = models.ForeignKey(
        Soin, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='paiements'
    )
    
    reference = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Référence paiement"
    )
    
    mode_paiement = models.CharField(
        max_length=20, 
        choices=MODE_PAIEMENT_CHOICES
    )
    
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(default=timezone.now)
    date_validation = models.DateTimeField(null=True, blank=True)
    
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default='initie'
    )
    
    valide_par = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assureur_paiements_valides'
    )
    
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='assureur_paiements_crees'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ['-date_paiement']

    def __str__(self):
        return f"Paiement {self.reference} - {self.montant} FCFA"


class Cotisation(models.Model):
    """Cotisations mensuelles"""
    
    STATUT_CHOICES = [
        ('due', 'Due'),
        ('payee', 'Payée'),
        ('en_retard', 'En retard'),
        ('annulee', 'Annulée'),
    ]

    TYPE_COTISATION_CHOICES = [
        ('normale', 'Cotisation normale - 5000 FCFA'),
        ('femme_enceinte', 'Cotisation femme enceinte - 7500 FCFA'),
    ]

    # CRITIQUE : Utiliser directement agents.models.Membre
    membre = models.ForeignKey(
        Membre,  # ← IMPORTANT : Utiliser l'objet importé
        on_delete=models.CASCADE, 
        related_name='cotisations_assureur',
        verbose_name="Membre"
    )
    
    periode = models.CharField(max_length=7, verbose_name="Période (YYYY-MM)")
    type_cotisation = models.CharField(
        max_length=20, 
        choices=TYPE_COTISATION_CHOICES,
        default='normale'
    )
    
    montant = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Montant de la cotisation (FCFA)"
    )
    
    date_emission = models.DateField(
        auto_now_add=True, 
        verbose_name="Date d'émission"
    )
    
    date_echeance = models.DateField(verbose_name="Date d'échéance")
    date_paiement = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Date de paiement"
    )
    
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default='due'
    )
    
    reference = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Référence"
    )
    
    
    enregistre_par = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='cotisations_enregistrees',
        verbose_name="Enregistré par l'assureur"
    )
    
    notes = models.TextField(blank=True, verbose_name="Notes internes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cotisation"
        verbose_name_plural = "Cotisations"
        ordering = ['-periode', 'membre']
        unique_together = ['membre', 'periode']

    def __str__(self):
        return f"Cotisation {self.periode} - {self.membre}"

    def save(self, *args, **kwargs):
        # Génération automatique de la référence
        if not self.reference:
            date_str = timezone.now().strftime('%Y%m%d')
            last_cotisation = Cotisation.objects.filter(
                reference__startswith=f'COT{date_str}'
            ).count()
            self.reference = f'COT{date_str}{last_cotisation + 1:04d}'
        
        super().save(*args, **kwargs)


# ==========================================================================
# MODÈLES DE SUPPORT (facultatifs)
# ==========================================================================

class StatistiquesAssurance(models.Model):
    """Statistiques et indicateurs de performance"""
    periode = models.CharField(
        max_length=10, 
        unique=True, 
        verbose_name="Période (YYYY-MM)"
    )
    total_membres = models.IntegerField(default=0)
    nouveaux_membres = models.IntegerField(default=0)
    chiffre_affaires = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=0
    )
    total_remboursements = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=0
    )
    date_calcul = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Statistique assurance"
        verbose_name_plural = "Statistiques assurance"
        ordering = ['-periode']

    def __str__(self):
        return f"Statistiques {self.periode}"


class ConfigurationAssurance(models.Model):
    """Configuration du système d'assurance"""
    nom_assureur = models.CharField(max_length=200, default="Notre Assureur")
    taux_couverture_defaut = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=80.00,
        verbose_name="Taux de couverture par défaut (%)"
    )
    delai_validite_bon = models.IntegerField(
        default=30,
        verbose_name="Délai de validité des bons (jours)"
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuration assurance"
        verbose_name_plural = "Configurations assurance"

    def __str__(self):
        return f"Configuration {self.nom_assureur}"


class RapportAssureur(models.Model):
    """Rapports personnalisés"""
    titre = models.CharField(max_length=200)
    assureur = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='rapports_assureur'
    )
    type_rapport = models.CharField(max_length=50, choices=[
        ('MENSUEL', 'Mensuel'),
        ('TRIMESTRIEL', 'Trimestriel'), 
        ('ANNUEL', 'Annuel'),
        ('SPECIAL', 'Spécial')
    ])
    periode_debut = models.DateField()
    periode_fin = models.DateField()
    nombre_bons_emis = models.IntegerField(default=0)
    nombre_bons_utilises = models.IntegerField(default=0)
    montant_total_emis = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0
    )
    montant_total_rembourse = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0
    )
    date_generation = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Rapport Assureur"
        verbose_name_plural = "Rapports Assureurs"
        ordering = ['-date_generation']

    def __str__(self):
        return f"{self.titre} - {self.assureur.username}"


# ==========================================================================
# MODÈLES PROXY POUR COMPATIBILITÉ
# ==========================================================================

class BonPriseEnCharge(Bon):
    """Modèle proxy pour compatibilité"""
    class Meta:
        proxy = True
        verbose_name = "Bon de prise en charge"
        verbose_name_plural = "Bons de prise en charge"

    def __str__(self):
        return f"BonPriseEnCharge {self.numero_bon}"


class BonDeSoin(Bon):
    """Modèle proxy pour compatibilité"""
    class Meta:
        proxy = True
        verbose_name = "Bon de soin"
        verbose_name_plural = "Bons de soin"

    def __str__(self):
        return f"BonDeSoin {self.numero_bon}"


# ==========================================================================
# SIGNALS
# ==========================================================================

@receiver(post_save, sender=User)
def creer_profil_assureur(sender, instance, created, **kwargs):
    """Crée automatiquement un profil assureur pour un nouvel utilisateur staff"""
    if created and instance.is_staff:
        if not hasattr(instance, 'assureur_profile'):
            try:
                dernier_assureur = Assureur.objects.order_by('-id').first()
                if dernier_assureur:
                    dernier_num = int(dernier_assureur.numero_employe.replace('EMP', ''))
                    nouveau_num = dernier_num + 1
                else:
                    nouveau_num = 1
                
                Assureur.objects.create(
                    user=instance,
                    numero_employe=f"EMP{nouveau_num:04d}",
                    departement='admin',
                )
            except Exception as e:
                logger.error(f"Erreur création profil assureur: {e}")