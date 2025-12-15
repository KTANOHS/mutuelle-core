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
