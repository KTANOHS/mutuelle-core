# test_recherche_live.py
import requests

# Test avec session pour gérer l'authentification
session = requests.Session()

# URL de connexion (à adapter si nécessaire)
login_url = "http://127.0.0.1:8000/accounts/login/"
search_url = "http://127.0.0.1:8000/assureur/membres/?q=ASIA"

print("🔍 TEST DE RECHERCHE EN DIRECT")
print("="*50)

# Si vous avez besoin de vous connecter (remplacez par vos identifiants)
credentials = {
    'username': 'DOUA',  # ou l'utilisateur que vous voyez dans les logs
    'password': 'votre_mot_de_passe'  # à remplacer
}

try:
    print("1. Tentative de connexion...")
    # Récupérer le token CSRF
    login_page = session.get(login_url)
    
    # Si vous avez besoin d'authentification, décommentez :
    # from bs4 import BeautifulSoup
    # soup = BeautifulSoup(login_page.text, 'html.parser')
    # csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    # credentials['csrfmiddlewaretoken'] = csrf_token
    # response = session.post(login_url, data=credentials)
    # print(f"   Status login: {response.status_code}")
    
    print("\n2. Test de recherche 'ASIA'...")
    response = session.get(search_url)
    
    print(f"   Status: {response.status_code}")
    print(f"   Taille: {len(response.text)} caractères")
    
    if response.status_code == 200:
        # Analyse rapide du contenu
        content = response.text
        
        # Vérifications
        checks = [
            ('ASIA', 'Terme recherché'),
            ('DRAMANE', 'Membre 1'),
            ('Koné', 'Membre 2'), 
            ('numero_unique', 'Champ numéro'),
            ('date_inscription', 'Champ date'),
            ('2 résultat', 'Nombre de résultats'),
        ]
        
        print("\n3. Contenu trouvé :")
        for text, description in checks:
            if text.lower() in content.lower():
                print(f"   ✅ '{text}' : {description}")
            else:
                print(f"   ❌ '{text}' : NON TROUVÉ")
        
        # Chercher les lignes avec ASIA
        print("\n4. Lignes contenant 'ASIA' :")
        lines = content.split('\n')
        asia_lines = [line.strip() for line in lines if 'asia' in line.lower() and len(line.strip()) < 100]
        for line in asia_lines[:5]:
            print(f"   → {line[:80]}...")
            
    elif response.status_code == 302:
        print("   ❌ Redirection détectée (login requis)")
    else:
        print(f"   ❌ Erreur: {response.status_code}")
        
except Exception as e:
    print(f"❌ Erreur: {e}")

print("\n" + "="*50)
print("🎯 Pour tester dans le navigateur:")
print(f"   {search_url}")
print("="*50)