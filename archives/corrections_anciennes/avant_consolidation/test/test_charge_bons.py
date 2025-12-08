# scripts/test_charge_bons.py
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor
import threading

class TestChargeCreationBons:
    """Test de charge pour la création de bons de soin"""
    
    def __init__(self, base_url, nombre_utilisateurs=10, nombre_requetes=100):
        self.base_url = base_url
        self.nombre_utilisateurs = nombre_utilisateurs
        self.nombre_requetes = nombre_requetes
        self.resultats = []
        self.lock = threading.Lock()
        
    def creer_session_utilisateur(self, user_id):
        """Créer une session pour un utilisateur simulé"""
        session = requests.Session()
        # Ici, vous devriez implémenter la logique d'authentification
        return session
    
    def test_creation_bon(self, session, bon_id):
        """Tester la création d'un bon de soin"""
        debut = time.time()
        
        try:
            # Données du bon
            data = {
                'type_soin': 'consultation',
                'montant': '10000',
                'symptomes': f'Test charge {bon_id}',
                'diagnostic': f'Diagnostic charge {bon_id}'
            }
            
            # URL de création (à adapter)
            url = f"{self.base_url}/agents/creer-bon-soin/1/"  # ID membre 1 pour les tests
            
            response = session.post(url, data=data)
            duree = time.time() - debut
            
            with self.lock:
                self.resultats.append({
                    'bon_id': bon_id,
                    'statut': response.status_code,
                    'duree': duree,
                    'succes': response.status_code == 302  # Redirection après succès
                })
                
            return response.status_code == 302
            
        except Exception as e:
            with self.lock:
                self.resultats.append({
                    'bon_id': bon_id,
                    'statut': 0,
                    'duree': time.time() - debut,
                    'succes': False,
                    'erreur': str(e)
                })
            return False
    
    def executer_test_charge(self):
        """Exécuter le test de charge"""
        print(f"🚀 Début du test de charge avec {self.nombre_utilisateurs} utilisateurs")
        print(f"🎯 Nombre total de requêtes: {self.nombre_requetes}")
        
        debut_total = time.time()
        
        with ThreadPoolExecutor(max_workers=self.nombre_utilisateurs) as executor:
            # Préparer les sessions utilisateur
            sessions = [self.creer_session_utilisateur(i) for i in range(self.nombre_utilisateurs)]
            
            # Soumettre les tâches
            futures = []
            for i in range(self.nombre_requetes):
                session = sessions[i % self.nombre_utilisateurs]
                future = executor.submit(self.test_creation_bon, session, i)
                futures.append(future)
            
            # Attendre la fin
            for future in futures:
                future.result()
        
        duree_totale = time.time() - debut_total
        
        # Analyser les résultats
        self.analyser_resultats(duree_totale)
    
    def analyser_resultats(self, duree_totale):
        """Analyser et afficher les résultats du test"""
        succes = sum(1 for r in self.resultats if r['succes'])
        echecs = len(self.resultats) - succes
        durees = [r['duree'] for r in self.resultats if r['succes']]
        
        if durees:
            duree_moyenne = sum(durees) / len(durees)
            duree_max = max(durees)
            duree_min = min(durees)
        else:
            duree_moyenne = duree_max = duree_min = 0
        
        print("\n📊 RÉSULTATS DU TEST DE CHARGE")
        print("=" * 50)
        print(f"Requêtes totales: {len(self.resultats)}")
        print(f"Succès: {succes}")
        print(f"Échecs: {echecs}")
        print(f"Taux de succès: {(succes/len(self.resultats))*100:.1f}%")
        print(f"Durée totale: {duree_totale:.2f} secondes")
        print(f"Requêtes par seconde: {len(self.resultats)/duree_totale:.2f}")
        print(f"Temps de réponse moyen: {duree_moyenne*1000:.2f} ms")
        print(f"Temps de réponse min: {duree_min*1000:.2f} ms")
        print(f"Temps de réponse max: {duree_max*1000:.2f} ms")

if __name__ == "__main__":
    test = TestChargeCreationBons(
        base_url="http://localhost:8000",
        nombre_utilisateurs=5,
        nombre_requetes=50
    )
    test.executer_test_charge()