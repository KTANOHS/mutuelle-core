#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from communication.models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

print("🔍 DIAGNOSTIC MESSAGERIE - Conversation 5")
print("="*50)

# 1. Vérifier la conversation
try:
    conv = Conversation.objects.get(id=5)
    print(f"✅ Conversation trouvée: ID {conv.id}")
    # Essayer différents champs possibles pour le titre
    if hasattr(conv, 'sujet'):
        print(f"   Sujet: {conv.sujet}")
    elif hasattr(conv, 'nom'):
        print(f"   Nom: {conv.nom}")
    elif hasattr(conv, 'titre'):
        print(f"   Titre: {conv.titre}")
    else:
        print(f"   Aucun champ de titre trouvé. Attributs disponibles: {[attr for attr in dir(conv) if not attr.startswith('_')]}")
    
    print(f"   Participants: {[p.username for p in conv.participants.all()]}")
except Conversation.DoesNotExist:
    print("❌ Conversation 5 non trouvée")
    sys.exit(1)

# 2. Vérifier les messages
messages = Message.objects.filter(conversation=conv).order_by('date_envoi')
print(f"\n📊 Messages dans la conversation ({messages.count()} au total):")

for i, msg in enumerate(messages, 1):
    print(f"\n  Message {i}:")
    print(f"    ID: {msg.id}")
    print(f"    Titre: {msg.titre}")
    contenu_display = msg.contenu[:50] + "..." if len(msg.contenu) > 50 else msg.contenu
    print(f"    Contenu: {contenu_display}")
    print(f"    Expéditeur: {msg.expediteur.username} ({msg.expediteur.get_full_name()})")
    print(f"    Destinataire: {msg.destinataire.username} ({msg.destinataire.get_full_name()})")
    print(f"    Date: {msg.date_envoi}")
    print(f"    Lu: {msg.est_lu}")

# 3. Vérifier les doublons
print("\n🔎 Vérification des doublons:")
titles = {}
for msg in messages:
    if msg.titre in titles:
        titles[msg.titre].append(msg.id)
    else:
        titles[msg.titre] = [msg.id]

for title, ids in titles.items():
    if len(ids) > 1:
        print(f"⚠️  Doublon: '{title}' - IDs: {ids}")

# 4. Vérifier les utilisateurs
print("\n👥 Vérification des utilisateurs:")
users_in_conversation = set()
for msg in messages:
    users_in_conversation.add(msg.expediteur)
    users_in_conversation.add(msg.destinataire)

for user in users_in_conversation:
    print(f"  - {user.username}: {user.get_full_name()} | Email: {user.email}")

print("\n" + "="*50)
print("📋 RÉSUMÉ DU DIAGNOSTIC")
print(f"• Conversation ID: {conv.id}")
print(f"• Nombre de messages: {messages.count()}")
print(f"• Nombre de participants: {len(users_in_conversation)}")
if messages.exists():
    print(f"• Période: {messages.first().date_envoi} à {messages.last().date_envoi}")