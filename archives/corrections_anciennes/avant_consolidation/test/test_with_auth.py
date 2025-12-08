# test_with_auth.py
import requests
from requests.auth import HTTPBasicAuth

url = "http://localhost:8000/communication/api/simple/conversations/8/messages/"

# Essayer avec authentification basique
response = requests.get(url, auth=HTTPBasicAuth('Almoravide', 'ton_mot_de_passe'))
print(f"Status avec auth: {response.status_code}")
print(f"Response: {response.text[:500]}")