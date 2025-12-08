from django.contrib import admin
from .models import Message, Conversation, PieceJointe, Notification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['expediteur', 'destinataire', 'titre', 'date_envoi', 'est_lu']
    list_filter = ['est_lu', 'date_envoi']
    search_fields = ['titre', 'contenu']

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'date_creation', 'date_modification']
    list_filter = ['date_creation']
    filter_horizontal = ['participants']

@admin.register(PieceJointe)
class PieceJointeAdmin(admin.ModelAdmin):
    list_display = ['message', 'nom_original', 'date_upload']
    list_filter = ['date_upload']
    search_fields = ['nom_original']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'titre', 'date_creation', 'est_lue']
    list_filter = ['est_lue', 'date_creation', 'type_notification']
    search_fields = ['titre', 'message']  # Correction: 'message' au lieu de 'contenu'

@admin.register(GroupeCommunication)
class GroupeCommunicationAdmin(admin.ModelAdmin):
    list_display = ['nom', 'date_creation']
    filter_horizontal = ['membres']
    search_fields = ['nom']

@admin.register(MessageGroupe)
class MessageGroupeAdmin(admin.ModelAdmin):
    list_display = ['expediteur', 'groupe', 'date_envoi']
    list_filter = ['date_envoi', 'groupe']
    search_fields = ['contenu']