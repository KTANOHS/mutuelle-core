# test_membres_view.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import RequestFactory
from assureur.views import liste_membres
from django.contrib.auth.models import User

# Créer une requête simulée
factory = RequestFactory()

# Créer un utilisateur de test
user = User.objects.create_user(username='testuser', password='testpass')
user.save()

# Créer une requête GET avec des paramètres
request = factory.get('/assureur/membres/', {'q': 'test', 'statut': 'actif'})
request.user = user

# Exécuter la vue
try:
    response = liste_membres(request)
    print("✅ Vue exécutée avec succès")
    print(f"Status code: {response.status_code}")
    
    # Vérifier le contexte
    if hasattr(response, 'context_data'):
        print(f"Nombre de membres: {len(response.context_data.get('page_obj', []))}")
        print(f"Filtres appliqués: {response.context_data.get('filters', {})}")
    else:
        print("Aucun contexte retourné")
        
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()