#!/usr/bin/env python
"""
Script de test pour l'API de messagerie
"""
import requests
import json
import sys

BASE_URL = 'http://127.0.0.1:8000'

def test_login(username, password):
    """Teste la connexion"""
    print(f"\n🔐 Test de connexion pour {username}...")
    
    # Récupère d'abord le token CSRF
    session = requests.Session()
    response = session.get(f'{BASE_URL}/accounts/login/')
    
    # Extrait le token CSRF (simplifié)
    csrf_token = None
    if 'csrfmiddlewaretoken' in response.text:
        # Recherche simplifiée du token
        import re
        match = re.search(r"name='csrfmiddlewaretoken' value='([^']+)'", response.text)
        if match:
            csrf_token = match.group(1)
    
    if not csrf_token:
        print("⚠ Impossible de récupérer le token CSRF")
        return None
    
    # Tente la connexion
    login_data = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }
    
    headers = {
        'Referer': f'{BASE_URL}/accounts/login/'
    }
    
    response = session.post(
        f'{BASE_URL}/accounts/login/',
        data=login_data,
        headers=headers,
        allow_redirects=False
    )
    
    if response.status_code == 302:
        print("✅ Connexion réussie")
        return session
    else:
        print(f"❌ Échec connexion: {response.status_code}")
        return None

def test_send_message(session, destinataire_id, message):
    """Teste l'envoi d'un message"""
    print(f"\n📨 Test envoi message à {destinataire_id}...")
    
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
            f'{BASE_URL}/communication/envoyer-message-api/',
            json=json_data,
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        if response.status_code == 200:
            print("✅ Message envoyé avec succès")
        else:
            print("❌ Échec envoi message")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

def main():
    """Fonction principale"""
    print("🧪 Script de test API")
    print("=" * 40)
    
    # Demande les identifiants
    username = input("Nom d'utilisateur: ").strip()
    password = input("Mot de passe: ").strip()
    
    # Teste la connexion
    session = test_login(username, password)
    
    if session:
        # Teste l'envoi de message
        destinataire = input("\nID du destinataire (appuyez sur Entrée pour sauter): ").strip()
        if destinataire and destinataire.isdigit():
            message = input("Message: ").strip()
            if message:
                test_send_message(session, int(destinataire), message)
            else:
                print("⚠ Message vide, test annulé")
        else:
            print("⚠ Test d'envoi annulé")
    
    print("\n✅ Tests terminés")

if __name__ == '__main__':
    main()
