# test_endpoints.py
import requests

print("🔍 Test des endpoints de récupération")
print("="*50)

endpoints = [
    "/communication/api/conversations/",
    "/communication/api/simple/conversations/8/messages/",
    "/communication/api/public/conversations/8/messages/",
    "/communication/conversations/",
]

for endpoint in endpoints:
    url = f"http://localhost:8000{endpoint}"
    print(f"\nTesting: {endpoint}")
    try:
        response = requests.get(url)
        print(f"  Status: {response.status_code}")
        print(f"  Content-Type: {response.headers.get('Content-Type')}")
        print(f"  First 200 chars: {response.text[:200]}")
    except Exception as e:
        print(f"  Error: {e}")