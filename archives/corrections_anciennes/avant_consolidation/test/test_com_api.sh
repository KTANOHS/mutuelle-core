#!/bin/bash

echo "🔧 TEST COMPLET DES APIs COMMUNICATION"
echo "====================================="

# Démarrer le serveur si nécessaire
if ! ps aux | grep -q "python manage.py runserver"; then
    echo "🚀 Démarrage du serveur..."
    python manage.py runserver 0.0.0.0:8000 > /tmp/com_api_test.log 2>&1 &
    SERVER_PID=$!
    sleep 5
    echo "✅ Serveur démarré (PID: $SERVER_PID)"
fi

# Test Python complet
python -c "
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
    from communication.models import Message, Notification, Conversation
    
    print('🧪 TEST COMPLET DES APIs')
    print('=' * 50)
    
    client = Client()
    
    # 1. Authentification
    try:
        user = User.objects.get(username='GLORIA1')
        print(f'1. ✅ Authentification: {user.username}')
        client.force_login(user)
    except User.DoesNotExist:
        print('1. ❌ GLORIA1 non trouvé')
        exit(1)
    
    # 2. Test API notifications
    print('\\n2. 📊 API Notifications:')
    response = client.get('/communication/notifications/count/')
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f'   ✅ HTTP 200 - Notifications non lues: {data.get(\"count\", 0)}')
    else:
        print(f'   ❌ HTTP {response.status_code}')
    
    # 3. Test API conversations
    print('\\n3. 💬 API Conversations:')
    response = client.get('/communication/api/conversations/')
    if response.status_code == 200:
        data = json.loads(response.content)
        conv_count = len(data.get('conversations', []))
        print(f'   ✅ HTTP 200 - Conversations: {conv_count}')
        
        # Afficher les conversations si elles existent
        if conv_count > 0:
            for i, conv in enumerate(data['conversations'][:3]):
                print(f'      {i+1}. Conversation {conv[\"id\"]} avec {conv[\"autre_participant\"][\"nom\"]}')
    else:
        print(f'   ❌ HTTP {response.status_code}')
    
    # 4. Test création message
    print('\\n4. 📨 Test création message:')
    
    # Trouver un destinataire
    other_user = User.objects.exclude(username='GLORIA1').first()
    if other_user:
        print(f'   Destinataire: {other_user.username} (ID: {other_user.id})')
        
        # Test via formulaire HTML
        print('   a) Test formulaire HTML:')
        response = client.get('/communication/messages/nouveau/')
        print(f'      Formulaire: HTTP {response.status_code}')
        
        # Test API JSON
        print('   b) Test API JSON:')
        response = client.post('/communication/envoyer-message-api/',
            data=json.dumps({
                'destinataire': other_user.id,
                'titre': 'Test API',
                'contenu': 'Message de test via API',
                'type_message': 'MESSAGE'
            }),
            content_type='application/json'
        )
        
        if response.status_code == 200:
            data = json.loads(response.content)
            if data.get('success'):
                print(f'      ✅ Message envoyé - ID: {data.get(\"message_id\")}')
                
                # Vérifier en base
                msg = Message.objects.get(id=data['message_id'])
                print(f'      📦 En base: De {msg.expediteur.username} à {msg.destinataire.username}')
            else:
                print(f'      ❌ Échec: {data.get(\"error\", \"Unknown\")}')
        else:
            print(f'      ❌ HTTP {response.status_code}')
            print(f'      Erreur: {response.content[:200]}')
    else:
        print('   ❌ Aucun autre utilisateur trouvé')
    
    # 5. Statistiques
    print('\\n5. 📈 Statistiques:')
    total_messages = Message.objects.filter(expediteur=user).count()
    total_notifications = Notification.objects.filter(user=user).count()
    total_conversations = Conversation.objects.filter(participants=user).count()
    
    print(f'   • Messages envoyés: {total_messages}')
    print(f'   • Notifications totales: {total_notifications}')
    print(f'   • Conversations: {total_conversations}')
    
    print('\\n' + '=' * 50)
    print('🎉 TEST TERMINÉ AVEC SUCCÈS !')
    
except Exception as e:
    print(f'❌ ERREUR: {e}')
    import traceback
    traceback.print_exc()
"

# Arrêter le serveur si on l'a démarré
if [ -n "$SERVER_PID" ]; then
    echo ""
    echo "🛑 Arrêt du serveur..."
    kill $SERVER_PID 2>/dev/null
fi
