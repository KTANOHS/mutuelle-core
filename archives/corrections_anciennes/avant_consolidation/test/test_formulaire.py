# test_formulaire.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

try:
    django.setup()
    
    from django.test import RequestFactory
    from django.contrib.auth.models import User
    from agents.views import creer_bon_soin_membre
    from membres.models import Membre
    
    def test_formulaire_bon_soin():
        print("📝 TEST DU FORMULAIRE DE BON DE SOIN")
        print("-" * 50)
        
        # Créer une requête POST simulée
        factory = RequestFactory()
        
        # Récupérer un membre de test
        membre = Membre.objects.first()
        if not membre:
            print("❌ Aucun membre disponible pour le test")
            return
            
        print(f"✅ Membre de test: {membre.prenom} {membre.nom} (ID: {membre.id})")
        
        # Créer un utilisateur de test
        user, created = User.objects.get_or_create(
            username='test_agent',
            defaults={'is_staff': True, 'is_active': True}
        )
        
        # Données du formulaire
        form_data = {
            'type_soin': 'consultation',
            'montant': '150.75',
            'symptomes': 'Fièvre et maux de tête',
            'diagnostic': 'Grippe',
            'description': 'Consultation générale'
        }
        
        # Créer la requête POST
        request = factory.post(f'/agents/creer-bon-soin/{membre.id}/', form_data)
        request.user = user
        
        print("🧪 Simulation de la requête POST...")
        
        try:
            # Appeler la vue
            response = creer_bon_soin_membre(request, membre.id)
            print(f"✅ Vue exécutée - Statut: {getattr(response, 'status_code', 'Redirection')}")
            
            # Analyser la réponse
            if hasattr(response, 'url'):
                print(f"   Redirection vers: {response.url}")
            else:
                print(f"   Type de réponse: {type(response)}")
                
        except Exception as e:
            print(f"❌ ERREUR dans la vue: {e}")
            print(f"   Type: {type(e).__name__}")
            
    test_formulaire_bon_soin()
    
except Exception as e:
    print(f"❌ ERREUR: {e}")