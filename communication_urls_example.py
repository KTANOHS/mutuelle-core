
# Exemple de urls.py pour la messagerie multi-acteurs
from django.urls import path
from . import views

urlpatterns = [
    path('membre/messagerie/', views.messagerie_membre, name='messagerie_membre'),
    path('assureur/messagerie/', views.messagerie_assureur, name='messagerie_assureur'),
    path('medecin/messagerie/', views.messagerie_medecin, name='messagerie_medecin'),
    path('agent/messagerie/', views.messagerie_agent, name='messagerie_agent'),
]
