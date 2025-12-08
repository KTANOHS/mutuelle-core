# medecin/models.py
from django.db import models
from datetime import date, datetime, timedelta
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta  
from django.db.models.signals import post_save
from django.dispatch import receiver

import logging

logger = logging.getLogger(__name__)

class SpecialiteMedicale(models.Model):
    """Spécialités médicales disponibles"""
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Spécialité médicale"
        verbose_name_plural = "Spécialités médicales"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom

class EtablissementMedical(models.Model):
    """Établissements de santé (hôpitaux, cliniques, cabinets)"""
    TYPE_ETABLISSEMENT = [
        ('HOPITAL', 'Hôpital'),
        ('CLINIQUE', 'Clinique'),
        ('CABINET', 'Cabinet médical'),
        ('DISPENSAIRE', 'Dispensaire'),
        ('CENTRE_SANTE', 'Centre de santé'),
    ]
    
    nom = models.CharField(max_length=200)
    type_etablissement = models.CharField(max_length=20, choices=TYPE_ETABLISSEMENT)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100, default="Côte d'Ivoire")
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Établissement médical"
        verbose_name_plural = "Établissements médicaux"
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.get_type_etablissement_display()})"

class Medecin(models.Model):
    """Modèle principal pour les médecins - VERSION CORRIGÉE"""
    # Liaison avec l'utilisateur Django - CORRECTION APPLIQUÉE
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='medecin_profile'  # ✅ Nom unique et clair
    )
    
    # Informations professionnelles
    numero_ordre = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name="Numéro d'ordre des médecins"
    )
    specialite = models.ForeignKey(
        SpecialiteMedicale,
        on_delete=models.PROTECT,
        related_name='medecins'
    )
    etablissement = models.ForeignKey(
        EtablissementMedical,
        on_delete=models.PROTECT,
        related_name='medecins'
    )
    
    # Informations de contact professionnel
    telephone_pro = models.CharField(max_length=20, verbose_name="Téléphone professionnel")
    email_pro = models.EmailField(verbose_name="Email professionnel", blank=True)
    
    # Informations complémentaires
    annees_experience = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(60)]
    )
    tarif_consultation = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0,
        verbose_name="Tarif consultation (FCFA)"
    )
    
    # Statut et disponibilité
    actif = models.BooleanField(default=True)
    disponible = models.BooleanField(default=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_derniere_modif = models.DateTimeField(auto_now=True)
    
    # Horaires de travail
    horaires_travail = models.JSONField(
        default=dict,
        blank=True,
        help_text="Horaires de travail au format JSON"
    )
    
    # Documents (pourrait être déplacé dans un modèle séparé)
    diplome_verifie = models.BooleanField(default=False)
    cv_document = models.FileField(
        upload_to='medecins/cv/',
        blank=True,
        null=True,
        verbose_name="CV"
    )
    
    class Meta:
        verbose_name = "Médecin"
        verbose_name_plural = "Médecins"
        ordering = ['user__last_name', 'user__first_name']
        indexes = [
            models.Index(fields=['numero_ordre']),
            models.Index(fields=['actif', 'disponible']),
            models.Index(fields=['specialite']),
        ]
    
    def __str__(self):
        return f"Dr {self.user.get_full_name()} - {self.specialite}"
    
    def get_absolute_url(self):
        return reverse('medecin:detail_medecin', kwargs={'pk': self.pk})
    
    @property
    def nom_complet(self):
        return self.user.get_full_name()
    
    @property
    def est_actif(self):
        return self.actif and self.disponible
    
    @property
    def experience_text(self):
        if self.annees_experience == 0:
            return "Débutant"
        elif self.annees_experience == 1:
            return "1 an d'expérience"
        else:
            return f"{self.annees_experience} ans d'expérience"
    
    def get_statistiques(self):
        """Retourne les statistiques du médecin"""
        from .models import Ordonnance, Consultation  # Import local pour éviter les imports circulaires
        total_ordonnances = Ordonnance.objects.filter(medecin=self.user).count()
        total_consultations = Consultation.objects.filter(medecin=self).count()
        
        return {
            'total_ordonnances': total_ordonnances,
            'total_consultations': total_consultations,
        }

class DisponibiliteMedecin(models.Model):
    """Disponibilités du médecin pour les rendez-vous"""
    JOURS_SEMAINE = [
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    ]
    
    medecin = models.ForeignKey(
        Medecin,
        on_delete=models.CASCADE,
        related_name='disponibilites'
    )
    jour_semaine = models.IntegerField(choices=JOURS_SEMAINE)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Disponibilité médecin"
        verbose_name_plural = "Disponibilités médecins"
        unique_together = ['medecin', 'jour_semaine']
        ordering = ['medecin', 'jour_semaine']
    
    def __str__(self):
        return f"{self.medecin} - {self.get_jour_semaine_display()} {self.heure_debut}-{self.heure_fin}"

class Consultation(models.Model):
    """Consultations médicales"""
    STATUT_CONSULTATION = [
        ('PLANIFIEE', 'Planifiée'),
        ('EN_COURS', 'En cours'),
        ('TERMINEE', 'Terminée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    TYPE_CONSULTATION = [
        ('GENERALE', 'Consultation générale'),
        ('SPECIALISEE', 'Consultation spécialisée'),
        ('SUIVI', 'Consultation de suivi'),
        ('URGENCE', 'Urgence'),
    ]
    
    medecin = models.ForeignKey(
        Medecin,
        on_delete=models.PROTECT,
        related_name='consultations'
    )
    membre = models.ForeignKey(
        'membres.Membre',
        on_delete=models.CASCADE,
        related_name='consultations'
    )
    date_consultation = models.DateField()
    heure_consultation = models.TimeField(null=True, blank=True)
    duree = models.PositiveIntegerField(default=30, help_text="Durée en minutes")
    type_consultation = models.CharField(
        max_length=20,
        choices=TYPE_CONSULTATION,
        default='GENERALE'
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CONSULTATION,
        default='PLANIFIEE'
    )
    symptomes = models.TextField(blank=True, help_text="Symptômes décrits par le patient")
    notes = models.TextField(blank=True, help_text="Notes du médecin")
    diagnostic = models.TextField(blank=True, help_text="Diagnostic établi")
    traitement_prescrit = models.TextField(blank=True, help_text="Traitement prescrit")
    motifs = models.TextField(blank=True, help_text="Motifs de la consultation")
    recommandations = models.TextField(blank=True, help_text="Recommandations")
    
    # Informations de suivi
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Consultation"
        verbose_name_plural = "Consultations"
        ordering = ['-date_consultation']
        indexes = [
            models.Index(fields=['medecin', 'date_consultation']),
            models.Index(fields=['membre', 'date_consultation']),
            models.Index(fields=['statut']),
        ]
    
    def __str__(self):
        return f"Consultation {self.membre} avec Dr {self.medecin} - {self.date_consultation} {self.heure_consultation or ''}"
    
    @property
    def est_passee(self):
        from django.utils import timezone
        if self.heure_consultation:
            dt = timezone.datetime.combine(self.date_consultation, self.heure_consultation)
            return dt < timezone.now()
        return self.date_consultation < timezone.now().date()
    
    @property
    def duree_texte(self):
        return f"{self.duree} min"

class AvisMedecin(models.Model):
    """Avis des patients sur les médecins"""
    NOTE_CHOICES = [
        (1, '1 - Très mauvais'),
        (2, '2 - Mauvais'),
        (3, '3 - Moyen'),
        (4, '4 - Bon'),
        (5, '5 - Excellent'),
    ]
    
    medecin = models.ForeignKey(
        Medecin,
        on_delete=models.CASCADE,
        related_name='avis'
    )
    membre = models.ForeignKey(
        'membres.Membre',
        on_delete=models.CASCADE,
        related_name='avis_medecins'
    )
    note = models.PositiveIntegerField(choices=NOTE_CHOICES)
    commentaire = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    approuve = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Avis médecin"
        verbose_name_plural = "Avis médecins"
        unique_together = ['medecin', 'membre']
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Avis {self.note}/5 - {self.medecin} par {self.membre}"
    
    @property
    def note_etoiles(self):
        return '★' * self.note + '☆' * (5 - self.note)

class Medicament(models.Model):
    """Modèle pour stocker les médicaments"""
    nom = models.CharField(max_length=200, verbose_name="Nom commercial")
    dci = models.CharField(max_length=200, blank=True, verbose_name="DCI")
    forme_galenique = models.CharField(max_length=100, blank=True, verbose_name="Forme galénique")
    dosage = models.CharField(max_length=100, blank=True, verbose_name="Dosage")
    classe_therapeutique = models.CharField(max_length=200, blank=True, verbose_name="Classe thérapeutique")
    est_remboursable = models.BooleanField(default=True, verbose_name="Remboursable")
    
    class Meta:
        verbose_name = "Médicament"
        verbose_name_plural = "Médicaments"
        ordering = ['nom']
    
    def __str__(self):
        if self.dosage:
            return f"{self.nom} {self.dosage}"
        return self.nom

class Ordonnance(models.Model):
    """Ordonnances médicales avec système de partage automatique"""
    STATUT_ORDONNANCE = [
        ('ACTIVE', 'Active'),
        ('EXPIREE', 'Expirée'),
        ('ANNULEE', 'Annulée'),
        ('UTILISEE', 'Utilisée'),
        ('EN_ATTENTE_VALIDATION', 'En attente de validation'),
    ]
    
    TYPE_ORDONNANCE = [
        ('MEDICAMENTS', 'Médicaments'),
        ('ANALYSES', 'Analyses médicales'),
        ('IMAGERIE', 'Imagerie médicale'),
        ('SOINS', 'Soins infirmiers'),
        ('AUTRE', 'Autre'),
    ]
    
    # Informations de base
    numero = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name="Numéro d'ordonnance"
    )
    medecin = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='ordonnances_prescrites',
        verbose_name="Médecin prescripteur"
    )
    patient = models.ForeignKey(
        'membres.Membre',
        on_delete=models.CASCADE,
        related_name='ordonnances_medecin'
    )
    
    # Référence à l'assureur du patient
    assureur = models.ForeignKey(
        'assureur.Assureur',
        on_delete=models.PROTECT,
        related_name='ordonnances_assureur',
        verbose_name="Assureur du patient",
        null=True,
        blank=True
    )
    
    # Dates importantes
    date_prescription = models.DateField(default=timezone.now)
    date_expiration = models.DateField(
        help_text="Date d'expiration de l'ordonnance"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    # Informations médicales
    type_ordonnance = models.CharField(
        max_length=20,
        choices=TYPE_ORDONNANCE,
        default='MEDICAMENTS'
    )
    diagnostic = models.TextField(
        blank=True,
        help_text="Diagnostic justifiant la prescription"
    )
    medicaments = models.TextField(
        help_text="Liste des médicaments prescrits"
    )
    posologie = models.TextField(
        help_text="Posologie détaillée"
    )
    duree_traitement = models.PositiveIntegerField(
        default=7,
        help_text="Durée du traitement en jours"
    )
    
    # Caractéristiques de l'ordonnance
    renouvelable = models.BooleanField(default=False)
    nombre_renouvellements = models.PositiveIntegerField(default=0)
    renouvellements_effectues = models.PositiveIntegerField(default=0)
    
    # Statut et suivi
    statut = models.CharField(
        max_length=25,
        choices=STATUT_ORDONNANCE,
        default='EN_ATTENTE_VALIDATION'
    )
    est_urgent = models.BooleanField(default=False)
    notes = models.TextField(
        blank=True,
        help_text="Notes complémentaires"
    )
    
    # Suivi du partage
    partage_effectue = models.BooleanField(default=False, verbose_name="Partage automatique effectué")
    
    # Liaison avec consultation (optionnelle)
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ordonnances_consultation'
    )
    
    class Meta:
        verbose_name = "Ordonnance Médecin"
        verbose_name_plural = "Ordonnances Médecin"
        ordering = ['-date_prescription', '-date_creation']
        indexes = [
            models.Index(fields=['numero']),
            models.Index(fields=['patient', 'date_prescription']),
            models.Index(fields=['medecin', 'date_prescription']),
            models.Index(fields=['assureur', 'statut']),
            models.Index(fields=['statut', 'date_expiration']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(date_expiration__gte=models.F('date_prescription')),
                name='date_expiration_after_prescription'
            )
        ]
        permissions = [
            ("view_ordonnance_membre", "Peut voir les ordonnances en tant que membre"),
            ("view_ordonnance_assureur", "Peut voir les ordonnances en tant qu'assureur"),
            ("view_ordonnance_pharmacien", "Peut voir les ordonnances en tant que pharmacien"),
        ]
    
    def __str__(self):
        return f"Ordonnance {self.numero} - {self.patient.nom_complet}"
    
    def save(self, *args, **kwargs):
        """Génère automatiquement un numéro d'ordonnance si vide"""
        if not self.numero:
            date_str = timezone.now().strftime('%Y%m%d')
            last_ord = Ordonnance.objects.filter(
                numero__startswith=f'ORD{date_str}'
            ).count()
            self.numero = f'ORD{date_str}{last_ord + 1:04d}'
        
        # Définit la date d'expiration par défaut (30 jours)
        if not self.date_expiration:
            self.date_expiration = self.date_prescription + timedelta(days=30)
        
        # Récupère automatiquement l'assureur du patient si non défini
        if not self.assureur and self.patient and hasattr(self.patient, 'assureur'):
            self.assureur = self.patient.assureur
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('medecin:detail_ordonnance', kwargs={'pk': self.pk})
    
    @property
    def est_valide(self):
        """Vérifie si l'ordonnance est encore valide - VERSION CORRIGÉE"""
        from datetime import timedelta
        from django.utils import timezone
        
        if not self.date_prescription:
            return False
        
        # Validité de 3 mois (90 jours)
        duree_validite = timedelta(days=90)
        date_expiration = self.date_prescription + duree_validite
        
        # Retourne True si pas expirée
        return timezone.now().date() <= date_expiration
    
    @property
    def jours_restants(self):
        """Nombre de jours restants avant expiration"""
        today = timezone.now().date()
        if self.date_expiration >= today:
            return (self.date_expiration - today).days
        return 0
    
    @property
    def medicaments_liste(self):
        """Retourne la liste des médicaments formatée"""
        if self.medicaments:
            return [med.strip() for med in self.medicaments.split('\n') if med.strip()]
        return []
    
    def peut_etre_renouvelee(self):
        """Vérifie si l'ordonnance peut être renouvelée"""
        return (self.renouvelable and 
                self.renouvellements_effectues < self.nombre_renouvellements and
                self.est_valide)
    
    def renouveler(self):
        """Renouvelle l'ordonnance"""
        if self.peut_etre_renouvelee():
            self.renouvellements_effectues += 1
            # Prolonge la date d'expiration de 30 jours supplémentaires
            self.date_expiration += timedelta(days=30)
            self.save()
            return True
        return False
    
    def marquer_comme_utilisee(self):
        """Marque l'ordonnance comme utilisée"""
        self.statut = 'UTILISEE'
        self.save()
    
    def get_medecin_prescripteur(self):
        """Retourne le médecin prescripteur - VERSION CORRIGÉE"""
        try:
            # ✅ Utilise le bon related_name
            return self.medecin.medecin_profile
        except Medecin.DoesNotExist:
            return None
    
    # Méthodes de partage automatique
    def partager_automatiquement(self):
        """Partage automatiquement l'ordonnance avec les parties concernées"""
        try:
            from core.models import PartageAutomatique, Notification
            
            # Liste des utilisateurs concernés
            utilisateurs_concernes = []
            
            # 1. Le patient (membre)
            if hasattr(self.patient, 'user'):
                utilisateurs_concernes.append(self.patient.user)
            
            # 2. L'assureur (gestionnaires de l'assureur)
            if self.assureur:
                # Ajouter tous les utilisateurs liés à cet assureur
                gestionnaires = User.objects.filter(
                    assureur_gestionnaire__assureur=self.assureur
                )
                utilisateurs_concernes.extend(gestionnaires)
            
            # 3. Tous les pharmaciens
            pharmaciens = User.objects.filter(
                groups__name='Pharmacien',
                is_active=True
            )
            utilisateurs_concernes.extend(pharmaciens)
            
            # Éliminer les doublons
            utilisateurs_concernes = list(set(utilisateurs_concernes))
            
            # Créer l'entrée de partage
            partage, created = PartageAutomatique.objects.get_or_create(
                type_document=PartageAutomatique.ORDONNANCE,
                document_id=self.id
            )
            partage.visible_par.set(utilisateurs_concernes)
            
            # Créer des notifications
            for utilisateur in utilisateurs_concernes:
                if utilisateur != self.medecin:  # Pas de notification pour le créateur
                    Notification.objects.create(
                        utilisateur=utilisateur,
                        message=f"Nouvelle ordonnance prescrite par le Dr {self.medecin.get_full_name()} pour {self.patient.nom_complet}",
                        type_document=PartageAutomatique.ORDONNANCE,
                        document_id=self.id
                    )
            
            # Marquer le partage comme effectué
            self.partage_effectue = True
            self.save(update_fields=['partage_effectue'])
            
            logger.info(f"Ordonnance {self.numero} partagée avec {len(utilisateurs_concernes)} utilisateurs")
            return True
            
        except Exception as e:
            logger.error(f"Erreur partage automatique ordonnance {self.id}: {e}")
            return False

