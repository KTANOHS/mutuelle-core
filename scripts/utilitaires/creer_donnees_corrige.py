#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from communication.models import Conversation, Notification, Message
from pharmacien.models import Pharmacien
from medecin.models import Medecin
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

def creer_donnees_corrige():
    User = get_user_model()
    
    print("🚀 CRÉATION DE DONNÉES DE TEST CORRIGÉE")
    print("=" * 60)
    
    # 1. Trouver GLORIA1
    try:
        gloria = User.objects.get(username='GLORIA1')
        print(f"✅ GLORIA1 trouvée (ID: {gloria.id})")
    except User.DoesNotExist:
        print("❌ GLORIA1 non trouvée, création...")
        gloria = User.objects.create_user(
            username='GLORIA1',
            email='gloria@pharmacie.com',
            password='pharmacien123'
        )
        gloria.save()
        print(f"👤 GLORIA1 créée (ID: {gloria.id})")
    
    # 2. S'assurer que GLORIA1 est pharmacien
    pharmacien, created = Pharmacien.objects.get_or_create(
        user=gloria,
        defaults={
            'telephone': '0123456789',
            'pharmacie_nom': 'Pharmacie Centrale'
        }
    )
    if created:
        print(f"🏥 Pharmacien créé (ID: {pharmacien.id})")
    else:
        print(f"🏥 Pharmacien existant (ID: {pharmacien.id})")
    
    # 3. Créer des utilisateurs médecins
    medecins_users = []
    medecins_info = [
        {'username': 'medecin_test_1', 'nom': 'Dr. Martin'},
        {'username': 'medecin_test_2', 'nom': 'Dr. Dupont'},
        {'username': 'medecin_test_3', 'nom': 'Dr. Leroy'}
    ]
    
    for info in medecins_info:
        try:
            user = User.objects.get(username=info['username'])
            print(f"⚕️  Médecin existant: {info['username']}")
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=info['username'],
                email=f"{info['username']}@hopital.com",
                password='medecin123'
            )
            print(f"⚕️  Médecin créé: {info['username']}")
        
        medecins_users.append(user)
    
    # 4. Créer des conversations
    conversations_creees = []
    sujets = [
        "Suivi traitement Amoxicilline",
        "Ordonnance #2024-00123",
        "Question sur posologie"
    ]
    
    for i, (medecin_user, sujet) in enumerate(zip(medecins_users, sujets), 1):
        # Créer conversation
        conv = Conversation.objects.create()
        conv.participants.add(gloria, medecin_user)
        
        # Messages
        messages = [
            (gloria, f"Bonjour Docteur, je vous contacte concernant {sujet.lower()}."),
            (medecin_user, "Bonjour Pharmacien, de quoi s'agit-il précisément ?"),
            (gloria, "Le patient a besoin d'une clarification sur la posologie."),
            (medecin_user, "Je vous envoie les détails par message."),
            (gloria, "Merci Docteur, j'attends vos instructions.")
        ]
        
        for j, (expediteur, texte) in enumerate(messages):
            Message.objects.create(
                conversation=conv,
                expediteur=expediteur,
                contenu=texte
            )
        
        conversations_creees.append(conv)
        print(f"💬 Conversation {i} créée avec {medecin_user.username}")
    
    # 5. Créer des notifications
    notifications_data = [
        {
            "titre": "⚠️ Stock faible",
            "message": "Il reste seulement 15 boîtes de Paracétamol 500mg en stock.",
            "type_notification": "warning"
        },
        {
            "titre": "✅ Ordonnance validée",
            "message": "Ordonnance #2024-00123 pour M. Dupont validée.",
            "type_notification": "success"
        },
        {
            "titre": "📋 Nouvelle ordonnance",
            "message": "Nouvelle ordonnance du Dr. Martin en attente.",
            "type_notification": "info"
        },
        {
            "titre": "💬 Nouveau message",
            "message": "Le Dr. Leroy vous a envoyé un message.",
            "type_notification": "primary"
        }
    ]
    
    for i, notif_data in enumerate(notifications_data):
        Notification.objects.create(
            user=gloria,
            titre=notif_data["titre"],
            message=notif_data["message"],
            type_notification=notif_data.get("type_notification", "info"),
            est_lue=i % 2 == 0,  # Une notification sur deux est lue
            date_creation=timezone.now() - timedelta(hours=i)
        )
        print(f"🔔 Notification créée: '{notif_data['titre']}'")
    
    # 6. Vérification
    conv_count = Conversation.objects.filter(participants=gloria).count()
    notif_count = Notification.objects.filter(user=gloria).count()
    notif_unread = Notification.objects.filter(user=gloria, est_lue=False).count()
    
    print(f"\n🎉 DONNÉES CRÉÉES:")
    print(f"   Conversations: {conv_count}")
    print(f"   Notifications: {notif_count} ({notif_unread} non lues)")
    
    print(f"\n🌐 TESTER:")
    print(f"   1. Connectez-vous avec: GLORIA1 / pharmacien123")
    print(f"   2. Accédez à: http://127.0.0.1:8000/pharmacien/dashboard/")

if __name__ == "__main__":
    creer_donnees_corrige()
