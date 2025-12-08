# communication/models.py - VERSION FINALE COMPLÈTE CORRIGÉE
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Conversation(models.Model):
    """Modèle pour gérer les conversations entre utilisateurs"""
    participants = models.ManyToManyField(User, related_name='conversations')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_modification']
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
    
    def __str__(self):
        return f"Conversation {self.id}"
    
    def get_dernier_message(self):
        """Retourne le dernier message de la conversation"""
        return self.messages.order_by('-date_envoi').first()
    
    def get_messages_non_lus(self, user):
        """Retourne les messages non lus pour un utilisateur"""
        return self.messages.filter(destinataire=user, est_lu=False)
    
    def get_nombre_messages_non_lus(self, user):
        """Retourne le nombre de messages non lus"""
        return self.get_messages_non_lus(user).count()

class Message(models.Model):
    """Modèle pour les messages entre utilisateurs"""
    TYPE_MESSAGE = [
        ('NOTIFICATION', 'Notification'),
        ('ALERTE', 'Alerte'), 
        ('MESSAGE', 'Message'),
        ('BON_SOIN', 'Bon de Soin'),
        ('DOCUMENT', 'Document'),
    ]
    
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_recus')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    titre = models.CharField(max_length=200, blank=True)
    contenu = models.TextField()
    type_message = models.CharField(max_length=20, choices=TYPE_MESSAGE, default='MESSAGE')
    date_envoi = models.DateTimeField(auto_now_add=True)
    est_lu = models.BooleanField(default=False)
    date_lecture = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date_envoi']
        verbose_name = "Message"
        verbose_name_plural = "Messages"
    
    def __str__(self):
        return f"Message {self.id} - {self.titre}"
    
    # MÉTHODES MANQUANTES AJOUTÉES
    def marquer_comme_lu(self):
        """Marque le message comme lu et met à jour la date de lecture"""
        if not self.est_lu:
            self.est_lu = True
            self.date_lecture = timezone.now()
            self.save()
        return self
    
    def marquer_comme_non_lu(self):
        """Marque le message comme non lu"""
        self.est_lu = False
        self.date_lecture = None
        self.save()
        return self
    
    def est_destinataire(self, user):
        """Vérifie si l'utilisateur est le destinataire du message"""
        return self.destinataire == user
    
    def peut_voir(self, user):
        """Vérifie si l'utilisateur peut voir ce message"""
        return user in [self.expediteur, self.destinataire]
    
    def repondre(self, expediteur, contenu, titre=None):
        """Crée une réponse à ce message"""
        if not titre:
            titre = f"RE: {self.titre}"
        
        return Message.objects.create(
            expediteur=expediteur,
            destinataire=self.expediteur,
            titre=titre,
            contenu=contenu,
            conversation=self.conversation
        )
    
    def get_contenu_tronque(self, longueur=100):
        """Retourne le contenu tronqué pour l'affichage"""
        if len(self.contenu) > longueur:
            return self.contenu[:longueur] + "..."
        return self.contenu

