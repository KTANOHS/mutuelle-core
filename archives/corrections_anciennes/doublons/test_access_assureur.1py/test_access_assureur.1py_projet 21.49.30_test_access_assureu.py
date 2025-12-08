# test_access_assureur.py
import requests

# Test d'accès aux pages assureur sans authentification
print("🌐 Test d'accès aux pages assureur")
print("="*50)

endpoints = [
    "/assureur/dashboard/",
    "/assureur/liste_membres/",
    "/assureur/liste_bons/",
    "/assureur/statistiques/",
    "/assureur/communication/",
]

for endpoint in endpoints:
    url = f"http://localhost:8000{endpoint}"
    print(f"\nTesting: {endpoint}")
    try:
        response = requests.get(url, allow_redirects=False)
        print(f"  Status: {response.status_code}")
        if response.status_code == 302:
            print(f"  🔒 Redirection vers: {response.headers.get('Location')}")
        elif response.status_code == 200:
            print(f"  ✅ Accessible")
        else:
            print(f"  ❓ Code: {response.status_code}")
    except Exception as e:
        print(f"  💥 Error: {e}")