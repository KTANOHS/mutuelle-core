#!/usr/bin/env python
import os
import sys
import django

# Configure Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.urls import get_resolver

print("🔍 Diagnostic de l'API MaSante Directe")
print("=" * 50)

# Vérifier les URLs
resolver = get_resolver()
url_patterns = resolver.url_patterns

print("\n1. URLs principales disponibles:")
for pattern in url_patterns:
    if hasattr(pattern, 'pattern'):
        print(f"   - {pattern.pattern}")

# Vérifier l'application API
print("\n2. Vérification de l'application 'api':")
try:
    from api import urls
    print("   ✅ Application 'api' trouvée")
    
    # Vérifier les patterns de l'API
    print("\n3. Patterns dans api.urls:")
    for pattern in urls.urlpatterns:
        if hasattr(pattern, 'pattern'):
            print(f"   - {pattern.pattern}")
except ImportError as e:
    print(f"   ❌ Erreur: {e}")
    print("   L'application 'api' n'est pas trouvée ou configurée")

# Vérifier les dépendances
print("\n4. Vérification des dépendances:")
try:
    import rest_framework
    print("   ✅ Django REST Framework installé")
except ImportError:
    print("   ❌ Django REST Framework non installé")

try:
    import rest_framework_simplejwt
    print("   ✅ Simple JWT installé")
except ImportError:
    print("   ❌ Simple JWT non installé")

print("\n" + "=" * 50)
print("📋 Recommandations:")

# Vérifier si l'API est dans les URLs
api_included = any('api/' in str(p.pattern) for p in url_patterns if hasattr(p, 'pattern'))
if not api_included:
    print("1. ❌ L'API n'est pas incluse dans les URLs principales")
    print("   Ajoutez: path('api/', include('api.urls')) dans mutuelle_core/urls.py")
else:
    print("1. ✅ L'API est incluse dans les URLs")

# Vérifier l'application dans INSTALLED_APPS
from django.conf import settings
if 'api' in settings.INSTALLED_APPS:
    print("2. ✅ Application 'api' dans INSTALLED_APPS")
else:
    print("2. ❌ Application 'api' absente de INSTALLED_APPS")
    print("   Ajoutez 'api' à INSTALLED_APPS dans settings.py")

print("\n🚀 Pour tester après correction:")
print("   curl http://127.0.0.1:8000/api/")
print("   curl http://127.0.0.1:8000/api/health/")
print('   curl -X POST http://127.0.0.1:8000/api/token/ \\')
print('     -H "Content-Type: application/json" \\')
print('     -d \'{"username":"admin","password":"Admin123!"}\'')
