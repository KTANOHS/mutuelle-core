#!/bin/bash

echo "🔍 DIAGNOSTIC API ENVOI MESSAGE"
echo "================================"

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

print('🧪 Test détaillé de l\'API d\'envoi:')

client = Client()

try:
    # Authentification
    user = User.objects.get(username='GLORIA1')
    print(f'1. ✅ Utilisateur: {user.username} (ID: {user.id})')
    client.force_login(user)
    
    # Trouver un destinataire
    other_user = User.objects.exclude(username='GLORIA1').first()
    if not other_user:
        print('❌ Aucun autre utilisateur trouvé')
        exit(1)
    
    print(f'2. ✅ Destinataire: {other_user.username} (ID: {other_user.id})')
    
    # Test 1: Formulaire standard
    print('\\n3. 📝 Test formulaire HTML:')
    response = client.get('/communication/messages/nouveau/')
    print(f'   • GET formulaire: HTTP {response.status_code}')
    
    # Extraire le token CSRF
    import re
    csrf_match = re.search(r'name=\"csrfmiddlewaretoken\" value=\"([^\"]+)\"', response.content.decode())
    csrf_token = csrf_match.group(1) if csrf_match else None
    print(f'   • Token CSRF: {'✅ Trouvé' if csrf_token else '❌ Non trouvé'}')
    
    # Test 2: Envoi via formulaire HTML (POST standard)
    print('\\n4. 📨 Test POST formulaire HTML:')
    form_data = {
        'csrfmiddlewaretoken': csrf_token,
        'destinataire': other_user.id,
        'titre': 'Test diagnostique',
        'contenu': 'Message de test via formulaire',
        'type_message': 'MESSAGE'
    }
    
    response = client.post('/communication/messages/envoyer/', form_data)
    print(f'   • POST formulaire: HTTP {response.status_code}')
    
    if response.status_code == 302:  # Redirection après succès
        print(f'   • ✅ Redirection vers: {response.url}')
    else:
        print(f'   • ❌ Pas de redirection')
        print(f'   • Contenu: {response.content[:200]}...')
    
    # Test 3: API JSON avec CSRF
    print('\\n5. 🔧 Test API JSON avec CSRF:')
    
    # D'abord récupérer un token CSRF valide
    from django.middleware.csrf import get_token
    from django.http import HttpRequest
    
    request = HttpRequest()
    request.method = 'GET'
    request.user = user
    csrf_token_api = get_token(request)
    
    print(f'   • Token CSRF API: {csrf_token_api[:20]}...')
    
    # Envoyer avec le token
    headers = {
        'HTTP_X_CSRFTOKEN': csrf_token_api,
        'Content-Type': 'application/json'
    }
    
    api_data = {
        'destinataire': other_user.id,
        'titre': 'Test API diagnostique',
        'contenu': 'Message via API avec CSRF',
        'type_message': 'MESSAGE'
    }
    
    response = client.post('/communication/envoyer-message-api/', 
                         json.dumps(api_data), 
                         content_type='application/json',
                         **headers)
    
    print(f'   • POST API: HTTP {response.status_code}')
    print(f'   • Réponse: {response.content[:200]}')
    
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f'   • Succès: {data.get(\"success\", False)}')
        print(f'   • Message: {data.get(\"error\", data.get(\"errors\", \"N/A\"))}')
    
    # Test 4: Vérifier les messages existants
    print('\\n6. 📊 Vérification base de données:')
    from communication.models import Message, Conversation
    
    messages_gloria = Message.objects.filter(expediteur=user).count()
    conversations_gloria = Conversation.objects.filter(participants=user).count()
    
    print(f'   • Messages envoyés par GLORIA1: {messages_gloria}')
    print(f'   • Conversations de GLORIA1: {conversations_gloria}')
    
    # Afficher les derniers messages
    last_messages = Message.objects.filter(expediteur=user).order_by('-date_envoi')[:3]
    if last_messages:
        print(f'   • Derniers messages:')
        for msg in last_messages:
            print(f'      - À {msg.destinataire.username}: \"{msg.titre}\"')
    
except Exception as e:
    print(f'\\n❌ ERREUR: {e}')
    import traceback
    traceback.print_exc()
"
