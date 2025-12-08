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

def test_route_globale():
    """Tester la route globale de l'API"""
    print("🧪 TEST ROUTE GLOBALE API")
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
    
    # Tester l'ancienne route (devrait fonctionner)
    print("\n1. 🔗 TEST ANCIENNE ROUTE (/agents/api/...)")
    response_ancienne = client.get(f'/agents/api/bons/{bon.id}/details/')
    print(f"   📡 Statut: {response_ancienne.status_code}")
    
    # Tester la nouvelle route globale (celle que l'interface utilise)
    print("\n2. 🔗 TEST NOUVELLE ROUTE (/api/agents/...)")
    response_nouvelle = client.get(f'/api/agents/bons/{bon.id}/details/')
    print(f"   📡 Statut: {response_nouvelle.status_code}")
    
    if response_nouvelle.status_code == 200:
        try:
            data = json.loads(response_nouvelle.content)
            print("   ✅ NOUVELLE ROUTE FONCTIONNE!")
            if data.get('success'):
                bon_data = data['bon']
                print(f"   📋 Patient: {bon_data.get('patient')}")
                print(f"   🩺 Diagnostic: {bon_data.get('diagnostic')}")
        except Exception as e:
            print(f"   ❌ Erreur parsing: {e}")
    else:
        print(f"   ❌ Nouvelle route échoue: {response_nouvelle.status_code}")
    
    # Résumé
    print(f"\n3. 📊 RÉSUMÉ:")
    print(f"   ✅ Ancienne route: {response_ancienne.status_code}")
    print(f"   ✅ Nouvelle route: {response_nouvelle.status_code}")
    
    return response_nouvelle.status_code == 200

if __name__ == "__main__":
    success = test_route_globale()
    
    if success:
        print("\n🎉 ROUTE GLOBALE VALIDÉE!")
        print("🌐 L'historique des bons devrait maintenant fonctionner parfaitement")
    else:
        print("\n⚠️  LA NOUVELLE ROUTE NE FONCTIONNE PAS")
        print("💡 Vérifiez que la correction a été appliquée")