# debug_vue_ordonnance.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from medecin.views import creer_ordonnance
from django.test import RequestFactory
from django.contrib.auth.models import User
import json

def debug_vue():
    print("🐛 DEBUG VUE creer_ordonnance")
    print("=" * 40)
    
    factory = RequestFactory()
    user = User.objects.get(username='test_medecin')
    
    # Créer une requête POST simulée
    request = factory.post('/medecin/ordonnances/nouvelle/', {
        'patient': '1',
        'type_ordonnance': 'STANDARD',
        'diagnostic': 'Test debug',
        'medicaments': json.dumps([{'nom': 'Test', 'posologie': '1x', 'duree': '1j'}]),
    })
    request.user = user
    
    try:
        response = creer_ordonnance(request)
        print(f"✅ Vue exécutée - Statut: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Erreur dans la vue: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_vue()