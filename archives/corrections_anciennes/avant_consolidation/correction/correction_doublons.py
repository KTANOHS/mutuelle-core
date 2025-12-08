#!/usr/bin/env python3
"""
SCRIPT DE CORRECTION DES DOUBLONS URLs
"""

import os
import sys
import django

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def corriger_doublons():
    """Corrige les doublons d'URLs identifiés"""
    print("🔧 CORRECTION DES DOUBLONS URLs")
    
    doublons_a_corriger = {
        'agents:dashboard': "Supprimer une des deux définitions dans agents/urls.py",
        'soins:liste_soins': "Garder seulement soins:liste_soins dans soins/urls.py", 
        'soins:detail_soin': "Garder seulement soins:detail_soin dans soins/urls.py",
        'soins:valider_soin': "Garder une seule définition dans soins/urls.py",
        'medecin:creer_consultation': "Supprimer le doublon dans medecin/urls.py",
        'logout': "Garder seulement mutuelle_core.views.logout_view",
        'admin:auth_user_password_change': "Doublon admin - normal, ignorer"
    }
    
    print("\n📋 DOUBLONS À CORRIGER:")
    for doublon, solution in doublons_a_corriger.items():
        print(f"   🔴 {doublon}")
        print(f"      💡 Solution: {solution}")
    
    return doublons_a_corriger

def generer_corrections_fichiers():
    """Génère les corrections pour chaque fichier"""
    print("\n📝 CORRECTIONS À APPLIQUER:")
    
    corrections = {
        'soins/urls.py': """
# === CORRECTION SOINS URLs - SUPPRIMER LES DOUBLONS ===
from django.urls import path
from . import views

app_name = 'soins'

urlpatterns = [
    # Dashboard soins
    path('', views.dashboard_soins, name='dashboard_soins'),
    
    # Liste soins - UNE SEULE DÉFINITION
    path('liste/', views.liste_soins, name='liste_soins'),
    
    # Détail soin - UNE SEULE DÉFINITION  
    path('<int:soin_id>/', views.detail_soin, name='detail_soin'),
    
    # Validation soin - UNE SEULE DÉFINITION
    path('<int:soin_id>/valider/', views.valider_soin, name='valider_soin'),
    
    # Rejet soin
    path('<int:soin_id>/rejeter/', views.rejeter_soin, name='rejeter_soin'),
    
    # Statistiques
    path('statistiques/', views.statistiques_soins, name='statistiques_soins'),
]
""",
        
        'agents/urls.py': """
# === CORRECTION AGENTS URLs - UN SEUL DASHBOARD ===
from django.urls import path
from . import views

app_name = 'agents'

urlpatterns = [
    # UN SEUL DASHBOARD - Supprimer une des deux définitions
    path('tableau-de-bord/', views.dashboard, name='dashboard'),
    
    # Autres URLs agents...
    # Garder le reste du fichier existant
]
""",
        
        'medecin/urls.py': """
# === CORRECTION MEDECIN URLs - SUPPRIMER DOUBLON CONSULTATION ===
from django.urls import path
from . import views

app_name = 'medecin'

urlpatterns = [
    # UNE SEULE CRÉATION CONSULTATION
    path('creer-consultation/', views.creer_consultation, name='creer_consultation'),
    
    # Autres URLs medecin...
    # Garder le reste du fichier existant
]
""",
        
        'mutuelle_core/urls.py': """
# === CORRECTION URLs PRINCIPALES - UN SEUL LOGOUT ===
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    
    # UN SEUL LOGOUT - Supprimer les doublons
    path('logout/', views.logout_view, name='logout'),
    
    # Applications avec include
    path('agents/', include('agents.urls')),
    path('membres/', include('membres.urls')),
    path('soins/', include('soins.urls')),
    path('medecin/', include('medecin.urls')),
    path('assureur/', include('assureur.urls')),
    path('pharmacien/', include('pharmacien.urls')),
    path('communication/', include('communication.urls')),
    path('paiements/', include('paiements.urls')),
    
    # Redirection
    path('redirect-after-login/', views.redirect_to_user_dashboard, name='redirect_after_login'),
]
"""
    }
    
    for fichier, correction in corrections.items():
        print(f"\n📁 {fichier}:")
        print(correction)

def verifier_corrections():
    """Vérifie que les corrections résolvent les doublons"""
    print("\n✅ VÉRIFICATION APRÈS CORRECTIONS:")
    
    from django.urls import get_resolver
    
    resolver = get_resolver()
    noms_urls = []
    
    def collecter_noms(patterns, namespace=None):
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):
                new_ns = pattern.namespace
                if namespace:
                    new_ns = f"{namespace}:{new_ns}" if new_ns else namespace
                collecter_noms(pattern.url_patterns, new_ns)
            elif hasattr(pattern, 'name') and pattern.name:
                nom_complet = f"{namespace}:{pattern.name}" if namespace else pattern.name
                noms_urls.append(nom_complet)
    
    collecter_noms(resolver.url_patterns)
    
    # Chercher les doublons restants
    doublons_restants = {}
    for nom in noms_urls:
        if noms_urls.count(nom) > 1:
            if nom not in doublons_restants:
                doublons_restants[nom] = 0
            doublons_restants[nom] += 1
    
    if doublons_restants:
        print("❌ DOUBLONS RESTANTS:")
        for nom, count in doublons_restants.items():
            print(f"   - {nom}: {count} occurrences")
    else:
        print("🎉 TOUS LES DOUBLONS SONT CORRIGÉS !")

if __name__ == "__main__":
    corriger_doublons()
    generer_corrections_fichiers()
    verifier_corrections()