#!/usr/bin/env python
"""
Vérification des URLs pharmacien - Version corrigée
"""

import os
import sys
import django
from pathlib import Path

# Ajouter le répertoire parent au path Python
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Trouver le bon nom de module settings
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()
    
    print("✅ Configuration Django chargée avec succès")
except Exception as e:
    print(f"❌ Erreur avec mutuelle_core.settings: {e}")
    
    # Essayer d'autres noms communs
    settings_modules = ['core.settings', 'project.settings', 'settings']
    for module in settings_modules:
        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', module)
            django.setup()
            print(f"✅ Configuration Django chargée avec {module}")
            break
        except Exception:
            continue
    else:
        print("❌ Impossible de charger les settings Django")
        print("💡 Vérifiez le nom de votre projet dans manage.py")
        sys.exit(1)

from django.urls import reverse, NoReverseMatch

def verifier_urls_pharmacien():
    print("\n🔍 VÉRIFICATION DES URLS PHARMACIEN")
    print("=" * 50)
    
    # Liste complète des URLs à vérifier
    urls_a_verifier = [
        'pharmacien:dashboard',
        'pharmacien:liste_ordonnances_attente',
        'pharmacien:profil_pharmacien', 
        'pharmacien:stock',
        'pharmacien:ajouter_stock',
        'pharmacien:modifier_stock',
        'pharmacien:gestion_stock',
        'pharmacien:historique_validation',
        'pharmacien:detail_ordonnance',
        'pharmacien:valider_ordonnance',
        'pharmacien:refuser_ordonnance',
        'pharmacien:export_historique',
        'pharmacien:rechercher_ordonnances',
        'pharmacien:filtrer_ordonnances',
        'pharmacien:api_ordonnances_attente',
        'pharmacien:api_statistiques_temps_reel',
        'pharmacien:api_statistiques_pharmacien',
        'pharmacien:export_stock',
        'pharmacien:importer_stock',
        'pharmacien:desactiver_stock',
        'pharmacien:activer_stock',
        'pharmacien:reapprovisionner_stock',
    ]
    
    print("📋 TEST DE TOUTES LES URLS:")
    urls_valides = []
    urls_erreur = []
    
    for url_name in sorted(urls_a_verifier):
        try:
            url = reverse(url_name)
            print(f"✅ {url_name:40} -> {url}")
            urls_valides.append(url_name)
        except NoReverseMatch as e:
            print(f"❌ {url_name:40} -> NON TROUVÉE")
            urls_erreur.append(url_name)
    
    # Rapport final
    print(f"\n📊 RAPPORT FINAL:")
    print(f"✅ URLs valides: {len(urls_valides)}")
    print(f"❌ URLs en erreur: {len(urls_erreur)}")
    
    if urls_erreur:
        print(f"\n🚨 URLs PROBLEMATIQUES:")
        for url in urls_erreur:
            print(f"   - {url}")
    
    # Vérification des URLs critiques
    print(f"\n🎯 URLS CRITIQUES POUR LES TEMPLATES:")
    urls_critiques = [
        'pharmacien:dashboard',
        'pharmacien:liste_ordonnances_attente', 
        'pharmacien:profil_pharmacien',
        'pharmacien:stock'
    ]
    
    for url_name in urls_critiques:
        try:
            url = reverse(url_name)
            print(f"🎉 {url_name:35} -> FONCTIONNE")
        except NoReverseMatch:
            print(f"💥 {url_name:35} -> MANQUANTE")

if __name__ == '__main__':
    verifier_urls_pharmacien()