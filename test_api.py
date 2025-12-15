import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing /api/health/")
    response = requests.get(f"{BASE_URL}/api/health/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_endpoints():
    """Test all API endpoints"""
    endpoints = [
        "/api/",
        "/api/soins/",
        "/api/membres/",
        "/api/medecins/",
        "/api/statistiques/",
    ]
    
    for endpoint in endpoints:
        print(f"🔍 Testing {endpoint}")
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"Items: {len(data)}")
                elif isinstance(data, dict):
                    print(f"Keys: {list(data.keys())}")
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 50)

def test_auth():
    """Test authentication"""
    print("🔐 Testing authentication")
    
    # Test token auth
    auth_data = {
        "username": "test",  # Changez avec vos identifiants
        "password": "votre_mot_de_passe"  # Changez avec votre mot de passe
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/token/",
            json=auth_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Token Auth Status: {response.status_code}")
        if response.status_code == 200:
            token = response.json().get('token')
            print(f"Token: {token[:20]}...")
            
            # Test avec le token
            headers = {"Authorization": f"Token {token}"}
            response = requests.get(
                f"{BASE_URL}/api/soins/",
                headers=headers
            )
            print(f"Soins avec token: {response.status_code}")
    except Exception as e:
        print(f"Auth error: {e}")
    print()

def test_jwt():
    """Test JWT authentication"""
    print("🔐 Testing JWT authentication")
    
    auth_data = {
        "username": "test",
        "password": "votre_mot_de_passe"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/token/",
            json=auth_data
        )
        print(f"JWT Status: {response.status_code}")
        if response.status_code == 200:
            tokens = response.json()
            print(f"Access token: {tokens.get('access')[:30]}...")
            print(f"Refresh token: {tokens.get('refresh')[:30]}...")
    except Exception as e:
        print(f"JWT error: {e}")

if __name__ == "__main__":
    print("🧪 Starting API tests...")
    print("=" * 60)
    
    test_health()
    test_endpoints()
    test_auth()
    test_jwt()
    
    print("✅ Tests completed!")