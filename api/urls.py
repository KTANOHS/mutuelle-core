# api/urls.py - VERSION COMPLÈTE CORRIGÉE
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from .views import (
    TypeSoinViewSet, SoinViewSet, PrescriptionViewSet, MedecinViewSet,
    MembreViewSet, BonPriseEnChargeViewSet, PaiementViewSet, OrdonnanceViewSet,
    StatistiquesAPIView
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
    # API Professionnelle existante (v1)
    path('', include(router.urls)),
    path('statistiques/', StatistiquesAPIView.as_view(), name='api-statistiques'),
    
    # API Mobile (Nouvelle - v1/mobile/)
    path('mobile/', include('api.urls_mobile')),
    
    # Documentation API
    path('docs/', include_docs_urls(title='API Mutuelle Core')),
]