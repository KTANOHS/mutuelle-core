# script_recuperer_messages.py
import os
import sys
import django

# Configuration de Django
sys.path.append('/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from communication.models import Conversation, Message
import json

def recuperer_messages(conversation_id=5):
    try:
        conv = Conversation.objects.get(id=conversation_id)
        messages = Message.objects.filter(conversation=conv).order_by('id')
        
        data = []
        for msg in messages:
            data.append({
                'id': msg.id,
                'contenu': msg.contenu,
                'expediteur': msg.expediteur.username if msg.expediteur else None,
                'destinataire': msg.destinataire.username if msg.destinataire else None,
                'date_envoi': msg.date_envoi.isoformat() if msg.date_envoi else None,
                'est_lu': msg.est_lu,
                'titre': msg.titre if hasattr(msg, 'titre') else None,
            })
        
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return data
    except Exception as e:
        print(f"Erreur: {e}")
        return []

if __name__ == '__main__':
    recuperer_messages(5)