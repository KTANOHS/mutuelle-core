import os
import django
import sys
from datetime import datetime, timedelta

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

import pytest
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.management import call_command
from medecin.models import MedecinProfile
from membres.models import Membre

User = get_user_model()

class TestConnexionMedecin(TestCase):
    """
    Tests complets pour la connexion de l'application médecin
    """
    
    def setUp(self):
        """Initialisation des données de test"""
        self.client = Client()
        
        # Création d'un utilisateur médecin
        self.medecin_user = User.objects.create_user(
            username='dr.test',
            email='dr.test@clinique.com',
            password='Medecin123!',
            first_name='Jean',
            last_name='Test',
            is_active=True
        )
        
        # Création du profil médecin
        self.medecin_profile = MedecinProfile.objects.create(
            user=self.medecin_user,
            numero_ordre='MED123456',
            specialite='Generaliste',
            telephone='+2250102030405',
            adresse_cabinet='123 Rue de la Santé, Abidjan',
            est_actif=True
        )
        
        # Création d'un utilisateur normal (non médecin)
        self.user_normal = User.objects.create_user(
            username='user.normal',
            email='user@normal.com',
            password='User123!',
            first_name='Normal',
            last_name='User'
        )
        
        # URLs
        self.login_url = reverse('medecin:connexion')
        self.dashboard_url = reverse('medecin:dashboard')
        self.logout_url = reverse('medecin:deconnexion')
    
    def test_page_connexion_accessible(self):
        """Test que la page de connexion est accessible"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'medecin/auth/connexion.html')
        self.assertContains(response, 'Connexion Médecin')
    
    def test_connexion_success_medecin(self):
        """Test de connexion réussie pour un médecin"""
        data = {
            'username': 'dr.test',
            'password': 'Medecin123!'
        }
        
        response = self.client.post(self.login_url, data, follow=True)
        
        # Vérification de la redirection
        self.assertRedirects(response, self.dashboard_url)
        
        # Vérification que l'utilisateur est connecté
        self.assertTrue(response.context['user'].is_authenticated)
        
        # Vérification des messages de succès
        messages = list(response.context['messages'])
        self.assertTrue(any('connecté' in str(message) for message in messages))
    
    def test_connexion_echec_mauvais_password(self):
        """Test d'échec de connexion avec mauvais mot de passe"""
        data = {
            'username': 'dr.test',
            'password': 'MauvaisPassword123!'
        }
        
        response = self.client.post(self.login_url, data)
        
        # Vérification que l'utilisateur n'est pas connecté
        self.assertFalse(response.context['user'].is_authenticated)
        
        # Vérification du message d'erreur
        self.assertContains(response, 'Identifiants invalides')
    
    def test_connexion_echec_utilisateur_inexistant(self):
        """Test d'échec de connexion avec utilisateur inexistant"""
        data = {
            'username': 'utilisateur.inexistant',
            'password': 'Password123!'
        }
        
        response = self.client.post(self.login_url, data)
        self.assertContains(response, 'Identifiants invalides')
    
    def test_connexion_echec_utilisateur_non_medecin(self):
        """Test d'échec de connexion avec un utilisateur non médecin"""
        data = {
            'username': 'user.normal',
            'password': 'User123!'
        }
        
        response = self.client.post(self.login_url, data)
        self.assertContains(response, "n'est pas autorisé")
    
    def test_redirection_si_deja_connecte(self):
        """Test de redirection si l'utilisateur est déjà connecté"""
        # Connexion d'abord
        self.client.login(username='dr.test', password='Medecin123!')
        
        # Tentative d'accès à la page de connexion
        response = self.client.get(self.login_url, follow=True)
        
        # Doit rediriger vers le dashboard
        self.assertRedirects(response, self.dashboard_url)
    
    def test_deconnexion(self):
        """Test de la déconnexion"""
        # Connexion d'abord
        self.client.login(username='dr.test', password='Medecin123!')
        
        # Vérification que l'utilisateur est connecté
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        
        # Déconnexion
        response = self.client.get(self.logout_url, follow=True)
        
        # Vérification de la redirection
        self.assertRedirects(response, reverse('medecin:connexion'))
        
        # Vérification que l'utilisateur est déconnecté
        self.assertFalse(response.context['user'].is_authenticated)
    
    def test_acces_dashboard_sans_connexion(self):
        """Test d'accès au dashboard sans être connecté"""
        response = self.client.get(self.dashboard_url, follow=True)
        
        # Doit rediriger vers la page de connexion
        self.assertRedirects(response, f"{self.login_url}?next={self.dashboard_url}")
    
    def test_champs_obligatoires_formulaire(self):
        """Test des champs obligatoires du formulaire"""
        # Test sans username
        data = {'password': 'Medecin123!'}
        response = self.client.post(self.login_url, data)
        self.assertContains(response, 'Ce champ est obligatoire')
        
        # Test sans password
        data = {'username': 'dr.test'}
        response = self.client.post(self.login_url, data)
        self.assertContains(response, 'Ce champ est obligatoire')
    
    def test_medecin_inactif(self):
        """Test de connexion avec un médecin inactif"""
        # Désactivation du médecin
        self.medecin_profile.est_actif = False
        self.medecin_profile.save()
        
        data = {
            'username': 'dr.test',
            'password': 'Medecin123!'
        }
        
        response = self.client.post(self.login_url, data)
        self.assertContains(response, "n'est pas autorisé")

# Tests API et fonctionnalités avancées
class TestFonctionnalitesMedecin(TestCase):
    
    def setUp(self):
        self.client = Client()
        
        # Création médecin
        self.medecin_user = User.objects.create_user(
            username='dr.api',
            password='Medecin123!'
        )
        self.medecin_profile = MedecinProfile.objects.create(
            user=self.medecin_user,
            numero_ordre='MED789012',
            specialite='Cardiologie'
        )
        
        # Création patient
        self.patient = Membre.objects.create(
            numero_affiliation='PAT001',
            nom='Doe',
            prenom='John',
            telephone='+2250506070809',
            est_actif=True
        )
    
    def test_api_verifier_patient(self):
        """Test de l'API de vérification patient"""
        # Connexion d'abord
        self.client.login(username='dr.api', password='Medecin123!')
        
        url = reverse('medecin:verifier_patient_api')
        data = {'numero_affiliation': 'PAT001'}
        
        response = self.client.post(
            url, 
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('patient', response.json())
    
    def test_recherche_patient(self):
        """Test de la recherche de patient"""
        self.client.login(username='dr.api', password='Medecin123!')
        
        url = reverse('medecin:rechercher_patient')
        data = {'q': 'Doe'}
        
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Doe')