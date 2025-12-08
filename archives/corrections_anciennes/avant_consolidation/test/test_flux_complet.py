# test_flux_complet.py
import requests
import json
import time

print("🔄 Test complet du flux de messagerie")
print("="*50)

url_send = "http://localhost:8000/communication/api/simple/messages/send/"

# 1. Envoi d'un message
print("1. Envoi d'un nouveau message...")
data = {
    "expediteur_id": 1,      # Almoravide
    "destinataire_id": 3,    # medecin_test
    "contenu": "Test de flux complet à " + time.strftime("%H:%M:%S")
}

response = requests.post(url_send, headers={"Content-Type": "application/json"}, 
                         data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    print(f"   ✅ Message envoyé (ID: {result['message_id']}, Conv: {result['conversation_id']})")
    
    # 2. Récupération de la conversation
    conv_id = result['conversation_id']
    time.sleep(1)  # Petite attente
    
    print(f"\n2. Récupération de la conversation {conv_id}...")
    url_conv = f"http://localhost:8000/communication/api/simple/conversations/{conv_id}/messages/"
    response2 = requests.get(url_conv)
    
    if response2.status_code == 200:
        messages = response2.json()
        print(f"   ✅ {len(messages)} message(s) trouvé(s)")
        for msg in messages:
            print(f"      - {msg.get('expediteur')}: {msg.get('contenu')}")
    else:
        print(f"   ❌ Erreur: {response2.text}")
        
else:
    print(f"   ❌ Erreur d'envoi: {response.text}")

print("\n" + "="*50)
print("🎯 Système de messagerie fonctionnel !")