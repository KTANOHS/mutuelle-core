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

def test_details_bons():
    """Tester l'API des détails des bons"""
    print("🧪 TEST API DÉTAILS BONS")
    print("========================")
    
    client = Client()
    user = authenticate(username='agent_operateur', password='agent123')
    
    if not user:
        print("❌ Authentification échouée")
        return False
    
    client.force_login(user)
    print("✅ Authentification réussie")
    
    # Récupérer un bon existant
    bon = BonDeSoin.objects.first()
    if not bon:
        print("❌ Aucun bon de soin trouvé")
        return False
    
    print(f"🔍 Test avec le bon ID: {bon.id}")
    
    # Tester l'API
    response = client.get(f'/agents/api/bons/{bon.id}/details/')
    print(f"📡 Statut API: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = json.loads(response.content)
            print("✅ API fonctionnelle!")
            print(f"📋 Données reçues:")
            if data.get('success'):
                bon_data = data['bon']
                print(f"   👤 Patient: {bon_data.get('patient')}")
                print(f"   📅 Date soin: {bon_data.get('date_soin')}")
                print(f"   🩺 Diagnostic: {bon_data.get('diagnostic')}")
                print(f"   💰 Montant: {bon_data.get('montant')}")
                print(f"   📊 Statut: {bon_data.get('statut')}")
            else:
                print(f"   ❌ Erreur: {data.get('error')}")
        except Exception as e:
            print(f"❌ Erreur parsing JSON: {e}")
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        print(f"   Contenu: {response.content.decode('utf-8')[:200]}...")
    
    return response.status_code == 200

if __name__ == "__main__":
    success = test_details_bons()
    
    if success:
        print("\n🎉 API DÉTAILS BONS VALIDÉE!")
        print("🌐 L'historique des bons devrait maintenant fonctionner")
    else:
        print("\n⚠️  TEST ÉCHOUÉ - Vérifiez la correction")