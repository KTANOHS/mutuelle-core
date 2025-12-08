"""
URLs de test pour la communication assureur
À intégrer dans votre fichier assureur/urls.py
"""

from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # Page de messagerie
    path('communication/', 
         TemplateView.as_view(template_name='assureur/communication/messagerie.html'),
         name='messagerie_assureur'),
    
    # Page d'envoi de message
    path('communication/envoyer/',
         TemplateView.as_view(template_name='assureur/communication/envoyer_message.html'),
         name='envoyer_message_assureur'),
    
    # Page de liste des messages
    path('communication/messages/',
         TemplateView.as_view(template_name='assureur/communication/liste_messages.html'),
         name='liste_messages_assureur'),
    
    # Page de notifications
    path('communication/notifications/',
         TemplateView.as_view(template_name='assureur/communication/liste_notifications.html'),
         name='liste_notifications_assureur'),
]
