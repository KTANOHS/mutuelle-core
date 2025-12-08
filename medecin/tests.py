from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Ordonnance
from membres.models import Membre
from assureur.models import Assureur

class MedecinTests(TestCase):
    def setUp(self):
        """Configuration initiale pour tous les tests"""
        # Créer les groupes
        self.medecin_group, _ = Group.objects.get_or_create(name='Medecin')
        self.membre_group, _ = Group.objects.get_or_create(name='Membre')
        self.assureur_group, _ = Group.objects.get_or_create(name='Assureur')
        
        # Créer les utilisateurs AVEC PRÉNOM ET NOM
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
            username='assureur', 
            password='testpass123',
            first_name='Compagnie',
            last_name='Assurance'
        )
        self.assureur_user.groups.add(self.assureur_group)
        
        # Créer les profils
        self.assureur = Assureur.objects.create(user=self.assureur_user)
        self.membre = Membre.objects.create(user=self.membre_user)
        self.membre.assureur = self.assureur
        self.membre.save()
        
        self.client = Client()

    def test_creation_ordonnance(self):
        """Test la création d'une ordonnance"""
        # Se connecter comme médecin
        self.client.login(username='docteur', password='testpass123')
        
        # Données de l'ordonnance
        ordonnance_data = {
            'patient': self.membre.id,
            'diagnostic': 'Grippe sévère',
            'medicaments': 'Paracétamol 500mg\nVitamine C',
            'posologie': '1 comprimé 3 fois par jour',
            'duree_traitement': 7,
            'type_ordonnance': 'MEDICAMENTS',
            'renouvelable': False,
        }
        
        # Créer l'ordonnance via la vue (si la vue existe)
        # Pour l'instant, créons directement
        ordonnance = Ordonnance.objects.create(
            medecin=self.medecin_user,
            patient=self.membre,
            assureur=self.assureur,
            diagnostic='Grippe sévère',
            medicaments='Paracétamol 500mg\nVitamine C',
            posologie='1 comprimé 3 fois par jour',
            duree_traitement=7
        )
        
        # Vérifier que l'ordonnance a été créée
        self.assertEqual(Ordonnance.objects.count(), 1)
        
        # Vérifications
        self.assertEqual(ordonnance.medecin, self.medecin_user)
        self.assertEqual(ordonnance.patient, self.membre)
        self.assertEqual(ordonnance.diagnostic, 'Grippe sévère')
        self.assertEqual(ordonnance.statut, 'EN_ATTENTE_VALIDATION')
        self.assertTrue(ordonnance.numero)  # Numéro généré automatiquement

    def test_ordonnance_est_valide(self):
        """Test la validité d'une ordonnance"""
        ordonnance = Ordonnance.objects.create(
            medecin=self.medecin_user,
            patient=self.membre,
            assureur=self.assureur,
            diagnostic='Test diagnostic',
            medicaments='Test médicament',
            posologie='Test posologie',
            duree_traitement=7,
            date_expiration=timezone.now().date() + timedelta(days=10)
        )
        
        # Vérifier que l'ordonnance est valide
        self.assertTrue(ordonnance.est_valide)
        
        # Tester avec une ordonnance expirée
        ordonnance_expiree = Ordonnance.objects.create(
            medecin=self.medecin_user,
            patient=self.membre,
            assureur=self.assureur,
            diagnostic='Test diagnostic',
            medicaments='Test médicament',
            posologie='Test posologie',
            duree_traitement=7,
            date_expiration=timezone.now().date() - timedelta(days=1)
        )
        
        self.assertFalse(ordonnance_expiree.est_valide)

    def test_medicaments_liste(self):
        """Test la conversion des médicaments en liste"""
        ordonnance = Ordonnance.objects.create(
            medecin=self.medecin_user,
            patient=self.membre,
            assureur=self.assureur,
            diagnostic='Test diagnostic',
            medicaments='Paracétamol 500mg\nVitamine C\nAspirine',
            posologie='Test posologie',
            duree_traitement=7
        )
        
        medicaments_liste = ordonnance.medicaments_liste
        self.assertEqual(len(medicaments_liste), 3)
        self.assertIn('Paracétamol 500mg', medicaments_liste)
        self.assertIn('Vitamine C', medicaments_liste)
        self.assertIn('Aspirine', medicaments_liste)