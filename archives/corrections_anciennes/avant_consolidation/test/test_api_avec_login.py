# test_api_avec_login.py
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:8000"

def login_and_test():
    """Se connecte puis teste l'API"""
    
    session = requests.Session()
    
    # 1. Obtenir la page de login et le CSRF token
    print("1. Obtention du CSRF token...")
    login_url = BASE_URL + "/accounts/login/"
    response = session.get(login_url)
    
    # Parser le HTML pour trouver le CSRF token
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = None
    
    csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    if csrf_input:
        csrf_token = csrf_input.get('value')
    
    if not csrf_token:
        print("   ❌ CSRF token non trouvé")
        return
    
    print(f"   ✅ CSRF token trouvé: {csrf_token[:20]}...")
    
    # 2. Se connecter (remplacer avec vos identifiants)
    print("\n2. Connexion...")
    login_data = {
        'username': 'test_assureur',  # À remplacer
        'password': 'password123',    # À remplacer
        'csrfmiddlewaretoken': csrf_token
    }
    
    response = session.post(login_url, data=login_data)
    
    if response.status_code == 200 and "dashboard" in response.url:
        print("   ✅ Connexion réussie")
    else:
        print(f"   ❌ Échec de connexion: Status {response.status_code}")
        print(f"   URL après login: {response.url}")
        # Afficher la page pour voir l'erreur
        print(f"   Page: {response.text[:500]}")
        return
    
    # 3. Tester l'envoi de message
    print("\n3. Test d'envoi de message...")
    message_url = BASE_URL + "/communication/messages/envoyer/"
    
    message_data = {
        'destinataire_id': 2,  # ID d'un autre utilisateur
        'contenu': 'Message de test après login',
        'titre': 'Test API après login',
        'csrfmiddlewaretoken': csrf_token
    }
    
    response = session.post(message_url, data=message_data)
    
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        print(f"   ✅ Message envoyé avec succès")
        print(f"   Réponse: {response.text[:200]}")
    elif response.status_code == 302:
        print(f"   🔄 Redirection: {response.headers.get('Location')}")
    else:
        print(f"   ❌ Erreur: {response.status_code}")
        print(f"   Réponse: {response.text[:500]}")

if __name__ == "__main__":
    login_and_test()