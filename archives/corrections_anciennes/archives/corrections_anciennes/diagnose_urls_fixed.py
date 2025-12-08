#!/usr/bin/env python
"""
DIAGNOSTIC ROBUSTE DES URLs
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.urls import get_resolver, reverse, NoReverseMatch
from django.apps import apps

def diagnose_urls_safe():
    print("🔍 DIAGNOSTIC URLs (Version Sécurisée)")
    print("=" * 60)
    
    # Méthode simple pour lister les URLs
    print("📋 URLs DISPONIBLES:")
    
    urls_to_check = [
        # Agents
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
        
        # Membres
        'membres:dashboard',
        'membres:mes_paiements',
        'membres:mes_ordonnances',
        
        # Assureur
        'assureur:dashboard',
        'assureur:liste_membres',
        'assureur:liste_paiements',
        
        # Medecin
        'medecin:dashboard', 
        'medecin:liste_bons',
        'medecin:creer_ordonnance',
        
        # Pharmacien
        'pharmacien:dashboard',
        'pharmacien:liste_ordonnances',
        
        # Core
        'login',
        'logout',
        'home',
    ]
    
    available_urls = []
    missing_urls = []
    
    for url_name in urls_to_check:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name} -> {url}")
            available_urls.append(url_name)
        except NoReverseMatch:
            print(f"❌ {url_name} -> NON TROUVÉ")
            missing_urls.append(url_name)
    
    print(f"\n📊 Total: {len(available_urls)} URLs disponibles, {len(missing_urls)} manquantes")
    
    return available_urls, missing_urls

def check_urls_files():
    print("\n📁 VÉRIFICATION DES FICHIERS urls.py:")
    print("=" * 40)
    
    apps_to_check = ['agents', 'membres', 'assureur', 'medecin', 'pharmacien', 'core']
    
    for app_name in apps_to_check:
        try:
            # Vérifier si l'application existe
            app_config = apps.get_app_config(app_name)
            print(f"✅ {app_name}: Application chargée")
            
            # Vérifier le fichier urls.py
            app_path = app_config.path
            urls_file = os.path.join(app_path, 'urls.py')
            
            if os.path.exists(urls_file):
                print(f"   📄 urls.py: PRÉSENT")
                
                # Vérifier le contenu basique
                with open(urls_file, 'r') as f:
                    content = f.read()
                    if 'app_name' in content:
                        print(f"   🏷️  app_name: DÉFINI")
                    else:
                        print(f"   ⚠️  app_name: NON DÉFINI")
                    
                    if 'urlpatterns' in content:
                        print(f"   🔗 urlpatterns: PRÉSENT")
                    else:
                        print(f"   ❌ urlpatterns: MANQUANT")
            else:
                print(f"   ❌ urls.py: MANQUANT")
                
        except LookupError:
            print(f"❌ {app_name}: APPLICATION NON TROUVÉE")

def check_main_urls():
    print("\n🏠 VÉRIFICATION URLs PRINCIPALES:")
    print("=" * 40)
    
    main_urls_file = os.path.join(os.getcwd(), 'mutuelle_core', 'urls.py')
    
    if os.path.exists(main_urls_file):
        print(f"✅ mutuelle_core/urls.py: PRÉSENT")
        
        with open(main_urls_file, 'r') as f:
            content = f.read()
            
            # Vérifier les inclusions
            apps_to_include = ['agents', 'membres', 'assureur', 'medecin', 'pharmacien']
            for app in apps_to_include:
                if f"include('{app}.urls')" in content or f'include("{app}.urls")' in content:
                    print(f"   ✅ {app}: INCLUS")
                else:
                    print(f"   ❌ {app}: NON INCLUS")
    else:
        print(f"❌ mutuelle_core/urls.py: MANQUANT")

def generate_missing_urls(missing_urls):
    print("\n🔧 GÉNÉRATION DES FICHIERS MANQUANTS:")
    print("=" * 40)
    
    # Regrouper par application
    apps_missing = {}
    for url in missing_urls:
        app_name = url.split(':')[0] if ':' in url else 'core'
        if app_name not in apps_missing:
            apps_missing[app_name] = []
        apps_missing[app_name].append(url)
    
    for app_name, urls in apps_missing.items():
        print(f"\n📝 {app_name}/urls.py:")
        
        if app_name == 'agents':
            print("""
