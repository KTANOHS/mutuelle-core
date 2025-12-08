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

def test_champs_corriges():
    """Tester les nouveaux champs de l'API"""
    print("🧪 TEST CHAMPS API CORRIGÉS")
    print("===========================")
    
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
    
    # Tester l'API avec la nouvelle route
    response = client.get(f'/api/agents/bons/{bon.id}/details/')
    print(f"📡 Statut API: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = json.loads(response.content)
            print("✅ API fonctionnelle!")
            
            if data.get('success'):
                bon_data = data['bon']
                print(f"\n📋 CHAMPS PRINCIPAUX (pour le frontend):")
                print(f"   🔢 Code: {bon_data.get('code')}")
                print(f"   👤 Membre: {bon_data.get('membre')}")
                print(f"   💰 Montant max: {bon_data.get('montant_max')}")
                print(f"   📊 Statut: {bon_data.get('statut')}")
                print(f"   📅 Création: {bon_data.get('date_creation')}")
                print(f"   ⏰ Expiration: {bon_data.get('date_expiration')}")
                print(f"   ⏱️  Temps restant: {bon_data.get('temps_restant')}")
                print(f"   🩺 Motif: {bon_data.get('motif')}")
                print(f"   🏥 Type de soin: {bon_data.get('type_soin')}")
                print(f"   🚨 Urgence: {bon_data.get('urgence')}")
                
                print(f"\n📋 CHAMPS SUPPLÉMENTAIRES:")
                print(f"   👨‍⚕️ Médecin: {bon_data.get('medecin')}")
                print(f"   📝 Diagnostic: {bon_data.get('diagnostic')}")
                
                # Vérifier que tous les champs requis sont présents
                champs_requis = ['code', 'membre', 'montant_max', 'statut', 'date_creation', 'date_expiration', 'temps_restant', 'motif', 'type_soin', 'urgence']
                champs_manquants = [champ for champ in champs_requis if champ not in bon_data]
                
                if not champs_manquants:
                    print(f"\n✅ TOUS LES CHAMPS REQUIS SONT PRÉSENTS!")
                    return True
                else:
                    print(f"\n❌ CHAMPS MANQUANTS: {champs_manquants}")
                    return False
            else:
                print(f"❌ Erreur API: {data.get('error')}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur parsing JSON: {e}")
            return False
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return False

if __name__ == "__main__":
    success = test_champs_corriges()
    
    if success:
        print("\n🎉 API COMPLÈTEMENT CORRIGÉE!")
        print("🌐 L'historique des bons devrait maintenant afficher tous les détails correctement")
    else:
        print("\n⚠️  TEST ÉCHOUÉ - Vérifiez la correction")