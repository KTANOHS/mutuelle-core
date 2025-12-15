# test_auth.py
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    print("✅ Test de santé de l'API...")
    response = requests.get(f"{BASE_URL}/api/health/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def get_token(username, password):
    print(f"🔐 Obtention du token pour {username}...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/token/",
            json={"username": username, "password": password},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            token = response.json().get('token')
            print(f"✅ Token obtenu: {token[:20]}...")
            return token
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"Message: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_protected_endpoints(token):
    print("🔒 Test des endpoints protégés...")
    
    headers = {"Authorization": f"Token {token}"}
    endpoints = [
        "/api/soins/",
        "/api/membres/",
        "/api/medecins/",
        "/api/statistiques/",
        "/api/types-soins/",
    ]
    
    for endpoint in endpoints:
        print(f"\nTesting {endpoint}")
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict):
                    if 'count' in data:
                        print(f"  Count: {data['count']}")
                    elif 'results' in data:
                        print(f"  Items: {len(data['results'])}")
                elif isinstance(data, list):
                    print(f"  Items: {len(data)}")
            elif response.status_code == 403:
                print(f"  Message: Accès interdit - permissions insuffisantes")
            else:
                print(f"  Response: {response.text[:100]}...")
                
        except Exception as e:
            print(f"  Error: {e}")

def create_test_user():
    print("👤 Création d'un utilisateur de test...")
    
    # Créez d'abord un superutilisateur via la ligne de commande si nécessaire
    print("""
Pour créer un utilisateur, exécutez:
python manage.py createsuperuser --username test --email test@example.com
    """)

def main():
    print("🧪 Début des tests d'authentification API")
    print("=" * 60)
    
    # Test de santé
    test_health()
    
    # Demander les identifiants
    print("\nEntrez vos identifiants pour tester l'authentification:")
    username = input("Username (admin par défaut): ") or "admin"
    password = input("Password: ")
    
    if not password:
        print("\n⚠️  Mot de passe requis. Créez d'abord un utilisateur:")
        create_test_user()
        return
    
    # Obtenir le token
    token = get_token(username, password)
    
    if token:
        # Tester les endpoints protégés
        test_protected_endpoints(token)
    
    print("\n" + "=" * 60)
    print("✅ Tests terminés!")

if __name__ == "__main__":
    main()