from django.urls import path
from . import views

app_name = 'agents'

urlpatterns = [
    path('dashboard/', views.dashboard_agent, name='dashboard'),
    path('membres/', views.liste_membres, name='liste_membres'),
    path('membres/creer/', views.creer_membre, name='creer_membre'),
    path('bons/creer/', views.creer_bon_soin, name='creer_bon_soin'),
    path('bons/historique/', views.historique_bons_soin, name='historique_bons'),
    path('notifications/', views.agents_notifications, name='notifications'),
    path('verification-cotisation/', views.verification_cotisation, name='verification_cotisation'),
]
""")
        elif app_name == 'membres':
            print("""
from django.urls import path
from . import views

app_name = 'membres'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('paiements/', views.mes_paiements, name='mes_paiements'),
    path('ordonnances/', views.mes_ordonnances, name='mes_ordonnances'),
]
""")
        elif app_name == 'assureur':
            print("""
from django.urls import path
from . import views

app_name = 'assureur'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('membres/', views.liste_membres, name='liste_membres'),
    path('paiements/', views.liste_paiements, name='liste_paiements'),
]
""")
        elif app_name == 'medecin':
            print("""
from django.urls import path
from . import views

app_name = 'medecin'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bons/', views.liste_bons, name='liste_bons'),
    path('ordonnances/creer/', views.creer_ordonnance, name='creer_ordonnance'),
]
""")
        elif app_name == 'pharmacien':
            print("""
from django.urls import path
from . import views

app_name = 'pharmacien'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ordonnances/', views.liste_ordonnances, name='liste_ordonnances'),
]
""")

def create_quick_fix():
    print("\n🚀 CRÉATION RAPIDE DES FICHIERS MANQUANTS:")
    print("=" * 50)
    
    apps_to_create = ['membres', 'assureur', 'medecin', 'pharmacien']
    
    for app_name in apps_to_create:
        urls_file = os.path.join(app_name, 'urls.py')
        
        if not os.path.exists(urls_file):
            print(f"📁 Création de {urls_file}...")
            
            # Créer le répertoire si nécessaire
            os.makedirs(app_name, exist_ok=True)
            
            # Contenu du fichier
            content = f'''# {app_name}/urls.py
from django.urls import path
from . import views

app_name = '{app_name}'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]
'''
            with open(urls_file, 'w') as f:
                f.write(content)
            
            print(f"✅ {urls_file} créé avec succès!")
        else:
            print(f"ℹ️  {urls_file} existe déjà")

def main():
    print("🚀 DIAGNOSTIC URLs - VERSION CORRIGÉE")
    print("=" * 60)
    
    # 1. Vérification des URLs
    available_urls, missing_urls = diagnose_urls_safe()
    
    # 2. Vérification des fichiers
    check_urls_files()
    
    # 3. Vérification URLs principales
    check_main_urls()
    
    # 4. Génération des corrections
    if missing_urls:
        generate_missing_urls(missing_urls)
        
        # 5. Option de création automatique
        print("\n💡 SOUHAITEZ-VOUS CRÉER LES FICHIERS MANQUANTS AUTOMATIQUEMENT?")
        response = input("Tapez 'oui' pour créer les fichiers manquants: ")
        
        if response.lower() in ['oui', 'yes', 'o', 'y']:
            create_quick_fix()
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMUM DU DIAGNOSTIC")
    print("=" * 60)
    
    print(f"URLs disponibles: {len(available_urls)}")
    print(f"URLs manquantes: {len(missing_urls)}")
    
    if missing_urls:
        print("\n❌ URLs MANQUANTES:")
        for url in missing_urls:
            print(f"   - {url}")
    
    if len(missing_urls) == 0:
        print("🎉 TOUTES LES URLs SONT CONFIGURÉES!")
        return True
    else:
        print("🔧 DES FICHIERS URLs MANQUENT - Créez-les selon les instructions ci-dessus")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)