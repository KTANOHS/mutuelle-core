from django.test import TestCase
from django.urls import reverse

class URLTests(TestCase):
    """Tests pour les URLs de l'application assureur - VERSION CORRIGÉE"""
    
    def test_repondre_message_url(self):
        """Test que l'URL de réponse aux messages est correcte - VERSION CORRIGÉE"""
        # ✅ CORRECTION : Utiliser l'URL que vous avez réellement définie
        url = reverse('assureur:repondre_message', args=[1])
        # Votre URL est : 'repondre_message/<int:message_id>/'
        self.assertEqual(url, '/assureur/repondre_message/1/')
    
    def test_dashboard_url(self):
        """Test que l'URL du dashboard est correcte"""
        url = reverse('assureur:dashboard')
        self.assertEqual(url, '/assureur/dashboard/')
    
    def test_liste_membres_url(self):
        """Test que l'URL de la liste des membres est correcte"""
        url = reverse('assureur:liste_membres')
        self.assertEqual(url, '/assureur/membres/')
    
    def test_creer_membre_url(self):
        """Test que l'URL de création de membre est correcte"""
        url = reverse('assureur:creer_membre')
        self.assertEqual(url, '/assureur/creer-membre/')
    
    def test_liste_bons_url(self):
        """Test que l'URL de la liste des bons est correcte"""
        url = reverse('assureur:liste_bons')
        self.assertEqual(url, '/assureur/bons/')
    
    def test_creer_bon_url(self):
        """Test que l'URL de création de bon est correcte"""
        url = reverse('assureur:creer_bon', args=[1])
        self.assertEqual(url, '/assureur/bons/creer/1/')
    
    def test_liste_paiements_url(self):
        """Test que l'URL de la liste des paiements est correcte"""
        url = reverse('assureur:liste_paiements')
        self.assertEqual(url, '/assureur/paiements/')
    
    def test_liste_cotisations_url(self):
        """Test que l'URL de la liste des cotisations est correcte"""
        url = reverse('assureur:liste_cotisations')
        self.assertEqual(url, '/assureur/cotisations/')
    
    def test_configuration_url(self):
        """Test que l'URL de configuration est correcte"""
        url = reverse('assureur:configuration')
        self.assertEqual(url, '/assureur/configuration/')