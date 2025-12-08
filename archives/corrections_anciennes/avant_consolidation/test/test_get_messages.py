# test_get_messages.py
import requests
import json

print("📱 Test de récupération des messages")
print("="*50)

# Récupérer les messages de la conversation 6
url_conversation = "http://localhost:8000/communication/api/simple/conversations/6/messages/"

try:
    response = requests.get(url_conversation)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        messages = response.json()
        print(f"✅ {len(messages)} messages dans la conversation 6")
        for msg in messages:
            print(f"   - ID: {msg.get('id')}, De: {msg.get('expediteur')}, Contenu: {msg.get('contenu')[:50]}...")
    else:
        print(f"❌ Erreur: {response.text}")
        
except Exception as e:
    print(f"💥 Exception: {e}")