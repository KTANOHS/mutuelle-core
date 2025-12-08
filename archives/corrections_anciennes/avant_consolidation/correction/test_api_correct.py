import requests
import json

# Test avec l'API simple
url = "http://localhost:8000/communication/api/simple/messages/send/"

# Test 1: JSON
print("🔍 Test API Simple - Envoi JSON")
headers = {"Content-Type": "application/json"}
data = {
    "destinataire_id": 1,
    "contenu": "Test message via API simple"
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"   Status: {response.status_code}")
    print(f"   Headers: {response.headers}")
    print(f"   Response text: {response.text}")
    
    if response.status_code == 200:
        try:
            json_response = response.json()
            print(f"   ✅ JSON Response: {json_response}")
        except json.JSONDecodeError as e:
            print(f"   ❌ Réponse n'est pas du JSON: {e}")
            print(f"   Raw response: {response.text[:200]}")
    else:
        print(f"   ❌ Erreur HTTP: {response.status_code}")
        
except Exception as e:
    print(f"   💥 Exception: {e}")

print("\n" + "="*50 + "\n")

# Test 2: Form-Data
print("🔍 Test API Simple - Envoi Form-Data")
data_form = {
    "destinataire_id": 1,
    "contenu": "Test message via Form-Data API simple"
}

try:
    response2 = requests.post(url, data=data_form)
    print(f"   Status: {response2.status_code}")
    print(f"   Response text: {response2.text}")
    
    if response2.status_code == 200:
        try:
            json_response2 = response2.json()
            print(f"   ✅ JSON Response: {json_response2}")
        except json.JSONDecodeError as e:
            print(f"   ❌ Réponse n'est pas du JSON: {e}")
            print(f"   Raw response: {response2.text[:200]}")
    else:
        print(f"   ❌ Erreur HTTP: {response2.status_code}")
        
except Exception as e:
    print(f"   💥 Exception: {e}")