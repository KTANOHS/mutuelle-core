# tests/test_api_cotisation.py
import json
from rest_framework.test import APITestCase
from rest_framework import status

class TestAPICotisation(APITestCase):
    """Test API pour la création de cotisation"""
    
    def setUp(self):
        """Authentification et données de test"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.valid_payload = {
            'membre_id': 1,
            'montant': 150.50,
            'date_debut': '2025-01-01',
            'date_fin': '2025-12-31',
            'type_cotisation': 'annuelle'
        }
    
    def test_create_cotisation_authenticated(self):
        """Test création avec authentification"""
        response = self.client.post(
            '/api/cotisations/',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['montant'], '150.50')
    
    def test_create_cotisation_unauthenticated(self):
        """Test création sans authentification"""
        self.client.logout()
        response = self.client.post('/api/cotisations/', self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_with_missing_fields(self):
        """Test création avec champs manquants"""
        invalid_payload = {'membre_id': 1, 'montant': 100.00}
        response = self.client.post('/api/cotisations/', invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)