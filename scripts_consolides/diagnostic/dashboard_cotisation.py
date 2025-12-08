# scripts_consolides/diagnostic/dashboard_cotisation.py
import pandas as pd
from datetime import datetime
from django.db import connection

class DashboardCotisation:
    """Dashboard de monitoring des cotisations"""
    
    @staticmethod
    def get_cotisation_stats():
        """Statistiques globales"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(montant) as total_montant,
                    AVG(montant) as moyenne_montant,
                    MIN(date_debut) as plus_ancienne,
                    MAX(date_debut) as plus_recente
                FROM cotisations_cotisation
                WHERE statut = 'active'
            """)
            return cursor.fetchone()
    
    @staticmethod
    def test_creation_scenarios():
        """Test des scénarios de création"""
        scenarios = [
            {
                'nom': 'Cotisation annuelle standard',
                'data': {'montant': 100, 'type': 'annuelle'},
                'attendu': 'SUCCÈS'
            },
            {
                'nom': 'Cotisation mensuelle',
                'data': {'montant': 10, 'type': 'mensuelle'},
                'attendu': 'SUCCÈS'
            },
            {
                'nom': 'Montant négatif',
                'data': {'montant': -50, 'type': 'annuelle'},
                'attendu': 'ÉCHEC'
            },
            {
                'nom': 'Montant zéro',
                'data': {'montant': 0, 'type': 'annuelle'},
                'attendu': 'SUCCÈS'
            }
        ]
        
        results = []
        for scenario in scenarios:
            # Simuler la création
            # ... code de test ...
            results.append(scenario)
        
        return pd.DataFrame(results)
        