#!/usr/bin/env python
import os
import sys
import django

print("🔍 DIAGNOSTIC COMPLET POUR RENDER")
print("=" * 70)

# Test 1: Vérifier les imports critiques
print("\n1. Vérification des imports critiques:")
try:
    from django.http import HttpResponse
    print("   ✅ django.http.HttpResponse")
except ImportError as e:
    print(f"   ❌ Erreur: {e}")

try:
    from rest_framework_simplejwt.views import TokenObtainPairView
    print("   ✅ rest_framework_simplejwt.views.TokenObtainPairView")
except ImportError as e:
    print(f"   ❌ Erreur: {e}")

# Test 2: Vérifier la configuration
print("\n2. Vérification de la configuration Django:")
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()
    print("   ✅ Django configuré avec succès")
    
    from django.conf import settings
    print(f"   - DEBUG: {settings.DEBUG}")
    print(f"   - ALLOWED_HOSTS: {settings.ALLOWED_HOSTS[:3]}...")
    
    # Vérifier la base de données
    db_engine = settings.DATABASES['default']['ENGINE']
    print(f"   - DATABASE ENGINE: {db_engine}")
    
except Exception as e:
    print(f"   ❌ Erreur de configuration: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Vérifier les URLs
print("\n3. Vérification des URLs:")
try:
    from django.urls import get_resolver
    
    # Chercher spécifiquement l'URL /api/token/
    resolver = get_resolver()
    
    def find_url(pattern, url_patterns, prefix=''):
        for p in url_patterns:
            if hasattr(p, 'pattern'):
                current = prefix + str(p.pattern)
                if 'token' in current.lower():
                    return current
                if hasattr(p, 'url_patterns'):
                    result = find_url(pattern, p.url_patterns, current)
                    if result:
                        return result
        return None
    
    token_url = find_url('token', resolver.url_patterns)
    if token_url:
        print(f"   ✅ URL token trouvée: {token_url}")
    else:
        print("   ❌ URL /api/token/ non trouvée")
        
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# Test 4: Vérifier les fichiers critiques
print("\n4. Vérification des fichiers:")
files_to_check = [
    ('./mutuelle_core/urls.py', 'Fichier URLs principal'),
    ('./api/urls.py', 'Fichier URLs API'),
    ('./api/views.py', 'Vues API'),
    ('./mutuelle_core/settings.py', 'Configuration Django'),
]

for file_path, description in files_to_check:
    if os.path.exists(file_path):
        print(f"   ✅ {description}: {os.path.getsize(file_path)} octets")
        
        # Vérifier le contenu
        with open(file_path, 'r') as f:
            content = f.read()
            if 'HttpResponse' in file_path and 'from django.http import HttpResponse' not in content:
                print(f"      ⚠️  Import HttpResponse manquant")
            if 'api/urls.py' in file_path and 'TokenObtainPairView' not in content:
                print(f"      ⚠️  TokenObtainPairView non trouvé")
    else:
        print(f"   ❌ {description}: Fichier manquant")

print("\n" + "=" * 70)
print("📋 RECOMMANDATIONS:")
print("1. Vérifiez les logs Render pour l'erreur exacte")
print("2. Assurez-vous que les imports sont corrects dans urls.py")
print("3. Vérifiez que 'api' est dans INSTALLED_APPS")
print("4. Testez avec: python manage.py check --deploy")
