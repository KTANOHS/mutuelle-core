# pharmacien/models.py - VERSION COMPLÈTEMENT CORRIGÉE
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Medicament(models.Model):
    """Modèle pour les médicaments"""
    nom = models.CharField(max_length=200, verbose_name="Nom du médicament")
    description = models.TextField(blank=True, verbose_name="Description")
    prix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Médicament"
        verbose_name_plural = "Médicaments"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom

class Pharmacien(models.Model):
    """Profil du pharmacien - VERSION CORRIGÉE"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_pharmacie = models.CharField(max_length=255, verbose_name="Nom de la pharmacie")
    adresse_pharmacie = models.TextField(verbose_name="Adresse de la pharmacie")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    actif = models.BooleanField(default=True, verbose_name="Pharmacie active")
    date_inscription = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    
    # Champs optionnels pour plus d'informations
    numero_pharmacien = models.CharField(
        max_length=50, 
        unique=True, 
        null=True, 
        blank=True,
        verbose_name="Numéro de pharmacien"
    )
    specialite = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Spécialité"
    )
    horaires_ouverture = models.TextField(
        blank=True, 
        verbose_name="Horaires d'ouverture"
    )
    
    class Meta:
        verbose_name = "Pharmacien"
        verbose_name_plural = "Pharmaciens"
        ordering = ['nom_pharmacie']
    
    def __str__(self):
        if self.user.get_full_name():
            return f"{self.user.get_full_name()} - {self.nom_pharmacie}"
        return f"{self.user.username} - {self.nom_pharmacie}"
    
    def get_nom_complet(self):
        """Retourne le nom complet du pharmacien"""
        return self.user.get_full_name() or self.user.username
    
    def get_email(self):
        """Retourne l'email du pharmacien"""
        return self.user.email
    
    def est_actif(self):
        """Vérifie si le pharmacien est actif"""
        return self.actif and self.user.is_active

