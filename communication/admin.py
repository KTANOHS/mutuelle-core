from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Conversation, Message, Notification, PieceJointe, 
    GroupeCommunication, MessageGroupe
)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_participants', 'date_creation', 'date_modification']
    list_filter = ['date_creation', 'date_modification']
    search_fields = ['participants__username', 'participants__first_name', 'participants__last_name']
    filter_horizontal = ['participants']
    readonly_fields = ['date_creation', 'date_modification']
    
    # ✅ CORRECTION : Toujours définir actions comme liste
    actions = []
    
    def get_participants(self, obj):
        return ", ".join([user.get_full_name() or user.username for user in obj.participants.all()[:3]])
    get_participants.short_description = 'Participants'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'expediteur', 'destinataire', 'type_message', 'est_lu', 'date_envoi']
    list_filter = ['type_message', 'est_lu', 'date_envoi']
    search_fields = [
        'expediteur__username', 'expediteur__first_name', 'expediteur__last_name',
        'destinataire__username', 'destinataire__first_name', 'destinataire__last_name',
        'titre', 'contenu'
    ]
    readonly_fields = ['date_envoi']
    date_hierarchy = 'date_envoi'
    
    # ✅ CORRECTION : Définir actions
    actions = []
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('expediteur', 'destinataire', 'conversation', 'type_message')
        }),
        ('Contenu du message', {
            'fields': ('titre', 'contenu')
        }),
        ('Statut et dates', {
            'fields': ('est_lu', 'date_lecture', 'date_envoi')
        })
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'titre', 'type_notification', 'est_lue', 'date_creation']
    list_filter = ['type_notification', 'est_lue', 'date_creation']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'titre', 'message']
    readonly_fields = ['date_creation']
    date_hierarchy = 'date_creation'
    
    def mark_as_read(self, request, queryset):
        queryset.update(est_lue=True)
        self.message_user(request, f"{queryset.count()} notifications marquées comme lues.")
    mark_as_read.short_description = "Marquer comme lu"
    
    # ✅ CORRECTION : Utiliser le nom de la méthode en string
    actions = ['mark_as_read']

@admin.register(PieceJointe)
class PieceJointeAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom_original', 'message', 'type_fichier', 'get_taille_lisible_admin', 'date_upload', 'est_valide']
    list_filter = ['type_fichier', 'est_valide', 'date_upload']
    search_fields = ['nom_original', 'message__contenu']
    readonly_fields = ['date_upload', 'taille', 'type_fichier']
    
    # ✅ CORRECTION : Définir actions
    actions = []
    
    def get_taille_lisible_admin(self, obj):
        return obj.get_taille_lisible()
    get_taille_lisible_admin.short_description = 'Taille'
    
    def peut_etre_visualise_display(self, obj):
        if obj.peut_etre_visualise():
            return format_html('<span style="color: green;">✓</span> Oui')
        return format_html('<span style="color: red;">✗</span> Non')
    peut_etre_visualise_display.short_description = 'Visualisable'

@admin.register(GroupeCommunication)
class GroupeCommunicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'type_groupe', 'get_membres_count', 'createur', 'est_actif', 'est_public', 'date_creation']
    list_filter = ['type_groupe', 'est_actif', 'est_public', 'date_creation']
    search_fields = ['nom', 'description', 'createur__username']
    filter_horizontal = ['membres']
    readonly_fields = ['date_creation', 'date_modification']
    
    # ✅ CORRECTION : Définir actions
    actions = []
    
    fieldsets = (
        ('Informations du groupe', {
            'fields': ('nom', 'description', 'type_groupe', 'createur')
        }),
        ('Paramètres', {
            'fields': ('est_actif', 'est_public', 'code_acces')
        }),
        ('Membres', {
            'fields': ('membres',)
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification')
        })
    )
    
    def get_membres_count(self, obj):
        return obj.get_membres_count()
    get_membres_count.short_description = 'Nb membres'
    
    def get_dernier_message_display(self, obj):
        dernier_message = obj.get_dernier_message()
        if dernier_message:
            return f"{dernier_message.expediteur.username} - {dernier_message.date_envoi.strftime('%d/%m/%Y %H:%M')}"
        return "Aucun message"
    get_dernier_message_display.short_description = 'Dernier message'

@admin.register(MessageGroupe)
class MessageGroupeAdmin(admin.ModelAdmin):
    list_display = ['id', 'expediteur', 'groupe', 'type_message', 'est_important', 'date_envoi', 'get_pieces_jointes_count']
    list_filter = ['type_message', 'est_important', 'date_envoi', 'groupe']
    search_fields = [
        'expediteur__username', 'expediteur__first_name', 'expediteur__last_name',
        'groupe__nom', 'titre', 'contenu'
    ]
    readonly_fields = ['date_envoi']
    filter_horizontal = ['pieces_jointes']
    date_hierarchy = 'date_envoi'
    
    # ✅ CORRECTION : Définir actions
    actions = []
    
    fieldsets = (
        ('Informations du message', {
            'fields': ('expediteur', 'groupe', 'type_message', 'est_important')
        }),
        ('Contenu', {
            'fields': ('titre', 'contenu')
        }),
        ('Pièces jointes', {
            'fields': ('pieces_jointes',)
        }),
        ('Date', {
            'fields': ('date_envoi',)
        })
    )
    
    def get_pieces_jointes_count(self, obj):
        return obj.get_pieces_jointes_count()
    get_pieces_jointes_count.short_description = 'Nb pièces jointes'
    
    def get_contenu_tronque_display(self, obj):
        return obj.get_contenu_tronque()
    get_contenu_tronque_display.short_description = 'Contenu (tronqué)'

# Configuration de l'interface d'administration
admin.site.site_header = "Administration de la Communication"
admin.site.site_title = "Système de Communication"
admin.site.index_title = "Gestion de la communication"