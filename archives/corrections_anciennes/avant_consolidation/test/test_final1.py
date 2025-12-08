# test_final.py
import requests
import json

# Crée une session
session = requests.Session()

# Simule une connexion Django
login_url = "http://localhost:8000/admin/login/"
response = session.get(login_url)
csrf_token = None

# Essaye de te connecter (remplace avec tes vraies infos)
login_data = {
    'username': 'Almoravide',
    'password': 'ton_mot_de_passe',
    'csrfmiddlewaretoken': csrf_token
}

# Teste l'API de conversations après login
api_url = "http://localhost:8000/communication/api/simple/conversations/8/messages/"
response = session.get(api_url)

print(f"Status: {response.status_code}")
if response.text:
    print(f"Response: {response.text[:1000]}")
else:
    print("Empty response")