
#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from communication.models import Conversation, Message
from django.contrib.auth import get_user_model

def diagnostic_complet():
    User = get_user_model()
    
    try:
        gloria = User.objects.get(username='GLORIA1')
        print(f"🔍 Diagnostic pour: {gloria.username} (ID: {gloria.id})")
        print("=" * 50)
        
        # 1. Conversations via différentes méthodes
        print("1. RECHERCHE DES CONVERSATIONS:")
        convs_method1 = Conversation.objects.filter(participants=gloria)
        print(f"   - filter(participants=user): {convs_method1.count()} conversations")
        
        convs_method2 = gloria.conversation_set.all()
        print(f"   - user.conversation_set.all(): {convs_method2.count()} conversations")
        
        # 2. Détail des conversations
        print("\n2. DÉTAIL DES CONVERSATIONS:")
        all_conversations = Conversation.objects.all()
        print(f"   Total en base: {all_conversations.count()} conversations")
        
        for i, conv in enumerate(all_conversations, 1):
            participants = list(conv.participants.all())
            participant_names = [p.username for p in participants]
            print(f"   {i}. Conversation {conv.id}:")
            print(f"      Participants: {participant_names}")
            print(f"      GLORIA1 dans participants: {gloria in participants}")
            print(f"      Date: {conv.date_creation}")
            
            # Messages dans cette conversation
            messages = Message.objects.filter(conversation=conv)
            print(f"      Messages: {messages.count()}")
            print()
        
        # 3. Vérification des relations
        print("3. VÉRIFICATION DES RELATIONS:")
        print(f"   GLORIA1 a {gloria.conversation_set.count()} conversations (relation inverse)")
        
    except User.DoesNotExist:
        print("❌ Utilisateur GLORIA1 non trouvé")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    diagnostic_complet()


