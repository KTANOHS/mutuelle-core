import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    from django.test import Client
    from medecin.models import Medecin
    
    def test_template_suivi():
        print("🧪 TEST DU TEMPLATE SUIVI CHRONIQUE")
        print("=" * 40)
        
        client = Client()
        
        # Vérifier médecin
        try:
            medecin = Medecin.objects.get(user__username='medecin_test')
            print(f"✅ Médecin: Dr {medecin.user.first_name} {medecin.user.last_name}")
        except Medecin.DoesNotExist:
            print("❌ Médecin non trouvé")
            return
        
        # Connexion
        print("🔑 Connexion...")
        if not client.login(username='medecin_test', password='password123'):
            print("❌ Échec connexion")
            return
        print("✅ Connecté")
        
        # Test de la page suivi chronique
        print("\n🚀 Test page suivi chronique...")
        response = client.get('/medecin/suivi-chronique/')
        
        if response.status_code == 200:
            print("✅ Page accessible (status 200)")
            
            # Vérifier le contenu
            content = response.content.decode('utf-8')
            
            # Vérifications importantes
            checks = [
                ('Structure HTML', '<html' in content.lower() or '<!DOCTYPE' in content.lower()),
                ('Titre', 'suivi' in content.lower() or 'chronique' in content.lower()),
                ('Développement', 'développement' in content.lower() or 'development' in content.lower()),
                ('Bouton retour', 'tableau de bord' in content.lower() or 'dashboard' in content.lower())
            ]
            
            print("📊 Vérifications du contenu:")
            for check_name, check_result in checks:
                status = "✅" if check_result else "⚠️"
                print(f"   {status} {check_name}")
            
            print(f"📏 Taille de la page: {len(content)} caractères")
            
        elif response.status_code == 302:
            print(f"🔀 Redirection vers: {response.url}")
        else:
            print(f"❌ Erreur: Status {response.status_code}")
        
        print("\n🎯 TEST TERMINÉ!")
    
    test_template_suivi()
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()