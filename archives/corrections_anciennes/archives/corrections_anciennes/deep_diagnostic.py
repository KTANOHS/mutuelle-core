# deep_diagnostic.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.core.handlers.base import BaseHandler
from django.core.handlers.wsgi import WSGIRequest
from io import StringIO
import sys

def deep_diagnostic():
    print("🔍 DIAGNOSTIC PROFOND")
    print("=" * 50)
    
    # 1. Vérifier la résolution d'URL
    print("\n🔗 Vérification URL:")
    try:
        match = resolve('/medecin/ordonnances/nouvelle/')
        print(f"   Vue: {match.func.__name__}")
        print(f"   App: {match.app_name}")
        print(f"   Namespace: {match.namespace}")
    except Exception as e:
        print(f"   ❌ Erreur résolution: {e}")
    
    # 2. Vérifier la vue directement
    print("\n👁️ Vérification vue:")
    try:
        from medecin.views import creer_ordonnance
        print("   ✅ Vue importable")
        
        # Créer une requête simulée
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/medecin/ordonnances/nouvelle/')
        request.user = User.objects.get(username='test_medecin')
        
        # Essayer d'appeler la vue
        response = creer_ordonnance(request)
        print(f"   ✅ Vue exécutable - Statut: {response.status_code}")
        
    except Exception as e:
        print(f"   ❌ Erreur vue: {e}")
        import traceback
        traceback.print_exc()
    
    # 3. Vérifier le contexte
    print("\n📋 Vérification contexte:")
    try:
        client = Client()
        user = User.objects.get(username='test_medecin')
        client.force_login(user)
        
        response = client.get(reverse('medecin:creer_ordonnance'))
        
        if hasattr(response, 'context'):
            print("   ✅ Contexte disponible")
            if 'medecin' in response.context:
                print("   ✅ Medecin dans contexte")
            if 'patients' in response.context:
                print(f"   ✅ Patients dans contexte: {len(response.context['patients'])}")
        else:
            print("   ❌ Pas de contexte")
            
    except Exception as e:
        print(f"   ❌ Erreur contexte: {e}")

if __name__ == "__main__":
    deep_diagnostic()