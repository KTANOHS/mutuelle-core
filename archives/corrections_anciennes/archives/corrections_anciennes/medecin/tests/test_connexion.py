from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from medecin.models import Medecin, SpecialiteMedicale, EtablissementMedical

User = get_user_model()

class TestConnexionMedecin(TestCase):
    """Tests unitaires pour la connexion médecin - Adapté à la structure existante"""
    
    def setUp(self):
        self.client = Client()
        
        # Créer les données de base
        self.specialite = SpecialiteMedicale.objects.create(
            nom='Généraliste',
            description='Médecine générale'
        )
        
        self.etablissement = EtablissementMedical.objects.create(
            nom='Hôpital Test',
            type_etablissement='HOPITAL',
            adresse='123 Rue Test',
            telephone='+2250102030405',
            ville='Abidjan'
        )
        
        self.groupe_medecin, _ = Group.objects.get_or_create(name='medecin')
        
        # Créer un utilisateur médecin
        self.medecin_user = User.objects.create_user(
            username='dr.unittest',
            password='Medecin123!',
            first_name='Unit',
            last_name='Test',
            email='unit@test.com',
            is_active=True
        )
        self.medecin_user.groups.add(self.groupe_medecin)
        
        # Créer le profil médecin
        self.medecin = Medecin.objects.create(
            user=self.medecin_user,
            numero_ordre='MEDUNIT001',
            specialite=self.specialite,
            etablissement=self.etablissement,
            telephone_pro='+2250506070809',
            actif=True,
            disponible=True
        )
        
        # Créer un utilisateur normal (non médecin)
        self.user_normal = User.objects.create_user(
            username='user.normal',
            password='User123!'
        )
    
    def test_page_connexion_accessible(self):
        """Test que la page de connexion est accessible"""
        response = self.client.get('/medecin/connexion/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Connexion')
    
    def test_connexion_medecin_valide(self):
        """Test de connexion réussie pour un médecin"""
        response = self.client.post('/medecin/connexion/', {
            'username': 'dr.unittest',
            'password': 'Medecin123!'
        }, follow=True)
        
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].username, 'dr.unittest')
        
        # Vérifier que l'utilisateur a un profil médecin
        self.assertTrue(hasattr(response.context['user'], 'medecin_profile'))
    
    def test_connexion_medecin_invalide(self):
        """Test d'échec de connexion avec mauvais mot de passe"""
        response = self.client.post('/medecin/connexion/', {
            'username': 'dr.unittest',
            'password': 'MauvaisPassword'
        })
        
        self.assertFalse(response.context['user'].is_authenticated)
    
    def test_connexion_utilisateur_non_medecin(self):
        """Test qu'un utilisateur normal ne peut pas se connecter à l'espace médecin"""
        response = self.client.post('/medecin/connexion/', {
            'username': 'user.normal',
            'password': 'User123!'
        })
        
        # L'utilisateur ne devrait pas pouvoir se connecter à l'espace médecin
        # même avec des identifiants valides car il n'a pas de profil médecin
        self.assertFalse(response.context['user'].is_authenticated)
    
    def test_medecin_inactif(self):
        """Test qu'un médecin inactif ne peut pas se connecter"""
        # Désactiver le médecin
        self.medecin.actif = False
        self.medecin.save()
        
        response = self.client.post('/medecin/connexion/', {
            'username': 'dr.unittest',
            'password': 'Medecin123!'
        })
        
        self.assertFalse(response.context['user'].is_authenticated')
    
    def test_redirection_si_deja_connecte(self):
        """Test de redirection si l'utilisateur est déjà connecté"""
        # Se connecter d'abord
        self.client.login(username='dr.unittest', password='Medecin123!')
        
        # Tenter d'accéder à la page de connexion
        response = self.client.get('/medecin/connexion/', follow=True)
        
        # Devrait rediriger vers le dashboard
        self.assertEqual(response.status_code, 200)
        # Vérifier qu'on est sur une page autre que la connexion
        self.assertNotContains(response, 'Connexion Médecin')
    
    def test_deconnexion(self):
        """Test de la déconnexion"""
        # Se connecter d'abord
        self.client.login(username='dr.unittest', password='Medecin123!')
        
        # Vérifier qu'on est connecté
        response = self.client.get('/medecin/dashboard/')
        self.assertEqual(response.status_code, 200)
        
        # Se déconnecter
        response = self.client.get('/medecin/deconnexion/', follow=True)
        
        # Vérifier qu'on est déconnecté
        self.assertFalse(response.context['user'].is_authenticated)
        
        # Vérifier la redirection
        self.assertRedirects(response, '/medecin/connexion/')