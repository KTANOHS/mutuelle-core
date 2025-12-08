# test_api_public.py
import requests

# Test de l'API publique
url = "http://localhost:8000/communication/api/public/conversations/8/messages/"
print(f"Testing public API: {url}")

try:
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Text: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")