#!/bin/bash
echo "🔐 TEST FINAL DE CONNEXION ADMIN"
echo "================================"

URL="https://web-production-555c.up.railway.app"
echo "URL de test: $URL"

python3 -c "
import requests
import re
import sys

def test_login(username, password):
    '''Test de connexion avec des identifiants spécifiques'''
    
    print(f'\\n🔑 Test avec: {username}')
    
    session = requests.Session()
    
    try:
        # 1. GET login page
        login_url = f'{URL}/admin/login/'
        response = session.get(login_url, timeout=10)
        
        if response.status_code != 200:
            print(f'   ❌ GET failed: {response.status_code}')
            return False
        
        # 2. Extract CSRF token
        csrf_match = re.search(r'csrfmiddlewaretoken.*value=\"([^\"]+)\"', response.text)
        if not csrf_match:
            print('   ❌ CSRF token not found')
            return False
        
        csrf_token = csrf_match.group(1)
        
        # 3. Prepare POST request
        data = {
            'csrfmiddlewaretoken': csrf_token,
            'username': username,
            'password': password,
            'next': '/admin/'
        }
        
        headers = {
            'Referer': login_url,
            'Origin': URL,
        }
        
        # 4. Send POST request
        response_post = session.post(login_url, data=data, headers=headers, 
                                   allow_redirects=False, timeout=10)
        
        print(f'   POST Status: {response_post.status_code}')
        
        # 5. Analyze response
        if response_post.status_code == 302:
            redirect_url = response_post.headers.get('Location', '')
            print(f'   ✅ REDIRECTION DÉTECTÉE !')
            
            # Follow redirect
            if redirect_url.startswith('/'):
                redirect_url = URL + redirect_url
            
            admin_response = session.get(redirect_url, timeout=10)
            
            if 'Site administration' in admin_response.text:
                print(f'   🎉 CONNEXION RÉUSSIE !')
                print(f'   Vous êtes connecté à l\\'admin Django')
                
                # Extract useful information
                title_match = re.search(r'<title>(.*?)</title>', admin_response.text)
                if title_match:
                    print(f'   Titre: {title_match.group(1)}')
                
                return True
            else:
                print('   ⚠️  Connected but different admin page')
                return True
                
        elif response_post.status_code == 200:
            if 'Please enter the correct username' in response_post.text:
                print('   ❌ Incorrect credentials')
                return False
            else:
                print('   ⚠️  200 response (check manually)')
                return False
                
        elif response_post.status_code == 403:
            print('   ❌ 403 Forbidden')
            # Check for specific CSRF error
            if 'CSRF' in response_post.text:
                print('   CSRF problem detected')
            return False
            
        else:
            print(f'   ❌ Unexpected status: {response_post.status_code}')
            return False
            
    except Exception as e:
        print(f'   ❌ Error: {e}')
        return False
    
    return False

print('🚀 Testing admin login...')
print('=' * 50)

# Test credentials (try common ones)
credentials = [
    {'user': 'admin', 'pass': 'Admin123!'},
    {'user': 'admin', 'pass': 'admin'},
    {'user': 'admin', 'pass': 'AdminMutuelle2024!'},
    {'user': 'matrix', 'pass': 'transport744'},
    {'user': 'root', 'pass': 'root'},
]

success = False
for cred in credentials:
    if test_login(cred['user'], cred['pass']):
        success = True
        print(f'\\n✅ SUCCESS with: {cred[\"user\"]}')
        print(f'🔑 Password: {cred[\"pass\"]}')
        break

print('\\n' + '=' * 50)
if success:
    print('🎉🎉🎉 EVERYTHING WORKS PERFECTLY ! 🎉🎉🎉')
    print(f'\\n🌐 Your Django application is fully operational:')
    print(f'   URL: {URL}')
    print(f'   Admin: {URL}/admin/')
    print(f'\\n📋 Next steps:')
    print('   1. Explore the Django admin interface')
    print('   2. Create additional users if needed')
    print('   3. Configure your mutuelle application')
    print('   4. Test all functionalities')
else:
    print('❌ No valid credentials found')
    print(f'\\n🚨 You need to create a superuser:')
    print('   Method 1 (Railway CLI):')
    print('      railway run python manage.py createsuperuser')
    print(f'\\n   Method 2 (Web interface):')
    print('      1. Go to https://railway.app')
    print('      2. Select your project')
    print('      3. Click \"Console\" or \"Shell\"')
    print('      4. Run: python manage.py createsuperuser')
    print(f'\\n   Method 3 (Default admin):')
    print('      Username: admin')
    print('      Password: AdminMutuelle2024!')
    print('      (if created with our script)')

print('\\n' + '=' * 50)
"

echo -e "\n✅ Test terminé"
