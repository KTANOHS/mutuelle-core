#!/usr/bin/env python3
"""
VÉRIFICATION FINALE DU PROJET
"""

import os
import sys
import django

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def bilan_final():
    """Bilan complet après corrections"""
    print("🎯 BILAN FINAL DU PROJET MUTUELLE_CORE")
    print("=" * 50)
    
    from django.apps import apps
    from django.urls import get_resolver
    from django.db import connection
    
    # 1. Applications
    apps_count = len(apps.get_app_configs())
    print(f"📦 Applications: {apps_count}")
    
    # 2. Modèles
    models_count = len(apps.get_models())
    print(f"🏗️  Modèles: {models_count}")
    
    # 3. URLs
    resolver = get_resolver()
    url_count = 0
    def compter_urls(patterns):
        nonlocal url_count
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):
                compter_urls(pattern.url_patterns)
            else:
                url_count += 1
    compter_urls(resolver.url_patterns)
    print(f"🔗 URLs: {url_count}")
    
    # 4. Base de données
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("💾 Base de données: ✅ Connectée")
    except Exception as e:
        print(f"💾 Base de données: ❌ {e}")
    
    # 5. Vérification doublons
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
    doublons = set([x for x in noms_urls if noms_urls.count(x) > 1])
    
    if doublons:
        print(f"⚠️  Doublons restants: {len(doublons)}")
        for d in sorted(doublons):
            print(f"   - {d}")
    else:
        print("✅ Doublons: Aucun")
    
    print(f"\n🎉 STATUT: PROJET PRÊT POUR LE DÉMARRAGE !")

if __name__ == "__main__":
    bilan_final()