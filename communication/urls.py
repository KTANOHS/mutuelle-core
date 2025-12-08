# communication/urls.py - VERSION CORRIGÉE ET COMPLÈTE
from django.urls import path, include
from django.http import JsonResponse, HttpResponse
from . import views
from . import views_api

app_name = 'communication'

# =============================================================================
# URLS API SIMPLES (déplacé en premier pour éviter les duplications)
# =============================================================================
simple_api_patterns = [
    # API pour récupérer les messages d'une conversation
    path('api/simple/conversations/<int:conversation_id>/messages/', 
         views_api.api_conversation_messages_simple, 
         name='api_simple_conversation_messages'),
    
    # API pour envoyer un message
    path('api/simple/messages/send/', 
         views_api.api_send_message, 
         name='api_simple_send_message'),
    
    # API publique (sans authentification)
    path('api/public/test/', 
         views_api.api_public_test, 
         name='api_public_test'),
    
    path('api/public/conversations/<int:conversation_id>/messages/', 
         views_api.api_public_conversation_messages, 
         name='api_public_conversation_messages'),
]

# =============================================================================
# URLS PRINCIPALES
# =============================================================================
urlpatterns = [
    # =========================================================================
    # URL RACINE DU MODULE - LA PLUS IMPORTANTE !
    # =========================================================================
    path('', views.communication_home, name='communication_home'),
    
    # =========================================================================
    # MESSAGERIE ET CONVERSATIONS
    # =========================================================================
    path('messagerie/', views.messagerie, name='messagerie'),
    path('conversations/', views.conversations, name='conversations'),
    path('conversations/<int:conversation_id>/', views.detail_conversation, name='detail_conversation'),
    path('conversations/<int:conversation_id>/envoyer/', views.envoyer_message_conversation, name='envoyer_message_conversation'),
    
    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('messages/liste/', views.liste_messages, name='liste_messages'),
    path('messages/nouveau/', views.MessageCreateView.as_view(), name='message_create'),
    path('messages/envoyer/', views.envoyer_message, name='envoyer_message'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:message_id>/detail/', views.detail_message, name='detail_message'),
    path('messages/<int:message_id>/supprimer/', views.supprimer_message, name='supprimer_message'),
    
    # API Messages
    path('envoyer-message-api/', views.envoyer_message_api, name='envoyer_message_api'),
    path('api/messages/<int:message_id>/marquer-lu/', views.marquer_message_lu, name='marquer_message_lu'),
    
    # =========================================================================
    # NOTIFICATIONS - COMPLÈTES ET CORRIGÉES
    # =========================================================================
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('notifications/list/', views.NotificationListView.as_view(), name='liste_notifications'),
    path('notifications/count/', views.notification_non_lue_count, name='notifications_count'),
    path('notifications/marquer-lue/<int:notification_id>/', views.marquer_notification_lue, name='marquer_notification_lue'),
    path('notifications/marquer-toutes-lues/', views.marquer_toutes_notifications_lues, name='marquer_toutes_notifications_lues'),
    
    # =========================================================================
    # FICHIERS ET PIÈCES JOINTES
    # =========================================================================
    path('fichiers/', views.liste_fichiers, name='liste_fichiers'),
    path('fichier/<int:fichier_id>/telecharger/', views.telecharger_fichier, name='telecharger_fichier'),
    path('upload/', views.upload_fichier, name='upload_fichier'),
    
    # =========================================================================
    # GROUPES DE COMMUNICATION
    # =========================================================================
    path('groupes/', views.liste_groupes, name='liste_groupes'),
    path('groupes/creer/', views.creer_groupe, name='creer_groupe'),
    path('groupes/<int:groupe_id>/', views.detail_groupe, name='detail_groupe'),
    path('groupes/<int:groupe_id>/envoyer/', views.envoyer_message_groupe, name='envoyer_message_groupe'),
    
    # =========================================================================
    # STATISTIQUES ET RECHERCHE
    # =========================================================================
    path('stats/', views.stats_communication, name='stats_communication'),
    path('recherche/', views.search_messages, name='search_messages'),
    path('derniere-activite/', views.derniere_activite_api, name='derniere_activite'),
    
    # =========================================================================
    # API AJAX ET WEB SERVICES
    # =========================================================================
    path('api/conversations/', views.api_conversations, name='api_conversations'),
    path('api/messages/<int:conversation_id>/', views.api_messages, name='api_messages'),
    
    # =========================================================================
    # MESSAGERIE MULTI-ACTEURS
    # =========================================================================
    path('membre/messagerie/', views.messagerie_membre, name='messagerie_membre'),
    path('assureur/messagerie/', views.messagerie_assureur, name='messagerie_assureur'),
    path('medecin/messagerie/', views.messagerie_medecin, name='messagerie_medecin'),
    path('agent/messagerie/', views.messagerie_agent, name='messagerie_agent'),
    
    # =========================================================================
    # ALIAS POUR COMPATIBILITÉ
    # =========================================================================
    path('nouveau-message/', views.nouveau_message, name='nouveau_message'),
    
    path('agent/messages/', views.liste_messages_agent, name='liste_messages_agent'),
    path('agent/notifications/', views.liste_notifications_agent, name='liste_notifications_agent'),
    path('agent/envoyer-message/', views.envoyer_message_agent, name='envoyer_message_agent'),
    path('agent/messages/<int:message_id>/', views.detail_message_agent, name='detail_message_agent'),
    
    path('assureur/messages/', views.liste_messages_assureur, name='liste_messages_assureur'),
    path('assureur/notifications/', views.liste_notifications_assureur, name='liste_notifications_assureur'),
    path('assureur/envoyer-message/', views.envoyer_message_assureur, name='envoyer_message_assureur'),
    path('assureur/messages/<int:message_id>/', views.detail_message_assureur, name='detail_message_assureur'),
    path('pharmacien/', views.messagerie_pharmacien, name='messagerie_pharmacien'),
    
    # =========================================================================
    # PAGES DE TEST ET DIAGNOSTIC
    # =========================================================================
    path('test-ultime/', views.test_conversations_ultime, name='test_ultime'),
    path('test-messagerie/', views.test_messagerie, name='test_messagerie'),
    path('test-urgence/', views.test_urgence, name='test_urgence'),
    path('test-simple/', views.test_simple, name='test_simple'),
    path('test/messages/', lambda request: JsonResponse({'status': 'API test working'}), name='api_test'),
    
    # =========================================================================
    # INCLUSION DES URLS API SIMPLES
    # =========================================================================
    path('', include(simple_api_patterns)),
]