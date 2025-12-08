#!/usr/bin/env python
"""
Script de test API amélioré avec gestion automatique du serveur
"""

import subprocess
import time
import sys
import requests
import json
from threading import Thread
import signal
import atexit

# Variables globales
SERVER_URL = "http://127.0.0.1:8000"
SERVER_PROCESS = None

def start_server():
    """Démarre le serveur Django en arrière-plan"""
    global SERVER_PROCESS
    
    print("🚀 Démarrage du serveur Django...")
    
    try:
        # Vérifie si le serveur est déjà en cours d'exécution
        response = requests.get(f"{SERVER_URL}/", timeout=2)
        if response.status_code < 500:
            print("✅ Serveur déjà en cours d'exécution")
            return True
    except:
        pass  # Le serveur n'est pas démarré, continuons
    
    # Démarre le serveur
    SERVER_PROCESS = subprocess.Popen(
        [sys.executable, "manage.py", "runserver", "--noreload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Attends que le serveur soit prêt
    print("⏳ Attente du démarrage du serveur...")
    for i in range(30):  # 30 secondes maximum
        try:
            response = requests.get(f"{SERVER_URL}/", timeout=2)
            if response.status_code < 500:
                print("✅ Serveur démarré avec succès!")
                return True
        except:
            pass
        
        time.sleep(1)
        print(f".", end="", flush=True)
    
    print("\n❌ Le serveur n'a pas démarré dans le temps imparti")
    return False

def stop_server():
    """Arrête le serveur Django"""
    global SERVER_PROCESS
    
    if SERVER_PROCESS:
        print("\n🛑 Arrêt du serveur...")
        SERVER_PROCESS.terminate()
        SERVER_PROCESS.wait()
        print("✅ Serveur arrêté")

def test_connection():
    """Teste la connexion au serveur"""
    print("\n🔗 Test de connexion au serveur...")
    
    try:
        response = requests.get(f"{SERVER_URL}/", timeout=5)
        print(f"✅ Connexion réussie (HTTP {response.status_code})")
        return True
    except Exception as e:
        print(f"❌ Échec de connexion: {str(e)}")
        return False

def test_login(username, password):
    """Teste la connexion utilisateur"""
    print(f"\n🔐 Test de connexion pour {username}...")
    
    # Crée une session
    session = requests.Session()
    
    # Récupère le token CSRF
    try:
        response = session.get(f"{SERVER_URL}/accounts/login/")
        
        # Extrait le token CSRF (méthode simplifiée)
        csrf_token = None
        if 'csrfmiddlewaretoken' in response.text:
            import re
            match = re.search(r"name=['\"]csrfmiddlewaretoken['\"] value=['\"]([^'\"]+)['\"]", response.text)
            if match:
                csrf_token = match.group(1)
        
        if not csrf_token:
            print("⚠ Token CSRF non trouvé dans la page de login")
            # Essaye sans token
            csrf_token = ""
    except Exception as e:
        print(f"❌ Erreur récupération CSRF: {str(e)}")
        return None
    
    # Tente la connexion
    login_data = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }
    
    headers = {
        'Referer': f'{SERVER_URL}/accounts/login/'
    }
    
    try:
        response = session.post(
            f"{SERVER_URL}/accounts/login/",
            data=login_data,
            headers=headers,
            allow_redirects=False
        )
        
        if response.status_code == 302:
            print("✅ Connexion réussie!")
            
            # Vérifie la redirection
            if 'Location' in response.headers:
                redirect_url = response.headers['Location']
                print(f"📤 Redirection vers: {redirect_url}")
                
                # Suit la redirection
                response = session.get(f"{SERVER_URL}{redirect_url}" if redirect_url.startswith('/') else redirect_url)
                print(f"📄 Page de redirection chargée (HTTP {response.status_code})")
            
            return session
        else:
            print(f"❌ Échec connexion (HTTP {response.status_code})")
            
            # Affiche plus de détails si disponible
            if response.text:
                error_msg = response.text[:200]
                print(f"Message d'erreur: {error_msg}...")
            
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors de la connexion: {str(e)}")
        return None

def test_message_api(session, destinataire_id, message):
    """Teste l'API d'envoi de message"""
    print(f"\n📨 Test API message vers destinataire {destinataire_id}...")
    
    # Test avec JSON
    json_data = {
        'destinataire': destinataire_id,
        'contenu': message
    }
    
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    }
    
    try:
        response = session.post(
            f"{SERVER_URL}/communication/envoyer-message-api/",
            json=json_data,
            headers=headers
        )
        
        print(f"📊 Réponse API:")
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type')}")
        
        if response.text:
            try:
                json_response = response.json()
                print(f"   JSON: {json.dumps(json_response, indent=2)}")
            except:
                print(f"   Texte: {response.text[:500]}")
        
        if response.status_code == 200:
            print("✅ Message envoyé avec succès!")
            return True
        else:
            print("⚠ Réponse non-200 de l'API")
            return False
            
    except Exception as e:
        print(f"❌ Erreur API: {str(e)}")
        return False

