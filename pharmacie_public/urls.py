# pharmacie_public/urls.py
from django.urls import path
from . import views

app_name = 'pharmacie_public'

urlpatterns = [
    # Inscription publique
    path('inscription/', views.InscriptionPharmaciePublicView.as_view(), name='inscription'),
    path('inscription/success/', views.inscription_success, name='inscription_success'),
    
    # Recherche et consultation
    path('pharmacies/', views.liste_pharmacies, name='liste_pharmacies'),
    path('pharmacies/garde/', views.pharmacies_garde, name='pharmacies_garde'),
    path('pharmacie/<int:pk>/', views.detail_pharmacie, name='detail_pharmacie'),
    
    # Commandes (nécessitent connexion)
    path('commander/<int:pharmacie_id>/', views.passer_commande, name='passer_commande'),
    path('mes-commandes/', views.mes_commandes, name='mes_commandes'),
    
    # API
    path('api/pharmacies-garde/', views.api_pharmacies_garde, name='api_pharmacies_garde'),
]