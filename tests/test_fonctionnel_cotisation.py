# tests/test_fonctionnel_cotisation.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class TestFonctionnelCreationCotisation(StaticLiveServerTestCase):
    """Test fonctionnel de création via interface web"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    def test_creation_via_interface(self):
        """Test complet via l'interface utilisateur"""
        # Connexion
        self.selenium.get(f'{self.live_server_url}/login')
        username_input = self.selenium.find_element(By.NAME, 'username')
        password_input = self.selenium.find_element(By.NAME, 'password')
        username_input.send_keys('admin')
        password_input.send_keys('admin123')
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        
        # Navigation vers création cotisation
        self.selenium.get(f'{self.live_server_url}/cotisations/nouvelle')
        
        # Remplissage du formulaire
        self.selenium.find_element(By.NAME, 'montant').send_keys('200.00')
        self.selenium.find_element(By.NAME, 'date_debut').send_keys('01012025')
        self.selenium.find_element(By.NAME, 'date_fin').send_keys('31122025')
        
        # Soumission
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        
        # Vérification du succès
        success_message = self.selenium.find_element(By.CLASS_NAME, 'alert-success')
        self.assertIn('Cotisation créée avec succès', success_message.text)