def test_alternative_login():
    """Teste une connexion alternative avec différents utilisateurs"""
    print("\n🔍 Test de connexion avec différents utilisateurs...")
    
    # Liste d'utilisateurs à tester (selon votre base de données)
    test_users = [
        {"username": "GLORIA1", "password": "GLORIA1"},
        {"username": "Almoravide", "password": "Almoravide1084"},
        {"username": "admin", "password": "admin123"},
    ]
    
    for user in test_users:
        print(f"\n➡ Test avec {user['username']}...")
        session = test_login(user['username'], user['password'])
        
        if session:
            # Teste l'accès au tableau de bord
            try:
                response = session.get(f"{SERVER_URL}/")
                print(f"✅ Accès à l'accueil (HTTP {response.status_code})")
                
                # Teste une page spécifique
                response = session.get(f"{SERVER_URL}/communication/messagerie/")
                print(f"✅ Accès à la messagerie (HTTP {response.status_code})")
                
                return session, user['username']
            except Exception as e:
                print(f"❌ Erreur d'accès: {str(e)}")
    
    return None, None

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🧪 TESTS AVANCÉS DE L'API MUTUELLE")
    print("=" * 60)
    
    # S'assure que le serveur est arrêté à la fin
    atexit.register(stop_server)
    
    # Démarre le serveur
    if not start_server():
        print("❌ Impossible de démarrer le serveur")
        return
    
    # Teste la connexion
    if not test_connection():
        print("❌ Impossible de se connecter au serveur")
        return
    
    # Teste la connexion avec différents utilisateurs
    session, username = test_alternative_login()
    
    if not session:
        print("\n❌ Aucun utilisateur n'a pu se connecter")
        print("\n💡 SOLUTIONS:")
        print("1. Vérifiez les identifiants dans la base de données:")
        print("   python manage.py shell -c \"from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.all().values('username'))\"")
        print("\n2. Créez un nouvel utilisateur:")
        print("   python manage.py createsuperuser")
        return
    
    # Teste l'API d'envoi de message
    print(f"\n🎯 Utilisateur connecté: {username}")
    
    # Demande le destinataire
    destinataire_input = input("\n📋 ID du destinataire (appuyez sur Entrée pour utiliser ID 1): ").strip()
    if not destinataire_input:
        destinataire_id = 1
    elif destinataire_input.isdigit():
        destinataire_id = int(destinataire_input)
    else:
        print("⚠ ID invalide, utilisation de l'ID 1 par défaut")
        destinataire_id = 1
    
    message = input("💬 Message à envoyer (défaut: 'Test API'): ").strip()
    if not message:
        message = "Test API depuis le script amélioré"
    
    # Teste l'envoi
    test_message_api(session, destinataire_id, message)
    
    # Teste d'autres endpoints
    print("\n🔍 Tests des autres endpoints...")
    
    endpoints_to_test = [
        "/communication/notifications/count/",
        "/communication/messagerie/",
        "/communication/messages/",
        "/pharmacien/dashboard/",
    ]
    
    for endpoint in endpoints_to_test:
        try:
            response = session.get(f"{SERVER_URL}{endpoint}")
            print(f"✅ {endpoint}: HTTP {response.status_code} ({len(response.text)} caractères)")
        except Exception as e:
            print(f"❌ {endpoint}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ TESTS TERMINÉS")
    print("=" * 60)
    
    # Demande si on veut arrêter le serveur
    stop = input("\n🛑 Arrêter le serveur ? (o/N): ").lower()
    if stop == 'o':
        stop_server()

if __name__ == "__main__":
    main()