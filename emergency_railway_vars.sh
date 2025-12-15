#!/bin/bash
echo "🚨 CONFIGURATION D'URGENCE VIA VARIABLES RAILWAY"
echo "================================================"

echo "📋 COPIEZ ET COLLEZ CES VARIABLES EXACTEMENT DANS RAILWAY:"
echo ""
echo "========================================================"
echo "🚨 SUPPRIMEZ TOUTES LES VARIABLES EXISTANTES D'ABORD !"
echo "========================================================"
echo ""
echo "RAILWAY=true"
echo "DEBUG=True"
echo "SECRET_KEY=$(openssl rand -hex 32)"
echo ""
echo "ALLOWED_HOSTS=web-production-555c.up.railway.app,*.railway.app,localhost,127.0.0.1,*,0.0.0.0,[::1]"
echo ""
echo "CSRF_TRUSTED_ORIGINS=https://web-production-555c.up.railway.app,http://web-production-555c.up.railway.app,https://*.railway.app,http://*.railway.app"
echo ""
echo "CORS_ALLOWED_ORIGINS=https://web-production-555c.up.railway.app,http://web-production-555c.up.railway.app,https://*.railway.app,http://*.railway.app"
echo ""
echo "RAILWAY_PUBLIC_DOMAIN=web-production-555c.up.railway.app"
echo ""
echo "SECURE_PROXY_SSL_HEADER=true"
echo "USE_X_FORWARDED_HOST=true"
echo "USE_X_FORWARDED_PORT=true"
echo ""
echo "DISABLE_COLLECTSTATIC=1"
echo ""
echo "CSRF_COOKIE_DOMAIN=none"
echo "SESSION_COOKIE_DOMAIN=none"
echo ""
echo "========================================================"
echo ""
echo "📝 INSTRUCTIONS:"
echo "1. Allez sur: https://railway.app/project/$(railway project 2>/dev/null | grep -o 'ID: [^ ]*' | cut -d' ' -f2 || echo 'VOTRE-PROJET-ID')/variables"
echo "2. Supprimez TOUTES les variables existantes"
echo "3. Ajoutez CHAQUE variable ci-dessus"
echo "4. Sauvegardez"
echo "5. Redéployez manuellement depuis l'interface Railway"
echo ""
echo "🔄 Après déploiement, testez avec:"
cat > test_after_vars_fix.py << 'TESTVARS'
#!/usr/bin/env python3
import requests
import re

print("🧪 TEST APRÈS VARIABLES RAILWAY")
print("="*60)

URL = "https://web-production-555c.up.railway.app"

def test_csrf():
    try:
        session = requests.Session()
        
        # Test 1: GET admin login
        print("1. Test GET admin/login...")
        resp = session.get(f"{URL}/admin/login/", timeout=10)
        print(f"   Status: {resp.status_code}")
        
        if resp.status_code != 200:
            print("   ❌ Échec GET")
            return False
        
        # Test 2: CSRF token
        csrf_match = re.search(r'csrfmiddlewaretoken.*value="([^"]+)"', resp.text)
        if not csrf_match:
            print("   ❌ CSRF non trouvé")
            return False
        
        csrf_token = csrf_match.group(1)
        print(f"2. CSRF token: {csrf_token[:20]}...")
        
        # Test 3: POST request
        print("3. Test POST...")
        data = {
            'csrfmiddlewaretoken': csrf_token,
            'username': 'testuser',
            'password': 'testpass',
            'next': '/admin/'
        }
        
        headers = {
            'Referer': f"{URL}/admin/login/",
            'Origin': URL,
        }
        
        resp_post = session.post(f"{URL}/admin/login/", data=data, headers=headers, 
                                allow_redirects=False, timeout=10)
        
        print(f"   POST Status: {resp_post.status_code}")
        
        # Analyse
        if resp_post.status_code == 403:
            if 'Origin checking failed' in resp_post.text:
                print("   ❌ Origin checking failed PERSISTE")
                print("   Les variables Railway ne sont pas appliquées")
                return False
            else:
                print("   ⚠️  403 autre (identifiants probablement)")
                print("   ✅ CSRF FONCTIONNE !")
                return True
        elif resp_post.status_code in [200, 302]:
            print(f"   ✅ CSRF FONCTIONNE (Status: {resp_post.status_code})")
            return True
        else:
            print(f"   ⚠️  Code inattendu: {resp_post.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

# Exécuter le test
if test_csrf():
    print("\n" + "="*60)
    print("🎉 SUCCÈS ! Les variables Railway ont corrigé le problème CSRF")
    print(f"\n🌐 Votre application: {URL}")
    print(f"🔑 Créez maintenant un superutilisateur:")
    print("   railway run python manage.py createsuperuser")
else:
    print("\n" + "="*60)
    print("❌ ÉCHEC - Le problème CSRF persiste")
    print("\n🚨 ACTIONS REQUISES:")
    print("1. Vérifiez que les variables sont bien sauvegardées")
    print("2. Redéployez manuellement depuis l'interface Railway")
    print("3. Attendez 3-5 minutes pour le cache")
    print("4. Réessayez ce test")

print("="*60)
TESTVARS

chmod +x test_after_vars_fix.py
echo "   python test_after_vars_fix.py"
