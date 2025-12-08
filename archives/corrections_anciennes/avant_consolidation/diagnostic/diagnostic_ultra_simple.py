# diagnostic_ultra_simple.py
import requests
import json

def main():
    print("🚀 DIAGNOSTIC ULTRA-SIMPLE - Conversation 5")
    print("="*60)
    
    url = "http://127.0.0.1:8000/communication/api/public/conversations/5/messages/"
    
    print(f"\n🔗 Test de l'API: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                total = data.get('total_messages', 0)
                print(f"✅ SUCCÈS: {total} messages récupérés")
                
                print(f"\n📊 MESSAGES TROUVÉS:")
                messages = data.get('messages', [])
                
                # Messages recherchés
                searched = [
                    "Test diagnostique",
                    "Test API diagnostique", 
                    "Test API",
                    "Shell Test",
                    "Test Diagnostic",
                    "CAPTURE",
                    "Message via API"
                ]
                
                found_count = 0
                for search in searched:
                    found = False
                    for msg in messages:
                        if search in msg.get('titre', '') or search in msg.get('contenu', ''):
                            found = True
                            break
                    
                    if found:
                        print(f"   ✅ {search}")
                        found_count += 1
                    else:
                        print(f"   ❌ {search}")
                
                print(f"\n🎯 RÉSULTAT: {found_count}/{len(searched)} messages trouvés")
                print(f"📋 TOTAL: {total} messages dans la conversation")
                
                # Sauvegarder
                with open('messages_conversation_5.json', 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"\n💾 Données sauvegardées: messages_conversation_5.json")
                
            else:
                print(f"❌ ERREUR API: {data.get('error')}")
        else:
            print(f"❌ CODE ERREUR: {response.status_code}")
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
    
    print("\n" + "="*60)
    print("COMMANDES DE TEST:")
    print("="*60)
    print("curl http://127.0.0.1:8000/communication/api/public/conversations/5/messages/")
    print("\nAfficher en JSON formaté:")
    print("curl -s http://127.0.0.1:8000/communication/api/public/conversations/5/messages/ | python -m json.tool")

if __name__ == "__main__":
    main()