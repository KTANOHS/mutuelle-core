
#!/usr/bin/env python3
# test_api_auth.py - Test avec authentification
import requests
from requests.cookies import RequestsCookieJar
import json
import sys

def get_auth_session():
    """Créer une session authentifiée"""
    session = requests.Session()
    
    # URL de login
    login_url = "http://127.0.0.1:8000/accounts/login/"
    
    # D'abord, récupérer le token CSRF
    print("🔐 Récupération du token CSRF...")
    response = session.get(login_url)
    
    # Chercher le token CSRF dans la réponse HTML
    csrf_token = None
    if 'csrfmiddlewaretoken' in response.text:
        import re
        match = re.search(r"name='csrfmiddlewaretoken' value='([^']+)'", response.text)
        if match:
            csrf_token = match.group(1)
            print(f"✅ Token CSRF trouvé: {csrf_token[:20]}...")
    
    # Se connecter avec l'utilisateur GLORIA1
    login_data = {
        'username': 'GLORIA1',
        'password': '1234',  # Mot de passe par défaut
        'csrfmiddlewaretoken': csrf_token,
        'next': '/communication/'
    }
    
    print("🔐 Connexion en tant que GLORIA1...")
    response = session.post(login_url, data=login_data, headers={'Referer': login_url})
    
    if response.status_code == 200 and 'GLORIA1' in response.text:
        print("✅ Connecté avec succès!")
        return session
    else:
        print(f"❌ Échec de la connexion: {response.status_code}")
        print(f"   Redirection vers: {response.url}")
        return None

def test_api_with_auth():
    """Tester l'API avec authentification"""
    print("🔍 TEST API AVEC AUTHENTIFICATION")
    print("=" * 50)
    
    # Obtenir une session authentifiée
    session = get_auth_session()
    if not session:
        print("❌ Impossible d'obtenir une session authentifiée")
        return
    
    # Test 1: JSON
    print("\n📨 Test 1: Envoi JSON")
    url = "http://127.0.0.1:8000/communication/envoyer-message-api/"
    data_json = {
        "destinataire_id": 1,
        "contenu": "Test message via JSON API avec auth",
        "titre": "Test API Auth"
    }
    
    try:
        headers = {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        response = session.post(url, json=data_json, headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        print(f"   Texte réponse: {response.text[:500]}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   ✅ JSON valide: {json.dumps(result, indent=2)}")
            except json.JSONDecodeError:
                print("   ❌ Réponse non JSON")
        elif response.status_code == 302:
            print("   ⚠️  Redirection détectée (probablement vers login)")
            print(f"   Location: {response.headers.get('Location')}")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"   💥 Exception: {str(e)}")
    
    # Test 2: Form-Data
    print("\n📝 Test 2: Envoi Form-Data")
    data_form = {
        "destinataire": 1,
        "contenu": "Test message via Form-Data avec auth",
        "titre": "Test Form Auth"
    }
    
    try:
        response = session.post(url, data=data_form)
        print(f"   Status: {response.status_code}")
        print(f"   Texte réponse: {response.text[:500]}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   ✅ JSON valide: {json.dumps(result, indent=2)}")
            except json.JSONDecodeError:
                print("   ❌ Réponse non JSON")
        elif response.status_code == 302:
            print("   ⚠️  Redirection détectée")
            print(f"   Location: {response.headers.get('Location')}")
            
    except Exception as e:
        print(f"   💥 Exception: {str(e)}")

if __name__ == "__main__":
    test_api_with_auth()

# Exécuter le test avec authentification
