# api/serializers.py - VERSION COMPLÈTE CORRIGÉE
from rest_framework import serializers
from django.contrib.auth.models import User
from membres.models import Membre, Bon, Profile
from medecin.models import Medecin, Ordonnance
from paiements.models import Paiement
from assureur.models import BonDeSoin, BonPriseEnCharge, RapportAssureur
from soins.models import TypeSoin, Soin, Prescription  # AJOUTER CES IMPORTS

# ==============================================================================
# ✅ SERIALIZERS POUR LES MODÈLES EXISTANTS
# ==============================================================================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'user', 'role', 'telephone', 'adresse', 'date_naissance', 'created_at']


class MembreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membre
        fields = [
            'id', 'numero_membre', 'nom', 'prenom', 'email', 'telephone', 
            'date_naissance', 'adresse', 'ville', 'pays', 'date_adhesion',
            'statut', 'type_mutuelle', 'numero_secu_sociale', 'created_at'
        ]


class MedecinSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Medecin
        fields = [
            'id', 'user', 'numero_ordre', 'specialite', 'etablissement',
            'telephone_pro', 'email_pro', 'annees_experience', 'tarif_consultation',
            'actif', 'disponible', 'date_inscription'
        ]


class OrdonnanceSerializer(serializers.ModelSerializer):
    medecin = UserSerializer(read_only=True)
    patient = MembreSerializer(read_only=True)
    
    class Meta:
        model = Ordonnance
        fields = [
            'id', 'numero', 'medecin', 'patient', 'date_prescription', 'date_expiration',
            'type_ordonnance', 'diagnostic', 'medicaments', 'posologie', 'duree_traitement',
            'renouvelable', 'nombre_renouvellements', 'renouvellements_effectues', 'statut',
            'est_urgent', 'notes', 'consultation', 'date_creation', 'date_modification'
        ]


class BonSerializer(serializers.ModelSerializer):
    membre = MembreSerializer(read_only=True)
    
    class Meta:
        model = Bon
        fields = [
            'id', 'numero_bon', 'membre', 'date_creation', 'date_emission',
            'type_soin', 'description', 'lieu_soins', 'date_soins', 'diagnostic',
            'medecin_traitant', 'numero_ordonnance', 'montant_total', 'taux_remboursement',
            'montant_rembourse', 'frais_dossier', 'statut', 'date_validation',
            'valide_par', 'motif_refus', 'piece_jointe', 'facture', 'created_at', 'updated_at'
        ]


class PaiementSerializer(serializers.ModelSerializer):
    bon = BonSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Paiement
        fields = [
            'id', 'bon', 'montant', 'mode_paiement', 'statut', 'numero_transaction',
            'banque', 'date_paiement', 'notes', 'created_by', 'created_at'
        ]


# ==============================================================================
# ✅ SERIALIZERS POUR LES MODÈLES SOINS (DÉCOMMENTÉS)
# ==============================================================================

class TypeSoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeSoin
        fields = ['id', 'nom', 'description', 'cout_reference', 'actif', 'created_at']


class SoinSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    medecin = MedecinSerializer(read_only=True)
    type_soin = TypeSoinSerializer(read_only=True)
    valide_par = UserSerializer(read_only=True)
    
    class Meta:
        model = Soin
        fields = [
            'id', 'patient', 'medecin', 'type_soin', 'date_realisation', 
            'date_creation', 'statut', 'cout', 'description', 'valide_par', 
            'date_validation', 'motif_rejet', 'created_by', 'duree_sejour',
            'diagnostic', 'taux_prise_charge', 'cout_estime', 'observations'
        ]


class SoinCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soin
        fields = [
            'patient', 'type_soin', 'date_realisation', 'cout', 'description',
            'duree_sejour', 'diagnostic', 'taux_prise_charge', 'cout_estime', 'observations'
        ]


class PrescriptionSerializer(serializers.ModelSerializer):
    soin = SoinSerializer(read_only=True)
    
    class Meta:
        model = Prescription
        fields = [
            'id', 'soin', 'medicament', 'posologie', 'duree_traitement', 'date_prescription'
        ]


