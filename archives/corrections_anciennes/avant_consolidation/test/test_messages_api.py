#!/usr/bin/env python3
"""
Script de test pour l'API de messages
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_get_messages(conversation_id=5):
    """Teste la récupération des messages"""
    print(f"📨 Récupération des messages de la conversation {conversation_id}...")
    
    urls = [
        f"/communication/api/simple/conversations/{conversation_id}/messages/",
        f"/api/communication/conversations/{conversation_id}/messages/",
        f"/communication/conversations/{conversation_id}/messages/json/",
    ]
    
    for url_path in urls:
        url = BASE_URL + url_path
        print(f"
🔗 Test URL: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict) and 'messages' in data:
                        messages = data['messages']
                        print(f"   ✅ {len(messages)} messages trouvés")
                        
                        # Afficher les messages
                        for i, msg in enumerate(messages[:5]):  # Afficher les 5 premiers
                            print(f"   📝 Message {i+1}: {msg.get('titre', 'Sans titre')}")
                            print(f"      Contenu: {msg.get('contenu', '')[:50]}...")
                            print(f"      De: {msg.get('expediteur', {}).get('username', 'Inconnu')}")
                            print(f"      À: {msg.get('destinataire', {}).get('username', 'Inconnu')}")
                            print()
                    elif isinstance(data, list):
                        print(f"   ✅ {len(data)} messages trouvés (liste directe)")
                        
                        # Afficher les messages
                        for i, msg in enumerate(data[:3]):  # Afficher les 3 premiers
                            print(f"   📝 Message {i+1}: {msg.get('titre', 'Sans titre')}")
                            print(f"      Contenu: {msg.get('contenu', '')[:50]}...")
                    else:
                        print(f"   ℹ️  Format de réponse: {type(data)}")
                        print(f"   📊 Données: {json.dumps(data, indent=2)[:200]}...")
                        
                except json.JSONDecodeError:
                    print(f"   ❌ Réponse non-JSON: {response.text[:200]}")
            elif response.status_code == 404:
                print(f"   ❌ Endpoint non trouvé")
            elif response.status_code == 403:
                print(f"   🔒 Accès refusé (authentification requise)")
            else:
                print(f"   ❌ Erreur {response.status_code}: {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Impossible de se connecter au serveur")
        except Exception as e:
            print(f"   ⚠️  Erreur: {e}")

def test_send_message():
    """Teste l'envoi d'un message"""
    print("
📤 Test d'envoi de message...")
    
    # Données de test
    test_data = {
        "expediteur_id": 1,  # GLORIA1
        "destinataire_id": 2,  # Almoravide
        "titre": "Test depuis script API",
        "contenu": "Ceci est un message de test envoyé via l'API",
        "type_message": "TEST"
    }
    
    url = BASE_URL + "/communication/api/simple/messages/send/"
    
    print(f"🔗 URL: {url}")
    print(f"📝 Données: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            url,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"
📨 Réponse - Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Succès!")
            print(f"   📊 Résultat: {json.dumps(result, indent=2)}")
        else:
            print(f"   ❌ Erreur: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ⚠️  Exception: {e}")

def main():
    print("=" * 60)
    print("SCRIPT DE TEST API MESSAGES")
    print("=" * 60)
    
    # Test de récupération
    test_get_messages(5)
    
    # Test d'envoi (optionnel)
    print("
" + "=" * 60)
    choice = input("Voulez-vous tester l'envoi d'un message? (o/n): ")
    if choice.lower() == 'o':
        test_send_message()
    
    print("
" + "=" * 60)
    print("TEST TERMINÉ")
    print("=" * 60)

if __name__ == "__main__":
    main()
