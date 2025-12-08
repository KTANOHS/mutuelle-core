#!/usr/bin/env python3
"""
MIGRATION URLs - Corrigé avec le bon chemin
"""

import os
import sys
import django

# Configuration du chemin
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_urls():
    """Vérifie toutes les URLs"""
    print("🔍 VÉRIFICATION DES URLs")
    
    from django.urls import get_resolver
    from django.core.checks.urls import check_url_config
    
    # Vérifier la configuration
    errors = check_url_config(None)
    if errors:
        print("❌ ERREURS DE CONFIGURATION:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("✅ Aucune erreur de configuration")
    
    # Lister les URLs
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
    print(f"📊 URLs totales: {url_count}")
    
    # Vérifier les conflits spécifiques
    print("\n🔍 CONFLITS IDENTIFIÉS:")
    
    conflits = [
        ("/soins/", "soins.views.wrapper ET mutuelle_core.views.liste_soins"),
        ("/membres/creer/", "membres.views.creer_membre ET mutuelle_core.views.creer_membre"),
        ("/communication/notifications/count/", "URL dupliquée")
    ]
    
    for url, description in conflits:
        print(f"   ⚠️  {url}: {description}")

if __name__ == "__main__":
    verifier_urls()