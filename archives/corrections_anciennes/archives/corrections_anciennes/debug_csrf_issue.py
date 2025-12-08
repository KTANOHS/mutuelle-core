# debug_csrf_issue.py
import os
import django
import sys

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.urls import reverse

def test_csrf_endpoints():
    """Teste les endpoints qui pourraient causer des erreurs CSRF"""
    
    client = Client(enforce_csrf_checks=True)
    
    # Liste des URLs à tester
    endpoints = [
        ('login', 'registration/login.html'),
        ('register', 'registration/register.html'),
        # Ajoutez vos URLs problématiques ici
    ]
    
    print("🔍 Test des endpoints CSRF...")
    print("=" * 50)
    
    for endpoint, template in endpoints:
        try:
            # Test GET (devrait fonctionner)
            response = client.get(reverse(endpoint))
            if response.status_code == 200:
                print(f"✅ GET {endpoint}: OK")
            else:
                print(f"❌ GET {endpoint}: {response.status_code}")
            
            # Test POST sans CSRF (devrait échouer)
            response = client.post(reverse(endpoint), {})
            if response.status_code == 403 and 'CSRF' in str(response.content):
                print(f"🔒 POST {endpoint}: Protection CSRF active (comportement normal)")
            else:
                print(f"⚠️  POST {endpoint}: Statut {response.status_code} - Vérification CSRF peut-être désactivée")
                
        except Exception as e:
            print(f"❌ {endpoint}: Erreur - {e}")

def check_csrf_middleware():
    """Vérifie la configuration CSRF"""
    
    from django.conf import settings
    
    print(f"\n🔧 Configuration CSRF:")
    print("-" * 30)
    
    # Vérifier le middleware
    if 'django.middleware.csrf.CsrfViewMiddleware' in settings.MIDDLEWARE:
        print("✅ Middleware CSRF activé")
    else:
        print("❌ Middleware CSRF désactivé")
    
    # Vérifier les paramètres CSRF
    print(f"   CSRF_COOKIE_SECURE: {getattr(settings, 'CSRF_COOKIE_SECURE', 'Non défini')}")
    print(f"   CSRF_COOKIE_HTTPONLY: {getattr(settings, 'CSRF_COOKIE_HTTPONLY', 'Non défini')}")
    print(f"   CSRF_USE_SESSIONS: {getattr(settings, 'CSRF_USE_SESSIONS', 'Non défini')}")

def find_ajax_requests():
    """Cherche les requêtes AJAX potentielles dans les templates"""
    
    import re
    
    print(f"\n🔍 Recherche de requêtes AJAX...")
    print("-" * 30)
    
    js_patterns = [
        r'\.post\([^)]*\)',
        r'\.ajax\([^)]*\)',
        r'fetch\([^)]*\)',
        r'XMLHttpRequest'
    ]
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(('.html', '.js')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for pattern in js_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            print(f"📄 {file_path}")
                            for match in matches[:2]:  # Montre 2 premiers matches
                                print(f"   🚨 {match[:100]}...")
                            break
                except:
                    pass

if __name__ == "__main__":
    check_csrf_middleware()
    find_ajax_requests()
    # test_csrf_endpoints()  # Décommentez si vous avez les URLs configurées