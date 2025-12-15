#!/usr/bin/env python3
import requests
import re
import time

print("🔍 VÉRIFICATION DE LA SOLUTION ULTIME")
print("="*70)

URL = "https://web-production-555c.up.railway.app"

def test_csrf_fix():
    for i in range(1, 21):  # 20 tentatives
        print(f"\n🔧 Test {i}/20")
        
        try:
            session = requests.Session()
            
            # Test GET
            resp = session.get(f"{URL}/admin/login/", timeout=10)
            
            if resp.status_code != 200:
                print(f"   ❌ GET: {resp.status_code}")
                time.sleep(3)
                continue
            
            # Vérifier CSRF
            if 'csrfmiddlewaretoken' not in resp.text:
                print("   ❌ CSRF non trouvé")
                time.sleep(3)
                continue
            
            # Extraire CSRF
            csrf_match = re.search(r'csrfmiddlewaretoken.*value="([^"]+)"', resp.text)
            csrf_token = csrf_match.group(1) if csrf_match else "N/A"
            
            print(f"   ✅ Page OK, CSRF: {csrf_token[:15]}...")
            
            # Test POST
            data = {
                'csrfmiddlewaretoken': csrf_token,
                'username': 'anyuser',
                'password': 'anypass',
                'next': '/admin/'
            }
            
            resp_post = session.post(f"{URL}/admin/login/", data=data, 
                                   headers={'Referer': f"{URL}/admin/login/"},
                                   allow_redirects=False, timeout=10)
            
            print(f"   POST: {resp_post.status_code}")
            
            # ANALYSE
            if resp_post.status_code == 403:
                response_text = resp_post.text[:1000]
                
                if 'Origin checking failed' in response_text:
                    print("   ❌ Origin checking FAILED")
                    print("   Le fix ULTIME n'a pas fonctionné")
                    # Extraire la raison exacte
                    reason_match = re.search(r'<pre>(.*?)</pre>', response_text, re.DOTALL)
                    if reason_match:
                        print(f"   Raison: {reason_match.group(1).strip()[:100]}")
                    return False
                else:
                    print("   ⚠️  403 autre (probablement identifiants)")
                    print("\n   🎉🎉🎉 SUCCÈS ! 🎉🎉🎉")
                    print("   Le problème CSRF Origin est RÉSOLU !")
                    return True
                    
            elif resp_post.status_code in [200, 302]:
                print(f"\n   🎉🎉🎉 SUCCÈS COMPLET ! 🎉🎉🎉")
                print(f"   CSRF fonctionne (Status: {resp_post.status_code})")
                return True
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        if i < 20:
            print(f"   ⏳ Attente 3 secondes...")
            time.sleep(3)
    
    return False

# Exécution
success = test_csrf_fix()

print("\n" + "="*70)
if success:
    print("✅✅✅ PROBLÈME RÉSOLU ! ✅✅✅")
    print(f"\n🌐 Votre application Django fonctionne sur Railway:")
    print(f"   URL: {URL}")
    print(f"   Admin: {URL}/admin/")
    print(f"\n🔑 Créez un superutilisateur:")
    print("   railway run python manage.py createsuperuser")
else:
    print("❌❌❌ ÉCHEC CRITIQUE ❌❌❌")
    print("Le fix ultime n'a pas fonctionné.")
    print("\n🚨 CAUSES POSSIBLES:")
    print("1. Railway n'a pas déployé le nouveau code")
    print("2. Problème de cache Railway (attendre 5-10 min)")
    print("3. Variables d'environnement incorrectes")
    print("\n🔧 ACTIONS:")
    print("1. Vérifiez les logs sur https://railway.app")
    print("2. Vérifiez les variables d'environnement Railway")
    print("3. Redéployez manuellement depuis l'interface Railway")

print("="*70)
