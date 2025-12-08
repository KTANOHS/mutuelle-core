from django.urls import path
from . import views

app_name = 'soins'

urlpatterns = [
    path('', views.dashboard_soins, name='dashboard_soins'),
    path('liste/', views.liste_soins, name='liste_soins'),
    path('<int:soin_id>/', views.detail_soin, name='detail_soin'),
    path('<int:soin_id>/valider/', views.valider_soin, name='valider_soin'),
    path('<int:soin_id>/rejeter/', views.rejeter_soin, name='rejeter_soin'),
    path('statistiques/', views.statistiques_soins, name='statistiques_soins'),
]
