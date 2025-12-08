# diagnostic_communication_corrige.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from communication.models import Message, Notification
from django.utils import timezone

def diagnostic_communication():
    User = get_user_model()
    
    print("=== DIAGNOSTIC SYSTÈME DE COMMUNICATION CORRIGÉ ===")
    
    # 1. Vérification des sessions
    print("\n1. SESSIONS ACTIVES:")
    sessions = Session.objects.filter(expire_date__gt=timezone.now())
    print(f"   {sessions.count()} session(s) active(s)")
    
    # 2. Vérification des utilisateurs et groupes
    print("\n2. UTILISATEURS ET GROUPES:")
    try:
        assureurs_group = Group.objects.filter(name='ASSUREUR').first()
        if assureurs_group:
            assureurs = assureurs_group.user_set.all()
            print(f"   {assureurs.count()} assureur(s) trouvé(s) dans le groupe ASSUREUR")
            for user in assureurs:
                print(f"   - {user.username} | {user.email}")
        else:
            print("   ❌ Groupe ASSUREUR non trouvé")
            
        # Vérifier tous les utilisateurs
        all_users = User.objects.all()
        print(f"   Total utilisateurs: {all_users.count()}")
        for user in all_users:
            groups = [g.name for g in user.groups.all()]
            print(f"   - {user.username} | Groupes: {groups}")
            
    except Exception as e:
        print(f"   ❌ Erreur utilisateurs: {e}")
    
    # 3. Vérification des messages (CORRIGÉ - utiliser 'titre' au lieu de 'sujet')
    print("\n3. MESSAGES:")
    messages = Message.objects.all()
    print(f"   {messages.count()} message(s) dans la base")
    
    for msg in messages:
        # CORRECTION: Utiliser msg.titre au lieu de msg.sujet
        print(f"   - Message {msg.id}: {msg.type_message} - {msg.titre}")
        print(f"     De: {msg.expediteur.username} → À: {msg.destinataire.username}")
        print(f"     Contenu: {msg.contenu[:50]}...")
        print(f"     Lu: {msg.est_lu} | Date: {msg.date_envoi}")
    
    # 4. Vérification des notifications
    print("\n4. NOTIFICATIONS:")
    notifications = Notification.objects.all()
    print(f"   {notifications.count()} notification(s)")
    
    for notif in notifications:
        print(f"   - {notif.titre} ({notif.type_notification}) - Pour: {notif.user.username}")

    # 5. Configuration
    print("\n5. CONFIGURATION:")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   TIME_ZONE: {settings.TIME_ZONE}")
    print(f"   USE_TZ: {settings.USE_TZ}")

if __name__ == "__main__":
    diagnostic_communication()