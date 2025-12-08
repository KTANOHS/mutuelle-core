from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from medecin.models import Ordonnance
from membres.models import Membre
from assureur.models import Assureur, Bon
from .models import Pharmacien, OrdonnancePharmacien, StockPharmacie

class PharmacienTests(TestCase):
    def setUp(self):
        """Configuration initiale pour tous les tests - VERSION FINALE CORRIGÉE"""
        # Créer les groupes
        self.pharmacien_group, _ = Group.objects.get_or_create(name='Pharmacien')
        self.medecin_group, _ = Group.objects.get_or_create(name='Medecin')
        self.membre_group, _ = Group.objects.get_or_create(name='Membre')
        self.assureur_group, _ = Group.objects.get_or_create(name='Assureur')
        
        # Créer les utilisateurs AVEC PRÉNOM ET NOM
        self.pharmacien_user = User.objects.create_user(
            username='pharmacien', 
            password='testpass123',
            first_name='Pierre',
            last_name='Pharmacien'
        )
        self.pharmacien_user.groups.add(self.pharmacien_group)
        
        self.medecin_user = User.objects.create_user(
            username='docteur', 
            password='testpass123',
            first_name='Jean',
            last_name='Dupont'
        )
        self.medecin_user.groups.add(self.medecin_group)
        
        self.membre_user = User.objects.create_user(
            username='patient', 
            password='testpass123',
            first_name='Marie',
            last_name='Martin'
        )
        self.membre_user.groups.add(self.membre_group)
        
        self.assureur_user = User.objects.create_user(
            username='assureur_test', 
            password='testpass123',
            first_name='Compagnie',
            last_name='Assurance'
        )
        self.assureur_user.groups.add(self.assureur_group)
        
        # Créer les profils
        self.pharmacien = Pharmacien.objects.create(
            user=self.pharmacien_user,
            numero_pharmacien='PHARM001',
            nom_pharmacie='Pharmacie Centrale',
            adresse_pharmacie='123 Rue Principale',
            telephone='0123456789'
        )
        
        # 🔥 CORRECTION: L'assureur doit être créé avec user seulement
        self.assureur = Assureur.objects.create(user=self.assureur_user)
        
        # 🔥 CORRECTION: Le membre se crée automatiquement avec l'utilisateur qui a first_name et last_name
        # Pas besoin de créer Membre manuellement, il se crée via le signal
        # Mais si vous devez le créer manuellement, assurez-vous que l'utilisateur a first_name et last_name
        self.membre = Membre.objects.create(user=self.membre_user)
        
        self.client = Client()

    def test_creation_ordonnance_pharmacien(self):
        """Test la création d'une ordonnance pharmacien - VERSION CORRIGÉE"""
        # Créer d'abord une ordonnance médecin
        ordonnance_medecin = Ordonnance.objects.create(
            medecin=self.medecin_user,
            patient=self.membre,
            assureur=self.assureur,
            diagnostic='Test diagnostic',
            medicaments='Paracétamol',
            posologie='1 comprimé',
            duree_traitement=7
        )
        
        # Créer un bon
        bon = Bon.objects.create(
            ordonnance=ordonnance_medecin,
            membre=self.membre,
            created_by=self.assureur.user,
            type_soin='pharmacie',
            montant_total=5000,
            montant_prise_charge=4000,
            nom_medecin='Dr Test',
            date_soin=timezone.now().date(),
            date_expiration=timezone.now().date() + timedelta(days=30)
        )
        
        # Créer l'ordonnance pharmacien
        ordonnance_pharma = OrdonnancePharmacien.objects.create(
            ordonnance_medecin=ordonnance_medecin,
            bon_prise_charge=bon,
            medicament='Paracétamol 500mg',
            posologie_appliquee='1 comprimé 3 fois par jour',
            duree_traitement=7,
            pharmacien_validateur=self.pharmacien_user
        )
        
        # Vérifications
        self.assertEqual(ordonnance_pharma.ordonnance_medecin, ordonnance_medecin)
        self.assertEqual(ordonnance_pharma.bon_prise_charge, bon)
        self.assertEqual(ordonnance_pharma.statut, 'ACTIVE')

    def test_gestion_stock(self):
        """Test la gestion du stock - VERSION CORRIGÉE"""
        stock = StockPharmacie.objects.create(
            pharmacie=self.pharmacien,
            medicament='Paracétamol 500mg',
            code_medicament='PARA500',
            quantite_en_stock=50,
            seuil_alerte=10,
            prix_achat=500,
            prix_vente=800
        )
        
        # Vérifications initiales
        self.assertFalse(stock.en_rupture)
        self.assertFalse(stock.besoin_reapprovisionnement)
        
        # Diminuer le stock
        stock.diminuer_stock(45)  # Descend à 5
        self.assertTrue(stock.besoin_reapprovisionnement)
        
        # Augmenter le stock
        stock.augmenter_stock(20)  # Monte à 25
        self.assertFalse(stock.besoin_reapprovisionnement)