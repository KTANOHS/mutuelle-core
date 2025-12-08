

# Create your models here.
# pharmacie_public/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PharmaciePublic(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente de validation'),
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('rejete', 'Rejeté'),
    ]
    
    TYPE_PHARMACIE = [
        ('officine', 'Officine'),
        ('hospitaliere', 'Hospitalière'),
        ('parapharmacie', 'Parapharmacie'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_pharmacie = models.CharField(max_length=255)
    adresse = models.TextField()
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=10)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    type_pharmacie = models.CharField(max_length=20, choices=TYPE_PHARMACIE, default='officine')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    horaires_ouverture = models.TextField(default='Lun-Ven: 08:00-19:00, Sam: 08:00-12:00')
    date_inscription = models.DateTimeField(auto_now_add=True)
    
    # Garde
    est_de_garde = models.BooleanField(default=False)
    prochaine_garde = models.DateTimeField(null=True, blank=True)
    
    # Mutuelle
    partenaire_mutuelle = models.BooleanField(default=False)
    numero_agrement = models.CharField(max_length=50, blank=True)
    
    # Coordonnées GPS
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    def __str__(self):
        return self.nom_pharmacie
    
    class Meta:
        verbose_name = "Pharmacie publique"
        verbose_name_plural = "Pharmacies publiques"

class MedicamentPublic(models.Model):
    CATEGORIE_CHOICES = [
        ('generique', 'Générique'),
        ('princeps', 'Princeps'),
        ('OTC', 'Médicament en vente libre'),
        ('ordonnance', 'Sur ordonnance'),
    ]
    
    pharmacie = models.ForeignKey(PharmaciePublic, on_delete=models.CASCADE, related_name='medicaments')
    nom = models.CharField(max_length=200)
    principe_actif = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    forme_galenique = models.CharField(max_length=100)
    laboratoire = models.CharField(max_length=200)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField(default=0)
    necessite_ordonnance = models.BooleanField(default=False)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nom} - {self.dosage}"
    
    class Meta:
        verbose_name = "Médicament public"
        verbose_name_plural = "Médicaments publics"

class CommandePublic(models.Model):
    STATUT_COMMANDE = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('en_preparation', 'En préparation'),
        ('pret', 'Prête à être retirée'),
        ('retiree', 'Retirée'),
        ('annulee', 'Annulée'),
    ]
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commandes_pharmacie_public')
    pharmacie = models.ForeignKey(PharmaciePublic, on_delete=models.CASCADE, related_name='commandes')
    numero_commande = models.CharField(max_length=20, unique=True)
    statut = models.CharField(max_length=20, choices=STATUT_COMMANDE, default='en_attente')
    date_commande = models.DateTimeField(auto_now_add=True)
    date_retrait_prevu = models.DateTimeField(null=True, blank=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    
    def generer_numero_commande(self):
        return f"CMDP{timezone.now().strftime('%Y%m%d')}{self.id:06d}"
    
    def save(self, *args, **kwargs):
        if not self.numero_commande:
            self.numero_commande = self.generer_numero_commande()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Commande {self.numero_commande}"
    
    class Meta:
        verbose_name = "Commande publique"
        verbose_name_plural = "Commandes publiques"

class LigneCommandePublic(models.Model):
    commande = models.ForeignKey(CommandePublic, on_delete=models.CASCADE, related_name='lignes')
    medicament = models.ForeignKey(MedicamentPublic, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=8, decimal_places=2)
    
    @property
    def sous_total(self):
        return self.quantite * self.prix_unitaire
    
    def __str__(self):
        return f"{self.medicament.nom} x{self.quantite}"
    
    class Meta:
        verbose_name = "Ligne de commande publique"
        verbose_name_plural = "Lignes de commande publiques"

class GardePublic(models.Model):
    pharmacie = models.ForeignKey(PharmaciePublic, on_delete=models.CASCADE)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    type_garde = models.CharField(max_length=50, choices=[
        ('nuit', 'Garde de nuit'),
        ('weekend', 'Garde de weekend'),
        ('jour_ferie', 'Jour férié'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_debut']
        verbose_name = "Garde publique"
        verbose_name_plural = "Gardes publiques"
    
    def __str__(self):
        return f"Garde {self.pharmacie.nom_pharmacie} - {self.date_debut}"