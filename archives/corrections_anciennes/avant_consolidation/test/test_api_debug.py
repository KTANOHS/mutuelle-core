# test_api_debug.py
import requests

def test_api_sans_auth():
    """Test sans authentification pour voir ce que l'API retourne"""
    url = "http://localhost:8000/api/messages/envoyer/"
    
    # Test GET pour voir la réponse
    print("🔍 Test GET (pour voir si l'API existe):")
    response = requests.get(url)
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type')}")
    print(f"   Premiers 200 caractères: {response.text[:200]}")
    
    # Test POST vide
    print("\n🔍 Test POST vide:")
    response = requests.post(url, data={})
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type')}")
    print(f"   Réponse complète:\n{response.text}")

if __name__ == "__main__":
    test_api_sans_auth()