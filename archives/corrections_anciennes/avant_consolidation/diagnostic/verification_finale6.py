# verification_finale.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_finale():
    """Vérification finale que la messagerie fonctionne"""
    
    print("🎯 VÉRIFICATION FINALE")
    print("=" * 50)
    
    from django.test import Client
    from django.contrib.auth.models import User
    
    try:
        # Tester avec assureur_test qui a des conversations
        user = User.objects.get(username='assureur_test')
        client = Client()
        client.force_login(user)
        
        # Tester la messagerie principale
        response = client.get('/communication/')
        content = response.content.decode('utf-8')
        
        print(f"📊 Statut: {response.status_code}")
        
        # Vérifications critiques
        checks = {
            'Conversation 4': 'Conversation #4' in content,
            'koffitanoh': 'koffitanoh' in content,
            'assureur_test': 'assureur_test' in content,
            'Messages: 2': 'Messages: 2' in content,
            'Dernière activité': 'Dernière activité' in content
        }
        
        print("\n✅ VÉRIFICATIONS:")
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"   {status} {check}: {'TROUVÉ' if result else 'NON TROUVÉ'}")
        
        if all(checks.values()):
            print("\n🎉 SUCCÈS TOTAL ! La messagerie fonctionne parfaitement.")
            print("🌐 L'URL http://127.0.0.1:8000/communication/ affiche maintenant les conversations")
        else:
            print("\n⚠️  Il reste des problèmes d'affichage")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    verification_finale()