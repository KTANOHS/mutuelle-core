# tests/test_performance_cotisation.py
import time
from locust import HttpUser, task, between

class CotisationLoadTest(HttpUser):
    """Test de performance pour création de cotisations"""
    
    wait_time = between(1, 3)
    
    def on_start(self):
        """Authentification avant les tests"""
        self.client.post("/api/auth/login/", {
            "username": "loadtest",
            "password": "test123"
        })
    
    @task
    def create_cotisation(self):
        """Tâche de création de cotisation"""
        headers = {'Content-Type': 'application/json'}
        data = {
            'membre_id': 1,
            'montant': 100.00,
            'date_debut': '2025-01-01',
            'date_fin': '2025-12-31'
        }
        
        start_time = time.time()
        response = self.client.post(
            "/api/cotisations/",
            json=data,
            headers=headers
        )
        end_time = time.time()
        
        # Log des métriques
        if response.status_code == 201:
            print(f"Temps de réponse: {end_time - start_time:.3f}s")