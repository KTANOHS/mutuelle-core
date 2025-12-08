# test_final_corrige.py
import requests
import json

print("🎯 Test du système complet avec API publique")
print("="*50)

# 1. Envoi de message (API simple sans auth)
url_send = "http://localhost:8000/communication/api/simple/messages/send/"
data = {
    "expediteur_id": 1,
    "destinataire_id": 2,
    "contenu": "Test final du système"
}

response = requests.post(url_send, headers={"Content-Type": "application/json"}, 
                         data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    conv_id = result['conversation_id']
    print(f"✅ Message envoyé (Conv ID: {conv_id})")
    
    # 2. Récupération avec API publique
    url_public = f"http://localhost:8000/communication/api/public/conversations/{conv_id}/messages/"
    response2 = requests.get(url_public)
    
    if response2.status_code == 200:
        messages = response2.json()
        print(f"✅ {messages['total_messages']} message(s) récupéré(s)")
        for msg in messages['messages']:
            print(f"   📨 {msg['expediteur']['username']} → {msg['destinataire']['username']}:")
            print(f"      '{msg['contenu']}'")
            print(f"      À: {msg['date_envoi']}")
    else:
        print(f"❌ Erreur récupération: {response2.status_code}")
else:
    print(f"❌ Erreur envoi: {response.text}")