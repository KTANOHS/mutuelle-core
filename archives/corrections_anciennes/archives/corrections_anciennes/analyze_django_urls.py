"""
Script complet pour analyser les URLs Django et le processus d'authentification
"""
import os
import sys
import django
from django.conf import settings
from django.urls import get_resolver
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configuration pour pouvoir importer votre projet Django
try:
    # Ajoutez le chemin de votre projet si nécessaire
    sys.path.append('/koffitanohsoualiho@koffis-MBP projet ')  # À modifier
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')  # À modifier
    
    django.setup()
    DJANGO_AVAILABLE = True
except Exception as e:
    print(f"❌ Impossible de configurer Django: {e}")
    DJANGO_AVAILABLE = False

def analyze_django_urls():
    """Analyse la configuration des URLs Django"""
    if not DJANGO_AVAILABLE:
        print("❌ Django n'est pas disponible pour l'analyse")
        return
    
    print("🔍 ANALYSE DES URLS DJANGO")
    print("=" * 60)
    
    resolver = get_resolver()
    
    print("\n📋 Liste de toutes les URLs configurées:")
    print("-" * 40)
    
    url_count = 0
    
    def _analyze_patterns(patterns, prefix="", depth=0):
        nonlocal url_count
        for pattern in patterns:
            # Pour Django 2.0+
            if hasattr(pattern, 'pattern'):
                current_pattern = pattern.pattern
                if hasattr(pattern, 'url_patterns'):
                    # Namespace ou include
                    print(f"{prefix}📁 {current_pattern} [include]")
                    _analyze_patterns(pattern.url_patterns, prefix + "  ", depth + 1)
                else:
                    # URL simple
                    callback = pattern.callback
                    callback_name = getattr(callback, '__name__', 'Unknown')
                    callback_module = getattr(callback, '__module__', 'Unknown')
                    print(f"{prefix}📍 {current_pattern} -> {callback_module}.{callback_name}")
                    url_count += 1
            # Pour les versions plus anciennes
            elif hasattr(pattern, '_regex'):
                print(f"{prefix}📍 {pattern._regex} -> {pattern.callback.__name__}")
                url_count += 1
    
    try:
        _analyze_patterns(resolver.url_patterns)
        print(f"\n✅ Total d'URLs trouvées: {url_count}")
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse des URLs: {e}")

def analyze_auth_urls():
    """Analyse spécifique des URLs d'authentification"""
    if not DJANGO_AVAILABLE:
        return
    
    print("\n🔐 ANALYSE DES URLS D'AUTHENTIFICATION")
    print("=" * 50)
    
    auth_urls = [
        '/login/',
        '/logout/',
        '/signup/',
        '/redirect-after-login/',
        '/admin/login/'
    ]
    
    resolver = get_resolver()
    
    for url in auth_urls:
        try:
            match = resolver.resolve(url)
            print(f"📍 {url} -> {match.func.__module__}.{match.func.__name__}")
            print(f"   Arguments: {match.args}")
            print(f"   Kwargs: {match.kwargs}")
            print(f"   URL Name: {getattr(match, 'url_name', 'N/A')}")
        except Exception as e:
            print(f"❌ {url} -> Non trouvée ({e})")

