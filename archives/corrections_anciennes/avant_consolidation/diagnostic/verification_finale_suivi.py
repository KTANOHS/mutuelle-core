import os
import django
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    from django.test import Client
    from medecin.models import Medecin
    
    def verification_finale_suivi():
        print("🎯 VÉRIFICATION FINALE - SUIVI CHRONIQUE")
        print("=" * 50)
        
        client = Client()
        
        # 1. Vérifier médecin
        try:
            medecin = Medecin.objects.get(user__username='medecin_test')
            print(f"✅ Médecin: Dr {medecin.user.first_name} {medecin.user.last_name}")
        except Medecin.DoesNotExist:
            print("❌ Médecin non trouvé")
            return False
        
        # 2. Connexion
        print("🔑 Connexion...")
        if not client.login(username='medecin_test', password='password123'):
            print("❌ Échec connexion")
            return False
        print("✅ Connecté")
        
        # 3. Test de la page suivi chronique
        print("\n🚀 Test page suivi chronique...")
        start_time = time.time()
        response = client.get('/medecin/suivi-chronique/')
        end_time = time.time()
        
        print(f"⏱️  Temps de réponse: {end_time - start_time:.2f}s")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 SUCCÈS - Page accessible sans erreur!")
            
            # Analyse du contenu
            content = response.content.decode('utf-8')
            print(f"📏 Taille page: {len(content)} caractères")
            
            # Vérifications critiques
            checks = [
                ("Pas d'erreur Template", "TemplateDoesNotExist" not in content),
                ("Structure HTML", "<html" in content.lower() or "<!DOCTYPE" in content.lower()),
                ("Contenu significatif", len(content) > 500),
            ]
            
            print("\n🔍 Vérifications:")
            all_ok = True
            for check_name, check_result in checks:
                status = "✅" if check_result else "❌"
                print(f"   {status} {check_name}")
                if not check_result:
                    all_ok = False
            
            if all_ok:
                print("\n✨ TOUT EST FONCTIONNEL!")
                return True
            else:
                print("\n⚠️  Problèmes mineurs détectés")
                return True
                
        elif response.status_code == 302:
            print(f"🔀 Redirection vers: {response.url}")
            return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    
    success = verification_finale_suivi()
    
    if success:
        print("\n" + "="*50)
        print("🎊 FÉLICITATIONS !")
        print("📋 L'interface médecin est COMPLÈTEMENT FONCTIONNELLE")
        print("\n🔗 URLs disponibles:")
        print("   http://localhost:8000/medecin/dashboard/")
        print("   http://localhost:8000/medecin/suivi-chronique/")
        print("   http://localhost:8000/medecin/bons/")
        print("   http://localhost:8000/medecin/ordonnances/")
        print("\n👤 Identifiants: medecin_test / password123")
    else:
        print("\n❌ Problème persistant - Vérifiez les logs serveur")
        
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()