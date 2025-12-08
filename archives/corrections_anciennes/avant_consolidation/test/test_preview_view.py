# test_preview_view.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import RequestFactory
from assureur.views import preview_generation
from django.contrib.auth.models import User

# Créer une requête simulée
factory = RequestFactory()

# Créer un utilisateur de test (simplifié)
user, _ = User.objects.get_or_create(
    username='view_test_user',
    defaults={'is_staff': True}
)
user.set_password('test123')
user.save()

# Tester la vue
try:
    request = factory.get('/preview/', {'periode': '2024-12'})
    request.user = user
    
    response = preview_generation(request)
    print(f"Status: {response.status_code}")
    print(f"Content type: {response['Content-Type'] if 'Content-Type' in response else 'N/A'}")
    
except Exception as e:
    print(f"Erreur: {e}")
    import traceback
    traceback.print_exc()