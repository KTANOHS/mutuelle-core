import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    from django.test import RequestFactory
    from django.contrib.sessions.middleware import SessionMiddleware
    from django.contrib.auth.models import User
    from membres.models import Medecin
    from medecin.views import tableau_de_bord_medecin
    
    def diagnostic_corrige():
        print("🔍 DIAGNOSTIC TEMPLATE CORRIGÉ:")
        print("=" * 50)
        
        # Créer une requête simulée
        factory = RequestFactory()
        request = factory.get('/medecin/tableau-de-bord/')
        
        # Ajouter la session
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        
        # Créer et connecter un médecin de test
        try:
            user = User.objects.get(username='medecin_test')
        except User.DoesNotExist:
            user = User.objects.create_user('medecin_test', 'medecin@test.com', 'password123')
            user.save()
        
        try:
            medecin = Medecin.objects.get(user=user)
        except Medecin.DoesNotExist:
            medecin = Medecin.objects.create(
                user=user,
                nom="Docteur Test",
                prenom="Jean",
                specialite="Generaliste"
            )
        
        request.user = user
        
        # Appeler la vue
        response = tableau_de_bord_medecin(request)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 302:  # Redirection
            print(f"🔀 REDIRECTION DÉTECTÉE vers: {response.url}")
            print("📋 Raisons possibles:")
            print("   - Utilisateur non connecté")
            print("   - Utilisateur n'est pas médecin") 
            print("   - Décorateur de permission redirige")
            print("   - Session manquante")
        elif response.status_code == 200:
            print("✅ Template affiché avec succès")
            if hasattr(response, 'template_name'):
                print(f"Template utilisé: {response.template_name}")
        else:
            print(f"❌ Status inattendu: {response.status_code}")
            
    diagnostic_corrige()
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()