class OrdonnancePharmacien(models.Model):
    """Ordonnance gérée par le pharmacien - VERSION CORRIGÉE"""
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDEE', 'Validée'),
        ('PREPAREE', 'Préparée'),
        ('SERVIE', 'Servie'),
        ('ANNULEE', 'Annulée'),
        ('REFUSEE', 'Refusée'),
    ]
    
    # Référence à l'ordonnance du médecin
    ordonnance_medecin = models.ForeignKey(
        'medecin.Ordonnance',
        on_delete=models.CASCADE,
        related_name='gestion_pharmacien',
        verbose_name="Ordonnance du médecin"
    )
    
    # Référence au bon de prise en charge
    bon_prise_charge = models.ForeignKey(
        'assureur.Bon',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ordonnances_pharmacien',
        verbose_name="Bon de prise en charge"
    )
    
    # Informations sur le service
    medicament_delivre = models.CharField(
        max_length=255, 
        verbose_name="Médicament délivré"
    )
    posologie_appliquee = models.TextField(
        verbose_name="Posologie appliquée"
    )
    duree_traitement = models.PositiveIntegerField(
        default=7,
        verbose_name="Durée du traitement (jours)"
    )
    instructions_supplementaires = models.TextField(
        blank=True,
        verbose_name="Instructions supplémentaires"
    )
    
    # Dates importantes
    date_reception = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de réception"
    )
    date_validation = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Date de validation"
    )
    date_preparation = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Date de préparation"
    )
    date_service = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Date de service"
    )
    
    # Statut de l'ordonnance
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default='EN_ATTENTE',
        verbose_name="Statut"
    )
    
    # Référence au pharmacien validateur
    pharmacien_validateur = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='ordonnances_validees'
    )
    
    # Notes et observations
    notes_pharmacien = models.TextField(
        blank=True, 
        verbose_name="Notes du pharmacien"
    )
    observations_service = models.TextField(
        blank=True, 
        verbose_name="Observations lors du service"
    )
    
    # Informations quantitatives et financières
    quantite_delivree = models.PositiveIntegerField(
        default=1,
        verbose_name="Quantité délivrée"
    )
    prix_unitaire = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Prix unitaire"
    )
    montant_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Montant total"
    )
    taux_remboursement = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.70,
        verbose_name="Taux de remboursement"
    )
    montant_rembourse = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Montant remboursé"
    )
    
    class Meta:
        verbose_name = "Ordonnance Pharmacien"
        verbose_name_plural = "Ordonnances Pharmacien"
        ordering = ['-date_reception']
        indexes = [
            models.Index(fields=['statut']),
            models.Index(fields=['date_reception']),
            models.Index(fields=['ordonnance_medecin']),
            models.Index(fields=['pharmacien_validateur']),
        ]
    
    def __str__(self):
        return f"Ordonnance Pharma #{self.id} - {self.medicament_delivre}"
    
    def save(self, *args, **kwargs):
        """Calcul automatique des montants"""
        # Calcul du montant total
        if self.prix_unitaire and self.quantite_delivree:
            self.montant_total = self.prix_unitaire * self.quantite_delivree
        
        # Calcul du montant remboursé
        if self.montant_total and self.taux_remboursement:
            self.montant_rembourse = self.montant_total * self.taux_remboursement
        
        super().save(*args, **kwargs)
    
    def get_patient(self):
        """Retourne le patient via l'ordonnance du médecin"""
        return self.ordonnance_medecin.patient
    
    def get_medecin_prescripteur(self):
        """Retourne le médecin prescripteur"""
        return self.ordonnance_medecin.medecin
    
    def est_valide(self):
        """Vérifie si l'ordonnance est validée"""
        return self.statut == 'VALIDEE'
    
    def est_servie(self):
        """Vérifie si l'ordonnance est servie"""
        return self.statut == 'SERVIE'
    
    def peut_etre_validee(self):
        """Vérifie si l'ordonnance peut être validée"""
        return self.statut in ['EN_ATTENTE', 'PREPAREE']
    
    def peut_etre_servie(self):
        """Vérifie si l'ordonnance peut être servie"""
        return self.statut in ['VALIDEE', 'PREPAREE']
    
    def valider(self, pharmacien=None, notes=""):
        """Valide l'ordonnance"""
        if self.peut_etre_validee():
            self.statut = 'VALIDEE'
            self.date_validation = timezone.now()
            if pharmacien:
                self.pharmacien_validateur = pharmacien
            if notes:
                self.notes_pharmacien = notes
            self.save()
            return True
        return False
    
    def preparer(self):
        """Marque l'ordonnance comme préparée"""
        if self.statut == 'VALIDEE':
            self.statut = 'PREPAREE'
            self.date_preparation = timezone.now()
            self.save()
            return True
        return False
    
    def servir(self, quantite=1, prix_unitaire=0, observations=""):
        """Marque l'ordonnance comme servie"""
        if self.peut_etre_servie():
            self.statut = 'SERVIE'
            self.date_service = timezone.now()
            self.quantite_delivree = quantite
            self.prix_unitaire = prix_unitaire
            if observations:
                self.observations_service = observations
            self.save()
            return True
        return False
    
    def annuler(self, raison=""):
        """Annule l'ordonnance"""
        self.statut = 'ANNULEE'
        if raison:
            self.notes_pharmacien += f"\n--- ANNULATION ---\nRaison: {raison}"
        self.save()
    
    def get_duree_attente(self):
        """Retourne la durée d'attente en heures"""
        if self.date_service and self.date_reception:
            delta = self.date_service - self.date_reception
            return delta.total_seconds() / 3600  # Heures
        return None

