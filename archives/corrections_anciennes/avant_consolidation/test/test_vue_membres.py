# test_vue_membres.py
import os
import sys
import django
from django.test import RequestFactory

# Configuration Django
projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("="*70)
print("🧪 TEST DIRECT DE LA VUE liste_membres")
print("="*70)

# Créer une requête simulée
factory = RequestFactory()

# Créer un utilisateur de test
from django.contrib.auth.models import User
user = User.objects.create_user(username='testuser', password='testpass')

try:
    # Importer la vue
    from assureur.views import liste_membres
    
    print("✅ Vue importée avec succès")
    
    # Tester différentes requêtes
    tests = [
        ("Sans filtres", {}),
        ("Recherche 'ASIA'", {'q': 'ASIA'}),
        ("Filtre statut 'actif'", {'statut': 'actif'}),
        ("Combinaison", {'q': 'Jean', 'statut': 'en_retard'}),
    ]
    
    for test_name, params in tests:
        print(f"\n🔍 Test: {test_name}")
        print(f"   Paramètres: {params}")
        
        # Créer la requête
        request = factory.get('/assureur/membres/', params)
        request.user = user
        
        # Ajouter la session
        from django.contrib.sessions.middleware import SessionMiddleware
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        
        # Exécuter la vue
        response = liste_membres(request)
        
        print(f"   Status code: {response.status_code}")
        
        if hasattr(response, 'context_data'):
            context = response.context_data
            print(f"   Nombre de membres: {context.get('page_obj', {}).paginator.count if hasattr(context.get('page_obj', {}), 'paginator') else 'N/A'}")
            print(f"   Filtres appliqués: {context.get('filters', {})}")
        else:
            print("   Aucun contexte retourné")
            
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)