# test_api_corrige.py
import requests
import json

BASE_URL = "http://localhost:8000"

def test_urls_communication():
    """Teste les différentes URLs de communication"""
    
    print("🔍 Test des URLs de communication")
    print("="*50)
    
    # Liste des URLs à tester
    urls = [
        ("/communication/messagerie/", "GET", "Messagerie standard"),
        ("/communication/messages/envoyer/", "POST", "Envoyer message (communication)"),
        ("/assureur/communication/", "GET", "Messagerie assureur"),
        ("/assureur/communication/envoyer/", "POST", "Envoyer message (assureur)"),
    ]
    
    for url_path, method, description in urls:
        print(f"\n{description}:")
        print(f"  URL: {url_path}")
        
        if method == "GET":
            response = requests.get(BASE_URL + url_path)
        else:  # POST
            response = requests.post(BASE_URL + url_path, data={})
        
        print(f"  Status: {response.status_code}")
        print(f"  Type: {response.headers.get('Content-Type', 'Non spécifié')}")
        
        if response.status_code == 200:
            if "text/html" in response.headers.get('Content-Type', ''):
                print(f"  ✅ Page HTML accessible")
                # Vérifier si c'est une page de login
                if "login" in response.text.lower() or "connexion" in response.text.lower():
                    print(f"  ⚠️  C'est une page de login/connexion")
            elif "application/json" in response.headers.get('Content-Type', ''):
                print(f"  ✅ API JSON accessible")
                try:
                    data = response.json()
                    print(f"  Réponse JSON: {json.dumps(data, indent=2)}")
                except:
                    print(f"  ❌ Réponse JSON invalide")
        elif response.status_code in [302, 301]:
            print(f"  🔄 Redirection vers: {response.headers.get('Location', 'Inconnu')}")
        elif response.status_code == 403:
            print(f"  🔒 Accès interdit (CSRF ou authentification)")
        elif response.status_code == 404:
            print(f"  ❌ URL non trouvée")

def test_api_messages():
    """Teste spécifiquement l'API d'envoi de messages"""
    print("\n" + "="*50)
    print("🔍 Test spécifique de l'API d'envoi de messages")
    print("="*50)
    
    # URL correcte d'après le diagnostic
    url = BASE_URL + "/communication/messages/envoyer/"
    
    # 1. Test GET (pour voir la réponse)
    print("\n1. Test GET:")
    response = requests.get(url)
    print(f"   Status: {response.status_code}")
    
    # 2. Test POST avec données minimales
    print("\n2. Test POST avec données minimales:")
    
    # Créer une session pour gérer les cookies
    session = requests.Session()
    
    # D'abord récupérer la page pour obtenir le CSRF token
    response = session.get(BASE_URL + "/communication/messagerie/")
    
    # Essayer d'extraire le CSRF token du HTML
    csrf_token = None
    if 'csrfmiddlewaretoken' in response.text:
        # Méthode simple pour extraire le token
        import re
        match = re.search(r"name=['\"]csrfmiddlewaretoken['\"] value=['\"]([^'\"]+)['\"]", response.text)
        if match:
            csrf_token = match.group(1)
    
    # Préparer les données
    data = {
        'destinataire_id': 1,  # ID d'un utilisateur existant
        'contenu': 'Test de l\'API depuis le script Python',
        'titre': 'Test API'
    }
    
    # Ajouter le CSRF token si trouvé
    if csrf_token:
        data['csrfmiddlewaretoken'] = csrf_token
        headers = {'X-CSRFToken': csrf_token}
    else:
        headers = {}
    
    print(f"   CSRF Token: {'Trouvé' if csrf_token else 'Non trouvé'}")
    
    # Envoyer la requête
    response = session.post(url, data=data, headers=headers)
    
    print(f"   Status: {response.status_code}")
    print(f"   Type: {response.headers.get('Content-Type', 'Non spécifié')}")
    
    if response.status_code == 200:
        print(f"   Réponse: {response.text[:200]}...")
    elif response.status_code == 302:
        print(f"   Redirection vers: {response.headers.get('Location', 'Inconnu')}")
        print(f"   Cela signifie probablement que l'utilisateur n'est pas authentifié")

if __name__ == "__main__":
    test_urls_communication()
    test_api_messages()