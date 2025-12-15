# api/urls.py - VERSION SIMPLIFIÉE ET ROBUSTE

from django.urls import path, include
from .views import api_health  # Toujours disponible

# =============================================================================
# URLS DE BASE (toujours disponibles)
# =============================================================================

urlpatterns = [
    path('health/', api_health, name='api_health'),
]

# =============================================================================
# ESSAYER D'IMPORTER LES AUTRES COMPOSANTS
# =============================================================================

try:
    from rest_framework.routers import DefaultRouter
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
    
    # Ajouter les URLs JWT
    urlpatterns += [
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    ]
    
    print("✅ JWT URLs ajoutées")
    
except ImportError as e:
    print(f"⚠️  JWT non disponible: {e}")

try:
    # Importer les ViewSets
    from .views import (
        TypeSoinViewSet, SoinViewSet, PrescriptionViewSet,
        MedecinViewSet, MembreViewSet, BonPriseEnChargeViewSet,
        PaiementViewSet, OrdonnanceViewSet, StatistiquesAPIView
    )
    
    # Configurer le router
    router = DefaultRouter()
    router.register(r'types-soin', TypeSoinViewSet)
    router.register(r'soins', SoinViewSet)
    router.register(r'prescriptions', PrescriptionViewSet)
    router.register(r'medecins', MedecinViewSet)
    router.register(r'membres', MembreViewSet)
    router.register(r'bons-prise-en-charge', BonPriseEnChargeViewSet)
    router.register(r'paiements', PaiementViewSet)
    router.register(r'ordonnances', OrdonnanceViewSet)
    
    # Ajouter les URLs du router
    urlpatterns += [
        path('', include(router.urls)),
        path('statistiques/', StatistiquesAPIView.as_view(), name='api-statistiques'),
    ]
    
    print("✅ ViewSets et router configurés")
    
except ImportError as e:
    print(f"⚠️  ViewSets non disponibles: {e}")
except Exception as e:
    print(f"⚠️  Erreur configuration API: {e}")

# =============================================================================
# DOCUMENTATION API (optionnelle)
# =============================================================================

try:
    from rest_framework.documentation import include_docs_urls
    
    urlpatterns += [
        path('docs/', include_docs_urls(title='API Mutuelle Core')),
    ]
    
    print("✅ Documentation API ajoutée")
    
except ImportError:
    print("⚠️  Documentation API non disponible")

print(f"✅ API configurée avec {len(urlpatterns)} patterns d'URL")