#!/bin/bash

echo "🔍 DIAGNOSTIC API ENVOI MESSAGE (CORRIGÉ)"
echo "========================================="

python3 -c "
import sys
import os
import json
sys.path.insert(0, '.')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    import django
    django.setup()
    
    from django.test import Client
    from django.contrib.auth.models import User
    
    print('🧪 Test détaillé de l\\'API d\\'envoi:')
    
    client = Client()
    
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
    content = response.content.decode('utf-8', errors='ignore')
    csrf_match = re.search(r'name=[\"\']csrfmiddlewaretoken[\"\'] value=[\"\']([^\"\']+)[\"\']', content)
    csrf_token = csrf_match.group(1) if csrf_match else None
    print(f'   • Token CSRF: {\"✅ Trouvé\" if csrf_token else \"❌ Non trouvé\"}')
    
    # Test 2: Envoi via formulaire HTML (POST standard)
    print('\\n4. 📨 Test POST formulaire HTML:')
    if csrf_token:
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
            print(f'   • ✅ Redirection après succès')
            print(f'   • Redirigé vers: {response.url}')
        else:
            print(f'   • ❌ Pas de redirection')
            if hasattr(response, 'content'):
                print(f'   • Contenu: {response.content[:200]}...')
    else:
        print('   • ❌ Impossible - token CSRF manquant')
    
    # Test 3: API JSON avec @csrf_exempt
    print('\\n5. 🔧 Test API JSON (avec @csrf_exempt):')
    
    api_data = {
        'destinataire': other_user.id,
        'titre': 'Test API diagnostique',
        'contenu': 'Message via API avec CSRF exempt',
        'type_message': 'MESSAGE'
    }
    
    response = client.post('/communication/envoyer-message-api/', 
                         json.dumps(api_data), 
                         content_type='application/json')
    
    print(f'   • POST API: HTTP {response.status_code}')
    
    if response.status_code == 200:
        try:
            data = json.loads(response.content)
            print(f'   • Réponse JSON: {data}')
            print(f'   • Succès: {data.get(\"success\", False)}')
            
            if data.get('success'):
                print(f'   • ✅ Message ID: {data.get(\"message_id\")}')
            else:
                print(f'   • ❌ Erreur: {data.get(\"error\", data.get(\"errors\", \"Unknown\"))}')
        except:
            print(f'   • ❌ Réponse non-JSON: {response.content[:200]}')
    else:
        print(f'   • ❌ HTTP {response.status_code}')
        print(f'   • Erreur: {response.content[:200]}')
    
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
            print(f'      - À {msg.destinataire.username}: \"{msg.titre}\" ({msg.date_envoi})')
    
except Exception as e:
    print(f'\\n❌ ERREUR: {e}')
    import traceback
    traceback.print_exc()
"
