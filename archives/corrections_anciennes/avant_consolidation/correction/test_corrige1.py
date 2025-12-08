import requests
import json

# Test avec l'API simple
url = "http://localhost:8000/communication/api/simple/messages/send/"

# Utilisons des IDs valides de ta liste
# Almoravide (ID: 1) envoie un message à GLORIA (ID: 2)

print("🔍 Test API Simple - Envoi JSON complet")
headers = {"Content-Type": "application/json"}
data = {
    "expediteur_id": 1,      # Almoravide
    "destinataire_id": 2,    # GLORIA  
    "contenu": "Bonjour GLORIA, ceci est un test de l'API de messagerie"
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        json_response = response.json()
        print(f"   ✅ Succès: {json_response}")
    elif response.status_code == 400:
        json_response = response.json()
        print(f"   ❌ Erreur 400: {json_response}")
        print(f"   Détails de la requête envoyée:")
        print(f"   {data}")
    else:
        print(f"   ❌ Autre erreur HTTP: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"   💥 Exception: {e}")

print("\n" + "="*50 + "\n")

# Test 2: Entre médecins
print("🔍 Test 2: Message entre médecins")
data2 = {
    "expediteur_id": 2,      # GLORIA (médecin)
    "destinataire_id": 40,   # medecin_test_1
    "contenu": "Bonjour collègue, voici une ordonnance pour revoir"
}

try:
    response2 = requests.post(url, headers=headers, data=json.dumps(data2))
    print(f"   Status: {response2.status_code}")
    
    if response2.status_code == 200:
        json_response2 = response2.json()
        print(f"   ✅ Succès: {json_response2}")
    elif response2.status_code == 400:
        json_response2 = response2.json()
        print(f"   ❌ Erreur 400: {json_response2}")
    else:
        print(f"   Response: {response2.text}")
        
except Exception as e:
    print(f"   💥 Exception: {e}")