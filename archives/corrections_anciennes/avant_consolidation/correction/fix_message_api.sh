#!/bin/bash

echo "🔧 CORRECTION API ENVOI MESSAGE"
echo "================================"

# Vérifier la vue envoyer_message_api dans views.py
echo "🔍 Analyse de la vue envoyer_message_api:"
grep -n -A 20 "def envoyer_message_api" communication/views.py | head -30

# Vérifier si le décorateur csrf_exempt est présent
if ! grep -q "@csrf_exempt" communication/views.py; then
    echo "⚠️  Décorateur @csrf_exempt manquant, ajout..."
    
    # Trouver la ligne de la fonction
    LINE=$(grep -n "def envoyer_message_api" communication/views.py | cut -d: -f1)
    
    if [ -n "$LINE" ]; then
        # Ajouter l'import et le décorateur
        sed -i '' "${LINE}i\\
from django.views.decorators.csrf import csrf_exempt\\
\\
@csrf_exempt" communication/views.py
        
        echo "✅ Décorateur @csrf_exempt ajouté"
    fi
else
    echo "✅ Décorateur @csrf_exempt déjà présent"
fi

# Vérifier aussi la fonction dans le fichier
echo ""
echo "📝 Vérification de la fonction:"
python -c "
import sys
sys.path.insert(0, '.')
import inspect
from communication.views import envoyer_message_api

print('Signature:')
print(inspect.signature(envoyer_message_api))
print('\\nSource (extrait):')
print(inspect.getsource(envoyer_message_api)[:500])
"

# Test après correction
echo ""
echo "🧪 Test après correction:"
python -c "
import sys
import os
import json
sys.path.insert(0, '.')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User

print('Test API simplifié:')

client = Client()

try:
    user = User.objects.get(username='GLORIA1')
    client.force_login(user)
    
    other_user = User.objects.exclude(username='GLORIA1').first()
    
    # Test avec @csrf_exempt
    response = client.post('/communication/envoyer-message-api/',
        {'destinataire': other_user.id, 'titre': 'Test fix', 'contenu': 'Test après correction'},
        format='multipart'  # Utiliser multipart pour simuler un formulaire
    )
    
    print(f'HTTP Status: {response.status_code}')
    print(f'Response: {response.content[:200]}')
    
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f'Success: {data.get(\"success\", False)}')
        if data.get('success'):
            print('✅ API fonctionne maintenant!')
        else:
            print(f'❌ Erreur: {data.get(\"error\", data.get(\"errors\", \"Unknown\"))}')
            
except Exception as e:
    print(f'❌ Erreur: {e}')
"
