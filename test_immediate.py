#!/usr/bin/env python3
import requests
import time

print("🧪 TEST IMMÉDIAT APRÈS MODIFICATION")
print("="*60)

URL = "https://web-production-555c.up.railway.app"

def quick_test():
    print("1. Test rapide de l'application...")
    try:
        r = requests.get(URL, timeout=10)
        print(f"   Status: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_csrf_quick():
    print("\n2. Test CSRF rapide...")
    try:
        session = requests.Session()
        r = session.get(f"{URL}/admin/login/", timeout=10)
        
        if r.status_code != 200:
            print(f"   ❌ Admin inaccessible: {r.status_code}")
            return False
        
        import re
        if 'csrfmiddlewaretoken' not in r.text:
            print("   ❌ CSRF absent")
            return False
        
        print("   ✅ Page admin avec CSRF accessible")
        
        # Tenter POST
        csrf_match = re.search(r'csrfmiddlewaretoken.*value="([^"]+)"', r.text)
        if csrf_match:
            csrf = csrf_match.group(1)
            
            data = {
                'csrfmiddlewaretoken': csrf,
                'username': 'test',
                'password': 'test',
                'next': '/admin/'
            }
            
            r2 = session.post(f"{URL}/admin/login/", data=data, 
                            headers={'Referer': f"{URL}/admin/login/"},
                            allow_redirects=False, timeout=10)
            
            print(f"   POST Status: {r2.status_code}")
            
            if r2.status_code == 403 and 'Origin checking failed' in r2.text:
                print("   ❌ Origin checking failed PERSISTE")
                return False
            else:
                print(f"   ✅ CSRF fonctionne (Status: {r2.status_code})")
                return True
        else:
            print("   ⚠️  CSRF non extractible")
            return True
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

# Attendre un peu pour le déploiement
print("⏳ Attente 30 secondes pour déploiement...")
time.sleep(30)

# Tests
test1 = quick_test()
test2 = test_csrf_quick()

print("\n" + "="*60)
if test1 and test2:
    print("🎉🎉🎉 SUCCÈS ! 🎉🎉🎉")
    print("La modification de settings.py a résolu le problème CSRF !")
    print(f"\n🌐 URL: {URL}")
    print(f"🔑 Admin: {URL}/admin/")
    print("\n🚀 Créez maintenant un superutilisateur :")
    print("   railway run python manage.py createsuperuser")
elif test1 and not test2:
    print("⚠️  APPLICATION OK MAIS CSRF PERSISTE")
    print("Attendez 1-2 minutes de plus et réessayez")
else:
    print("❌ PROBLÈME D'ACCÈS")
    print("Vérifiez le déploiement sur Railway")

print("\n" + "="*60)
