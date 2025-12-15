# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.views.generic import TemplateView

from . import views

# =============================================================================
# CONFIGURATION DU ROUTER
# =============================================================================

router = DefaultRouter()

# Enregistrement conditionnel des viewsets basé sur la disponibilité des modèles
try:
    # Viewsets principaux
    router.register(r'types-soins', views.TypeSoinViewSet, basename='typesoin')
    router.register(r'soins', views.SoinViewSet, basename='soin')
    router.register(r'prescriptions', views.PrescriptionViewSet, basename='prescription')
    router.register(r'medecins', views.MedecinViewSet, basename='medecin')
    router.register(r'membres', views.MembreViewSet, basename='membre')
    router.register(r'bons-prise-charge', views.BonPriseEnChargeViewSet, basename='bonprisecharge')
    router.register(r'paiements', views.PaiementViewSet, basename='paiement')
    router.register(r'ordonnances', views.OrdonnanceViewSet, basename='ordonnance')
    
    print("✅ Routes API enregistrées avec succès")
except Exception as e:
    print(f"⚠️  Erreur lors de l'enregistrement des routes: {e}")

# =============================================================================
# URLS DE L'API
# =============================================================================

urlpatterns = [
    # Routes du router
    path('', include(router.urls)),
    
    # Authentification Token (DRF)
    path('token/', obtain_auth_token, name='api_token_auth'),
    
    # Authentification JWT
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Santé de l'API (version améliorée)
    path('health/', views.api_health, name='api_health'),
    
    # Statistiques
    path('statistiques/', views.StatistiquesAPIView.as_view(), name='statistiques'),
    
    # Pages de documentation
    path('docs/', TemplateView.as_view(
        template_name='api/docs.html',
        extra_context={'title': 'API Documentation'}
    ), name='api_docs'),
    
    # Page d'accueil de l'API
    path('', TemplateView.as_view(
        template_name='api/home.html',
        extra_context={'title': 'Mutuelle API'}
    ), name='api_home'),
]

# =============================================================================
# AJOUTER LES ROUTES POUR LA DOCUMENTATION SWAGGER (si drf-yasg est installé)
# =============================================================================

try:
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from rest_framework import permissions
    
    schema_view = get_schema_view(
        openapi.Info(
            title="Mutuelle API",
            default_version='v1',
            description="API pour la gestion de la mutuelle de santé",
            terms_of_service="https://votresite.com/terms/",
            contact=openapi.Contact(email="contact@votresite.com"),
            license=openapi.License(name="Licence MIT"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )
    
    # Ajouter les URLs Swagger
    swagger_urls = [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), 
             name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), 
             name='schema-redoc'),
        path('swagger.json', schema_view.without_ui(cache_timeout=0), 
             name='schema-json'),
    ]
    
    urlpatterns = swagger_urls + urlpatterns
    print("✅ Swagger/Redoc intégré avec succès")
except ImportError:
    print("⚠️  drf-yasg non installé, Swagger désactivé")