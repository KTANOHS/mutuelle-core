# intercepteur_erreur.py
import os
import sys
import django
import logging

# Configuration du logging détaillé
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('debug_intercept')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

def tester_creation_bon_soin_avec_logging():
    """Test avec logging détaillé pour intercepter l'erreur"""
    print("🔍 INTERCEPTION DÉTAILLÉE DE L'ERREUR")
    print("=" * 60)
    
    try:
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        from membres.models import Membre
        from soins.models import BonDeSoin
        from agents.views import creer_bon_soin_membre
        from datetime import date
        
        # 1. Préparer les données
        user = User.objects.get(username='koffitanoh')
        membre = Membre.objects.first()
        
        print(f"👤 Utilisateur: {user.username}")
        print(f"📋 Membre: {membre.prenom} {membre.nom} (ID: {membre.id})")
        
        # 2. Créer une requête POST simulée
        factory = RequestFactory()
        request = factory.post(f'/agents/creer-bon-soin/{membre.id}/', {
            'type_soin': 'consultation',
            'montant': '150.75',
            'symptomes': 'Fièvre et toux persistante',
            'diagnostic': 'Infection respiratoire',
            'description': 'Consultation générale avec ordonnance'
        })
        request.user = user
        
        # Ajouter la session (nécessaire pour les messages)
        from django.contrib.sessions.middleware import SessionMiddleware
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        
        # 3. Exécuter la vue avec interception détaillée
        print("🧪 Exécution de la vue creer_bon_soin_membre...")
        
        try:
            response = creer_bon_soin_membre(request, membre.id)
            print(f"✅ RÉUSSITE - Statut: {getattr(response, 'status_code', 'Redirection')}")
            if hasattr(response, 'url'):
                print(f"   Redirection vers: {response.url}")
            return response
                
        except Exception as e:
            print(f"❌ ERREUR DANS LA VUE: {e}")
            print(f"   Type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return None
            
    except Exception as e:
        print(f"❌ ERREUR GÉNÉRALE: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    tester_creation_bon_soin_avec_logging()