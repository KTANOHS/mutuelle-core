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

def creer_donnees_test_complet():
    User = get_user_model()
    
    print("🚀 CRÉATION DE DONNÉES DE TEST COMPLÈTES")
    print("=" * 60)
    
    # 1. Trouver ou créer GLORIA1 (pharmacien)
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
    
    # 2. Créer/s'assurer que GLORIA1 est pharmacien
    pharmacien, created = Pharmacien.objects.get_or_create(
        user=gloria,
        defaults={
            'nom_complet': 'Gloria Pharmacien',
            'telephone': '0123456789',
            'pharmacie_nom': 'Pharmacie Centrale'
        }
    )
    if created:
        print(f"🏥 Pharmacien créé: {pharmacien.nom_complet}")
    else:
        print(f"🏥 Pharmacien existant: {pharmacien.nom_complet}")
    
    # 3. Créer des médecins de test pour les conversations
    medecins_users = []
    medecins_noms = ['Dr. Martin', 'Dr. Dupont', 'Dr. Leroy']
    
    for i, nom in enumerate(medecins_noms, 1):
        username = f'medecin_test_{i}'
        try:
            user = User.objects.get(username=username)
            print(f"⚕️  Médecin existant: {username}")
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                email=f'{username}@hopital.com',
                password='medecin123'
            )
            print(f"⚕️  Médecin créé: {username}")
        
        # Créer le profil médecin
        medecin, _ = Medecin.objects.get_or_create(
            user=user,
            defaults={'nom_complet': nom, 'specialite': 'Généraliste'}
        )
        medecins_users.append(user)
    
    # 4. Créer des conversations
    conversations_creees = []
    sujets = [
        "Suivi traitement Amoxicilline",
        "Ordonnance #2024-00123",
        "Question sur posologie",
        "Disponibilité médicament",
        "Renouvellement ordonnance"
    ]
    
    for i, (medecin_user, sujet) in enumerate(zip(medecins_users, sujets), 1):
        # Créer conversation
        conv = Conversation.objects.create()
        conv.participants.add(gloria, medecin_user)
        
        # Messages de la conversation
        messages_texts = [
            f"Bonjour Docteur, je vous contacte concernant {sujet.lower()}.",
            f"Bonjour Pharmacien, je vous envoie les informations demandées.",
            f"Le patient doit prendre le traitement pendant 7 jours.",
            f"Merci, j'ai bien reçu. Je prépare les médicaments.",
            f"Le patient peut venir les récupérer demain matin."
        ]
        
        for j, texte in enumerate(messages_texts):
            expediteur = gloria if j % 2 == 0 else medecin_user
            Message.objects.create(
                conversation=conv,
                expediteur=expediteur,
                contenu=texte,
                date_envoi=timezone.now() - timedelta(hours=j)  # Messages à différents moments
            )
        
        conversations_creees.append(conv)
        print(f"💬 Conversation {i} créée avec {medecin_user.username}: '{sujet}'")
    
    # 5. Créer des notifications
    notifications_data = [
        {
            "titre": "⚠️ Stock faible: Paracétamol 500mg",
            "message": "Il reste seulement 15 boîtes en stock. Seuil d'alerte: 20 boîtes.",
            "type_notification": "warning",
            "lien": "/pharmacien/stock/"
        },
        {
            "titre": "✅ Ordonnance validée: #2024-00123",
            "message": "Ordonnance pour M. Dupont validée avec succès.",
            "type_notification": "success", 
            "lien": "/pharmacien/ordonnances/123/"
        },
        {
            "titre": "📋 Nouvelle ordonnance reçue",
            "message": "Nouvelle ordonnance du Dr. Martin en attente de validation.",
            "type_notification": "info",
            "lien": "/pharmacien/ordonnances/"
        },
        {
            "titre": "💬 Nouveau message du Dr. Leroy",
            "message": "Le Dr. Leroy vous a envoyé un message concernant le patient Moreau.",
            "type_notification": "primary",
            "lien": "/communication/messagerie/"
        },
        {
            "titre": "📅 Rappel: Inventaire mensuel",
            "message": "L'inventaire mensuel est prévu pour demain à 9h.",
            "type_notification": "secondary"
        }
    ]
    
    for i, notif_data in enumerate(notifications_data):
        Notification.objects.create(
            user=gloria,
            titre=notif_data["titre"],
            message=notif_data["message"],
            type_notification=notif_data.get("type_notification", "info"),
            lien=notif_data.get("lien", ""),
            est_lue=i % 3 == 0,  # 1/3 des notifications sont lues
            date_creation=timezone.now() - timedelta(hours=i*2)  # Dates différentes
        )
        print(f"🔔 Notification créée: '{notif_data['titre'][:30]}...'")
    
    # 6. Vérification finale
    print(f"\n🎉 DONNÉES CRÉÉES AVEC SUCCÈS:")
    print(f"   👤 Utilisateur: {gloria.username}")
    print(f"   🏥 Pharmacien: {pharmacien.nom_complet}")
    print(f"   💬 Conversations: {len(conversations_creees)}")
    print(f"   🔔 Notifications: {len(notifications_data)}")
    print(f"   ⚕️  Médecins: {len(medecins_users)}")
    
    # Statistiques
    conv_count = Conversation.objects.filter(participants=gloria).count()
    notif_count = Notification.objects.filter(user=gloria).count()
    notif_unread = Notification.objects.filter(user=gloria, est_lue=False).count()
    
    print(f"\n📊 STATISTIQUES FINALES:")
    print(f"   Conversations de GLORIA1: {conv_count}")
    print(f"   Notifications totales: {notif_count}")
    print(f"   Notifications non lues: {notif_unread}")
    
    print(f"\n🌐 URLS DE TEST:")
    print(f"   Dashboard: http://127.0.0.1:8000/pharmacien/dashboard/")
    print(f"   Messagerie: http://127.0.0.1:8000/communication/messagerie/")

if __name__ == "__main__":
    creer_donnees_test_complet()
