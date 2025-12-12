# mutuelle_core/urls.py - VERSION COMPLÈTEMENT CORRIGÉE
from django.contrib import admin
from django.urls import path, include
from agents.views import details_bon_soin_api
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse  # <-- AJOUT IMPORT MANQUANT

def health_check(request):
    """Simple health check pour Render"""
    return HttpResponse("OK", status=200)

urlpatterns = [
    # ========================
    # PAGES PRINCIPALES
    # ========================
    path('api/agents/bons/<int:bon_id>/details/', details_bon_soin_api, name='api_details_bon_global'),
    path('', views.home, name='home'),
    path('redirect-after-login/', views.redirect_to_user_dashboard, name='redirect_after_login'),
    path('rapports/', views.rapports, name='rapports'),
    path('rapports/statistiques/', views.rapport_statistiques, name='rapport_statistiques'),
    path('health/', health_check, name='health_check'),
    path('', include('core.urls', namespace='core')),

    
    # ========================
    # DASHBOARDS SPÉCIFIQUES - AVEC AGENTS
    # ========================
    path('agent-dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assureur-dashboard/', views.assureur_dashboard, name='assureur_dashboard'),
    path('medecin-dashboard/', views.medecin_dashboard, name='medecin_dashboard'),
    path('pharmacien-dashboard/', views.pharmacien_dashboard, name='pharmacien_dashboard'),
    path('membre-dashboard/', views.membre_dashboard, name='membre_dashboard'),
    path('generic-dashboard/', views.generic_dashboard, name='generic_dashboard'),
    
    # ========================
    # APPLICATIONS INCLUSES - AVEC NAMESPACE AGENTS CORRIGÉ
    # ========================
    path('agents/', include('agents.urls', namespace='agents')),
    path('soins/', include('soins.urls')),
    path('assureur/', include('assureur.urls')),
    path('medecin/', include('medecin.urls')),
    path('pharmacien/', include('pharmacien.urls')),
    path('membres/', include('membres.urls')),
    path('inscription/', include('inscription.urls')),
    path('communication/', include('communication.urls')),
    path('pharmacie-public/', include('pharmacie_public.urls')),
    
    # ========================
    # API ENDPOINTS - AJOUTEZ CETTE LIGNE !!!
    # ========================
    path('api/', include('api.urls')),  # <-- LIGNE AJOUTÉE ICI
    
    # ========================
    # GESTION DES MEMBRES
    # ========================
    path('membres/', views.liste_membres, name='liste_membres'),
    path('membres/creer/', views.creer_membre, name='creer_membre'),
    path('membres/selection/', views.selection_membre, name='selection_membre'),
    path('membres/<int:membre_id>/', views.detail_membre, name='detail_membre'),
    
    # ========================
    # GESTION DES BONS
    # ========================
    path('bons/', views.liste_bons, name='liste_bons'),
    path('bons/creer/', views.creer_bon, name='creer_bon'),
    path('bons/<int:bon_id>/', views.detail_bon, name='detail_bon'),
    
    # ========================
    # GESTION DES PAIEMENTS
    # ========================
    path('paiements/', views.liste_paiements, name='liste_paiements'),
    path('paiements/creer/', views.creer_paiement, name='creer_paiement'),
    path('paiements/<int:paiement_id>/', views.detail_paiement, name='detail_paiement'),
    
    # ========================
    # GESTION DES SOINS
    # ========================
    path('soins/', views.liste_soins, name='liste_soins'),
    path('soins/<int:soin_id>/', views.detail_soin, name='detail_soin'),
    
    # ========================
    # AUTHENTIFICATION
    # ========================
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.logout_view, name='logout'),
    
    # ========================
    # FAVICON - CORRECTION APPLIQUÉE
    # ========================
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('img/favicon.ico'),
        permanent=True
    ), name='favicon'),
    
    # ========================
    # ADMIN
    # ========================
    path('admin/', admin.site.urls),
]

# ========================
# SERVIR LES FICHIERS MÉDIA/STATIC EN DÉVELOPPEMENT
# ========================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ========================
# HANDLERS D'ERREURS - CORRIGÉS
# ========================
handler400 = 'mutuelle_core.views.view_400'
handler403 = 'mutuelle_core.views.view_403'
handler404 = 'mutuelle_core.views.view_404'
handler500 = 'mutuelle_core.views.view_500'