# test_login_assureur.py
import requests
from bs4 import BeautifulSoup

print("🔐 Test de connexion pour l'assureur")
print("="*50)

# 1. Obtenir la page de login et le token CSRF
login_url = "http://localhost:8000/accounts/login/"
session = requests.Session()

try:
    # GET pour obtenir le token CSRF
    response = session.get(login_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        
        if csrf_token:
            token = csrf_token.get('value')
            print(f"✅ Token CSRF trouvé")
            
            # 2. Tentative de login
            login_data = {
                'username': 'assureur_system',
                'password': 'assureur123',  # Mot de passe défini dans le script
                'csrfmiddlewaretoken': token
            }
            
            login_response = session.post(login_url, data=login_data)
            
            if login_response.status_code == 200:
                if "Bienvenue" in login_response.text or "Dashboard" in login_response.text:
                    print(f"✅ Connexion réussie !")
                    
                    # 3. Test d'accès au dashboard assureur
                    dashboard_url = "http://localhost:8000/assureur/"
                    dashboard_response = session.get(dashboard_url)
                    
                    print(f"\n📊 Test du dashboard assureur:")
                    print(f"  URL: {dashboard_url}")
                    print(f"  Status: {dashboard_response.status_code}")
                    
                    if dashboard_response.status_code == 200:
                        print(f"  ✅ Dashboard accessible !")
                        print(f"  Titre trouvé: {'Dashboard' in dashboard_response.text}")
                    elif dashboard_response.status_code == 302:
                        print(f"  🔄 Redirection détectée")
                        print(f"  Location: {dashboard_response.headers.get('Location')}")
                    else:
                        print(f"  ❌ Échec: {dashboard_response.status_code}")
                else:
                    print(f"❌ Échec de connexion (mauvais identifiants)")
            else:
                print(f"❌ Échec de requête login: {login_response.status_code}")
        else:
            print(f"❌ Token CSRF non trouvé dans la page")
    else:
        print(f"❌ Impossible d'accéder à la page login: {response.status_code}")
        
except Exception as e:
    print(f"💥 Exception: {e}")