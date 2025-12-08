import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')

import django
django.setup()

from django.test import RequestFactory
from assureur.views import generer_cotisations
from django.contrib.auth.models import User

print("=== TEST DIRECT DE LA VUE ===")

# Créer une requête simulée
factory = RequestFactory()

# Créer un utilisateur test
user = User.objects.create_user('quick_test', 'test@test.com', 'test123')
user.is_staff = True
user.save()

# Tester la vue
try:
    request = factory.get('/assureur/cotisations/generer/')
    request.user = user
    
    response = generer_cotisations(request)
    print(f"Status: {response.status_code}")
    print(f"Template utilisé: {getattr(response, 'template_name', 'Non défini')}")
    
    if response.status_code == 200:
        print("✅ Vue fonctionne correctement")
    else:
        print(f"❌ Erreur: {response.status_code}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()
