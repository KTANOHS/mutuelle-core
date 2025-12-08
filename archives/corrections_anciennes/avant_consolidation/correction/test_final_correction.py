import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    from django.test import Client
    from medecin.models import Medecin
    
    def test_final_correction():
        print("🎯 TEST FINAL APRÈS CORRECTION")
        print("=" * 50)
        
        client = Client()
        
        # Connexion
        print("🔑 Connexion...")
        if not client.login(username='medecin_test', password='password123'):
            print("❌ Échec connexion")
            return
        
        print("✅ Connecté")
        
        # Test de la page suivi chronique
        print("\n🚀 Test page suivi chronique...")
        response = client.get('/medecin/suivi-chronique/')
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 SUCCÈS - Page accessible sans erreur!")
            
            content = response.content.decode('utf-8')
            print(f"📏 Taille: {len(content)} caractères")
            
            # Vérifications critiques
            checks = [
                ("Pas d'erreur template", "TemplateDoesNotExist" not in content),
                ("Interface complète", len(content) > 1000),
                ("Titre correct", "Suivi des Maladies Chroniques" in content),
                ("Navigation", "Tableau de Bord" in content),
                ("Cartes statistiques", "card border-left-primary" in content),
            ]
            
            print("\n🔍 Vérifications détaillées:")
            success_count = 0
            for check_name, check_result in checks:
                status = "✅" if check_result else "❌"
                print(f"   {status} {check_name}")
                if check_result:
                    success_count += 1
            
            if success_count == len(checks):
                print("\n✨ TOUT FONCTIONNE PARFAITEMENT!")
            else:
                print(f"\n⚠️  {success_count}/{len(checks)} vérifications passées")
                
        elif response.status_code == 302:
            print(f"🔀 Redirection vers: {response.url}")
        else:
            print(f"❌ Erreur: Status {response.status_code}")
    
    test_final_correction()
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()