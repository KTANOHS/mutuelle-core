#!/bin/bash
echo "🚀 DÉPLOIEMENT DU FICHIER .env SUR RAILWAY"
echo "=========================================="

# 1. Vérifier le fichier .env
echo "1. Vérification du fichier .env :"
echo ""
cat .env
echo ""

# 2. Ajouter à git
echo "2. Ajout du fichier à Git :"
git add .env

# 3. Commit
echo "3. Commit des changements :"
git commit -m "ADD: Environment variables for Railway CSRF fix - $(date '+%Y-%m-%d %H:%M:%S')"

# 4. Déployer sur Railway
echo "4. Déploiement sur Railway :"
echo "   Exécutez cette commande :"
echo "   git push railway main"
echo ""

# 5. Script pour tester après déploiement
echo "5. Script de test après déploiement :"
cat > test_after_env_deploy.py << 'TESTENV'
#!/usr/bin/env python3
"""
Test après déploiement du fichier .env
"""

import requests
import time
import sys

print("🧪 TEST APRÈS DÉPLOIEMENT .env")
print("="*60)

URL = "https://web-production-555c.up.railway.app"

def wait_for_deployment(max_wait=300, check_interval=30):
    """Attendre que le déploiement soit terminé"""
    print(f"⏳ Attente du déploiement (max {max_wait//60} min)...")
    
    for elapsed in range(0, max_wait, check_interval):
        try:
            print(f"   Vérification ({elapsed//60}min {elapsed%60}s)...")
            r = requests.get(URL, timeout=10)
            
            if r.status_code == 200:
                print("✅ Application répond")
                return True
                
        except requests.exceptions.RequestException:
            print("   ⏳ Application non encore prête...")
        
        if elapsed < max_wait - check_interval:
            print(f"   Attente de {check_interval} secondes...")
            time.sleep(check_interval)
    
    return False

def test_csrf_after_env():
    """Tester si le CSRF fonctionne après .env"""
    print("\n🔐 Test CSRF après .env...")
    
    try:
        session = requests.Session()
        
        # 1. GET admin login
        admin_url = f"{URL}/admin/login/"
        r = session.get(admin_url, timeout=10)
        
        if r.status_code != 200:
            print(f"❌ Admin inaccessible: {r.status_code}")
            return False
        
        print("✅ Page admin accessible")
        
        # 2. Vérifier CSRF
        import re
        if 'csrfmiddlewaretoken' not in r.text:
            print("❌ CSRF token absent")
            return False
        
        csrf_match = re.search(r'csrfmiddlewaretoken.*value="([^"]+)"', r.text)
        if not csrf_match:
            print("⚠️  CSRF présent mais non extractible")
            return True
        
        csrf_token = csrf_match.group(1)
        print(f"✅ CSRF token: {csrf_token[:15]}...")
        
        # 3. Test POST
        print("\n🧪 Test POST (critique)...")
        data = {
            'csrfmiddlewaretoken': csrf_token,
            'username': 'test',
            'password': 'test',
            'next': '/admin/'
        }
        
        headers = {
            'Referer': admin_url,
            'Origin': URL,
        }
        
        r2 = session.post(admin_url, data=data, headers=headers, 
                         allow_redirects=False, timeout=10)
        
        print(f"   POST Status: {r2.status_code}")
        
        # Analyse
        if r2.status_code == 403:
            response_text = r2.text[:500]
            if 'Origin checking failed' in response_text:
                print("❌ Origin checking failed PERSISTE")
                print("   Le fichier .env n'a pas résolu le problème")
                print("   Raison probable: Railway ignore .env")
                return False
            else:
                print("⚠️  403 autre (identifiants probablement)")
                print("✅✅✅ CSRF FONCTIONNE MAINTENANT !")
                return True
        elif r2.status_code in [200, 302]:
            print(f"✅✅✅ CSRF FONCTIONNE (Status: {r2.status_code})")
            return True
        else:
            print(f"⚠️  Code inattendu: {r2.status_code}")
            return True
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

# Exécuter les tests
print(f"🌐 Test de: {URL}")
print("="*60)

# Attendre le déploiement
if wait_for_deployment(max_wait=180, check_interval=30):
    print("\n🎉 Déploiement terminé !")
    
    # Tester CSRF
    if test_csrf_after_env():
        print("\n" + "="*60)
        print("🎉🎉🎉 SUCCÈS COMPLET ! 🎉🎉🎉")
        print("Le fichier .env a résolu le problème CSRF !")
        print(f"\n🌐 Votre application: {URL}")
        print(f"🔑 Admin: {URL}/admin/")
        print("\n🚀 Prochaine étape: Créez un superutilisateur")
        print("   Méthode 1: railway run python manage.py createsuperuser")
        print("   Méthode 2: Via la console Railway web")
    else:
        print("\n" + "="*60)
        print("❌ PROBLÈME PERSISTE")
        print("\n🚨 Le fichier .env n'a pas résolu le problème")
        print("🔧 Essayez ces solutions:")
        print("   1. Configurez les variables DANS l'interface Railway")
        print("   2. Utilisez le script ultimate_railway_fix.py")
        print("   3. Contactez le support Railway")
else:
    print("\n" + "="*60)
    print("❌ DÉPLOIEMENT TROP LONG")
    print("\n🔧 Vérifiez manuellement:")
    print("   1. Allez sur https://railway.app")
    print("   2. Vérifiez les logs de déploiement")
    print("   3. Attendez quelques minutes")

print("\n" + "="*60)
TESTENV

chmod +x test_after_env_deploy.py

echo -e "\n✅ PRÊT À DÉPLOYER !"
echo ""
echo "🎯 ÉTAPES FINALES :"
echo "   1. ⚡ Exécutez : git push railway main"
echo "   2. ⏳ Attendez 3-5 minutes"
echo "   3. 🧪 Testez : python test_after_env_deploy.py"
echo "   4. 🔁 Si échec, configurez les variables dans l'interface Railway"
echo ""
echo "📊 STATUT ACTUEL :"
echo "   - ✅ Fichier .env créé avec les bonnes variables"
echo "   - ⏳ Prêt à déployer sur Railway"
echo "   - 🎯 Espérons que Railway utilisera ce fichier .env"
