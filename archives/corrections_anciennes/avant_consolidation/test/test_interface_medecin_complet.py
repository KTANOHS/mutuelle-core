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
    
    def test_interface_medecin_complet():
        print("🎯 TEST COMPLET INTERFACE MÉDECIN")
        print("=" * 50)
        
        client = Client()
        
        # 1. Vérifier que le médecin existe
        print("1. 🔍 Vérification médecin...")
        try:
            user = User.objects.get(username='medecin_test')
            medecin = Medecin.objects.get(user=user)
            print(f"   ✅ Médecin prêt: Dr {medecin.prenom} {medecin.nom}")
        except (User.DoesNotExist, Medecin.DoesNotExist):
            print("   ❌ Médecin de test non trouvé")
            print("   📋 Exécutez d'abord: python creer_medecin_corrige.py")
            return
        
        # 2. Test sans connexion (doit rediriger vers login)
        print("\n2. 🔒 Test accès sans connexion...")
        urls_sans_connexion = [
            '/medecin/dashboard/',
            '/medecin/bons/',
            '/medecin/ordonnances/'
        ]
        
        for url in urls_sans_connexion:
            response = client.get(url)
            status_icon = "✅" if response.status_code == 302 else "❌"
            print(f"   {status_icon} {url} -> Status: {response.status_code}", end="")
            if response.status_code == 302:
                print(f" (Redirection vers: {response.url})")
            else:
                print()
        
        # 3. Connexion
        print("\n3. 🔑 Connexion...")
        login_success = client.login(username='medecin_test', password='password123')
        print(f"   ✅ Connexion réussie: {login_success}")
        
        if not login_success:
            print("   ❌ Échec de connexion - vérifiez le mot de passe")
            return
        
        # 4. Test avec connexion
        print("\n4. 🚀 Test accès après connexion...")
        urls_avec_connexion = [
            ('/medecin/dashboard/', 'Tableau de bord'),
            ('/medecin/', 'Accueil (redirection)'),
            ('/medecin/bons/', 'Liste des bons'),
            ('/medecin/ordonnances/', 'Mes ordonnances'),
            ('/medecin/profil/', 'Profil médecin'),
            ('/medecin/statistiques/', 'Statistiques'),
        ]
        
        for url, description in urls_avec_connexion:
            response = client.get(url)
            if response.status_code == 200:
                status_icon = "✅"
                details = f" - Template chargé"
            elif response.status_code == 302:
                status_icon = "🔀"
                details = f" - Redirection vers: {response.url}"
            else:
                status_icon = "❌"
                details = f" - Status inattendu"
            
            print(f"   {status_icon} {description} ({url}) -> Status: {response.status_code}{details}")
        
        # 5. Test des fonctionnalités principales
        print("\n5. 📊 Test fonctionnalités...")
        
        # Dashboard
        response = client.get('/medecin/dashboard/')
        if response.status_code == 200:
            print("   ✅ Dashboard accessible")
            # Vérifier le contexte
            if hasattr(response, 'context') and response.context:
                print("   ✅ Contexte disponible")
            else:
                print("   ℹ️  Aucun contexte disponible")
        else:
            print(f"   ❌ Dashboard inaccessible: {response.status_code}")
        
        # Liste des bons
        response = client.get('/medecin/bons/')
        if response.status_code == 200:
            print("   ✅ Liste des bons accessible")
        else:
            print(f"   ❌ Liste des bons inaccessible: {response.status_code}")
        
        # Ordonnances
        response = client.get('/medecin/ordonnances/')
        if response.status_code == 200:
            print("   ✅ Ordonnances accessible")
        else:
            print(f"   ❌ Ordonnances inaccessible: {response.status_code}")
        
        print("\n🎉 TEST TERMINÉ!")
        
    test_interface_medecin_complet()
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()