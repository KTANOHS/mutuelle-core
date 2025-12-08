# test_with_session.py
from django.test import Client

client = Client()
client.login(username='Almoravide', password='ton_mot_de_passe')

response = client.get('/communication/api/simple/conversations/8/messages/')
print(f"Status: {response.status_code}")
print(f"Content: {response.content[:500]}")