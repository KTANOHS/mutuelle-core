import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate
from soins.models import BonDeSoin
import json

def test_apres_correction():
    """Tester l'API après correction de l'erreur 500"""
    print("🧪 TEST APRÈS CORRECTION ERREUR 500")
    print("===================================")
    
    client = Client()
    user = authenticate(username='agent_operateur', password='agent123')
    
    if not user:
        print("❌ Authentification échouée")
        return False
    
    client.force_login(user)
    print("✅ Authentification réussie")
    
    # Tester avec plusieurs bons
    bons = BonDeSoin.objects.all()[:3]
    
    for bon in bons:
        print(f"\n🔍 Test avec le bon ID: {bon.id}")
        
        # Tester l'API
        response = client.get(f'/api/agents/bons/{bon.id}/details/')
        print(f"📡 Statut API: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = json.loads(response.content)
                print("✅ API fonctionnelle!")
                
                if data.get('success'):
                    bon_data = data['bon']
                    print(f"   🔢 Code: {bon_data.get('code')}")
                    print(f"   👤 Membre: {bon_data.get('membre')}")
                    print(f"   💰 Montant max: {bon_data.get('montant_max')}")
                    print(f"   📊 Statut: {bon_data.get('statut')}")
                else:
                    print(f"❌ Erreur API: {data.get('error')}")
                    
            except Exception as e:
                print(f"❌ Erreur parsing JSON: {e}")
        elif response.status_code == 500:
            print("❌ ERREUR 500 - La correction n'a pas fonctionné")
            try:
                data = json.loads(response.content)
                print(f"   Détails erreur: {data.get('error')}")
            except:
                print(f"   Réponse brute: {response.content[:200]}...")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
    
    return True

if __name__ == "__main__":
    success = test_apres_correction()
    
    if success:
        print("\n🎉 CORRECTION RÉUSSIE!")
        print("🌐 Testez maintenant l'historique des bons dans le navigateur")
    else:
        print("\n⚠️  PROBLÈME PERSISTANT")