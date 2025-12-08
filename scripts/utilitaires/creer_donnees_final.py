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

def creer_donnees_final():
    User = get_user_model()
    
    print("🚀 CRÉATION DE DONNÉES - VERSION FINALE")
    print("=" * 60)
    
    # 1. Trouver GLORIA1
    gloria = User.objects.get(username='GLORIA1')
    print(f"✅ GLORIA1 trouvée (ID: {gloria.id})")
    
    # 2. Créer des utilisateurs médecins s'ils n'existent pas
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
    
    # 3. Vérifier la structure du modèle Message
    print(f"\n🔍 Vérification du modèle Message...")
    # Inspecter les champs du modèle
    from django.db import models
    message_fields = Message._meta.fields
    field_names = [f.name for f in message_fields]
    print(f"   Champs Message: {field_names}")
    
    # 4. Créer des conversations avec messages adaptés
    conversations_creees = []
    
    for i, medecin_user in enumerate(medecins_users, 1):
        print(f"\n�� Création conversation {i} avec {medecin_user.username}...")
        
        # Créer conversation
        conv = Conversation.objects.create()
        conv.participants.add(gloria, medecin_user)
        
        # Créer des messages selon la structure du modèle
        try:
            # Essayer avec destinataire si le champ existe
            if 'destinataire' in field_names:
                # Message de GLORIA au médecin
                Message.objects.create(
                    conversation=conv,
                    expediteur=gloria,
                    destinataire=medecin_user,
                    contenu=f"Bonjour Docteur, je vous contacte concernant une ordonnance."
                )
                print(f"   📤 Message 1: GLORIA → {medecin_user.username}")
                
                # Réponse du médecin à GLORIA
                Message.objects.create(
                    conversation=conv,
                    expediteur=medecin_user,
                    destinataire=gloria,
                    contenu=f"Bonjour Pharmacien, de quoi s'agit-il précisément ?"
                )
                print(f"   📥 Message 2: {medecin_user.username} → GLORIA")
                
                # Suite de la conversation
                Message.objects.create(
                    conversation=conv,
                    expediteur=gloria,
                    destinataire=medecin_user,
                    contenu=f"Le patient a besoin d'une clarification sur la posologie du traitement."
                )
                print(f"   📤 Message 3: GLORIA → {medecin_user.username}")
            else:
                # Si pas de champ destinataire
                Message.objects.create(
                    conversation=conv,
                    expediteur=gloria,
                    contenu=f"Bonjour Docteur, je vous contacte concernant une ordonnance."
                )
                Message.objects.create(
                    conversation=conv,
                    expediteur=medecin_user,
                    contenu=f"Bonjour Pharmacien, de quoi s'agit-il précisément ?"
                )
                Message.objects.create(
                    conversation=conv,
                    expediteur=gloria,
                    contenu=f"Le patient a besoin d'une clarification sur la posologie."
                )
                print(f"   📝 3 messages créés (sans destinataire)")
                
        except Exception as e:
            print(f"   ⚠️  Erreur création messages: {e}")
            # Version simplifiée
            try:
                Message.objects.create(
                    conversation=conv,
                    expediteur=gloria,
                    contenu=f"Message test de GLORIA"
                )
                print(f"   📝 Message test créé")
            except Exception as e2:
                print(f"   ❌ Impossible de créer des messages: {e2}")
                # Au moins on a la conversation
        
        conversations_creees.append(conv)
    
    # 5. Créer des notifications (plus simple, devrait fonctionner)
    print(f"\n🔔 Création des notifications...")
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
        }
    ]
    
    for i, notif_data in enumerate(notifications_data):
        try:
            Notification.objects.create(
                user=gloria,
                titre=notif_data["titre"],
                message=notif_data["message"],
                type_notification=notif_data.get("type_notification", "info"),
                est_lue=i % 2 == 0
            )
            print(f"   ✅ Notification: '{notif_data['titre']}'")
        except Exception as e:
            print(f"   ❌ Erreur notification: {e}")
            # Version simplifiée
            try:
                Notification.objects.create(
                    user=gloria,
                    titre=notif_data["titre"],
                    message=notif_data["message"]
                )
                print(f"   ✅ Notification créée (simplifiée)")
            except Exception as e2:
                print(f"   ❌ Impossible de créer notification: {e2}")
    
    # 6. Vérification finale
    print(f"\n🎉 VÉRIFICATION FINALE:")
    
    conv_count = Conversation.objects.filter(participants=gloria).count()
    print(f"   Conversations: {conv_count}")
    
    notif_count = Notification.objects.filter(user=gloria).count()
    notif_unread = Notification.objects.filter(user=gloria, est_lue=False).count()
    print(f"   Notifications: {notif_count} ({notif_unread} non lues)")
    
    print(f"\n🌐 POUR TESTER:")
    print(f"   1. Redémarrez: python manage.py runserver")
    print(f"   2. Connectez-vous: GLORIA1 / pharmacien123")
    print(f"   3. Dashboard: http://127.0.0.1:8000/pharmacien/dashboard/")

if __name__ == "__main__":
    creer_donnees_final()
