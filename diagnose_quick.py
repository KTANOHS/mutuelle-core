#!/usr/bin/env python
# diagnose_quick.py
import os
import sys

def quick_check():
    print("🔍 DIAGNOSTIC RAPIDE RAILWAY")
    
    # 1. Vérifier Django
    try:
        import django
        print(f"✅ Django {django.get_version()}")
    except:
        print("❌ Django non installé")
        return False
    
    # 2. Vérifier settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    try:
        from django.conf import settings
        print(f"✅ Settings chargés (DEBUG={settings.DEBUG})")
    except Exception as e:
        print(f"❌ Erreur settings: {e}")
        return False
    
    # 3. Vérifier API
    try:
        from api import views
        print("✅ api.views importé")
    except Exception as e:
        print(f"❌ Erreur api.views: {e}")
        return False
    
    # 4. Vérifier URLs
    try:
        from api import urls
        print(f"✅ api.urls importé ({len(urls.urlpatterns)} URLs)")
    except Exception as e:
        print(f"❌ Erreur api.urls: {e}")
        return False
    
    # 5. Vérifier base de données
    try:
        from django.db import connection
        with connection.cursor() as c:
            c.execute("SELECT 1")
        print("✅ Base de données connectée")
    except Exception as e:
        print(f"⚠️  Base de données: {e}")
    
    return True

if __name__ == "__main__":
    if quick_check():
        print("\n✅ Application prête pour Railway!")
        
        # Tester l'URL de santé
        try:
            from api.views import api_health
            from django.test import RequestFactory
            factory = RequestFactory()
            request = factory.get('/api/health/')
            response = api_health(request)
            print(f"✅ API health: {response.status_code}")
        except:
            print("⚠️  API health non testable")
    else:
        print("\n❌ Corrections nécessaires avant Railway")