class StockPharmacie(models.Model):
    """Gestion du stock de la pharmacie - VERSION CORRIGÉE"""
    CATEGORIE_MEDICAMENT = [
        ('ANTIBIOTIQUE', 'Antibiotique'),
        ('ANALGESIQUE', 'Analgésique'),
        ('ANTI_INFLAMMATOIRE', 'Anti-inflammatoire'),
        ('VITAMINE', 'Vitamine'),
        ('AUTRE', 'Autre'),
    ]
    
    pharmacie = models.ForeignKey(
        Pharmacien, 
        on_delete=models.CASCADE, 
        related_name='stocks'
    )
    nom_medicament = models.CharField(
        max_length=255,
        verbose_name="Nom du médicament"
    )
    code_medicament = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="Code du médicament"
    )
    categorie = models.CharField(
        max_length=50,
        choices=CATEGORIE_MEDICAMENT,
        default='AUTRE',
        verbose_name="Catégorie"
    )
    quantite_stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantité en stock"
    )
    seuil_alerte = models.PositiveIntegerField(
        default=10,
        verbose_name="Seuil d'alerte"
    )
    prix_achat = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Prix d'achat"
    )
    prix_vente = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Prix de vente"
    )
    date_peremption = models.DateField(
        null=True, 
        blank=True,
        verbose_name="Date de péremption"
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Médicament actif"
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )
    
    class Meta:
        verbose_name = "Stock Pharmacie"
        verbose_name_plural = "Stocks Pharmacie"
        unique_together = ['pharmacie', 'nom_medicament', 'code_medicament']
        ordering = ['nom_medicament']
        indexes = [
            models.Index(fields=['pharmacie', 'actif']),
            models.Index(fields=['quantite_stock']),
            models.Index(fields=['date_peremption']),
            models.Index(fields=['categorie']),
        ]
    
    def __str__(self):
        return f"{self.nom_medicament} - Stock: {self.quantite_stock}"
    
    def est_en_rupture(self):
        """Vérifie si le médicament est en rupture de stock"""
        return self.quantite_stock == 0
    
    def besoin_reapprovisionnement(self):
        """Vérifie si besoin de réapprovisionnement"""
        return self.quantite_stock <= self.seuil_alerte
    
    def est_perime(self):
        """Vérifie si le médicament est périmé"""
        if self.date_peremption:
            return self.date_peremption < timezone.now().date()
        return False
    
    def diminuer_stock(self, quantite=1):
        """Diminue le stock du médicament"""
        if self.quantite_stock >= quantite:
            self.quantite_stock -= quantite
            self.save()
            return True
        return False
    
    def augmenter_stock(self, quantite=1):
        """Augmente le stock du médicament"""
        self.quantite_stock += quantite
        self.save()
    
    def get_marge(self):
        """Calcule la marge bénéficiaire"""
        return self.prix_vente - self.prix_achat
    
    def get_jours_avant_peremption(self):
        """Retourne le nombre de jours avant péremption"""
        if self.date_peremption:
            today = timezone.now().date()
            delta = self.date_peremption - today
            return delta.days
        return None

    @property
    def marge(self):
        """Calcule la marge bénéficiaire"""
        try:
            return float(self.prix_vente) - float(self.prix_achat)
        except (ValueError, TypeError):
            return 0
    
    @property
    def taux_marge(self):
        """Calcule le taux de marge en pourcentage"""
        try:
            if float(self.prix_achat) > 0:
                return ((float(self.prix_vente) - float(self.prix_achat)) / float(self.prix_achat)) * 100
            return 0
        except (ValueError, TypeError):
            return 0
    
    @property
    def statut_stock(self):
        """Retourne le statut du stock"""
        if self.quantite_stock == 0:
            return 'rupture'
        elif self.quantite_stock <= self.seuil_alerte:
            return 'alerte'
        elif self.est_perime():
            return 'perime'
        else:
            return 'normal'
    
    @property
    def pourcentage_stock(self):
        """Calcule le pourcentage par rapport au seuil d'alerte"""
        try:
            if self.seuil_alerte > 0:
                return min(100, (self.quantite_stock / (self.seuil_alerte + 10)) * 100)
            return 0
        except (ZeroDivisionError, TypeError):
            return 0

