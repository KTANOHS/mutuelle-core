import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    from django.test import Client
    from medecin.models import Medecin
    
    def test_interface_complet():
        print("🎯 TEST COMPLET INTERFACE MÉDECIN")
        print("=" * 50)
        
        client = Client()
        
        # Vérifier que le médecin existe
        try:
            medecin = Medecin.objects.get(user__username='medecin_test')
            print(f"✅ Médecin de test trouvé: Dr {medecin.user.first_name} {medecin.user.last_name}")
        except Medecin.DoesNotExist:
            print("❌ Médecin de test non trouvé")
            print("📋 Exécutez d'abord: python creer_medecin_exact.py")
            return
        
        # URLs principales à tester (basées sur medecin/urls.py)
        urls_principales = [
            ('/medecin/dashboard/', 'Dashboard principal'),
            ('/medecin/', 'Accueil (redirection)'),
            ('/medecin/bons/', 'Liste des bons'),
            ('/medecin/bons/attente/', 'Bons en attente'),
            ('/medecin/ordonnances/', 'Mes ordonnances'),
            ('/medecin/profil/', 'Profil médecin'),
            ('/medecin/statistiques/', 'Statistiques'),
        ]
        
        print("\n1. 🔐 TESTS SANS CONNEXION (redirections attendues):")
        for url, description in urls_principales[:3]:  # Tester seulement 3 URLs
            response = client.get(url)
            if response.status_code == 302:
                print(f"   ✅ {description}: Redirection vers → {response.url}")
            else:
                print(f"   ❌ {description}: Status {response.status_code} (attendu: 302)")
        
        print("\n2. 🔑 CONNEXION AU COMPTE MÉDECIN...")
        login_success = client.login(username='medecin_test', password='password123')
        print(f"   ✅ Connexion réussie: {login_success}")
        
        if not login_success:
            print("   ❌ Échec de la connexion")
            return
        
        print("\n3. 🚀 TESTS AVEC CONNEXION:")
        results = []
        
        for url, description in urls_principales:
            response = client.get(url)
            
            if response.status_code == 200:
                status = "✅"
                details = "Page chargée"
                # Vérifier le contenu basique
                content = response.content.decode('utf-8')
                if len(content) > 100:  # Contenu significatif
                    details += " (contenu OK)"
                else:
                    details += " (contenu court)"
                    
            elif response.status_code == 302:
                status = "🔀"
                details = f"Redirection → {response.url}"
            else:
                status = "❌"
                details = f"Status {response.status_code}"
            
            results.append((status, description, url, details))
            print(f"   {status} {description}: {details}")
        
        print("\n4. 📊 RÉSUMÉ DES TESTS:")
        success_count = sum(1 for r in results if r[0] == "✅")
        redirect_count = sum(1 for r in results if r[0] == "🔀")
        error_count = sum(1 for r in results if r[0] == "❌")
        
        print(f"   ✅ Pages chargées: {success_count}")
        print(f"   🔀 Redirections: {redirect_count}")
        print(f"   ❌ Erreurs: {error_count}")
        
        # Test spécifique du dashboard
        print("\n5. 🎯 TEST DÉTAILLÉ DU DASHBOARD:")
        response = client.get('/medecin/dashboard/')
        if response.status_code == 200:
            print("   ✅ Dashboard accessible")
            
            # Vérifier le contexte
            if hasattr(response, 'context'):
                context_keys = list(response.context.keys()) if response.context else []
                print(f"   📋 Contexte disponible: {len(context_keys)} variables")
                if context_keys:
                    print(f"   🔑 Clés du contexte: {', '.join(context_keys[:5])}...")
            else:
                print("   ℹ️  Aucun contexte disponible")
                
            # Vérifier le contenu HTML
            content = response.content.decode('utf-8')
            if '<html' in content.lower() or '<body' in content.lower():
                print("   🌐 Structure HTML détectée")
            if 'medecin' in content.lower() or 'dashboard' in content.lower():
                print("   📝 Contenu pertinent détecté")
                
        else:
            print(f"   ❌ Dashboard inaccessible: {response.status_code}")
        
        print("\n🎉 TEST TERMINÉ!")
        
        # Vérifier si au moins 3 pages principales fonctionnent
        if success_count >= 3:
            print("✨ INTERFACE MÉDECIN FONCTIONNELLE!")
        else:
            print("⚠️  Problèmes détectés, vérification nécessaire")
    
    test_interface_complet()
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()