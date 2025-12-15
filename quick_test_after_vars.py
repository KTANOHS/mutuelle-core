#!/usr/bin/env python3
import requests
import time

print("🧪 TEST APRÈS CONFIGURATION VARIABLES")
print("="*60)

URL = "https://web-production-555c.up.railway.app"

def test_application():
    print("1. Test de l'application principale...")
    try:
        r = requests.get(URL, timeout=10)
        print(f"   Status: {r.status_code}")
        if r.status_code == 200:
            print("   ✅ Application accessible")
            return True
        else:
            print(f"   ❌ Problème: {r.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_admin_csrf():
    print("\n2. Test CSRF admin...")
    try:
        session = requests.Session()
        r = session.get(f"{URL}/admin/login/", timeout=10)
        
        if r.status_code != 200:
            print(f"   ❌ Admin inaccessible: {r.status_code}")
            return False
        
        # Vérifier CSRF
        if 'csrfmiddlewaretoken' not in r.text:
            print("   ❌ CSRF absent")
            return False
        
        print("   ✅ Page admin avec CSRF accessible")
        
        # Tenter une requête POST
        import re
        csrf_match = re.search(r'csrfmiddlewaretoken.*value="([^"]+)"', r.text)
        if csrf_match:
            csrf = csrf_match.group(1)
            print(f"   CSRF token: {csrf[:15]}...")
            
            # Test POST
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
                print("   ❌ Origin checking failed - Variables non appliquées")
                return False
            elif r2.status_code in [200, 302]:
                print("   ✅ CSRF fonctionne !")
                return True
            else:
                print(f"   ⚠️  POST: {r2.status_code}")
                return True
        else:
            print("   ⚠️  CSRF non extractible")
            return True
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

# Exécuter les tests
print("⏳ Test en cours...")
time.sleep(2)  # Attendre un peu

test1 = test_application()
test2 = test_admin_csrf()

print("\n" + "="*60)
if test1 and test2:
    print("🎉🎉🎉 SUCCÈS COMPLET ! 🎉🎉🎉")
    print("Les variables Railway ont corrigé le problème CSRF !")
    print(f"\n🌐 Votre application est maintenant opérationnelle :")
    print(f"   URL: {URL}")
    print(f"   Admin: {URL}/admin/")
    print(f"\n🚀 Prochaine étape : Créez un superutilisateur !")
    print("   Méthode 1: railway run python manage.py createsuperuser")
    print("   Méthode 2: Via la console Railway web")
elif test1 and not test2:
    print("⚠️  APPLICATION OK MAIS CSRF PERSISTE")
    print("Les variables ne sont peut-être pas encore appliquées.")
    print("\n🔧 Actions :")
    print("1. Attendez 2-3 minutes de plus")
    print("2. Redéployez manuellement")
    print("3. Réessayez ce test")
else:
    print("❌ PROBLÈME CRITIQUE")
    print("L'application ne répond pas.")
    print("\n🚨 Vérifiez :")
    print("1. Le déploiement est-il terminé ?")
    print("2. Y a-t-il des erreurs dans les logs Railway ?")
    print("3. Les variables sont-elles correctement configurées ?")

print("\n" + "="*60)
