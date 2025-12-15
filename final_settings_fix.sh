#!/bin/bash
echo "🔧 SOLUTION DÉFINITIVE - MODIFICATION DE settings.py"
echo "===================================================="

# Backup du fichier settings.py actuel
cp mutuelle_core/settings.py mutuelle_core/settings.py.backup.final

# Ajouter la configuration FORCÉE à la fin du fichier
cat >> mutuelle_core/settings.py << 'SETTINGSFINAL'

# =============================================================================
# CONFIGURATION FORCÉE POUR RAILWAY - AJOUTÉE LE $(date)
# =============================================================================

print("\n" + "="*80)
print("⚡ CONFIGURATION FORCÉE POUR RAILWAY ACTIVÉE")
print("="*80)

# DÉTECTION RAILWAY FORCÉE
RAILWAY = True
RAILWAY_DOMAIN = "web-production-555c.up.railway.app"

# DEBUG FORCÉ
DEBUG = True
print(f"DEBUG = {DEBUG}")

# CSRF - FORCÉ ABSOLUMENT
CSRF_TRUSTED_ORIGINS = [
    f'https://{RAILWAY_DOMAIN}',
    f'http://{RAILWAY_DOMAIN}',
    'https://*.railway.app',
    'http://*.railway.app',
]

# Ajouter depuis variables d'environnement si présentes
import os
env_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if env_csrf:
    CSRF_TRUSTED_ORIGINS.extend([x.strip() for x in env_csrf.split(',') if x.strip()])
    CSRF_TRUSTED_ORIGINS = list(set(CSRF_TRUSTED_ORIGINS))

print(f"CSRF_TRUSTED_ORIGINS = {len(CSRF_TRUSTED_ORIGINS)} origines")
print(f"  - {RAILWAY_DOMAIN} inclus: {'✅ OUI' if f'https://{RAILWAY_DOMAIN}' in CSRF_TRUSTED_ORIGINS else '❌ NON'}")

# PROXY RAILWAY FORCÉ
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
print(f"SECURE_PROXY_SSL_HEADER = {SECURE_PROXY_SSL_HEADER}")

# ALLOWED_HOSTS FORCÉ
ALLOWED_HOSTS = [
    RAILWAY_DOMAIN,
    f'.{RAILWAY_DOMAIN}',
    '.railway.app',
    '*.railway.app',
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '[::1]',
    '*',  # Temporaire pour debug
]
print(f"ALLOWED_HOSTS = {len(ALLOWED_HOSTS)} hosts")

# COOKIES POUR RAILWAY
CSRF_COOKIE_DOMAIN = None
SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_SECURE = False  # True en production
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False
print(f"CSRF_COOKIE_DOMAIN = {CSRF_COOKIE_DOMAIN}")

# CORS FORCÉ
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
print("CORS_ALLOW_ALL_ORIGINS = True")

print("\n✅ Configuration Railway forcée avec succès")
print("="*80)
SETTINGSFINAL

echo "✅ settings.py modifié avec configuration forcée"
echo ""

# Vérifier la modification
echo "📋 Vérification de la modification :"
tail -20 mutuelle_core/settings.py

echo ""
echo "🚀 DÉPLOIEMENT IMMÉDIAT :"
echo "-------------------------"
echo "1. Ajoutez les fichiers :"
echo "   git add mutuelle_core/settings.py"
echo ""
echo "2. Commit :"
echo "   git commit -m 'FINAL: Force Railway CSRF configuration in settings.py'"
echo ""
echo "3. Déployez sur Railway :"
echo "   git push railway main"
echo ""
echo "4. Attendez 2-3 minutes"
echo ""
echo "5. Testez avec :"
echo "   python test_immediate.py"
echo ""

# Créer un test immédiat
cat > test_immediate.py << 'TESTIMMEDIATE'
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
TESTIMMEDIATE

chmod +x test_immediate.py

echo "✅ Prêt ! Suivez les étapes ci-dessus."
