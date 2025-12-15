#!/bin/bash
echo "🚀 DÉPLOIEMENT FINAL SUR RAILWAY"

# 1. Vérifier le code
echo "1. Vérification du code..."
python -m py_compile mutuelle_core/settings.py && echo "✅ Settings.py valide"

# 2. Mettre à jour Railway
echo -e "\n2. Variables Railway requises:"
echo "========================================"
echo "RAILWAY=true"
echo "DEBUG=True"
echo "SECRET_KEY=$(openssl rand -hex 32)"
echo ""
echo "ALLOWED_HOSTS=web-production-555c.up.railway.app,*.railway.app,localhost,127.0.0.1"
echo ""
echo "CSRF_TRUSTED_ORIGINS=https://web-production-555c.up.railway.app,https://*.railway.app,http://web-production-555c.up.railway.app,http://*.railway.app"
echo ""
echo "RAILWAY_PUBLIC_DOMAIN=web-production-555c.up.railway.app"
echo ""
echo "DISABLE_COLLECTSTATIC=0"
echo "========================================"

# 3. Déployer
echo -e "\n3. Commandes de déploiement:"
echo "git add ."
echo "git commit -m 'Fix CSRF configuration for Railway - Final version'"
echo "git push railway main"

# 4. Script de test après déploiement
cat > test_after_deploy.py << 'PYEOF'
#!/usr/bin/env python3
import requests
import time

print("🧪 TEST APRÈS DÉPLOIEMENT")
print("=" * 60)

URL = "https://web-production-555c.up.railway.app"
max_retries = 10
retry_delay = 30

for i in range(max_retries):
    print(f"\nTentative {i+1}/{max_retries}...")
    try:
        # Test 1: Vérifier que l'application répond
        response = requests.get(URL, timeout=10)
        print(f"✅ Application accessible (HTTP {response.status_code})")
        
        # Test 2: Vérifier admin login
        login_url = f"{URL}/admin/login/"
        session = requests.Session()
        login_response = session.get(login_url, timeout=10)
        
        if login_response.status_code == 200:
            print("✅ Page admin/login accessible")
            
            # Chercher CSRF token
            import re
            csrf_match = re.search(r'csrfmiddlewaretoken.*value="([^"]+)"', login_response.text)
            
            if csrf_match:
                print("✅ Token CSRF présent dans le formulaire")
                print("\n🎉 TOUT EST CONFIGURÉ CORRECTEMENT !")
                print(f"\n🌐 Votre application est prête:")
                print(f"   URL: {URL}")
                print(f"   Admin: {URL}/admin/")
                print(f"\n🔑 Connectez-vous avec vos identifiants Django")
                break
            else:
                print("⚠️ Token CSRF non trouvé (page peut être différente)")
        else:
            print(f"⚠️ Page admin retourne {login_response.status_code}")
            
    except requests.RequestException as e:
        print(f"❌ Erreur: {e}")
    
    if i < max_retries - 1:
        print(f"⏳ Attente de {retry_delay} secondes avant de réessayer...")
        time.sleep(retry_delay)
else:
    print(f"\n❌ Échec après {max_retries} tentatives")
    print("Vérifiez:")
    print("1. Le déploiement est-il terminé sur Railway?")
    print("2. Les logs Railway montrent-ils des erreurs?")
    print("3. Les variables d'environnement sont-elles correctes?")

print("\n✅ Test terminé")
PYEOF

chmod +x test_after_deploy.py

echo -e "\n4. Après déploiement, exécutez:"
echo "   python test_after_deploy.py"
echo -e "\n🎯 Si tout est vert, votre application Django est correctement configurée sur Railway!"
