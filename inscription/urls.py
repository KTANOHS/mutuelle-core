# inscription/urls.py
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

# Assurez-vous d'avoir cette ligne
app_name = 'inscription'

urlpatterns = [
    path('', views.inscription_membre, name='inscription_membre'),
    path('success/', views.inscription_success, name='success'),
    path('demande-rappel/', csrf_exempt(views.demande_rappel), name='demande_rappel'),
]