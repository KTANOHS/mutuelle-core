# creer_conversations_test.py
import os
import django
import sys

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from communication.models import Conversation, Message
from django.contrib.auth import get_user_model
from django.utils import timezone

def creer_conversations_test():
    print("🚀 CRÉATION DE CONVERSATIONS DE TEST")
    print("=" * 50)
    
    User = get_user_model()
    
    # Récupérer les utilisateurs existants
    try:
        test_agent = User.objects.get(username='test_agent')
        test_assureur = User.objects.get(username='test_assureur')
        test_medecin = User.objects.get(username='test_medecin')
        
        print("✅ Utilisateurs trouvés:")
        print(f"   • Agent: {test_agent}")
        print(f"   • Assureur: {test_assureur}") 
        print(f"   • Médecin: {test_medecin}")
        
    except User.DoesNotExist:
        print("❌ Utilisateurs de test non trouvés")
        return
    
    # Créer une conversation entre agent et assureur
    conv1, created1 = Conversation.objects.get_or_create()
    if created1:
        conv1.participants.add(test_agent, test_assureur)
        conv1.save()
        
        # Créer des messages de test
        Message.objects.create(
            expediteur=test_agent,
            destinataire=test_assureur,
            conversation=conv1,
            titre="Demande d'information",
            contenu="Bonjour, je souhaite avoir des informations sur la couverture des soins.",
            est_lu=False
        )
        
        Message.objects.create(
            expediteur=test_assureur,
            destinataire=test_agent, 
            conversation=conv1,
            titre="Réponse à votre demande",
            contenu="Bonjour, je vous envoie les informations demandées sur la couverture.",
            est_lu=True
        )
        
        print("✅ Conversation Agent-Assureur créée avec 2 messages")
    
    # Créer une conversation entre agent et médecin
    conv2, created2 = Conversation.objects.get_or_create()
    if created2:
        conv2.participants.add(test_agent, test_medecin)
        conv2.save()
        
        Message.objects.create(
            expediteur=test_agent,
            destinataire=test_medecin,
            conversation=conv2,
            titre="Question médicale",
            contenu="Docteur, un patient présente ces symptômes...",
            est_lu=False
        )
        
        print("✅ Conversation Agent-Médecin créée avec 1 message")
    
    # Vérifier le résultat
    total_conv = Conversation.objects.count()
    total_msg = Message.objects.count()
    
    print(f"\n📊 RÉSULTAT:")
    print(f"   • Conversations créées: {total_conv}")
    print(f"   • Messages créés: {total_msg}")
    print(f"   • Conversations de l'agent: {test_agent.conversations.count()}")

if __name__ == "__main__":
    creer_conversations_test()