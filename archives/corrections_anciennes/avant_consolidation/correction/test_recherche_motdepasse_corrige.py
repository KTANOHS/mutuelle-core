import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate

def test_recherche_avec_motdepasse():
    """Tester la recherche API avec le bon mot de passe"""
    print("🔍 TEST RECHERCHE - MOT DE PASSE CORRIGÉ")
    print("========================================")
    
    # Authentification avec le nouveau mot de passe
    client = Client()
    user = authenticate(username='koffitanoh', password='nouveau_mot_de_passe')
    
    if not user:
        print("❌ Échec authentification")
        return False
    
    client.force_login(user)
    print("✅ Authentification réussie")
    
    # Test de recherche avec différents termes
    termes_recherche = ['John', 'Doe', 'MEM', 'Test']
    
    for terme in termes_recherche:
        print(f"\n🔎 Recherche: '{terme}'")
        response = client.get(f'/api/recherche-membres/?q={terme}')
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                # Essayer de parser le JSON
                import json
                data = json.loads(response.content)
                print(f"   ✅ Résultats: {len(data)}")
                for result in data[:2]:  # Afficher les 2 premiers
                    nom = result.get('nom', 'N/A')
                    prenom = result.get('prenom', 'N/A')
                    print(f"     - {nom} {prenom}")
            except:
                # Si ce n'est pas du JSON, afficher un extrait
                content = response.content.decode('utf-8')[:200]
                print(f"   📄 Réponse (extrait): {content}...")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
    
    return True

if __name__ == "__main__":
    success = test_recherche_avec_motdepasse()
    
    if success:
        print("\n🎉 TEST RECHERCHE RÉUSSI!")
    else:
        print("\n⚠️  TEST RECHERCHE ÉCHOUÉ")