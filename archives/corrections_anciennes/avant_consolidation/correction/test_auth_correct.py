# test_auth_correct.py
import requests
from django.test import Client

# Utilise le client de test Django (sans serveur)
client = Client()

# Se connecter d'abord
login_success = client.login(username='Almoravide', password='TON_MOT_DE_PASSE')
print(f"Login réussi: {login_success}")

# Maintenant tester l'API simple
response = client.get('/communication/api/simple/conversations/8/messages/')
print(f"Status: {response.status_code}")
print(f"Content-Type: {response['Content-Type']}")
print(f"Contenu (premiers 500 chars): {response.content[:500]}")