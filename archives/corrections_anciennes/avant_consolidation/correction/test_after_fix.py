# test_after_fix.py
import requests

print("🔍 Test après correction")
print("="*50)

# Test sans session
print("1. Test sans authentification :")
urls = ['/assureur/', '/assureur/dashboard/']
for url in urls:
    full_url = f'http://localhost:8000{url}'
    response = requests.get(full_url, allow_redirects=False)
    print(f"   {url}: {response.status_code} {'(redirige vers login)' if response.status_code == 302 else ''}")

print("\n2. Instructions pour tester :")
print("   a. Allez sur : http://localhost:8000/admin/")
print("   b. Connectez-vous avec DOUA")
print("   c. Allez sur : http://localhost:8000/assureur/")
print("   d. Si ça marche, le système assureur est opérationnel !")