@receiver(post_save, sender=Ordonnance)
def declencher_partage_ordonnance(sender, instance, created, **kwargs):
    """Déclenche le partage automatique après création d'une ordonnance"""
    if created and not instance.partage_effectue:
        try:
            instance.partager_automatiquement()
        except Exception as e:
            logger.error(f"Erreur déclenchement partage ordonnance {instance.id}: {e}")

class BonDeSoin(models.Model):
    """Bons de soins pour la prise en charge des patients"""
    STATUT_BON_SOIN = [
        ('BROUILLON', 'Brouillon'),
        ('EN_ATTENTE', 'En attente de validation'),
        ('VALIDE', 'Validé'),
        ('REFUSE', 'Refusé'),
        ('UTILISE', 'Utilisé'),
    ]
    
    numero = models.CharField(max_length=50, unique=True)
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name='bons_soin'
    )
    patient = models.ForeignKey(
        'membres.Membre',
        on_delete=models.CASCADE,
        related_name='bons_soin'
    )
    medecin = models.ForeignKey(
        Medecin,
        on_delete=models.PROTECT,
        related_name='bons_soin'
    )
    date_soin = models.DateField()
    date_realisation = models.DateField(null=True, blank=True)
    type_soin = models.ForeignKey(
        'soins.TypeSoin',
        on_delete=models.PROTECT,
        related_name='bons_soin'
    )
    cout_estime = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cout_reel = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    taux_prise_charge = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    statut = models.CharField(max_length=20, choices=STATUT_BON_SOIN, default='BROUILLON')
    diagnostic = models.TextField(blank=True)
    observations = models.TextField(blank=True)
    motif_refus = models.TextField(blank=True)
    duree_sejour = models.PositiveIntegerField(default=0, help_text="Durée en jours si hospitalisation")
    
    # Champs de suivi
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='bons_soin_crees'
    )
    valide_par = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='bons_soin_valides'
    )
    date_validation = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Bon de soin"
        verbose_name_plural = "Bons de soin"
        ordering = ['-date_soin', '-created_at']
    
    def __str__(self):
        return f"Bon de soin {self.numero} - {self.patient.nom_complet}"
    
    def save(self, *args, **kwargs):
        if not self.numero:
            date_str = timezone.now().strftime('%Y%m%d')
            last_bon = BonDeSoin.objects.filter(
                numero__startswith=f'BS{date_str}'
            ).count()
            self.numero = f'BS{date_str}{last_bon + 1:04d}'
        super().save(*args, **kwargs)

