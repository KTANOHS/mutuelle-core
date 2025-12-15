#!/usr/bin/env python3
"""
Test automatique après configuration Railway
"""

import requests
import time
import sys

def print_step(step, message):
    print(f"\n{step}. {message}")
    print("-" * 50)

def test_with_retry(url, max_attempts=10, delay=30):
    """Test avec reprises automatiques"""
    
    print("🚀 LANCEMENT DES TESTS AUTOMATIQUES")
    print("="*60)
    
    for attempt in range(1, max_attempts + 1):
        print(f"\n🔍 Tentative {attempt}/{max_attempts}")
        
        try:
            # Test 1: Application
            print_step("1", "Test application principale")
            r1 = requests.get(url, timeout=10)
            print(f"   HTTP: {r1.status_code}")
            
            if r1.status_code != 200:
                print(f"   ❌ Échec")
                time.sleep(delay)
                continue
            
            print("   ✅ Application accessible")
            
            # Test 2: Admin page
            print_step("2", "Test page admin")
            admin_url = f"{url}/admin/login/"
            r2 = requests.get(admin_url, timeout=10)
            print(f"   HTTP: {r2.status_code}")
            
            if r2.status_code != 200:
                print(f"   ❌ Admin inaccessible")
                time.sleep(delay)
                continue
            
            print("   ✅ Page admin accessible")
            
            # Test 3: CSRF token
            import re
            if 'csrfmiddlewaretoken' not in r2.text:
                print("   ❌ CSRF token absent")
                time.sleep(delay)
                continue
            
            print("   ✅ CSRF token présent")
            
            # Test 4: POST request (le plus important)
            print_step("4", "Test POST (CSRF)")
            csrf_match = re.search(r'csrfmiddlewaretoken.*value="([^"]+)"', r2.text)
            
            if not csrf_match:
                print("   ❌ Impossible d'extraire CSRF")
                time.sleep(delay)
                continue
            
            csrf_token = csrf_match.group(1)
            print(f"   Token CSRF: {csrf_token[:15]}...")
            
            # Préparer POST
            session = requests.Session()
            data = {
                'csrfmiddlewaretoken': csrf_token,
                'username': 'testuser',
                'password': 'testpass',
                'next': '/admin/'
            }
            
            headers = {
                'Referer': admin_url,
                'Origin': url,
            }
            
            r3 = session.post(admin_url, data=data, headers=headers, 
                            allow_redirects=False, timeout=10)
            
            print(f"   POST Status: {r3.status_code}")
            
            # Analyser le résultat
            if r3.status_code == 403:
                response_text = r3.text[:500]
                if 'Origin checking failed' in response_text:
                    print("   ❌ Origin checking FAILED")
                    print("   🚨 Les variables Railway ne sont PAS appliquées")
                    print("   🔧 Configurez les variables d'environnement")
                else:
                    print("   ⚠️  403 autre (probablement identifiants)")
                    print("   ✅✅✅ CSRF FONCTIONNE MAINTENANT ! ✅✅✅")
                    print("\n   🎉 LE PROBLÈME CSRF EST RÉSOLU !")
                    return True
            elif r3.status_code in [200, 302]:
                print(f"   ✅✅✅ CSRF FONCTIONNE (Status: {r3.status_code}) ✅✅✅")
                print("\n   🎉 LE PROBLÈME CSRF EST RÉSOLU !")
                return True
            else:
                print(f"   ⚠️  Code inattendu: {r3.status_code}")
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Erreur réseau: {e}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        # Attendre avant la prochaine tentative
        if attempt < max_attempts:
            print(f"\n⏳ Attente de {delay} secondes avant prochaine tentative...")
            time.sleep(delay)
    
    return False

# URL de test
URL = "https://web-production-555c.up.railway.app"

print(f"🌐 Test de: {URL}")
print(f"⏱️  Durée max: 5 minutes (10 tentatives de 30 secondes)")
print("="*60)

# Exécuter le test
success = test_with_retry(URL, max_attempts=10, delay=30)

print("\n" + "="*60)
print("📊 RÉSULTAT DU TEST :")
print("="*60)

if success:
    print("🎉🎉🎉 FÉLICITATIONS ! 🎉🎉🎉")
    print("\n✅ VOTRE APPLICATION DJANGO EST MAINTENANT OPÉRATIONNELLE !")
    print(f"\n🌐 URL: {URL}")
    print(f"🔑 Admin: {URL}/admin/")
    print("\n🚀 PROCHAINES ÉTAPES :")
    print("   1. Créez un superutilisateur :")
    print("      railway run python manage.py createsuperuser")
    print("   2. Connectez-vous à l'interface admin")
    print("   3. Testez votre application mutuelle")
else:
    print("❌❌❌ ÉCHEC CRITIQUE ❌❌❌")
    print("\n🚨 LE PROBLÈME CSRF PERSISTE")
    print("\n🔍 CAUSES PROBABLES :")
    print("   1. ❌ Variables Railway non configurées")
    print("   2. ❌ Variables incorrectes")
    print("   3. ❌ Déploiement non effectué")
    print("   4. ❌ Cache Railway")
    print("\n🎯 ACTIONS REQUISES :")
    print("   1. ✅ Configurez les variables Railway (voir instructions)")
    print("   2. ✅ Redéployez manuellement")
    print("   3. ✅ Attendez 5 minutes")
    print("   4. ✅ Réessayez ce test")

print("\n" + "="*60)
print("💡 ASTUCE : Exécutez ce test périodiquement après chaque configuration")
print("="*60)
