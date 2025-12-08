# test_avec_messages.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import TestCase
from django.contrib.auth.models import User

class TestGenerationCotisations(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_page_generation(self):
        """Test de la page de génération"""
        response = self.client.get('/assureur/cotisations/generer/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'periode')
        print("✅ Test page génération: PASSÉ")
    
    def test_preview(self):
        """Test de la prévisualisation"""
        response = self.client.get('/assureur/cotisations/preview/?periode=2025-03')
        self.assertEqual(response.status_code, 200)
        print("✅ Test prévisualisation: PASSÉ")
    
    def test_generation_post(self):
        """Test de la génération par POST"""
        # D'abord GET pour obtenir le CSRF token
        response = self.client.get('/assureur/cotisations/generer/')
        csrf_token = self._extract_csrf(response.content.decode('utf-8'))
        
        # Ensuite POST
        response = self.client.post('/assureur/cotisations/generer/', {
            'periode': '2025-03',
            'csrfmiddlewaretoken': csrf_token
        })
        
        # La réponse devrait être 302 (redirection) ou 200 avec succès
        self.assertIn(response.status_code, [200, 302])
        print(f"✅ Test génération POST: PASSÉ (status: {response.status_code})")
    
    def _extract_csrf(self, content):
        """Extrait le token CSRF du HTML"""
        import re
        match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)
        return match.group(1) if match else None

# Exécution
if __name__ == '__main__':
    import unittest
    unittest.main()