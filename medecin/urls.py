from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'medecin'

urlpatterns = [
    # ==========================================================================
    # DASHBOARD ET ACCUEIL
    # ==========================================================================
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ordonnances/', views.liste_ordonnances, name='liste_ordonnances'),

    path('', views.dashboard, name='dashboard_root'),  # Redirection vers dashboard
    
    # ==========================================================================
    # BONS DE SOIN
    # ==========================================================================
    path('bons/', views.liste_bons, name='liste_bons'),
    path('bons/attente/', views.liste_bons_attente, name='liste_bons_attente'),
    path('bons/<int:bon_id>/', views.detail_bon_soin, name='detail_bon_soin'),
    path('bons/<int:bon_id>/valider/', views.valider_bon_soin, name='valider_bon_soin'),
    path('bons/<int:bon_id>/refuser/', views.refuser_bon_soin, name='refuser_bon_soin'),
    
    # ==========================================================================
    # ORDONNANCES
    # ==========================================================================
    path('ordonnances/creer/', views.creer_ordonnance, name='creer_ordonnance'),
    path('ordonnances/', views.mes_ordonnances, name='mes_ordonnances'),
    path('ordonnances/historique/', views.historique_ordonnances, name='historique_ordonnances'),
    path('ordonnances/<int:ordonnance_id>/', views.detail_ordonnance, name='detail_ordonnance'),
    
    # ==========================================================================
    # CONSULTATIONS ET RENDEZ-VOUS
    # ==========================================================================
    path('rendez-vous/', views.mes_rendez_vous, name='mes_rendez_vous'),
    path('consultations/', views.mes_rendez_vous, name='liste_consultations'),  # Alias
    path('consultations/creer/', views.creer_consultation, name='creer_consultation'),
    path('consultations/creer/<int:rendez_vous_id>/', views.creer_consultation, name='creer_consultation_rdv'),
    path('consultations/creer/patient/<int:patient_id>/', views.creer_consultation, name='creer_consultation_patient'),  # ✅ AJOUTÉ
    path('consultations/<int:consultation_id>/', views.detail_consultation, name='detail_consultation'),
    path('rendez-vous/<int:rdv_id>/modifier-statut/', views.modifier_statut_rdv, name='modifier_statut_rdv'),  # ✅ AJOUTÉ
    
    # ==========================================================================
    # SUIVI MALADIES CHRONIQUES
    # ==========================================================================
    path('suivi-chronique/', views.tableau_bord_suivi, name='tableau_bord_suivi'),
    path('suivi-chronique/accompagnements/', views.liste_accompagnements, name='liste_accompagnements'),
    path('suivi-chronique/accompagnements/creer/', views.creer_accompagnement, name='creer_accompagnement'),
    path('suivi-chronique/accompagnements/creer/<int:patient_id>/', views.creer_accompagnement, name='creer_accompagnement_patient'),
    path('suivi-chronique/accompagnements/<int:programme_id>/', views.detail_accompagnement, name='detail_accompagnement'),
    path('suivi-chronique/accompagnements/<int:programme_id>/suivi/', views.ajouter_suivi, name='ajouter_suivi'),
    
    # ==========================================================================
    # PROFIL ET STATISTIQUES
    # ==========================================================================
    path('profil/', views.profil_medecin, name='profil_medecin'),
    path('statistiques/', views.statistiques, name='statistiques'),
    path('notifications/', views.liste_notifications, name='liste_notifications'),
    
    # ==========================================================================
    # API ET ACTIONS AJAX
    # ==========================================================================
    path('api/statistiques/', views.api_statistiques, name='api_statistiques'),
    path('api/toggle-disponibilite/', views.api_toggle_disponibilite, name='api_toggle_disponibilite'),
    path('api/ajouter-medicament/', views.ajouter_medicament, name='ajouter_medicament'),
    path('api/suivi-chronique/stats/', views.api_stats_suivi, name='api_stats_suivi'),
    
    # ==========================================================================
    # PAGES STATIQUES ET OUTILS
    # ==========================================================================
    path('diagnostic-rendez-vous/', TemplateView.as_view(template_name='medecin/diagnostic_rendez_vous.html'), name='diagnostic_rendez_vous'),
    
    # ==========================================================================
    # ALIAS POUR COMPATIBILITÉ (à supprimer progressivement)
    # ==========================================================================
    path('bons-attente/', views.liste_bons_attente, name='bons_attente'),  # Alias pour compatibilité
    # AJOUTEZ CETTE LIGNE DANS urlpatterns
    path('dashboard-medecin/', views.dashboard, name='dashboard_medecin'),  # Alias pour compatibilité
]