class MaladieChronique(models.Model):
    """Référentiel des maladies chroniques"""
    nom = models.CharField(max_length=200)
    code_cim = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True)
    recommandations_generales = models.TextField(blank=True)
    actif = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'maladies_chroniques'
        verbose_name = "Maladie chronique"
        verbose_name_plural = "Maladies chroniques"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom

class ProgrammeAccompagnement(models.Model):
    """Programme d'accompagnement personnalisé"""
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('suspendu', 'Suspendu'),
        ('termine', 'Terminé'),
        ('abandon', 'Abandonné'),
    ]
    
    patient = models.ForeignKey('membres.Membre', on_delete=models.CASCADE)
    medecin_referent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='programmes_medecin')
    pharmacien_referent = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='programmes_pharmacien'
    )
    maladie = models.ForeignKey(MaladieChronique, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin_prevue = models.DateField(null=True, blank=True)
    objectifs_therapeutiques = models.TextField()
    protocole_suivi = models.TextField(help_text="Protocole de suivi détaillé")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif')
    observations = models.TextField(blank=True)
    
    # Métriques de suivi
    frequence_controle = models.PositiveIntegerField(default=30, help_text="Jours entre chaque contrôle")
    prochain_controle = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'programmes_accompagnement'
        verbose_name = "Programme d'accompagnement"
        verbose_name_plural = "Programmes d'accompagnement"
        ordering = ['-date_debut']
    
    def __str__(self):
        return f"Accompagnement {self.maladie.nom} - {self.patient.nom_complet}"

class SuiviPatient(models.Model):
    """Journal de suivi du patient"""
    TYPE_SUIVI_CHOICES = [
        ('consultation', 'Consultation médicale'),
        ('teleconsultation', 'Téléconsultation'),
        ('pharmacie', 'Visite pharmacie'),
        ('appel', 'Appel téléphonique'),
        ('message', 'Message'),
        ('automesure', 'Auto-mesure'),
    ]
    
    OBSERVANCE_CHOICES = [
        ('excellente', 'Excellente (>90%)'),
        ('bonne', 'Bonne (70-90%)'),
        ('moyenne', 'Moyenne (50-70%)'),
        ('mauvaise', 'Mauvaise (<50%)'),
    ]
    
    programme = models.ForeignKey(ProgrammeAccompagnement, on_delete=models.CASCADE, related_name='suivis')
    type_suivi = models.CharField(max_length=20, choices=TYPE_SUIVI_CHOICES)
    date_suivi = models.DateTimeField(default=timezone.now)
    intervenant = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Données cliniques
    tension_arterielle = models.CharField(max_length=20, blank=True)
    glycemie = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    poids = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    symptomes_observes = models.TextField(blank=True)
    observance_traitement = models.CharField(
        max_length=20, 
        choices=OBSERVANCE_CHOICES, 
        blank=True
    )
    
    # Évaluation
    observations = models.TextField()
    actions_prises = models.TextField()
    recommendations = models.TextField(blank=True)
    prochain_rdv = models.DateField(null=True, blank=True)
    
    # Collaboration médecin-pharmacien
    transmission_pharmacien = models.BooleanField(default=False)
    notes_pharmacien = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'suivis_patients'
        verbose_name = "Suivi patient"
        verbose_name_plural = "Suivis patients"
        ordering = ['-date_suivi']
    
    def __str__(self):
        return f"Suivi {self.get_type_suivi_display()} - {self.date_suivi.strftime('%d/%m/%Y')}"

class ObjectifTherapeutique(models.Model):
    """Objectifs thérapeutiques personnalisés"""
    PRIORITE_CHOICES = [
        ('elevee', 'Élevée'),
        ('moyenne', 'Moyenne'),
        ('faible', 'Faible'),
    ]
    
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('atteint', 'Atteint'),
        ('non_atteint', 'Non atteint'),
        ('reporte', 'Reporté'),
    ]
    
    programme = models.ForeignKey(ProgrammeAccompagnement, on_delete=models.CASCADE, related_name='objectifs')
    description = models.TextField()
    echeance = models.DateField(null=True, blank=True)
    priorite = models.CharField(max_length=20, choices=PRIORITE_CHOICES, default='moyenne')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'objectifs_therapeutiques'
        verbose_name = "Objectif thérapeutique"
        verbose_name_plural = "Objectifs thérapeutiques"
        ordering = ['priorite', 'echeance']
    
    def __str__(self):
        return f"Objectif: {self.description[:50]}..."

