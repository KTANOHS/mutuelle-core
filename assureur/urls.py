"""
URLs pour l'application assureur - Version complète et CORRIGÉE
Toutes les vues correspondent aux fonctions existantes dans assureur.views
"""
from django.urls import path, include
from . import views
from . import views_correction

app_name = 'assureur'

urlpatterns = [
    # ==========================================================================
    # DASHBOARD ET ACCUEIL
    # ==========================================================================
    path('', views.dashboard_assureur, name='dashboard'),
    path('test/', views.test_assureur, name='test'),
    path('diagnostic/', views.diagnostic_assureur, name='diagnostic'),
    path('dashboard-simple/', views.dashboard_simple, name='dashboard_simple'),
    
    # ==========================================================================
    # GESTION DES MEMBRES
    # ==========================================================================
    path('membres/', views.liste_membres, name='liste_membres'),
    path('membres/creer/', views.creer_membre, name='creer_membre'),
    path('membres/<int:membre_id>/', views.detail_membre, name='detail_membre'),
    path('membres/recherche/', views.recherche_membre, name='recherche_membre'),
    
    # ==========================================================================
    # GESTION DES BONS DE PRISE EN CHARGE
    # ==========================================================================
    path('bons/', views.liste_bons, name='liste_bons'),
    path('bons/creer/', views.creer_bon, name='creer_bon'),
    path('bons/creer-pour-membre/<int:membre_id>/', views.creer_bon_pour_membre, name='creer_bon_pour_membre'),
    path('bons/<int:bon_id>/', views.detail_bon, name='detail_bon'),
    path('bons/<int:bon_id>/valider/', views.valider_bon, name='valider_bon'),
    path('bons/<int:bon_id>/rejeter/', views.rejeter_bon, name='rejeter_bon'),
    
    # ==========================================================================
    # GESTION DES SOINS
    # ==========================================================================
    path('soins/', views.liste_soins, name='liste_soins'),
    path('soins/<int:soin_id>/', views.detail_soin, name='detail_soin'),
    path('soins/<int:soin_id>/valider/', views.valider_soin, name='valider_soin'),
    path('soins/<int:soin_id>/rejeter/', views.rejeter_soin, name='rejeter_soin'),
    
    # ==========================================================================
    # GESTION DES PAIEMENTS
    # ==========================================================================
    path('paiements/', views.liste_paiements, name='liste_paiements'),
    path('paiements/creer/', views.creer_paiement, name='creer_paiement'),
    path('paiements/<int:paiement_id>/valider/', views.valider_paiement, name='valider_paiement'),
    path('paiements/<int:paiement_id>/annuler/', views.annuler_paiement, name='annuler_paiement'),
    path('paiements/<int:paiement_id>/', views.detail_paiement, name='detail_paiement'),

       
    
    # ==========================================================================
    # GESTION DES COTISATIONS
    # ==========================================================================
    path('cotisations/', views.liste_cotisations, name='liste_cotisations'),
    path('cotisations/generer/', views.generer_cotisations, name='generer_cotisations'),
    path('cotisations/<int:cotisation_id>/paiement/', 
         views.enregistrer_paiement_cotisation, 
         name='enregistrer_paiement_cotisation'),
    path('cotisations/preview/', views.preview_generation, name='preview_generation'),

        # Nouvelles URLs pour gestion individuelle
    path('cotisations/creer/', views.creer_cotisation_membre, name='creer_cotisation'),
    path('cotisations/creer/<int:membre_id>/', views.creer_cotisation_membre, name='creer_cotisation_membre'),
    path('cotisations/<int:cotisation_id>/editer/', views.editer_cotisation, name='editer_cotisation'),
    path('cotisations/<int:cotisation_id>/supprimer/', views.supprimer_cotisation, name='supprimer_cotisation'),
    path('cotisations/<int:cotisation_id>/paiement/', views.enregistrer_paiement_cotisation, name='enregistrer_paiement_cotisation'),
    
    # ==========================================================================
    # STATISTIQUES ET RAPPORTS - CORRECTIONS APPLIQUÉES
    # ==========================================================================
    path('statistiques/', views.statistiques_assureur, name='statistiques'),
    path('rapports/', views.rapports, name='rapports'),
    path('rapports/generer/', views.generer_rapport, name='generer_rapport'),
    path('rapports/<int:rapport_id>/', views.detail_rapport, name='detail_rapport'),
    path('rapports/<int:rapport_id>/export/', views.export_rapport, name='export_rapport'),
    path('rapport-statistiques/', views.statistiques_assureur, name='rapport_statistiques'),
    
    # ==========================================================================
    # CONFIGURATION - CORRECTION APPLIQUÉE
    # ==========================================================================
    path('configuration/', views.configuration_assureur, name='configuration'),
    
    # ==========================================================================
    # API ENDPOINTS (AJAX/JSON) - CORRECTIONS APPLIQUÉES
    # ==========================================================================
    path('api/bons/creer/<int:membre_id>/', views.api_creer_bon, name='api_creer_bon'),
    path('api/bons/<int:bon_id>/valider/', views.api_valider_bon, name='api_valider_bon'),
    path('api/stats/', views.api_statistiques, name='api_get_stats'),
    path('api/membres/recherche/', views.api_recherche_membre, name='api_recherche_membre'),
    
    # ==========================================================================
    # URL CRITIQUE POUR LE FILTRE SOINS - CORRECTION APPLIQUÉE
    # ==========================================================================
    path('api/soins-par-membre/<int:membre_id>/', views.get_soins_par_membre, name='api_soins_par_membre'),
       
    
    # ==========================================================================
    # EXPORT DE DONNÉES
    # ==========================================================================
    path('export/<str:type_donnees>/', views.export_donnees, name='export_donnees'),
    
    
    # ==========================================================================
    # COMMUNICATION (INTÉGRATION AVEC L'APP COMMUNICATION)
    # ==========================================================================
    path('communication/', views.messagerie_assureur, name='messagerie_assureur'),
    path('communication/envoyer/', views.envoyer_message_assureur, name='envoyer_message_assureur'),
    
    # ==========================================================================
    # URLS DE COMPATIBILITÉ (pour les anciennes URLs)
    # ==========================================================================
    path('liste-membres/', views.liste_membres, name='liste_membres_old'),
    path('liste-bons/', views.liste_bons, name='liste_bons_old'),
    path('bons/creer/<str:membre_id>/', views.api_creer_bon, name='creer_bon_old'),
    path('dashboard-soins/', views.dashboard_assureur, name='dashboard_soins'),
    
    # ==========================================================================
    # URLS D'ADMINISTRATION ASSUREUR - CORRECTIONS APPLIQUÉES
    # ==========================================================================
    path('admin-assureur/', include([
        path('dashboard/', views.dashboard_assureur, name='admin_dashboard'),
        path('configuration/', views.configuration_assureur, name='admin_configuration'),
        path('rapports/', views.rapports, name='admin_rapports'),
    ])),
]