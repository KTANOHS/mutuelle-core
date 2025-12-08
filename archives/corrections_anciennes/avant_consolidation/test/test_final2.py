#!/usr/bin/env python
"""
SCRIPT DE TEST FINAL - API Messagerie
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_api_direct():
    """Test direct de l'API sans interface web"""
    print("🧪 TEST DIRECT DE L'API MESSAGERIE")
    print("=" * 50)
    
    # 1. Récupérer un token CSRF
    print("\n1. Récupération token CSRF...")
    session = requests.Session()
    
    try:
        response = session.get(f"{BASE_URL}/accounts/login/")
        csrf_token = None
        
        # Extrait le token CSRF
        import re
        csrf_match = re.search(r'csrfmiddlewaretoken[\'"] value=[\'"]([^\'"]+)', response.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)
            print(f"✅ Token CSRF trouvé: {csrf_token[:20]}...")
        else:
            print("⚠ Token CSRF non trouvé, tentative sans...")
        
        # 2. Connexion avec GLORIA1
        print("\n2. Connexion avec GLORIA1...")
        login_data = {
            'username': 'GLORIA1',
            'password': 'Pharmacien123',
        }
        
        if csrf_token:
            login_data['csrfmiddlewaretoken'] = csrf_token
        
        response = session.post(
            f"{BASE_URL}/accounts/login/",
            data=login_data,
            headers={'Referer': f'{BASE_URL}/accounts/login/'},
            allow_redirects=False
        )
        
        if response.status_code == 302:
            print("✅ Connexion réussie!")
            
            # Suivre la redirection
            redirect_url = response.headers.get('Location', '/')
            if redirect_url:
                session.get(f"{BASE_URL}{redirect_url}" if redirect_url.startswith('/') else redirect_url)
                print(f"✅ Redirection suivie: {redirect_url}")
        else:
            print(f"❌ Échec connexion (HTTP {response.status_code})")
            print(f"   Réponse: {response.text[:200]}...")
            return None
        
        # 3. Tester l'API d'envoi de message
        print("\n3. Test API envoi message...")
        
        # Cherche un destinataire différent (pas soi-même)
        # GLORIA1 a l'ID 28, utilisons ID 2 (GLORIA)
        destinataire_id = 2
        message = "Test API direct depuis le script"
        
        api_data = {
            'destinataire': destinataire_id,
            'contenu': message
        }
        
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json'
        }
        
        response = session.post(
            f"{BASE_URL}/communication/envoyer-message-api/",
            json=api_data,
            headers=headers
        )
        
        print(f"📊 Réponse API:")
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        try:
            result = response.json()
            print(f"   JSON: {json.dumps(result, indent=2, ensure_ascii=False)}")
        except:
            print(f"   Texte: {response.text[:500]}")
        
        # 4. Tester d'autres endpoints
        print("\n4. Test autres endpoints...")
        
        endpoints = [
            "/communication/notifications/count/",
            "/communication/messages/",
            "/pharmacien/dashboard/",
        ]
        
        for endpoint in endpoints:
            try:
                resp = session.get(f"{BASE_URL}{endpoint}")
                print(f"✅ {endpoint}: HTTP {resp.status_code}")
            except Exception as e:
                print(f"❌ {endpoint}: {str(e)}")
        
        return session
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_with_already_logged_in():
    """Test avec l'utilisateur déjà connecté (Almoravide)"""
    print("\n" + "=" * 50)
    print("🔗 TEST AVEC SESSION EXISTANTE")
    print("=" * 50)
    
    # Crée une session (simule un navigateur)
    session = requests.Session()
    
    # 1. Connexion avec Almoravide
    print("\n1. Connexion avec Almoravide...")
    
    # Récupère CSRF
    response = session.get(f"{BASE_URL}/accounts/login/")
    csrf_token = None
    
    import re
    csrf_match = re.search(r'csrfmiddlewaretoken[\'"] value=[\'"]([^\'"]+)', response.text)
    if csrf_match:
        csrf_token = csrf_match.group(1)
    
    login_data = {
        'username': 'Almoravide',
        'password': 'Almoravide1084',
    }
    
    if csrf_token:
        login_data['csrfmiddlewaretoken'] = csrf_token
    
    response = session.post(
        f"{BASE_URL}/accounts/login/",
        data=login_data,
        headers={'Referer': f'{BASE_URL}/accounts/login/'},
        allow_redirects=False
    )
    
    if response.status_code != 302:
        print(f"❌ Échec connexion Almoravide")
        return
    
    print("✅ Almoravide connecté")
    
    # 2. Test API message vers GLORIA1 (ID 28)
    print("\n2. Test envoi message à GLORIA1...")
    
    api_data = {
        'destinataire': 28,  # GLORIA1
        'contenu': 'Message test de Almoravide vers GLORIA1'
    }
    
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    }
    
    response = session.post(
        f"{BASE_URL}/communication/envoyer-message-api/",
        json=api_data,
        headers=headers
    )
    
    print(f"📊 Réponse: HTTP {response.status_code}")
    
    try:
        result = response.json()
        print(f"   Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get('success'):
            print("✅ Message envoyé avec succès!")
            print(f"   Message ID: {result.get('message_id')}")
        else:
            print(f"❌ Erreur: {result.get('error')}")
    except:
        print(f"   Texte brut: {response.text[:200]}")

def quick_test():
    """Test rapide de l'API"""
    print("\n" + "=" * 50)
    print("⚡ TEST RAPIDE API")
    print("=" * 50)
    
    # Test sans authentification (doit échouer)
    print("\n1. Test sans authentification...")
    response = requests.post(
        f"{BASE_URL}/communication/envoyer-message-api/",
        json={'destinataire': 1, 'contenu': 'Test sans auth'},
        headers={'Content-Type': 'application/json'}
    )
    print(f"   Status: {response.status_code} (attendu: 302 ou 403)")
    
    # Test endpoints publics
    print("\n2. Test endpoints publics...")
    
    public_endpoints = [
        "/",
        "/accounts/login/",
    ]
    
    for endpoint in public_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            print(f"✅ {endpoint}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {str(e)}")

def main():
    """Fonction principale"""
    print("🚀 SCRIPT DE TEST COMPLET - API MUTUELLE")
    print("=" * 60)
    
    # Vérifie que le serveur est accessible
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"✅ Serveur accessible (HTTP {response.status_code})")
    except:
        print("❌ Serveur non accessible. Démarrez-le avec:")
        print("   python manage.py runserver")
        return
    
    # Menu de choix
    print("\n🔧 CHOIX DU TEST:")
    print("1. Test complet avec GLORIA1")
    print("2. Test avec Almoravide (déjà fonctionnel)")
    print("3. Test rapide API")
    print("4. Quitter")
    
    choix = input("\nVotre choix (1-4): ").strip()
    
    if choix == "1":
        test_api_direct()
    elif choix == "2":
        test_with_already_logged_in()
    elif choix == "3":
        quick_test()
    elif choix == "4":
        print("👋 Au revoir!")
        return
    else:
        print("❌ Choix invalide")
    
    print("\n" + "=" * 60)
    print("✅ TESTS TERMINÉS")
    print("=" * 60)

if __name__ == "__main__":
    main()