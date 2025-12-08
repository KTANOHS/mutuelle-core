from django.urls import path
from . import views

app_name = 'membres'

urlpatterns = [
    # ==========================================================================
    # URLs PUBLIQUES
    # ==========================================================================
    path('inscription/', views.inscription_membre, name='inscription'),
    path('liste/', views.liste_membres, name='liste_membres'),
    path('detail/<int:membre_id>/', views.detail_membre, name='detail_membre'),
    
    # ==========================================================================
    # URLs MEMBRES CONNECTÉS
    # ==========================================================================
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profil/', views.mon_profil, name='mon_profil'),
    path('soins/', views.mes_soins, name='mes_soins'),
    path('cotisations/', views.historique_cotisations, name='historique_cotisations'),
    path('paiements/', views.mes_paiements, name='mes_paiements'),
    path('solde-remboursements/', views.solde_remboursements, name='solde_remboursements'),
    path('paiements/<int:paiement_id>/', views.detail_mon_paiement, name='detail_mon_paiement'),


    path('creer/', views.creer_membre, name='creer_membre'),
    path('mes-membres/', views.liste_membres_agent, name='liste_membres_agent'),
    path('documents/<int:membre_id>/', views.upload_documents_membre, name='upload_documents'),
    
    # ==========================================================================
    # URLs VUES BASÉES SUR LES CLASSES
    # ==========================================================================
    path('ordonnances/', views.MesOrdonnancesView.as_view(), name='mes_ordonnances'),
    path('bons/', views.MesBonsView.as_view(), name='mes_bons'),
    path('ordonnances/<int:ordonnance_id>/', views.DetailOrdonnanceMembreView.as_view(), name='detail_ordonnance'),
    path('ordonnance-patient/<int:ordonnance_id>/', views.DetailOrdonnanceMembreView.as_view(), name='detail_ordonnance_patient'),
    
    # ==========================================================================
    # URLs ADMIN/AGENT
    # ==========================================================================
    path('admin/dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('admin/membres/', views.liste_membres_admin, name='liste_membres_admin'),
    path('admin/statistiques/', views.statistiques_avancees, name='statistiques_avancees'),
    path('admin/analytics/', views.dashboard_analytics, name='dashboard_analytics'),
    
    # Validation des documents
    path('validation/documents/<int:membre_id>/', views.validation_documents, name='validation_documents'),
    path('validation/liste-attente/', views.liste_membres_attente_validation, name='liste_membres_attente_validation'),
    
    # ==========================================================================
    # URLs API POUR AJAX
    # ==========================================================================
    path('api/statistiques-membres/', views.api_statistiques_membres, name='api_statistiques_membres'),
    path('api/statistiques-soins/', views.api_statistiques_soins, name='api_statistiques_soins'),
    path('api/analytics-data/', views.api_analytics_data, name='api_analytics_data'),
    
    # ==========================================================================
    # URLs UTILITAIRES
    # ==========================================================================
    path('recherche/', views.recherche_membres, name='recherche_membres'),
    path('export-analytics-csv/', views.export_analytics_csv, name='export_analytics_csv'),
    path('test-auth/', views.test_auth, name='test_auth'),
    path('export-analytics-excel/', views.export_analytics_excel, name='export_analytics_excel'),
]