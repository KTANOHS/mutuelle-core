# tests/test_modele_cotisation.py
import pytest
from datetime import date
from django.test import TestCase
from cotisations.models import Cotisation

class TestModeleCotisation(TestCase):
    """Test unitaire pour le modèle Cotisation"""
    
    def setUp(self):
        """Initialisation des données de test"""
        self.cotisation_data = {
            'membre_id': 1,
            'montant': 100.00,
            'date_debut': date(2025, 1, 1),
            'date_fin': date(2025, 12, 31),
            'statut': 'active',
            'type_cotisation': 'annuelle'
        }
    
    def test_creation_cotisation(self):
        """Test création d'une cotisation valide"""
        cotisation = Cotisation.objects.create(**self.cotisation_data)
        
        # Vérifications
        self.assertEqual(cotisation.montant, 100.00)
        self.assertEqual(cotisation.statut, 'active')
        self.assertEqual(cotisation.type_cotisation, 'annuelle')
        self.assertIsNotNone(cotisation.date_creation)
    
    def test_montant_negatif(self):
        """Test montant négatif (doit échouer)"""
        with self.assertRaises(ValidationError):
            Cotisation.objects.create(
                membre_id=1,
                montant=-50.00,
                date_debut=date(2025, 1, 1),
                date_fin=date(2025, 12, 31)
            )
    
    def test_periode_invalide(self):
        """Test date fin avant date début"""
        with self.assertRaises(ValidationError):
            Cotisation.objects.create(
                membre_id=1,
                montant=100.00,
                date_debut=date(2025, 12, 31),
                date_fin=date(2025, 1, 1)
            )