#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from pharmacien.views import dashboard_pharmacien
from django.test import RequestFactory
from django.contrib.auth.models import User, AnonymousUser

# Créer une requête de test
factory = RequestFactory()

# 1. Créer une requête avec GLORIA1
gloria = User.objects.get(username='GLORIA1')
request = factory.get('/pharmacien/dashboard/')
request.user = gloria

print("🔍 DEBUG SIMULÉ DU DASHBOARD")
print("=" * 60)
print(f"Utilisateur: {request.user.username} (ID: {request.user.id})")

# Simuler la logique de la vue
from communication.models import Conversation, Notification
from pharmacien.models import Pharmacien
from django.utils import timezone
from datetime import date

try:
    # Récupérer le profil pharmacien
    pharmacien = Pharmacien.objects.get(user=request.user)
    print(f"✅ Pharmacien trouvé: ID {pharmacien.id}")
except Pharmacien.DoesNotExist:
    print("❌ Pharmacien non trouvé")
    pharmacien = None

# Conversations
conversations = Conversation.objects.filter(participants=request.user).order_by('-date_modification')[:5]
print(f"📊 Conversations trouvées: {conversations.count()}")
for conv in conversations:
    participants = [p.username for p in conv.participants.all()]
    print(f"   - Conv {conv.id}: {participants}")

# Notifications
notifications_non_lues = Notification.objects.filter(user=request.user, est_lue=False)
unread_count = notifications_non_lues.count()
print(f"📊 Notifications non lues: {unread_count}")
for notif in notifications_non_lues[:3]:
    print(f"   - '{notif.titre}' (type: {notif.type_notification})")

# Ordonnances (medecin.Ordonnance)
try:
    from medecin.models import Ordonnance as MedecinOrdonnance
    ordonnances_attente = MedecinOrdonnance.objects.filter(statut="ACTIVE").count()
    print(f"📊 Ordonnances ACTIVE: {ordonnances_attente}")
except Exception as e:
    print(f"⚠️  Erreur ordonnances: {e}")

print(f"\n🌐 Pour tester: http://127.0.0.1:8000/pharmacien/dashboard/")