# ==============================================================================
# ✅ SERIALIZERS POUR LES MODÈLES ASSUREUR
# ==============================================================================

class BonDeSoinSerializer(serializers.ModelSerializer):
    membre = MembreSerializer(read_only=True)
    assureur = UserSerializer(read_only=True)
    
    class Meta:
        model = BonDeSoin
        fields = [
            'id', 'numero_bon', 'membre', 'assureur', 'type_soin', 'priorite', 'statut',
            'montant', 'montant_reel', 'taux_remboursement', 'date_emission', 
            'date_validation', 'date_utilisation', 'date_expiration', 'medecin_traitant',
            'etablissement_medical', 'diagnostic', 'prescriptions', 'observations',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['numero_bon', 'created_at', 'updated_at']


class BonPriseEnChargeSerializer(serializers.ModelSerializer):
    membre = MembreSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    valide_par = UserSerializer(read_only=True)
    
    class Meta:
        model = BonPriseEnCharge
        fields = [
            'id', 'membre', 'created_by', 'numero_bon', 'montant_prise_en_charge',
            'taux_remboursement', 'date_creation', 'date_expiration', 'date_validation',
            'statut', 'valide_par', 'motif_rejet', 'notes'
        ]
        read_only_fields = ['numero_bon', 'date_creation']


class RapportAssureurSerializer(serializers.ModelSerializer):
    assureur = UserSerializer(read_only=True)
    
    class Meta:
        model = RapportAssureur
        fields = [
            'id', 'titre', 'assureur', 'type_rapport', 'periode_debut', 'periode_fin',
            'nombre_bons_emis', 'nombre_bons_utilises', 'montant_total_emis',
            'montant_total_rembourse', 'filtre_statut', 'filtre_type_soin', 'filtre_membre',
            'date_generation', 'description', 'parametres'
        ]
        read_only_fields = ['date_generation']


# ==============================================================================
# ✅ SERIALIZERS POUR LES STATISTIQUES
# ==============================================================================

class StatistiquesSoinsSerializer(serializers.Serializer):
    total_soins = serializers.IntegerField()
    soins_valides = serializers.IntegerField()
    soins_attente = serializers.IntegerField()
    soins_rejetes = serializers.IntegerField()
    cout_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    cout_moyen = serializers.DecimalField(max_digits=10, decimal_places=2)


class StatistiquesMembresSerializer(serializers.Serializer):
    total_membres = serializers.IntegerField()
    membres_actifs = serializers.IntegerField()
    nouveaux_membres_mois = serializers.IntegerField()


class StatistiquesPaiementsSerializer(serializers.Serializer):
    total_paiements = serializers.IntegerField()
    paiements_payes = serializers.IntegerField()
    paiements_attente = serializers.IntegerField()
    montant_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    montant_mois = serializers.DecimalField(max_digits=10, decimal_places=2)


class StatistiquesAssureurSerializer(serializers.Serializer):
    total_bons_emis = serializers.IntegerField()
    total_bons_utilises = serializers.IntegerField()
    total_bons_annules = serializers.IntegerField()
    montant_total_emis = serializers.DecimalField(max_digits=12, decimal_places=2)
    montant_total_rembourse = serializers.DecimalField(max_digits=12, decimal_places=2)
    taux_utilisation = serializers.DecimalField(max_digits=5, decimal_places=2)


# ==============================================================================
# ✅ SERIALIZERS POUR LA CRÉATION (WRITE)
# ==============================================================================

class BonDeSoinCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonDeSoin
        fields = [
            'membre', 'type_soin', 'priorite', 'montant', 'taux_remboursement',
            'medecin_traitant', 'etablissement_medical', 'diagnostic', 'prescriptions', 'observations'
        ]


class BonPriseEnChargeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonPriseEnCharge
        fields = [
            'membre', 'montant_prise_en_charge', 'taux_remboursement', 'date_expiration', 'notes'
        ]


class OrdonnanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordonnance
        fields = [
            'patient', 'type_ordonnance', 'diagnostic', 'medicaments', 'posologie',
            'duree_traitement', 'renouvelable', 'nombre_renouvellements', 'est_urgent', 'notes'
        ]