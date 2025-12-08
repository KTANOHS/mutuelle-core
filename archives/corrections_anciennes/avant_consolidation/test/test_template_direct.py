import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    from django.test import Client
    from django.contrib.auth.models import User
    
    def test_connexion_medecin():
        print("🔐 TEST CONNEXION MÉDECIN:")
        print("=" * 40)
        
        client = Client()
        
        # 1. Essayer d'accéder sans connexion
        print("1. Accès sans connexion...")
        response = client.get('/medecin/tableau-de-bord/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 302:
            print(f"   Redirection vers: {response.url}")
        
        # 2. Se connecter
        print("2. Connexion...")
        user = User.objects.get(username='medecin_test')
        login_success = client.login(username='medecin_test', password='password123')
        print(f"   Login réussi: {login_success}")
        
        if login_success:
            # 3. Accéder après connexion
            print("3. Accès après connexion...")
            response = client.get('/medecin/tableau-de-bord/')
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ SUCCÈS - Template affiché")
                print(f"   Content-Type: {response.get('Content-Type', 'Non spécifié')}")
                print(f"   Taille du contenu: {len(response.content)} bytes")
            else:
                print(f"   ❌ Échec - Status: {response.status_code}")
                if response.status_code == 302:
                    print(f"   Redirection vers: {response.url}")
        
    test_connexion_medecin()
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()