class Notification(models.Model):
    """Modèle pour les notifications système"""
    TYPE_NOTIFICATION = [
        ('INFO', 'Information'),
        ('ALERTE', 'Alerte'),
        ('SUCCES', 'Succès'), 
        ('ERREUR', 'Erreur'),
        ('BON_SOIN', 'Bon de Soin'),
        ('RDV', 'Rendez-vous'),
        ('PAIEMENT', 'Paiement'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    titre = models.CharField(max_length=200)
    message = models.TextField()
    type_notification = models.CharField(max_length=50, choices=TYPE_NOTIFICATION, default='INFO')
    est_lue = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_lecture = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
    
    def __str__(self):
        return f"Notification {self.id} - {self.titre}"
    
    # MÉTHODES MANQUANTES AJOUTÉES
    def marquer_comme_lue(self):
        """Marque la notification comme lue et met à jour la date de lecture"""
        if not self.est_lue:
            self.est_lue = True
            self.date_lecture = timezone.now()
            self.save()
        return self
    
    def marquer_comme_non_lue(self):
        """Marque la notification comme non lue"""
        self.est_lue = False
        self.date_lecture = None
        self.save()
        return self
    
    def get_message_tronque(self, longueur=100):
        """Retourne le message tronqué pour l'affichage"""
        if len(self.message) > longueur:
            return self.message[:longueur] + "..."
        return self.message
    
    def est_recente(self):
        """Vérifie si la notification a été créée récemment (moins de 24h)"""
        return (timezone.now() - self.date_creation).days < 1

class PieceJointe(models.Model):
    """Modèle pour gérer les pièces jointes des messages"""
    TYPES_FICHIERS = [
        ('PDF', 'Document PDF'),
        ('IMAGE', 'Image'),
        ('DOCUMENT', 'Document Word/Excel'),
        ('AUTRE', 'Autre type'),
    ]
    
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='pieces_jointes')
    fichier = models.FileField(upload_to='pieces_jointes/%Y/%m/%d/')
    nom_original = models.CharField(max_length=255)
    type_fichier = models.CharField(max_length=20, choices=TYPES_FICHIERS, default='AUTRE')
    taille = models.BigIntegerField(default=0, help_text="Taille en octets")
    date_upload = models.DateTimeField(auto_now_add=True)
    est_valide = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Pièce jointe"
        verbose_name_plural = "Pièces jointes"
        ordering = ['-date_upload']
    
    def __str__(self):
        return f"{self.nom_original} ({self.get_taille_lisible()})"
    
    def get_taille_lisible(self):
        """Retourne la taille dans un format lisible"""
        if self.taille < 1024:
            return f"{self.taille} o"
        elif self.taille < 1024 * 1024:
            return f"{self.taille / 1024:.1f} Ko"
        else:
            return f"{self.taille / (1024 * 1024):.1f} Mo"
    
    def save(self, *args, **kwargs):
        """Surcharge pour calculer automatiquement la taille et le type"""
        skip_file_validation = kwargs.pop('skip_file_validation', False)
        
        if self.fichier and not skip_file_validation:
            # Calculer la taille si le fichier est nouveau
            if not self.pk and self.fichier.size:
                self.taille = self.fichier.size
            
            # Déterminer le type de fichier basé sur l'extension
            nom_fichier = self.fichier.name.lower()
            if nom_fichier.endswith(('.pdf',)):
                self.type_fichier = 'PDF'
            elif nom_fichier.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
                self.type_fichier = 'IMAGE'
            elif nom_fichier.endswith(('.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx')):
                self.type_fichier = 'DOCUMENT'
        
        super().save(*args, **kwargs)
    
    def peut_etre_visualise(self):
        """Vérifie si le fichier peut être visualisé directement"""
        return self.type_fichier in ['PDF', 'IMAGE']


class GroupeCommunication(models.Model):
    """Groupes de communication (équipes, services, départements)"""
    TYPE_GROUPE = [
        ('EQUIPE', 'Équipe de travail'),
        ('SERVICE', 'Service/Département'),
        ('PROJET', 'Projet spécifique'),
        ('GENERAL', 'Général'),
    ]
    
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom du groupe")
    description = models.TextField(blank=True, verbose_name="Description")
    type_groupe = models.CharField(max_length=20, choices=TYPE_GROUPE, default='EQUIPE', verbose_name="Type de groupe")
    membres = models.ManyToManyField(User, related_name='groupes_communication', verbose_name="Membres")
    createur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groupes_crees', verbose_name="Créateur")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    est_actif = models.BooleanField(default=True, verbose_name="Groupe actif")
    est_public = models.BooleanField(default=False, verbose_name="Groupe public")
    code_acces = models.CharField(max_length=50, blank=True, verbose_name="Code d'accès")
    
    class Meta:
        verbose_name = "Groupe de communication"
        verbose_name_plural = "Groupes de communication"
        ordering = ['nom']
        indexes = [
            models.Index(fields=['nom']),
            models.Index(fields=['type_groupe']),
            models.Index(fields=['est_actif']),
        ]
    
    def __str__(self):
        return f"{self.nom} ({self.get_type_groupe_display()})"
    
    def get_membres_count(self):
        """Retourne le nombre de membres du groupe"""
        return self.membres.count()
    
    def ajouter_membre(self, user):
        """Ajouter un membre au groupe"""
        self.membres.add(user)
        return f"{user.get_full_name()} ajouté au groupe {self.nom}"
    
    def retirer_membre(self, user):
        """Retirer un membre du groupe"""
        self.membres.remove(user)
        return f"{user.get_full_name()} retiré du groupe {self.nom}"
    
    def est_membre(self, user):
        """Vérifier si un utilisateur est membre du groupe"""
        return self.membres.filter(id=user.id).exists()
    
    def get_dernier_message(self):
        """Retourne le dernier message du groupe"""
        return self.messages.order_by('-date_envoi').first()
    
    def get_statistiques(self):
        """Retourne les statistiques du groupe"""
        return {
            'membres': self.get_membres_count(),
            'messages': self.messages.count(),
            'actif': self.est_actif,
            'createur': self.createur.get_full_name() or self.createur.username,
        }

class MessageGroupe(models.Model):
    """Messages envoyés à des groupes de communication"""
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_groupe_envoyes', verbose_name="Expéditeur")
    groupe = models.ForeignKey(GroupeCommunication, on_delete=models.CASCADE, related_name='messages', verbose_name="Groupe")
    titre = models.CharField(max_length=200, blank=True, verbose_name="Titre")
    contenu = models.TextField(verbose_name="Contenu")
    type_message = models.CharField(max_length=20, choices=Message.TYPE_MESSAGE, default='MESSAGE', verbose_name="Type de message")
    date_envoi = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    est_important = models.BooleanField(default=False, verbose_name="Message important")
    pieces_jointes = models.ManyToManyField(PieceJointe, blank=True, related_name='messages_groupe', verbose_name="Pièces jointes")
    
    class Meta:
        verbose_name = "Message de groupe"
        verbose_name_plural = "Messages de groupe"
        ordering = ['-date_envoi']
        indexes = [
            models.Index(fields=['groupe', 'date_envoi']),
            models.Index(fields=['expediteur', 'date_envoi']),
        ]
    
    def __str__(self):
        return f"Message groupe {self.id} - {self.groupe.nom}"
    
    def get_contenu_tronque(self):
        """Retourne le contenu tronqué pour l'affichage"""
        return self.contenu[:100] + "..." if len(self.contenu) > 100 else self.contenu
    
    def marquer_comme_important(self):
        """Marquer le message comme important"""
        self.est_important = True
        self.save()
    
    def get_membres_cibles(self):
        """Retourne la liste des membres destinataires"""
        return self.groupe.membres.all()
    
    def get_pieces_jointes_count(self):
        """Retourne le nombre de pièces jointes"""
        return self.pieces_jointes.count()