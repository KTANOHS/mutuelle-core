# communication/templatetags/communication_global.py
from django import template
from django.db.models import Count, Q

register = template.Library()

@register.simple_tag
def get_unread_notifications_count(user):
    """Retourne le nombre de notifications non lues"""
    try:
        if not user.is_authenticated:
            return 0
            
        from communication.models import Notification
        
        # Version simple et directe
        return Notification.objects.filter(user=user, est_lue=False).count()
                
    except Exception as e:
        print(f"Erreur dans get_unread_notifications_count: {e}")
        return 0

@register.simple_tag
def get_user_conversations(user, limit=5):
    """Retourne les conversations de l'utilisateur"""
    try:
        if not user.is_authenticated:
            return []
            
        from communication.models import Conversation
        
        # Version simplifiée sans annotations complexes
        return Conversation.objects.filter(participants=user).order_by('-date_modification')[:limit]
                
    except Exception as e:
        print(f"Erreur dans get_user_conversations: {e}")
        return []

@register.filter
def get_contact_name(user):
    """Retourne le nom formaté pour le contact"""
    try:
        if user and hasattr(user, 'get_full_name'):
            full_name = user.get_full_name()
            if full_name:
                return full_name
        return getattr(user, 'username', 'Utilisateur')
    except:
        return 'Utilisateur'

# Les autres fonctions peuvent être supprimées si non utilisées