class AlerteSuivi(models.Model):
    """Alertes pour le suivi des patients"""
    TYPE_ALERTE_CHOICES = [
        ('controle_retard', 'Contrôle en retard'),
        ('observance_basse', 'Observance basse'),
        ('parametre_anormal', 'Paramètre anormal'),
        ('rdv_manque', 'Rendez-vous manqué'),
        ('pharmacie_avis', 'Avis pharmacien requis'),
    ]
    
    SEVERITE_CHOICES = [
        ('basse', 'Basse'),
        ('moyenne', 'Moyenne'),
        ('haute', 'Haute'),
        ('critique', 'Critique'),
    ]
    
    programme = models.ForeignKey(ProgrammeAccompagnement, on_delete=models.CASCADE, related_name='alertes')
    type_alerte = models.CharField(max_length=50, choices=TYPE_ALERTE_CHOICES)
    severite = models.CharField(max_length=20, choices=SEVERITE_CHOICES, default='moyenne')
    message = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_resolution = models.DateTimeField(null=True, blank=True)
    resolue_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'alertes_suivi'
        verbose_name = "Alerte suivi"
        verbose_name_plural = "Alertes suivi"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Alerte {self.get_type_alerte_display()} - {self.programme.patient.nom_complet}"

# Signaux pour la création automatique du profil médecin - VERSION AMÉLIORÉE

