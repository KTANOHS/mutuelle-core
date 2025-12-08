import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    from django.test import Client
    from django.contrib.auth.models import User
    from medecin.models import Medecin
    
    def test_connexion_medecin_corrige():
        print("🔐 TEST CONNEXION MÉDECIN (CORRIGÉ):")
        print("=" * 50)
        
        client = Client()
        
        # 1. Vérifier/Créer le médecin de test
        print("1. 🔍 Vérification médecin de test...")
        try:
            user = User.objects.get(username='medecin_test')
            print("   ✅ Utilisateur medecin_test trouvé")
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='medecin_test',
                email='medecin@test.com',
                password='password123'
            )
            print("   ✅ Utilisateur medecin_test créé")
        
        try:
            medecin = Medecin.objects.get(user=user)
            print(f"   ✅ Médecin trouvé: {medecin}")
        except Medecin.DoesNotExist:
            medecin = Medecin.objects.create(
                user=user,
                nom="Test",
                prenom="Docteur",
                specialite="Généraliste"
            )
            print("   ✅ Profil médecin créé")
        
        # 2. Essayer d'accéder sans connexion
        print("\n2. 🔒 Accès sans connexion...")
        response = client.get('/medecin/tableau-de-bord/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 302:
            print(f"   🔀 Redirection vers: {response.url}")
        elif response.status_code == 404:
            print("   ❌ Page non trouvé - Vérifiez les URLs")
        elif response.status_code == 200:
            print("   ✅ Accès direct possible (inattendu)")
        
        # 3. Se connecter
        print("\n3. 🔑 Connexion...")
        login_success = client.login(username='medecin_test', password='password123')
        print(f"   Login réussi: {login_success}")
        
        if login_success:
            # 4. Accéder après connexion
            print("\n4. 🚀 Accès après connexion...")
            
            # Tester différentes URLs possibles
            urls_a_tester = [
                '/medecin/tableau-de-bord/',
                '/medecin/dashboard/',
                '/medecin/',
                '/medecin'
            ]
            
            for url in urls_a_tester:
                print(f"   Testing: {url}")
                response = client.get(url)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    print("   ✅ SUCCÈS - Template affiché!")
                    print(f"   Content-Type: {response.get('Content-Type', 'Non spécifié')}")
                    print(f"   Taille: {len(response.content)} bytes")
                    break
                elif response.status_code == 302:
                    print(f"   🔀 Redirection vers: {response.url}")
                elif response.status_code == 404:
                    print("   ❌ Page non trouvée")
                else:
                    print(f"   ❌ Status inattendu: {response.status_code}")
        
        else:
            print("   ❌ Échec de la connexion")
            
    test_connexion_medecin_corrige()
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()