#!/usr/bin/env python
"""
DIAGNOSTIC ET CORRECTION DES PROBLÈMES D'URLs
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.urls import get_resolver, reverse, NoReverseMatch
from django.apps import apps

def diagnose_all_urls():
    print("🔍 DIAGNOSTIC COMPLET DES URLs")
    print("=" * 60)
    
    # 1. Lister toutes les URLs enregistrées
    resolver = get_resolver()
    all_urls = []
    
    def extract_urls(url_patterns, prefix=''):
        for pattern in url_patterns:
            if hasattr(pattern, 'url_patterns'):
                # Namespace
                extract_urls(pattern.url_patterns, prefix + pattern.namespace + ':')
            elif hasattr(pattern, 'name') and pattern.name:
                all_urls.append(prefix + pattern.name)
    
    extract_urls(resolver.url_patterns)
    
    print("📋 URLs DISPONIBLES:")
    for url_name in sorted(all_urls):
        print(f"   🔗 {url_name}")
    
    print(f"\n📊 Total: {len(all_urls)} URLs enregistrées")
    
    return all_urls

def test_agent_urls():
    print("\n🎯 TEST DES URLs AGENT:")
    print("=" * 40)
    
    agent_urls_to_test = [
        'agents:dashboard',
        'agents:liste_membres', 
        'agents:creer_membre',
        'agents:creer_bon_soin',
        'agents:historique_bons',
        'agents:notifications',
        'agents:verification_cotisation',
        'agents:api_derniers_bons',
        'agents:api_stats_quotidiens',
        'agents:api_recherche_membres',
    ]
    
    results = {}
    
    for url_name in agent_urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name} -> {url}")
            results[url_name] = True
        except NoReverseMatch as e:
            print(f"❌ {url_name} -> NON TROUVÉ: {e}")
            results[url_name] = False
    
    return results

def test_all_dashboard_urls():
    print("\n🏠 TEST DES URLs DASHBOARD:")
    print("=" * 40)
    
    dashboard_urls = [
        'agents:dashboard',
        'membres:dashboard', 
        'assureur:dashboard',
        'medecin:dashboard',
        'pharmacien:dashboard',
    ]
    
    results = {}
    
    for url_name in dashboard_urls:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name} -> {url}")
            results[url_name] = True
        except NoReverseMatch as e:
            print(f"❌ {url_name} -> NON TROUVÉ: {e}")
            results[url_name] = False
    
    return results

def check_apps_configuration():
    print("\n📦 VÉRIFICATION DES APPLICATIONS:")
    print("=" * 40)
    
    apps_to_check = ['agents', 'membres', 'assureur', 'medecin', 'pharmacien']
    
    for app_name in apps_to_check:
        try:
            app_config = apps.get_app_config(app_name)
            print(f"✅ {app_name}: Chargé")
            
            # Vérifier si l'application a un fichier urls.py
            import importlib.util
            spec = importlib.util.find_spec(f"{app_name}.urls")
            if spec is not None:
                print(f"   📁 urls.py: Présent")
            else:
                print(f"   ❌ urls.py: MANQUANT")
                
        except LookupError:
            print(f"❌ {app_name}: NON TROUVÉ")

def generate_urls_fix():
    print("\n🔧 GÉNÉRATION DES CORRECTIONS:")
    print("=" * 40)
    
    corrections = {
        'agents': """
# agents/urls.py - CORRECTION COMPLÈTE
from django.urls import path
from . import views

app_name = 'agents'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard_agent, name='dashboard'),
    
    # Membres
    path('membres/', views.liste_membres, name='liste_membres'),
    path('membres/creer/', views.creer_membre, name='creer_membre'),
    
    # Bons de soin
    path('bons/creer/', views.creer_bon_soin, name='creer_bon_soin'),
    path('bons/historique/', views.historique_bons_soin, name='historique_bons'),
    
    # Notifications
    path('notifications/', views.agents_notifications, name='notifications'),
    
    # Vérifications
    path('verification-cotisation/', views.verification_cotisation, name='verification_cotisation'),
    path('verifier-cotisation/<int:membre_id>/', views.verifier_cotisation, name='verifier_cotisation'),
    
    # API
    path('api/derniers-bons/', views.api_derniers_bons, name='api_derniers_bons'),
    path('api/stats-quotidiens/', views.api_stats_quotidiens, name='api_stats_quotidiens'),
    path('api/recherche-membres/', views.api_recherche_membres, name='api_recherche_membres'),
    path('api/bon-details/<int:bon_id>/', views.api_bon_details, name='api_bon_details'),
    path('api/analytics/', views.api_analytics_dashboard, name='api_analytics'),
]
""",
        'membres': """
# membres/urls.py - CORRECTION
from django.urls import path
from . import views

app_name = 'membres'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('paiements/', views.mes_paiements, name='mes_paiements'),
    path('ordonnances/', views.mes_ordonnances, name='mes_ordonnances'),
]
""",
        'assureur': """
# assureur/urls.py - CORRECTION  
from django.urls import path
from . import views

app_name = 'assureur'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('membres/', views.liste_membres, name='liste_membres'),
    path('paiements/', views.liste_paiements, name='liste_paiements'),
]
""",
        'medecin': """
# medecin/urls.py - CORRECTION
from django.urls import path
from . import views

app_name = 'medecin'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bons/', views.liste_bons, name='liste_bons'),
    path('ordonnances/creer/', views.creer_ordonnance, name='creer_ordonnance'),
]
""",
        'pharmacien': """
# pharmacien/urls.py - CORRECTION
from django.urls import path
from . import views

app_name = 'pharmacien'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ordonnances/', views.liste_ordonnances, name='liste_ordonnances'),
]
"""
    }
    
    for app, code in corrections.items():
        print(f"\n📝 {app}/urls.py:")
        print(code)

def main():
    print("🚀 DÉMARRAGE DU DIAGNOSTIC URLs")
    print("=" * 60)
    
    # 1. Diagnostic complet
    all_urls = diagnose_all_urls()
    
    # 2. Test URLs agent
    agent_results = test_agent_urls()
    
    # 3. Test URLs dashboard
    dashboard_results = test_all_dashboard_urls()
    
    # 4. Vérification applications
    check_apps_configuration()
    
    # 5. Génération corrections
    generate_urls_fix()
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMUM DU DIAGNOSTIC")
    print("=" * 60)
    
    total_agent = sum(agent_results.values())
    total_dashboard = sum(dashboard_results.values())
    
    print(f"URLs Agent: {total_agent}/{len(agent_results)}")
    print(f"URLs Dashboard: {total_dashboard}/{len(dashboard_results)}")
    
    if total_agent == len(agent_results) and total_dashboard == len(dashboard_results):
        print("🎉 TOUTES LES URLs SONT CORRECTEMENT CONFIGURÉES!")
    else:
        print("🔧 DES CORRECTIONS SONT NÉCESSAIRES - Voir les corrections ci-dessus")
    
    return total_agent == len(agent_results) and total_dashboard == len(dashboard_results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)