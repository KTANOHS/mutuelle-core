#!/bin/bash

echo "🧪 TEST FINAL SIMPLIFIÉ"
echo "======================"

# Vérifier la syntaxe d'abord
echo "🔍 Vérification syntaxe Python:"
python3 -m py_compile communication/views.py 2>&1 | head -20

if [ $? -eq 0 ]; then
    echo "✅ Syntaxe Python OK"
else
    echo "❌ Erreur de syntaxe"
    exit 1
fi

# Test rapide avec Django
python3 -c "
import sys
import os
sys.path.insert(0, '.')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    import django
    django.setup()
    
    print('✅ Django configuré')
    
    # Importer la vue pour vérifier
    from communication.views import envoyer_message_api
    print('✅ Vue envoyer_message_api importée')
    
    # Vérifier les décorateurs
    import inspect
    source = inspect.getsource(envoyer_message_api)
    
    if '@csrf_exempt' in source:
        print('✅ Décorateur @csrf_exempt présent')
    else:
        print('❌ Décorateur @csrf_exempt manquant')
    
    if '@login_required' in source:
        print('✅ Décorateur @login_required présent')
    else:
        print('❌ Décorateur @login_required manquant')
        
except Exception as e:
    print(f'❌ Erreur: {e}')
    import traceback
    traceback.print_exc()
"

# Test fonctionnel simple
echo ""
echo "🚀 Test fonctionnel:"
python3 -c "
import sys
import os
sys.path.insert(0, '.')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

from django.test import RequestFactory
from communication.views import envoyer_message_api
from django.contrib.auth.models import AnonymousUser, User

print('🧪 Test unitaire de la vue:')

try:
    # Créer une requête simulée
    factory = RequestFactory()
    
    # Test 1: Requête GET (devrait retourner erreur)
    print('1. Test GET:')
    request = factory.get('/communication/envoyer-message-api/')
    request.user = AnonymousUser()
    
    import json
    response = envoyer_message_api(request)
    print(f'   Status: {response.status_code}')
    print(f'   Content: {json.loads(response.content)}')
    
    # Test 2: Requête POST sans données
    print('\\n2. Test POST sans données:')
    request = factory.post('/communication/envoyer-message-api/')
    request.user = AnonymousUser()
    
    response = envoyer_message_api(request)
    print(f'   Status: {response.status_code}')
    
    # Test 3: Avec utilisateur authentifié
    print('\\n3. Test avec utilisateur:')
    user = User.objects.get(username='GLORIA1')
    request = factory.post('/communication/envoyer-message-api/', 
                          {'test': 'data'})
    request.user = user
    
    response = envoyer_message_api(request)
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        print(f'   Response: {json.loads(response.content)}')
    
    print('\\n✅ Tests unitaires terminés')
    
except Exception as e:
    print(f'❌ Erreur: {e}')
    import traceback
    traceback.print_exc()
"
