
#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

# Configuration
BASE_URL = "https://web-production-555c.up.railway.app"
LOGIN_URL = f"{BASE_URL}/admin/login/"

# Créer une session persistante
session = requests.Session()

# 1. Obtenir la page de login AVEC cookie de session
print("1. Obtention de la page de login...")
response = session.get(LOGIN_URL)
print(f"   Status: {response.status_code}")

# Vérifier les cookies
print(f"   Cookies de session: {len(session.cookies)} cookie(s)")
for cookie in session.cookies:
    print(f"   - {cookie.name}: {cookie.value[:20]}...")

# 2. Extraire le token CSRF
soup = BeautifulSoup(response.text, 'html.parser')
csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})

if csrf_input:
    csrf_token = csrf_input['value']
    print(f"2. Token CSRF trouvé: {csrf_token[:20]}...")
else:
    print("2. ❌ Aucun token CSRF trouvé")
    print("   HTML snippet:")
    print(response.text[:500])
    exit(1)

# 3. Demander les identifiants
print("\n3. Entrez vos identifiants:")
username = input("   Username: ")
password = input("   Password: ")

# 4. Préparer les données
data = {
    'csrfmiddlewaretoken': csrf_token,
    'username': username,
    'password': password,
    'next': '/admin/'
}

headers = {
    'Referer': LOGIN_URL,
    'Origin': BASE_URL,
}

# 5. Envoyer la requête POST
print("\n4. Connexion en cours...")
login_response = session.post(LOGIN_URL, data=data, headers=headers, allow_redirects=False)

print(f"   Status: {login_response.status_code}")
print(f"   Redirection: {login_response.headers.get('Location', 'Aucune')}")

# Vérifier les cookies après login
print(f"   Cookies après login: {len(session.cookies)} cookie(s)")

# 6. Vérifier la connexion
if login_response.status_code in [302, 303]:
    print("\n5. ✅ Redirection détectée - Suivre la redirection...")
    
    # Suivre la redirection automatiquement avec la session
    admin_response = session.get(f"{BASE_URL}/admin/")
    
    if "Site administration" in admin_response.text or "Django administration" in admin_response.text:
        print("   🎉 SUCCÈS ! Vous êtes connecté à l'admin Django")
        print(f"   Titre: {soup.find('title').text if soup.find('title') else 'Non trouvé'}")
    else:
        print("   ⚠️  Connecté mais page admin différente")
        
elif login_response.status_code == 200:
    print("\n5. ❌ Échec - Analyser la page d'erreur...")
    soup = BeautifulSoup(login_response.text, 'html.parser')
    error_messages = soup.find_all(class_='errornote')
    if error_messages:
        print(f"   Message d'erreur: {error_messages[0].text.strip()}")
    
elif login_response.status_code == 403:
    print("\n5. ❌ ERREUR 403 - Détails CSRF:")
    # Analyser la page d'erreur
    soup = BeautifulSoup(login_response.text, 'html.parser')
    reason = soup.find('pre')
    if reason:
        print(f"   Raison: {reason.text.strip()}")
    
    # Afficher plus de détails
    print("\n   🔍 Détails de débogage:")
    print(f"   - URL: {LOGIN_URL}")
    print(f"   - Cookies envoyés: {session.cookies.get_dict()}")
    print(f"   - Headers envoyés: {login_response.request.headers}")

print("\n✅ Test terminé")


