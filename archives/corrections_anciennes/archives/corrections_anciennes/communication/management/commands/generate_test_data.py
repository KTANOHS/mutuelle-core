# communication/management/commands/generate_test_data.py
import os
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from communication.models import (
    Conversation, Message, Notification, PieceJointe, 
    GroupeCommunication, MessageGroupe
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Génère des données de test pour l\'application communication'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Nombre d\'utilisateurs à créer'
        )
        parser.add_argument(
            '--messages',
            type=int,
            default=50,
            help='Nombre de messages à créer'
        )
        parser.add_argument(
            '--notifications',
            type=int,
            default=30,
            help='Nombre de notifications à créer'
        )
        parser.add_argument(
            '--groups',
            type=int,
            default=5,
            help='Nombre de groupes à créer'
        )
        parser.add_argument(
            '--skip-files',
            action='store_true',
            help='Ignorer la création de pièces jointes'
        )
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Supprimer les données existantes avant de créer'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Début de la génération des données de test...'))
        
        # Option pour supprimer les données existantes
        if options['clear_existing']:
            self.clear_existing_data()
        
        # Créer des utilisateurs si nécessaire
        users = self.create_users(options['users'])
        
        # Créer des conversations et messages
        self.create_conversations_and_messages(users, options['messages'], options['skip_files'])
        
        # Créer des notifications
        self.create_notifications(users, options['notifications'])
        
        # Créer des groupes de communication
        self.create_groups(users, options['groups'])
        
        self.stdout.write(self.style.SUCCESS('✅ Génération des données de test terminée !'))

    def clear_existing_data(self):
        """Supprime les données existantes"""
        self.stdout.write('🗑️  Suppression des données existantes...')
        
        models_to_clear = [
            MessageGroupe,
            GroupeCommunication,
            PieceJointe,
            Message,
            Conversation,
            Notification,
        ]
        
        for model in models_to_clear:
            count, _ = model.objects.all().delete()
            if count > 0:
                self.stdout.write(f'   ✅ {count} {model._meta.verbose_name_plural} supprimés')

    def create_users(self, count):
        """Crée des utilisateurs de test"""
        self.stdout.write(f'👥 Création de {count} utilisateurs...')
        
        users = list(User.objects.all())
        
        # Si pas assez d'utilisateurs, en créer de nouveaux
        if len(users) < count:
            for i in range(len(users), count):
                username = f'user_test_{i}'
                email = f'user{i}@test.com'
                
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password='password123',
                        first_name=f'Prénom{i}',
                        last_name=f'Nom{i}'
                    )
                    users.append(user)
                    self.stdout.write(f'   ✅ Utilisateur créé: {username}')
        
        return users[:count]

    def create_conversations_and_messages(self, users, message_count, skip_files=False):
        """Crée des conversations et messages entre utilisateurs"""
        self.stdout.write(f'💬 Création de {message_count} messages...')
        
        types_message = ['NOTIFICATION', 'ALERTE', 'MESSAGE', 'BON_SOIN', 'DOCUMENT']
        conversations_created = 0
        messages_created = 0
        
        while messages_created < message_count:
            # Créer une conversation entre 2 utilisateurs aléatoires
            participant1, participant2 = random.sample(users, 2)
            
            # Vérifier si une conversation existe déjà entre ces utilisateurs
            conversation = Conversation.objects.filter(
                participants=participant1
            ).filter(
                participants=participant2
            ).first()
            
            if not conversation:
                conversation = Conversation.objects.create()
                conversation.participants.add(participant1, participant2)
                conversations_created += 1
                self.stdout.write(f'   ✅ Conversation créée: {participant1.username} ↔ {participant2.username}')
            
            # Créer 1-5 messages dans cette conversation
            num_messages = min(random.randint(1, 5), message_count - messages_created)
            
            for i in range(num_messages):
                # Alterner l'expéditeur
                expediteur = participant1 if i % 2 == 0 else participant2
                destinataire = participant2 if expediteur == participant1 else participant1
                
                message = Message.objects.create(
                    expediteur=expediteur,
                    destinataire=destinataire,
                    conversation=conversation,
                    titre=f"Sujet de conversation {messages_created + 1}",
                    contenu=self.generate_message_content(),
                    type_message=random.choice(types_message),
                    est_lu=random.choice([True, False]),
                    date_envoi=timezone.now() - timedelta(days=random.randint(0, 30))
                )
                
                # Marquer comme lu avec une date si c'est le cas
                if message.est_lu:
                    message.date_lecture = message.date_envoi + timedelta(hours=random.randint(1, 24))
                    message.save()
                
                messages_created += 1
                self.stdout.write(f'   📧 Message {messages_created}/{message_count} créé')
                
                # Créer occasionnellement une pièce jointe (sauf si skip_files=True)
                if not skip_files and random.random() < 0.2:  # 20% de chance
                    self.create_piece_jointe(message)
        
        self.stdout.write(f'   ✅ {conversations_created} conversations créées')
        self.stdout.write(f'   ✅ {messages_created} messages créés')

    def create_notifications(self, users, notification_count):
        """Crée des notifications pour les utilisateurs"""
        self.stdout.write(f'🔔 Création de {notification_count} notifications...')
        
        types_notification = ['INFO', 'ALERTE', 'SUCCES', 'ERREUR', 'BON_SOIN', 'RDV', 'PAIEMENT']
        titres_notifications = [
            "Nouveau message reçu",
            "Paiement confirmé",
            "Rendez-vous programmé",
            "Bon de soin validé",
            "Alerte système",
            "Mise à jour disponible",
            "Document à signer",
            "Échéance de paiement",
            "Nouvelle fonctionnalité",
            "Maintenance planifiée"
        ]
        
        for i in range(notification_count):
            user = random.choice(users)
            
            notification = Notification.objects.create(
                user=user,
                titre=random.choice(titres_notifications),
                message=self.generate_notification_content(),
                type_notification=random.choice(types_notification),
                est_lue=random.choice([True, False]),
                date_creation=timezone.now() - timedelta(days=random.randint(0, 15))
            )
            
            # Marquer comme lue avec une date si c'est le cas
            if notification.est_lue:
                notification.date_lecture = notification.date_creation + timedelta(hours=random.randint(1, 72))
                notification.save()
            
            self.stdout.write(f'   🔔 Notification {i+1}/{notification_count} créée pour {user.username}')

    def create_groups(self, users, group_count):
        """Crée des groupes de communication avec des messages"""
        self.stdout.write(f'👥 Création de {group_count} groupes de communication...')
        
        types_groupe = ['EQUIPE', 'SERVICE', 'PROJET', 'GENERAL']
        noms_groupes_base = [
            "Équipe Commerciale",
            "Service Médical", 
            "Projet Digital",
            "Support Client",
            "Administration",
            "Développement",
            "Communication",
            "Ressources Humaines",
            "Qualité",
            "Logistique",
            "Marketing",
            "Finance",
            "Juridique",
            "Technique",
            "Innovation"
        ]
        
        # Mélanger les noms pour éviter les doublons
        noms_groupes = random.sample(noms_groupes_base, min(group_count, len(noms_groupes_base)))
        
        for i, nom_groupe in enumerate(noms_groupes):
            createur = random.choice(users)
            
            # Vérifier si le groupe existe déjà
            groupe, created = GroupeCommunication.objects.get_or_create(
                nom=nom_groupe,
                defaults={
                    'description': f"Groupe de communication pour {nom_groupe.lower()}",
                    'type_groupe': random.choice(types_groupe),
                    'createur': createur,
                    'est_actif': True,
                    'est_public': random.choice([True, False])
                }
            )
            
            if created:
                self.stdout.write(f'   ✅ Groupe créé: {groupe.nom}')
            else:
                # Si le groupe existe déjà, on le met à jour
                groupe.description = f"Groupe de communication pour {nom_groupe.lower()} (mis à jour)"
                groupe.est_actif = True
                groupe.save()
                self.stdout.write(f'   🔄 Groupe existant mis à jour: {groupe.nom}')
            
            # Ajouter des membres au groupe (3-8 membres)
            membres = random.sample(users, random.randint(3, min(8, len(users))))
            groupe.membres.add(*membres)
            
            self.stdout.write(f'   👥 {len(membres)} membres ajoutés au groupe {groupe.nom}')
            
            # Créer quelques messages dans le groupe
            self.create_group_messages(groupe, random.randint(5, 15))

    def create_group_messages(self, groupe, message_count):
        """Crée des messages dans un groupe"""
        types_message = ['NOTIFICATION', 'ALERTE', 'MESSAGE', 'BON_SOIN', 'DOCUMENT']
        membres = list(groupe.membres.all())
        
        for i in range(message_count):
            expediteur = random.choice(membres)
            
            message = MessageGroupe.objects.create(
                expediteur=expediteur,
                groupe=groupe,
                titre=f"Message groupe {i+1}",
                contenu=self.generate_group_message_content(),
                type_message=random.choice(types_message),
                est_important=random.random() < 0.1,  # 10% de chance d'être important
                date_envoi=timezone.now() - timedelta(days=random.randint(0, 20))
            )
            
            self.stdout.write(f'   📢 Message de groupe {i+1}/{message_count} créé dans {groupe.nom}')

    def create_piece_jointe(self, message):
        """Crée une pièce jointe factice pour un message"""
        types_fichiers = ['PDF', 'IMAGE', 'DOCUMENT', 'AUTRE']
        noms_fichiers = [
            "document_important.pdf",
            "contrat_signé.docx",
            "photo_identite.jpg",
            "facture_mars.xlsx",
            "presentation.pptx",
            "bon_de_soin.pdf",
            "ordonnance_medicale.pdf"
        ]
        
        # Créer la pièce jointe sans utiliser le fichier réel
        piece_jointe = PieceJointe(
            message=message,
            nom_original=random.choice(noms_fichiers),
            type_fichier=random.choice(types_fichiers),
            taille=random.randint(1000, 5000000),  # 1KB à 5MB
            est_valide=True
        )
        
        # Sauvegarder en bypassant la validation du fichier
        piece_jointe.save(skip_file_validation=True)
        
        self.stdout.write(f'   📎 Pièce jointe créée: {piece_jointe.nom_original}')

    def generate_message_content(self):
        """Génère un contenu de message réaliste"""
        contenus = [
            "Bonjour, j'aimerais avoir des informations supplémentaires sur nos services.",
            "Merci pour votre message, je reviens vers vous rapidement.",
            "Pouvez-vous me confirmer la réception de ce document ?",
            "Je vous envoie les documents demandés en pièce jointe.",
            "Notre prochaine réunion est prévue pour la semaine prochaine.",
            "J'ai bien pris note de vos commentaires, merci.",
            "Pourriez-vous me rappeler au sujet de ce dossier ?",
            "Je vous confirme la bonne réception de votre demande.",
            "Voici les informations que vous m'avez demandées.",
            "Merci de votre rapidité à traiter ce dossier."
        ]
        return random.choice(contenus)

    def generate_notification_content(self):
        """Génère un contenu de notification réaliste"""
        contenus = [
            "Votre demande a été traitée avec succès.",
            "Un nouveau document est disponible dans votre espace.",
            "Pensez à mettre à jour vos informations personnelles.",
            "Votre rendez-vous est confirmé pour demain.",
            "Alerte : action requise de votre part.",
            "Félicitations ! Votre compte a été activé.",
            "Rappel : échéance de paiement dans 3 jours.",
            "Nouveau message dans votre boîte de réception.",
            "Maintenance système prévue ce week-end.",
            "Votre profil a été mis à jour avec succès."
        ]
        return random.choice(contenus)

    def generate_group_message_content(self):
        """Génère un contenu de message de groupe réaliste"""
        contenus = [
            "Bonjour à tous, je vous informe de la nouvelle procédure.",
            "N'oubliez pas notre réunion de demain à 10h.",
            "Quelqu'un pourrait m'aider sur ce dossier ?",
            "Les documents sont disponibles dans le dossier partagé.",
            "Merci pour votre travail sur le dernier projet.",
            "Rappel : date limite pour les rapports dans 2 jours.",
            "Bienvenue aux nouveaux membres de l'équipe !",
            "Je serai absent demain, merci de prendre le relais.",
            "Les résultats du dernier trimestre sont excellents !",
            "Pensez à mettre à jour vos compétences avec la nouvelle formation."
        ]
        return random.choice(contenus)