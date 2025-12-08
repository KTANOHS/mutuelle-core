"""
core/urls.py - URLs de l'application "core"
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),
    
    # Pages statiques
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('services/', views.services, name='services'),
    path('faq/', views.faq, name='faq'),
    
    # Pages d'information
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('pricing/', views.pricing, name='pricing'),
    path('site-status/', views.site_status, name='site_status'),
    
    # Pages utilitaires
    path('maintenance/', views.maintenance, name='maintenance'),
    path('coming-soon/', views.coming_soon, name='coming_soon'),
    path('placeholder/<str:template_name>/', views.placeholder, name='placeholder'),
    
    # API utilitaires
    path('api/health/', views.api_health_check, name='api_health_check'),
    path('api/system-info/', views.api_system_info, name='api_system_info'),
    
    # Sitemap
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    
    # Vue de test (protégée)
    path('test/', views.test_view, name='test_view'),
]

# Gestionnaires d'erreur spécifiques à l'app core
# (Ces handlers peuvent être redéfinis au niveau du projet si besoin)
handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'