import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate

def test_recherche_apres_correction():
    """Tester la recherche API après correction"""
    print("🔍 TEST RECHERCHE APRÈS CORRECTION")
    print("==================================")
    
    # Authentification
    client = Client()
    user = authenticate(username='koffitanoh', password='votre_mot_de_passe')
    
    if user:
        client.force_login(user)
        print("✅ Authentification réussie")
        
        # Test de recherche avec différents termes
        termes_recherche = ['John', 'Doe', 'MEM20250001', 'Doe John']
        
        for terme in termes_recherche:
            print(f"\n🔎 Recherche: '{terme}'")
            response = client.get(f'/api/recherche-membres/?q={terme}')
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   Résultats: {len(data)}")
                    for result in data[:3]:  # Afficher les 3 premiers
                        print(f"     - {result.get('nom', '')} {result.get('prenom', '')}")
                except:
                    print(f"   ❌ Erreur parsing JSON")
            else:
                print(f"   ❌ Erreur HTTP: {response.status_code}")
    
    else:
        print("❌ Échec authentification")

if __name__ == "__main__":
    test_recherche_apres_correction()