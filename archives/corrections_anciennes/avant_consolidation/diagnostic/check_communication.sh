#!/bin/bash
echo "🔄 Vérification rapide du module communication..."
source venv/bin/activate

echo "1. Vérification des modèles..."
python -c "
from communication.models import Message, Conversation
print(f'Messages: {Message.objects.count()}')
print(f'Conversations: {Conversation.objects.count()}')
"

echo "2. Test API..."
curl -s http://127.0.0.1:8000/communication/api/public/test/ | grep -o '"status":".*"' || echo "API non accessible"

echo "3. Nettoyage des sessions..."
python manage.py clearsessions --dry-run | grep "sessions" || echo "Aucune session à nettoyer"

echo "✅ Vérification terminée"