@receiver(post_save, sender=User)
def create_medecin_profile(sender, instance, created, **kwargs):
    """
    Crée automatiquement un profil médecin quand un utilisateur est ajouté au groupe médecin
    Version corrigée avec meilleure gestion des erreurs
    """
    try:
        # Vérifie si l'utilisateur est dans le groupe médecin
        if instance.groups.filter(name='medecin').exists():
            # Vérifie si un profil médecin existe déjà
            if not hasattr(instance, 'medecin_profile'):
                # Crée le profil médecin avec des valeurs par défaut
                Medecin.objects.get_or_create(
                    user=instance,
                    defaults={
                        'numero_ordre': f"MED{instance.id:06d}",
                        'specialite': SpecialiteMedicale.objects.first(),
                        'etablissement': EtablissementMedical.objects.first(),
                        'telephone_pro': getattr(instance, 'phone', ''),
                        'email_pro': instance.email,
                        'tarif_consultation': 10000,
                    }
                )
                logger.info(f"Profil médecin créé pour l'utilisateur {instance.username}")
    except Exception as e:
        logger.error(f"Erreur création profil médecin pour {instance.username}: {e}")

# ✅ AJOUT: Méthode utilitaire pour récupérer facilement le profil médecin
def get_user_medecin_profile(user):
    """
    Récupère le profil médecin d'un utilisateur de manière sécurisée
    Utilisation: medecin = get_user_medecin_profile(user)
    """
    try:
        return user.medecin_profile
    except Medecin.DoesNotExist:
        return None
    except AttributeError:
        return None