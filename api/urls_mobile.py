# api/urls_mobile.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_mobile import (
    MobileMembreViewSet,
    MobileBonViewSet,
    MobileNotificationViewSet,
    MobileSoinViewSet,
    MobilePaiementViewSet
)

router = DefaultRouter()
router.register(r'membres', MobileMembreViewSet, basename='mobile-membre')
router.register(r'bons', MobileBonViewSet, basename='mobile-bon')
router.register(r'notifications', MobileNotificationViewSet, basename='mobile-notification')
router.register(r'soins', MobileSoinViewSet, basename='mobile-soin')
router.register(r'paiements', MobilePaiementViewSet, basename='mobile-paiement')

urlpatterns = [
    path('', include(router.urls)),
]