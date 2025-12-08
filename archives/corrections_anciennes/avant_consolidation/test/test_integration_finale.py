# test_integration_finale.py - VERSION CORRIGÉE AVEC MATRICULE UNIQUE
import os
import django
import sys
from datetime import date
import random
import string

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from membres.models import Membre
from agents.models import Agent, VerificationCotisation

def generer_matricule_unique():
    """Génère un matricule unique pour les tests"""
    lettres = ''.join(random.choices(string.ascii_uppercase, k=3))
    chiffres = ''.join(random.choices(string.digits, k=3))
    return f"TEST-{lettres}{chiffres}"

class TestIntegrationAffichageUnifie(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Générer des identifiants uniques pour éviter les conflits
        timestamp = str(random.randint(1000, 9999))
        username = f"agent_test_{timestamp}"
        matricule = generer_matricule_unique()
        numero_membre = f"TESTMEM{timestamp}"
        
        self.user = User.objects.create_user(
            username=username,
            password='password123',
            first_name='Jean',
            last_name='Agent'
        )
        
        # CORRECTION : Matricule unique
        self.agent = Agent.objects.create(
            user=self.user,
            matricule=matricule,
            poste='Agent de terrain',
            date_embauche=date.today(),
            limite_bons_quotidienne=10,
            est_actif=True
        )
        
        self.membre = Membre.objects.create(
            nom='Doe',
            prenom='John',
            numero_unique=numero_membre,
            telephone='0123456789',
            email='john.doe@example.com'
        )
    
    def test_acces_fiche_unifiee(self):
        """Test l'accès à la fiche unifiée via l'URL"""
        # Login en tant qu'agent
        self.client.login(username=self.user.username, password='password123')
        
        # Accéder à la fiche unifiée
        response = self.client.get(f'/agents/fiche-cotisation-unifiee/{self.membre.id}/')
        
        # Vérifications
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'FICHE COTISATION UNIFIÉE')
        self.assertContains(response, 'John Doe')
        self.assertContains(response, self.membre.numero_unique)
    
    def test_fiche_avec_verification(self):
        """Test la fiche avec une vérification existante"""
        # Créer une vérification
        verification = VerificationCotisation.objects.create(
            agent=self.agent,
            membre=self.membre,
            statut_cotisation='a_jour',
            montant_dette_str='0 FCFA',
            prochaine_echeance=date.today(),
            observations='Test de vérification'
        )
        
        self.client.login(username=self.user.username, password='password123')
        response = self.client.get(f'/agents/fiche-cotisation-unifiee/{self.membre.id}/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'À jour')
        self.assertContains(response, '0 FCFA')

if __name__ == '__main__':
    import unittest
    unittest.main()