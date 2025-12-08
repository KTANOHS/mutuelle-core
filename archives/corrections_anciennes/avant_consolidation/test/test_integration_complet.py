# test_integration_complet.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_integration_complet():
    from django.contrib.auth import get_user_model
    from communication.models import Message, Conversation
    from communication.utils import creer_message_automatique, get_conversations_utilisateur
    
    User = get_user_model()
    
    print("=== TEST INTÉGRATION COMPLET ===")
    
    # 1. Vérifier les utilisateurs
    assureur = User.objects.filter(username='assureur_test').first()
    agent = User.objects.filter(username='koffitanoh').first()
    
    if not assureur or not agent:
        print("❌ Utilisateurs de test non trouvés")
        return
    
    print("✅ Utilisateurs trouvés:")
    print(f"   - Assureur: {assureur.username} (groupes: {[g.name for g in assureur.groups.all()]})")
    print(f"   - Agent: {agent.username} (groupes: {[g.name for g in agent.groups.all()]})")
    
    # 2. Test avec la fonction utilitaire
    print("\n2. TEST FONCTION UTILITAIRE:")
    try:
        message_auto = creer_message_automatique(
            expediteur=assureur,
            destinataire=agent,
            titre="Test intégration fonction utilitaire",
            contenu="Ce message est créé via la fonction utilitaire",
            type_message="MESSAGE"
        )
        print("✅ Message créé via fonction utilitaire")
        print(f"   - ID: {message_auto.id}")
        print(f"   - Conversation: {message_auto.conversation.id}")
    except Exception as e:
        print(f"❌ Erreur fonction utilitaire: {e}")
    
    # 3. Vérifier les conversations
    print("\n3. CONVERSATIONS DE L'ASSUREUR:")
    conversations_assureur = get_conversations_utilisateur(assureur)
    print(f"   {conversations_assureur.count()} conversation(s) trouvée(s)")
    
    for conv in conversations_assureur:
        participants = [p.username for p in conv.participants.all()]
        messages_count = conv.messages.count()
        print(f"   - Conversation {conv.id}: {participants} ({messages_count} messages)")
    
    # 4. Statistiques finales
    print("\n4. STATISTIQUES FINALES:")
    total_messages = Message.objects.count()
    total_conversations = Conversation.objects.count()
    
    print(f"   - Total messages dans le système: {total_messages}")
    print(f"   - Total conversations: {total_conversations}")
    print(f"   - Messages de l'assureur: {Message.objects.filter(expediteur=assureur).count()}")
    print(f"   - Messages à l'assureur: {Message.objects.filter(destinataire=assureur).count()}")

if __name__ == "__main__":
    test_integration_complet()