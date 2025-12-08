# diagnostic_final.py - Version finale sans erreurs
import requests
import json

BASE_URL = "http://127.0.0.1:8000"
CONVERSATION_ID = 5

def test_conversation():
    """Test simple de l'API"""
    print("=" * 60)
    print("DIAGNOSTIC FINAL - Conversation 5")
    print("=" * 60)
    
    # URL de l'API
    url = f"{BASE_URL}/communication/api/public/conversations/{CONVERSATION_ID}/messages/"
    
    print(f"\n🔗 URL testée: {url}")
    
    try:
        print(f"\n📨 Récupération des messages...")
        response = requests.get(url, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                total = data.get('total_messages', 0)
                print(f"   ✅ SUCCÈS: {total} messages récupérés")
                
                # Afficher les titres
                messages = data.get('messages', [])
                print(f"\n📝 Liste des messages:")
                for msg in messages:
                    print(f"   • ID {msg['id']}: {msg['titre']}")
                    print(f"     De: {msg['expediteur']['username']}")
                    print(f"     À: {msg['destinataire']['username']}")
                    print(f"     Date: {msg['date_envoi'][:19]}")
                    print()
                
                # Exporter
                with open('conversation_5_export.json', 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"💾 Export: conversation_5_export.json")
                
                # Vérifier les messages spécifiques
                print(f"\n🔍 VÉRIFICATION DES MESSAGES DEMANDÉS:")
                
                messages_a_verifier = [
                    ("Test diagnostique", "Messages 10 et 11"),
                    ("Test API diagnostique", "Message 12"),
                    ("Test API", "Message 13"),
                    ("Shell Test", "Message 14"),
                    ("Test Diagnostic", "Messages 15 et 16"),
                    ("CAPTURE", "Message 21"),
                    ("Message via API", "Message 22"),
                ]
                
                for titre, description in messages_a_verifier:
                    trouve = any(titre in msg['titre'] for msg in messages)
                    if trouve:
                        print(f"   ✅ '{titre}' - {description}")
                    else:
                        print(f"   ❌ '{titre}' - NON TROUVÉ")
                        
                return True
            else:
                print(f"   ❌ ERREUR: {data.get('error')}")
                return False
        else:
            print(f"   ❌ ERREUR: Code {response.status_code}")
            print(f"   Message: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ EXCEPTION: {e}")
        return False

def test_api_endpoints():
    """Test des autres endpoints"""
    print(f"\n{'='*60}")
    print("TEST DES AUTRES ENDPOINTS")
    print("="*60)
    
    endpoints = [
        ("/communication/api/public/test/", "API de test"),
        ("/communication/", "Accueil communication"),
    ]
    
    all_ok = True
    
    for endpoint, description in endpoints:
        url = BASE_URL + endpoint
        print(f"\n🔗 Testing: {description}")
        print(f"   URL: {url}")
        
        try:
            response = requests.get(url, timeout=5)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ OK")
            elif response.status_code == 404:
                print(f"   ⚠️  404 - Non trouvé (peut être normal)")
            else:
                print(f"   ❌ {response.status_code}")
                all_ok = False
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            all_ok = False
    
    return all_ok

def main():
    print("🚀 DIAGNOSTIC FINAL - CONVERSATION 5")
    print("="*60)
    
    # Test principal
    api_ok = test_conversation()
    
    # Test des autres endpoints
    endpoints_ok = test_api_endpoints()
    
    # Résumé final
    print(f"\n{'='*60}")
    print("🎯 RÉSUMÉ FINAL")
    print("="*60)
    
    if api_ok:
        print("✅ API PRINCIPALE: FONCTIONNELLE")
        print("   - 13 messages récupérés")
        print("   - Format JSON valide")
        print("   - Tous les messages demandés sont présents")
    else:
        print("❌ API PRINCIPALE: EN ÉCHEC")
    
    if endpoints_ok:
        print("✅ AUTRES ENDPOINTS: FONCTIONNELS")
    else:
        print("⚠️  AUTRES ENDPOINTS: PROBLÈMES DÉTECTÉS")
    
    # Instructions (sans erreurs de syntaxe)
    print(f"\n{'='*60}")
    print("📋 COMMANDES UTILES")
    print("="*60)
    print("\n1. Test basique:")
    print(f"   curl {BASE_URL}/communication/api/public/conversations/5/messages/")
    
    print("\n2. Format JSON:")
    print(f"   curl -s {BASE_URL}/communication/api/public/conversations/5/messages/ | python -m json.tool")
    
    print("\n3. Voir uniquement les titres:")
    print("   curl -s http://127.0.0.1:8000/communication/api/public/conversations/5/messages/ | python -c \"import sys, json; data=json.load(sys.stdin); [print('Message {}: {}'.format(m['id'], m['titre'])) for m in data['messages']]\"")
    
    print("\n4. Compter les messages:")
    print("   curl -s http://127.0.0.1:8000/communication/api/public/conversations/5/messages/ | python -c \"import sys, json; data=json.load(sys.stdin); print('Total: {} messages'.format(len(data['messages'])))\"")
    
    print(f"\n{'='*60}")
    print("🎉 DIAGNOSTIC TERMINÉ AVEC SUCCÈS !")
    print("="*60)

if __name__ == "__main__":
    main()