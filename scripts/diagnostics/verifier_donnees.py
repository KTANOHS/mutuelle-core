#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from communication.models import Conversation, Notification

User = get_user_model()

print("🔍 VÉRIFICATION DES DONNÉES")
print("=" * 60)

# 1. GLORIA1
try:
    gloria = User.objects.get(username='GLORIA1')
    print(f"✅ GLORIA1: ID={gloria.id}, Email={gloria.email}")
except:
    print("❌ GLORIA1 non trouvée")
    exit()

# 2. Conversations
conv_count = Conversation.objects.filter(participants=gloria).count()
print(f"📊 Conversations: {conv_count}")
if conv_count > 0:
    for conv in Conversation.objects.filter(participants=gloria)[:3]:
        participants = [p.username for p in conv.participants.all()]
        print(f"   - Conv {conv.id}: {participants}")

# 3. Notifications
notif_count = Notification.objects.filter(user=gloria).count()
notif_unread = Notification.objects.filter(user=gloria, est_lue=False).count()
print(f"📊 Notifications: {notif_count} (dont {notif_unread} non lues)")
if notif_count > 0:
    for notif in Notification.objects.filter(user=gloria)[:3]:
        status = "📌" if not notif.est_lue else "✅"
        print(f"   {status} '{notif.titre[:30]}...'")

# 4. URLs
print(f"\n🌐 POUR TESTER:")
print(f"   Dashboard: http://127.0.0.1:8000/pharmacien/dashboard/")
print(f"   Login: http://127.0.0.1:8000/accounts/login/")
