# communication/utils.py
from django.contrib.auth import get_user_model
from .models import Conversation

def get_or_create_conversation(expediteur, destinataire):
    """
    Crée ou récupère une conversation entre deux utilisateurs
    Retourne l'instance Conversation
    """
    User = get_user_model()
    
    # Chercher une conversation existante entre ces deux utilisateurs
    conversations = Conversation.objects.filter(
        participants=expediteur
    ).filter(
        participants=destinataire
    ).distinct()
    
    # Prendre la première conversation trouvée
    if conversations.exists():
        conversation = conversations.first()
        print(f"✅ Conversation existante trouvée: {conversation.id}")
    else:
        # Créer une nouvelle conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(expediteur, destinataire)
        conversation.save()
        print(f"✅ Nouvelle conversation créée: {conversation.id}")
    
    return conversation

def creer_message_automatique(expediteur, destinataire, titre, contenu, type_message='MESSAGE'):
    """
    Fonction utilitaire pour créer un message avec conversation automatique
    Retourne l'instance Message créée
    """
    from .models import Message
    
    conversation = get_or_create_conversation(expediteur, destinataire)
    
    message = Message.objects.create(
        expediteur=expediteur,
        destinataire=destinataire,
        conversation=conversation,
        titre=titre,
        contenu=contenu,
        type_message=type_message
    )
    
    print(f"✅ Message créé: {message.id} dans conversation: {conversation.id}")
    return message

def get_conversations_utilisateur(utilisateur):
    """
    Retourne toutes les conversations d'un utilisateur
    """
    return Conversation.objects.filter(participants=utilisateur).order_by('-date_modification')

def get_messages_non_lus(utilisateur):
    """
    Retourne le nombre de messages non lus pour un utilisateur
    """
    from .models import Message
    return Message.objects.filter(
        destinataire=utilisateur,
        est_lu=False
    ).count()

def marquer_messages_lus(utilisateur, conversation=None):
    """
    Marque tous les messages comme lus pour un utilisateur dans une conversation
    """
    from .models import Message
    from django.utils import timezone
    
    messages = Message.objects.filter(
        destinataire=utilisateur,
        est_lu=False
    )
    
    if conversation:
        messages = messages.filter(conversation=conversation)
    
    count = messages.update(est_lu=True, date_lecture=timezone.now())
    print(f"✅ {count} message(s) marqué(s) comme lu(s) pour {utilisateur.username}")
    return count