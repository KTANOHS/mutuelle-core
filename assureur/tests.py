from datetime import date  # AJOUTER CET IMPORT
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

from assureur.models import Membre, Bon, Cotisation, Assureur

class AssureurTests(TestCase):
    
    def setUp(self):
        """Configuration initiale pour tous les tests - VERSION CORRIGÉE"""
        # Créer un utilisateur assureur
        self.user_assureur = User.objects.create_user(
            username='assureur_test',
            password='password123',
            email='assureur@test.com',
            first_name='Jean',
            last_name='Dupont'
        )
        
        # Créer un profil Assureur
        self.assureur = Assureur.objects.create(
            user=self.user_assureur,
            numero_employe='EMP001',
            departement='gestion'
        )
        
        # ✅ CORRECTION : Utiliser date(1990, 1, 1) au lieu de string
        self.membre = Membre.objects.create(
            numero_membre="MEM20250001",
            nom="Doe",
            prenom="John", 
            date_naissance=date(1990, 1, 1),  # ✅ CORRIGÉ : objet date
            email="john.doe@example.com",
            telephone="+1234567890",
            adresse="123 Rue Test, Ville",
            date_adhesion=timezone.now().date(),
            type_contrat="individuel",
            numero_contrat="CONT001",
            date_effet=timezone.now().date(),
            date_expiration=timezone.now().date() + timezone.timedelta(days=365),
            taux_couverture=100.00,
            statut='actif'
        )
    
    def test_membre_est_actif(self):
        """Test le statut actif du membre - VERSION CORRIGÉE"""
        self.assertTrue(self.membre.est_actif())
        
        # ✅ CORRECTION : Calcul dynamique de l'âge au lieu de valeur fixe
        today = timezone.now().date()
        expected_age = today.year - 1990 - ((today.month, today.day) < (1, 1))
        self.assertEqual(self.membre.age(), expected_age)
    
    def test_montant_cotisation_membre(self):
        """Test le calcul du montant de cotisation"""
        montant_normal = self.membre.montant_cotisation_mensuelle()
        self.assertEqual(montant_normal, Decimal('5000.00'))
        
        # Tester pour une femme enceinte
        self.membre.est_femme_enceinte = True
        self.membre.date_accouchement_prevue = timezone.now().date() + timezone.timedelta(days=60)
        self.membre.save()
        
        montant_enceinte = self.membre.montant_cotisation_mensuelle()
        self.assertEqual(montant_enceinte, Decimal('7500.00'))