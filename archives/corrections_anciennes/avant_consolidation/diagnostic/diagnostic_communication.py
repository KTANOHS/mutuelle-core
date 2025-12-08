# diagnostic_communication.py
import os
import django
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from communication.models import Message, Notification
from django.utils import timezone

def diagnostic_communication():
    User = get_user_model()
    
    print("=== DIAGNOSTIC SYSTÈME DE COMMUNICATION ===")
    
    # 1. Vérification des sessions
    print("\n1. SESSIONS ACTIVES:")
    sessions = Session.objects.filter(expire_date__gt=timezone.now())
    print(f"   {sessions.count()} session(s) active(s)")
    
    for session in sessions:
        session_data = session.get_decoded()
        print(f"   - Session {session.session_key}: {session_data}")
    
    # 2. Vérification des utilisateurs
    print("\n2. UTILISATEURS:")
    assureurs = User.objects.filter(groups__name='ASSUREUR')
    print(f"   {assureurs.count()} assureur(s) trouvé(s)")
    
    # 3. Vérification des messages
    print("\n3. MESSAGES:")
    messages = Message.objects.all()
    print(f"   {messages.count()} message(s) dans la base")
    
    for msg in messages[:5]:  # 5 premiers messages
        print(f"   - Message {msg.id}: {msg.type_message} - {msg.sujet}")
    
    # 4. Vérification des notifications
    print("\n4. NOTIFICATIONS:")
    notifications = Notification.objects.all()
    print(f"   {notifications.count()} notification(s)")
    
    # 5. Vérification configuration
    print("\n5. CONFIGURATION:")
    print(f"   TIME_ZONE: {settings.TIME_ZONE}")
    print(f"   USE_TZ: {settings.USE_TZ}")
    print(f"   DEBUG: {settings.DEBUG}")

if __name__ == "__main__":
    diagnostic_communication()