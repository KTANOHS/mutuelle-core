# agents/urls.py - VERSION COMPLÈTEMENT CORRIGÉE SANS DOUBLONS

from django.urls import path, include
from . import views

app_name = 'agents'

urlpatterns = [
    # =========================================================================
    # URLs TABLEAU DE BORD
    # =========================================================================
    path('', views.dashboard, name='dashboard'),
    path('tableau-de-bord/', views.dashboard, name='dashboard'),
    
    # =========================================================================
    # URLs GESTION DES MEMBRES
    # =========================================================================
    path('creer-membre/', views.creer_membre, name='creer_membre'),
    path('liste-membres/', views.liste_membres, name='liste_membres'),

    # =========================================================================
    # URLs VÉRIFICATION COTISATIONS
    # =========================================================================
    path('verification-cotisations/', views.verification_cotisations, name='verification_cotisations'),
    path('rapport-performance/', views.rapport_performance, name='rapport_performance'),
    path('fiche-cotisation/<int:membre_id>/', views.afficher_fiche_cotisation, name='fiche_cotisation'),
    path('recherche-cotisations/', views.recherche_cotisations_avancee, name='recherche_cotisations_avancee'),
    path('fiche-cotisation-unifiee/<int:membre_id>/', 
         views.afficher_fiche_cotisation_unifiee_view, 
         name='fiche_cotisation_unifiee'),

    
    # =========================================================================
    # URLs API RECHERCHE ET VÉRIFICATION
    # =========================================================================
    path('api/recherche-membres/', views.recherche_membres_api, name='recherche_membres_api'),
    path('api/verifier-cotisation/', views.verifier_cotisation_api, name='verifier_cotisation_api'),
    path('api/test-simple/', views.test_simple_api, name='test_simple_api'),
    path('api/verifier-cotisation/<int:membre_id>/', views.verifier_cotisation_api, name='verifier_cotisation_api'),
    
    # =========================================================================
    # URLs GESTION BONS DE SOIN
    # =========================================================================
    path('creer-bon-soin/', views.creer_bon_soin, name='creer_bon_soin'),
    path('creer-bon-soin/<int:membre_id>/', views.creer_bon_soin_membre, name='creer_bon_soin_membre'),
    path('confirmation-bon-soin/<int:bon_id>/', views.confirmation_bon_soin, name='confirmation_bon_soin'),
    path('historique-bons/', views.historique_bons, name='historique_bons'),
    
    # =========================================================================
    # URLs API BONS DE SOIN
    # =========================================================================
    path('api/recherche-membres-bon-soin/', views.api_recherche_membres_bon_soin, name='api_recherche_membres_bon_soin'),
    path('api/bons/<int:bon_id>/details/', views.details_bon_soin_api, name='details_bon_soin_api'),

    # =========================================================================
    # URLs COMMUNICATION
    # =========================================================================
    path('communication/', views.get_stats_communication, name='communication'),
    path('messages/', views.liste_messages_agent, name='liste_messages'),
    path('notifications/', views.liste_notifications_agent, name='liste_notifications'),
    path('envoyer-message/', views.envoyer_message_agent, name='envoyer_message'),
    path('debug-recherche/', views.debug_recherche_membres, name='debug_recherche'),
    path('rechercher-membre/', views.rechercher_membre, name='rechercher_membre'),
    path('membre/<int:membre_id>/', views.details_membre, name='details_membre'),
]