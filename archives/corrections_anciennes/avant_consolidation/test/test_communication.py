#!/usr/bin/env python3
"""
SCRIPT DE TEST - Communication Assureur
Teste les URLs et templates de communication
"""

import requests
import sys

BASE_URL = "http://localhost:8000"

def test_url(url, expected_status=200):
    """Teste une URL"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == expected_status:
            print(f"✅ {url} - {response.status_code}")
            return True
        else:
            print(f"❌ {url} - {response.status_code} (attendu: {expected_status})")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {url} - Serveur non disponible")
        return False
    except Exception as e:
        print(f"❌ {url} - Erreur: {e}")
        return False

print("🔧 TEST DES URLS DE COMMUNICATION")
print("="*60)

# URLs à tester
urls_to_test = [
    f"{BASE_URL}/assureur/communication/",
    f"{BASE_URL}/assureur/communication/envoyer/",
    f"{BASE_URL}/communication/messagerie/",
    f"{BASE_URL}/communication/notifications/",
    f"{BASE_URL}/assureur/",
    f"{BASE_URL}/assureur/membres/",
]

success_count = 0
for url in urls_to_test:
    if test_url(url):
        success_count += 1

print("
" + "="*60)
print(f"📊 RÉSULTATS: {success_count}/{len(urls_to_test)} URLs fonctionnent")

if success_count == len(urls_to_test):
    print("🎉 Toutes les URLs fonctionnent parfaitement !")
else:
    print("⚠️  Certaines URLs ont des problèmes")
    print("
🔧 CONSEILS:")
    print("1. Vérifiez que le serveur Django est démarré")
    print("2. Vérifiez les logs Django pour les erreurs")
    print("3. Assurez-vous d'être connecté (les URLs peuvent nécessiter une authentification)")
    print("4. Testez manuellement dans le navigateur")
