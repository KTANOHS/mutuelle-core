#!/bin/bash
echo "🔧 CORRECTION IMMÉDIATE DE CSRF_TRUSTED_ORIGINS"

# 1. D'abord, afficher la configuration actuelle
echo "1. Vérification de la configuration actuelle..."
curl -s https://web-production-555c.up.railway.app | grep -o "CSRF_TRUSTED_ORIGINS.*\]\|DEBUG.*true\|DEBUG.*false" || echo "Configuration non détectée"

# 2. Vérifier si DEBUG=True
echo -e "\n2. Test du mode DEBUG..."
DEBUG_STATUS=$(curl -s https://web-production-555c.up.railway.app/admin/login/ | grep -o "DEBUG = True\|DEBUG = False")
echo "   $DEBUG_STATUS"

# 3. Créer un script Python pour vérifier les settings
cat > check_settings.py << 'PYEOF'
import os
import django

# Essayer d'importer les settings
try:
    # Ajouter le chemin de votre projet
    import sys
    sys.path.append('.')
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    
    # Configurer Django
    django.setup()
    
    from django.conf import settings
    
    print("🔍 CONFIGURATION ACTUELLE:")
    print(f"DEBUG = {settings.DEBUG}")
    print(f"ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
    print(f"CSRF_TRUSTED_ORIGINS = {getattr(settings, 'CSRF_TRUSTED_ORIGINS', 'Non défini')}")
    print(f"CSRF_COOKIE_DOMAIN = {getattr(settings, 'CSRF_COOKIE_DOMAIN', 'Non défini')}")
    print(f"SECURE_PROXY_SSL_HEADER = {getattr(settings, 'SECURE_PROXY_SSL_HEADER', 'Non défini')}")
    
    # Vérifier spécifiquement notre domaine
    domain = "https://web-production-555c.up.railway.app"
    if hasattr(settings, 'CSRF_TRUSTED_ORIGINS'):
        if domain in settings.CSRF_TRUSTED_ORIGINS:
            print(f"\n✅ {domain} est dans CSRF_TRUSTED_ORIGINS")
        else:
            print(f"\n❌ {domain} N'EST PAS dans CSRF_TRUSTED_ORIGINS")
            print(f"   Origines configurées: {settings.CSRF_TRUSTED_ORIGINS}")
    else:
        print(f"\n⚠️ CSRF_TRUSTED_ORIGINS n'est pas défini")
        
except Exception as e:
    print(f"Erreur: {e}")
    print("\n⚠️ Impossible de charger les settings")
PYEOF

echo -e "\n3. Exécution du diagnostic..."
python check_settings.py

# 4. Solution immédiate
echo -e "\n4. 🚨 SOLUTION IMMÉDIATE :"
echo "   Modifiez votre settings.py et AJOUTEZ ABSOLUMENT :"
cat << 'SETTINGS'

# =============================================================================
# CORRECTION URGENTE CSRF POUR RAILWAY
# =============================================================================

# LE DOMAINE EXACT DOIT ÊTRE DANS CSRF_TRUSTED_ORIGINS
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-555c.up.railway.app',  # <-- CE DOMAINE EXACT
    'http://web-production-555c.up.railway.app',   # Version HTTP aussi
    'https://*.railway.app',
    'http://*.railway.app',
]

# Configuration CRITIQUE pour Railway
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# IMPORTANT: Ces deux doivent être None pour Railway
CSRF_COOKIE_DOMAIN = None
SESSION_COOKIE_DOMAIN = None

# Autres settings importants
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SAMESITE = 'Lax'

# Assurez-vous que DEBUG=True pour le moment
DEBUG = True
SETTINGS

# 5. Script de test après correction
echo -e "\n5. 📋 Après avoir modifié settings.py :"
echo "   git add ."
echo "   git commit -m 'Fix CSRF_TRUSTED_ORIGINS'"
echo "   git push railway main"
echo "   Puis exécutez: ./test_after_fix.sh"

cat > test_after_fix.sh << 'TEST'
#!/bin/bash
echo "🧪 TEST APRÈS CORRECTION"

URL="https://web-production-555c.up.railway.app"
echo "Test de: $URL"

# Test simple de connexion
python3 -c "
import requests

url = '$URL/admin/login/'
session = requests.Session()

# 1. GET request
print('1. GET page login...')
resp = session.get(url)
print(f'   Status: {resp.status_code}')

# 2. Check CSRF token
import re
csrf_token = re.search(r'csrfmiddlewaretoken.*value=\"([^\"]+)\"', resp.text)
if csrf_token:
    csrf = csrf_token.group(1)
    print(f'2. CSRF token trouvé: {csrf[:20]}...')
    
    # 3. POST request
    print('3. Test POST...')
    data = {
        'csrfmiddlewaretoken': csrf,
        'username': 'matrix',
        'password': 'transport744',
        'next': '/admin/'
    }
    
    headers = {
        'Referer': url,
        'Origin': '$URL'
    }
    
    resp2 = session.post(url, data=data, headers=headers, allow_redirects=False)
    print(f'   Status POST: {resp2.status_code}')
    
    if resp2.status_code == 302:
        print('✅ SUCCÈS! Redirection détectée')
    else:
        print(f'❌ Échec. Réponse (500 premiers chars):')
        print(resp2.text[:500])
else:
    print('❌ Aucun token CSRF trouvé')
"
TEST

chmod +x test_after_fix.sh

echo -e "\n✅ Scripts créés. Suivez les instructions ci-dessus."
