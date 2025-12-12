# api/urls.py - VERSION COMPLÈTE CORRIGÉE AVEC JWT
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView  # <-- AJOUT
from .views import (
    TypeSoinViewSet, SoinViewSet, PrescriptionViewSet, MedecinViewSet,
    MembreViewSet, BonPriseEnChargeViewSet, PaiementViewSet, OrdonnanceViewSet,
    StatistiquesAPIView, api_health  # <-- AJOUT api_health
)

# Router pour l'API professionnelle
router = DefaultRouter()
router.register(r'types-soin', TypeSoinViewSet)
router.register(r'soins', SoinViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'medecins', MedecinViewSet)
router.register(r'membres', MembreViewSet)
router.register(r'bons-prise-en-charge', BonPriseEnChargeViewSet)
router.register(r'paiements', PaiementViewSet)
router.register(r'ordonnances', OrdonnanceViewSet)

urlpatterns = [
    # ========================
    # AUTHENTIFICATION JWT - NOUVEAUX ENDPOINTS
    # ========================
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # ========================
    # HEALTH CHECK
    # ========================
    path('health/', api_health, name='api_health'),
    
    # ========================
    # API PROFESSIONNELLE EXISTANTE (v1)
    # ========================
    path('', include(router.urls)),
    path('statistiques/', StatistiquesAPIView.as_view(), name='api-statistiques'),
    
    # ========================
    # API MOBILE (Nouvelle - v1/mobile/)
    # ========================
    path('mobile/', include('api.urls_mobile')),
    
    # ========================
    # DOCUMENTATION API
    # ========================
    path('docs/', include_docs_urls(title='API Mutuelle Core')),
]