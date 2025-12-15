#!/usr/bin/env python
import requests
import sys

BASE_URL = "https://mutuelle-core-19.onrender.com"
ENDPOINTS = [
    "/",
    "/health/",
    "/api/health/",
    "/api/token/",
    "/admin/",
]

print("🔍 Diagnostic des endpoints sur Render")
print("=" * 60)

for endpoint in ENDPOINTS:
    url = BASE_URL + endpoint
    print(f"\nTesting: {endpoint}")
    
    try:
        if endpoint == "/api/token/":
            # POST request pour le token
            response = requests.post(
                url,
                json={"username": "admin", "password": "Admin123!"},
                timeout=10
            )
        else:
            # GET request pour les autres
            response = requests.get(url, timeout=10)
        
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 500:
            print("  ❌ ERREUR 500 DÉTECTÉE")
            # Essayez d'obtenir plus d'informations
            print(f"  Response headers: {dict(response.headers)}")
            if "text/html" in response.headers.get("Content-Type", ""):
                print("  HTML Error page returned")
            else:
                print(f"  Response body (first 500 chars):")
                print(f"  {response.text[:500]}")
        
        elif response.status_code == 200:
            print("  ✅ Succès")
            if endpoint == "/health/":
                print(f"  Content: {response.text[:100]}")
        
        elif response.status_code == 404:
            print("  ⚠️  Non trouvé (mais pas d'erreur serveur)")
        
        elif response.status_code == 401:
            print("  🔐 Non autorisé (authentification requise)")
        
    except requests.exceptions.Timeout:
        print("  ⏱️  Timeout")
    except requests.exceptions.ConnectionError:
        print("  🔌 Connection Error - Le service est-il en ligne?")
    except Exception as e:
        print(f"  ❌ Exception: {e}")

print("\n" + "=" * 60)
print("📋 Recommandations:")
print("1. Vérifiez les logs Render pour l'erreur exacte")
print("2. Vérifiez que les migrations sont appliquées")
print("3. Vérifiez que l'utilisateur 'admin' existe")
print("4. Testez avec la commande: curl -v https://mutuelle-core-19.onrender.com/health/")
