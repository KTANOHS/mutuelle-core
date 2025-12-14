# api/urls.py - Version simplifiée
from django.urls import path, include
from .views import api_health  # Import simple d'abord

# URL patterns de base
urlpatterns = [
    path('health/', api_health, name='api_health'),
]

# Importer les ViewSets conditionnellement
try:
    from rest_framework.routers import DefaultRouter
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
    
    from .views import (
        TypeSoinViewSet, SoinViewSet, PrescriptionViewSet,
        MedecinViewSet, MembreViewSet, BonPriseEnChargeViewSet,
        PaiementViewSet, OrdonnanceViewSet, StatistiquesAPIView
    )
    
    # Vérifier si les ViewSets sont valides
    if hasattr(TypeSoinViewSet, 'queryset'):
        router = DefaultRouter()
        router.register(r'types-soin', TypeSoinViewSet)
        router.register(r'soins', SoinViewSet)
        router.register(r'prescriptions', PrescriptionViewSet)
        router.register(r'medecins', MedecinViewSet)
        router.register(r'membres', MembreViewSet)
        router.register(r'bons-prise-en-charge', BonPriseEnChargeViewSet)
        router.register(r'paiements', PaiementViewSet)
        router.register(r'ordonnances', OrdonnanceViewSet)
        
        urlpatterns += [
            path('', include(router.urls)),
            path('statistiques/', StatistiquesAPIView.as_view(), name='api-statistiques'),
        ]
    
    # URLs JWT
    urlpatterns += [
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    ]
    
except Exception as e:
    print(f"⚠️  Erreur dans l'importation des ViewSets: {e}")