class HistoriqueService(models.Model):
    """Historique des services rendus par le pharmacien - VERSION CORRIGÉE"""
    TYPE_ACTION = [
        ('VALIDATION', 'Validation ordonnance'),
        ('PREPARATION', 'Préparation ordonnance'),
        ('SERVICE', 'Service ordonnance'),
        ('ANNULATION', 'Annulation ordonnance'),
        ('MODIFICATION', 'Modification ordonnance'),
        ('CONSULTATION', 'Consultation ordonnance'),
    ]
    
    ordonnance = models.ForeignKey(
        OrdonnancePharmacien, 
        on_delete=models.CASCADE, 
        related_name='historique_services'
    )
    pharmacien = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name="Pharmacien"
    )
    type_action = models.CharField(
        max_length=20,
        choices=TYPE_ACTION,
        verbose_name="Type d'action"
    )
    details_action = models.TextField(
        verbose_name="Détails de l'action"
    )
    date_action = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de l'action"
    )
    
    # Informations supplémentaires
    ancien_statut = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name="Ancien statut"
    )
    nouveau_statut = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name="Nouveau statut"
    )
    
    class Meta:
        verbose_name = "Historique Service"
        verbose_name_plural = "Historiques Services"
        ordering = ['-date_action']
        indexes = [
            models.Index(fields=['ordonnance', 'date_action']),
            models.Index(fields=['pharmacien', 'date_action']),
            models.Index(fields=['type_action']),
        ]
    
    def __str__(self):
        return f"{self.type_action} - {self.date_action.strftime('%d/%m/%Y %H:%M')}"
    
    def get_pharmacien_nom(self):
        """Retourne le nom du pharmacien"""
        return self.pharmacien.get_full_name() or self.pharmacien.username

# Signaux pour automatiser certaines actions
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(post_save, sender=OrdonnancePharmacien)
def creer_historique_ordonnance(sender, instance, created, **kwargs):
    """Crée un historique lors de la création d'une ordonnance pharmacien"""
    if created:
        HistoriqueService.objects.create(
            ordonnance=instance,
            pharmacien=instance.pharmacien_validateur or instance.ordonnance_medecin.medecin.user,
            type_action='VALIDATION',
            details_action=f"Création de l'ordonnance pharmacien pour {instance.ordonnance_medecin}",
            ancien_statut='',
            nouveau_statut=instance.statut
        )

@receiver(pre_save, sender=OrdonnancePharmacien)
def suivre_changements_statut(sender, instance, **kwargs):
    """Suit les changements de statut des ordonnances"""
    if instance.pk:
        try:
            ancienne_instance = OrdonnancePharmacien.objects.get(pk=instance.pk)
            if ancienne_instance.statut != instance.statut:
                HistoriqueService.objects.create(
                    ordonnance=instance,
                    pharmacien=instance.pharmacien_validateur or instance.ordonnance_medecin.medecin.user,
                    type_action='MODIFICATION',
                    details_action=f"Changement de statut: {ancienne_instance.statut} → {instance.statut}",
                    ancien_statut=ancienne_instance.statut,
                    nouveau_statut=instance.statut
                )
        except OrdonnancePharmacien.DoesNotExist:
            pass

@receiver(post_save, sender=User)
def creer_profil_pharmacien(sender, instance, created, **kwargs):
    """Crée automatiquement un profil pharmacien si l'utilisateur est dans le groupe Pharmacien"""
    if created and instance.groups.filter(name='Pharmaciens').exists():
        Pharmacien.objects.get_or_create(
            user=instance,
            defaults={
                'nom_pharmacie': f"Pharmacie de {instance.get_full_name() or instance.username}",
                'adresse_pharmacie': 'Adresse à compléter',
                'telephone': 'Numéro à compléter'
            }
        )

@receiver(post_save, sender=User)
def sauvegarder_profil_pharmacien(sender, instance, **kwargs):
    """Sauvegarde le profil pharmacien associé"""
    if hasattr(instance, 'pharmacien'):
        instance.pharmacien.save()