class DjangoAuthDebugger:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        
        # Configuration pour debug
        self.session.max_redirects = 5
        
        # Setup retry strategy
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Headers pour simuler un vrai navigateur
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Auth-Debugger)'
        })

    def test_redirect_chain(self, start_url):
        """Teste une chaine de redirection spécifique"""
        print(f"\n🔄 TEST DE REDIRECTION: {start_url}")
        print("-" * 50)
        
        current_url = start_url
        redirect_chain = []
        redirect_count = 0
        max_redirects = 10
        
        while redirect_count < max_redirects:
            try:
                response = self.session.get(
                    f"{self.base_url}{current_url}", 
                    allow_redirects=False,
                    timeout=5
                )
                
                print(f"#{redirect_count + 1} GET {current_url}")
                print(f"  Status: {response.status_code}")
                print(f"  Cookies: {dict(self.session.cookies)}")
                
                redirect_chain.append({
                    'url': current_url,
                    'status': response.status_code,
                    'cookies': dict(self.session.cookies)
                })
                
                if response.status_code in [301, 302, 303, 307, 308]:
                    location = response.headers.get('Location', '')
                    print(f"  ↳ Redirection vers: {location}")
                    
                    if not location:
                        print("  ❌ Pas de header Location")
                        break
                    
                    # Normaliser l'URL
                    if location.startswith('/'):
                        current_url = location
                    elif location.startswith('http'):
                        # Extraire le chemin si c'est une URL absolue
                        from urllib.parse import urlparse
                        parsed = urlparse(location)
                        current_url = parsed.path
                        if parsed.query:
                            current_url += '?' + parsed.query
                    else:
                        current_url = location
                    
                    redirect_count += 1
                    
                    # Vérifier les boucles
                    if any(step['url'] == current_url for step in redirect_chain):
                        print(f"  ⚠️  BOUCLE DÉTECTÉE! URL déjà visitée: {current_url}")
                        break
                else:
                    print(f"  ✅ Redirection terminée")
                    break
                    
            except requests.exceptions.TooManyRedirects:
                print(f"  ❌ TROP DE REDIRECTIONS! Boucle infinie détectée")
                break
            except Exception as e:
                print(f"  ❌ Erreur: {e}")
                break
        
        if redirect_count >= max_redirects:
            print(f"  ⚠️  Arrêt: Limite de {max_redirects} redirections atteinte")
        
        return redirect_chain

    def debug_login_flow(self):
        """Debug le flux de connexion complet"""
        print("\n🔐 DEBUG DU FLUX DE CONNEXION COMPLET")
        print("=" * 60)
        
        # 1. Test de la page problématique
        print("\n1. TEST DE LA PAGE REDIRECT-AFTER-LOGIN")
        self.test_redirect_chain("/redirect-after-login/")
        
        # 2. Test de la page de login
        print("\n2. TEST DE LA PAGE DE LOGIN")
        self.test_redirect_chain("/login/")
        
        # 3. Vérification des cookies
        print("\n3. ANALYSE DES COOKIES")
        print(f"Cookies actuels: {dict(self.session.cookies)}")
        
        # 4. Test d'accès direct à l'admin (souvent différent)
        print("\n4. TEST ACCÈS ADMIN")
        self.test_redirect_chain("/admin/")

def check_django_settings():
    """Vérifie les paramètres Django importants pour l'authentification"""
    if not DJANGO_AVAILABLE:
        return
    
    print("\n⚙️  PARAMÈTRES DJANGO D'AUTHENTIFICATION")
    print("=" * 50)
    
    important_settings = [
        'LOGIN_URL',
        'LOGIN_REDIRECT_URL', 
        'LOGOUT_REDIRECT_URL',
        'AUTHENTICATION_BACKENDS',
        'MIDDLEWARE',
    ]
    
    for setting in important_settings:
        try:
            value = getattr(settings, setting, "NON DÉFINI")
            print(f"{setting}: {value}")
        except Exception as e:
            print(f"{setting}: ERREUR - {e}")

if __name__ == "__main__":
    print("🚀 LANCEMENT DE L'ANALYSE DJANGO")
    print("=" * 60)
    
    # 1. Analyse des paramètres Django
    check_django_settings()
    
    # 2. Analyse des URLs
    analyze_django_urls()
    
    # 3. Analyse spécifique auth
    analyze_auth_urls()
    
    # 4. Test des redirections (nécessite que le serveur tourne)
    debugger = DjangoAuthDebugger()
    
    print("\n" + "="*60)
    print("🎯 TESTS DE REDIRECTION (serveur doit être démarré)")
    print("="*60)
    
    try:
        debugger.debug_login_flow()
    except Exception as e:
        print(f"❌ Impossible d'exécuter les tests de redirection: {e}")
        print("💡 Assurez-vous que le serveur Django tourne sur http://127.0.0.1:8000")