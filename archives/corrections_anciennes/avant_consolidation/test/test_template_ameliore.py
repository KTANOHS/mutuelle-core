import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    from django.test import Client
    from medecin.models import Medecin
    
    def test_template_ameliore():
        print("🧪 TEST AVEC TEMPLATE COMPLET")
        print("=" * 40)
        
        client = Client()
        
        # Connexion
        print("🔑 Connexion...")
        if not client.login(username='medecin_test', password='password123'):
            print("❌ Échec connexion")
            return
        
        print("✅ Connecté")
        
        # Test de la page
        print("\n🚀 Test page suivi chronique...")
        response = client.get('/medecin/suivi-chronique/')
        
        if response.status_code == 200:
            print("✅ Page accessible (status 200)")
            
            content = response.content.decode('utf-8')
            print(f"📏 Taille: {len(content)} caractères")
            
            # Vérifications du template complet
            checks = [
                ("Interface complète", len(content) > 5000),
                ("Cartes statistiques", "card border-left-primary" in content),
                ("Tableau", "table table-hover" in content),
                ("Boutons d'action", "btn btn-primary" in content),
                ("Icônes FontAwesome", "fas fa-" in content),
            ]
            
            print("\n🔍 Vérifications template complet:")
            for check_name, check_result in checks:
                status = "✅" if check_result else "⚠️"
                print(f"   {status} {check_name}")
            
            if all(check for _, check in checks):
                print("\n🎉 INTERFACE COMPLÈTE FONCTIONNELLE!")
            else:
                print("\n⚠️  Template chargé mais éléments manquants")
                
        else:
            print(f"❌ Erreur: Status {response.status_code}")
    
    test_template_ameliore()
    
except Exception as e:
    print(f"❌ ERREUR: {e}")