# pharmacien/urls.py - VERSION CORRIGÉE

from django.urls import path
from . import views

app_name = 'pharmacien'

urlpatterns = [
    # ==================== DASHBOARD ET PAGES PRINCIPALES ====================
    path('dashboard/', views.dashboard_pharmacien, name='dashboard'),
    path('ordonnances/', views.liste_ordonnances_attente, name='liste_ordonnances_attente'),
    
    # ==================== GESTION DES ORDONNANCES ====================
    path('ordonnances/<int:ordonnance_id>/', views.detail_ordonnance, name='detail_ordonnance'),
    path('ordonnances/<int:ordonnance_id>/valider/', views.valider_ordonnance, name='valider_ordonnance'),
    path('ordonnances/<int:ordonnance_id>/refuser/', views.refuser_ordonnance, name='refuser_ordonnance'),

    path('validation/', views.liste_ordonnances_attente, name='validation_ordonnances'),
    # ==================== HISTORIQUE ET RECHERCHE ====================
    path('historique/', views.historique_validation, name='historique_validation'),
    path('export-historique/', views.export_historique, name='export_historique'),
    path('recherche/', views.rechercher_ordonnances, name='rechercher_ordonnances'),
    path('filtre/', views.filtrer_ordonnances, name='filtrer_ordonnances'),
    
    # ==================== PROFIL ====================
    path('profil/', views.profil_pharmacien, name='profil_pharmacien'),
    
    # ==================== GESTION DU STOCK ====================
    path('stock/', views.gestion_stock, name='stock'),
    path('stock/ajouter/', views.ajouter_stock, name='ajouter_stock'),
    path('stock/importer/', views.importer_stock, name='importer_stock'),
    path('stock/export/', views.export_stock, name='export_stock'),
    path('stock/<int:stock_id>/modifier/', views.modifier_stock, name='modifier_stock'),
    path('stock/<int:stock_id>/reapprovisionner/', views.reapprovisionner_stock, name='reapprovisionner_stock'),
    path('stock/<int:stock_id>/activer/', views.activer_stock, name='activer_stock'),
    path('stock/<int:stock_id>/desactiver/', views.desactiver_stock, name='desactiver_stock'),
    
    # ==================== API AJAX ====================
    path('api/ordonnances-attente/', views.api_ordonnances_attente, name='api_ordonnances_attente'),
    path('api/statistiques-temps-reel/', views.api_statistiques_temps_reel, name='api_statistiques_temps_reel'),
    path('api/statistiques-pharmacien/', views.api_statistiques_pharmacien, name='api_statistiques_pharmacien'),


    path('test/', views.test_affichage, name='test_affichage'),
    path('test-public/', views.test_public, name='test_public'),
    path('debug-data/', views.debug_data, name='debug_data'),
]