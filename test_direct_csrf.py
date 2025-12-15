import requests
import re

def test_csrf_with_method(method_name, url, headers=None):
    print(f'\n🔧 Méthode: {method_name}')
    session = requests.Session()
    
    # GET
    resp = session.get(url)
    csrf_match = re.search(r'csrfmiddlewaretoken.*value="([^"]+)"', resp.text)
    
    if not csrf_match:
        print('   ❌ CSRF non trouvé')
        return False
    
    csrf_token = csrf_match.group(1)
    
    # POST
    data = {
        'csrfmiddlewaretoken': csrf_token,
        'username': 'test',
        'password': 'test',
        'next': '/admin/'
    }
    
    post_headers = {'Referer': url}
    if headers:
        post_headers.update(headers)
    
    resp_post = session.post(url, data=data, headers=post_headers, allow_redirects=False)
    
    print(f'   GET: {resp.status_code}, POST: {resp_post.status_code}')
    
    if resp_post.status_code == 403:
        if 'Origin checking failed' in resp_post.text:
            print('   ❌ Origin checking failed')
            # Extraire la raison exacte
            import re
            reason = re.search(r'<pre>(.*?)</pre>', resp_post.text, re.DOTALL)
            if reason:
                print(f'   Raison: {reason.group(1).strip()[:100]}...')
        else:
            print('   ❌ 403 (autre raison)')
    elif resp_post.status_code == 302:
        print('   ✅ Redirection! (CSRF fonctionne)')
        return True
    elif resp_post.status_code == 200:
        print('   ⚠️  200 (identifiants incorrects mais CSRF OK)')
        return True
    
    return False

url = 'https://web-production-555c.up.railway.app/admin/login/'

print('Test des différentes méthodes CSRF:')
print('=' * 50)

# Méthode 1: Standard
test_csrf_with_method('Standard', url)

# Méthode 2: Avec Origin
test_csrf_with_method('Avec Origin', url, {'Origin': 'https://web-production-555c.up.railway.app'})

# Méthode 3: Avec headers Railway
test_csrf_with_method('Headers Railway', url, {
    'Origin': 'https://web-production-555c.up.railway.app',
    'X-Forwarded-Proto': 'https',
    'X-Forwarded-Host': 'web-production-555c.up.railway.app'
})

# Méthode 4: Sans Referer
test_csrf_with_method('Sans Referer', url, {})

print('\n' + '=' * 50)
print('📋 CONCLUSION:')
print('Si "Origin checking failed" persiste, le problème est dans settings.py')
print('Le fichier settings.py sur Railway n\'est PAS celui que vous pensez.')
print('\n🚨 ACTION REQUISE:')
print('1. Vérifiez que git push a bien fonctionné')
print('2. Vérifiez les logs Railway')
print('3. Essayez un settings.py ultra simple')
