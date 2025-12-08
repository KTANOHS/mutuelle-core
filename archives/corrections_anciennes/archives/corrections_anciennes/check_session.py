# check_session.py
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client

def check_session():
    client = Client()
    
    print("🔍 VÉRIFICATION SESSION")
    print("=======================")
    
    # Test de connexion
    response = client.post('/accounts/login/', {
        'username': 'agent_test', 
        'password': 'password123'
    }, follow=True)
    
    print(f"1. Après login - URL: {response.request['PATH_INFO']}")
    print(f"   Status: {response.status_code}")
    
    # Vérifier les cookies de session
    session_cookie = client.cookies.get('sessionid')
    if session_cookie:
        print(f"2. Cookie session: PRÉSENT (value: {session_cookie.value[:20]}...)")
    else:
        print("2. Cookie session: ABSENT")
    
    # Test avec le cookie de session
    if session_cookie:
        print("3. Test avec cookie session...")
        response2 = client.get('/agents/dashboard/')
        print(f"   Dashboard status: {response2.status_code}")
        print(f"   URL: {response2.request['PATH_INFO']}")

if __name__ == "__main__":
    check_session()