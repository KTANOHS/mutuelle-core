#!/usr/bin/env python3
"""
Vérification de la configuration Django pour l'agent - CORRIGÉ
"""

import os
from pathlib import Path  # AJOUT IMPORT MANQUANT

def check_urls_configuration():
    """Vérifier la configuration des URLs"""
    print("🔧 VÉRIFICATION CONFIGURATION URLS")
    print("=" * 40)
    
    # Vérifier si le fichier urls.py existe
    urls_files = [
        "urls.py",
        "agents/urls.py", 
    ]
    
    for urls_file in urls_files:
        if Path(urls_file).exists():
            print(f"✅ {urls_file} trouvé")
            # Lire le contenu pour vérifier les patterns
            content = Path(urls_file).read_text()
            if 'agent' in content.lower():
                print(f"   📍 Contient des URLs agent")
                
            # Vérifier les URLs spécifiques
            urls_to_check = ['creer_bon_soin', 'liste_membres', 'notifications', 'verification_cotisation']
            for url_name in urls_to_check:
                if f"name='{url_name}'" in content or f'name="{url_name}"' in content:
                    print(f"   ✅ URL '{url_name}' trouvée")
                else:
                    print(f"   ❌ URL '{url_name}' NON trouvée")
        else:
            print(f"❌ {urls_file} non trouvé")

def check_views_existence():
    """Vérifier l'existence des vues"""
    print(f"\n👁️ VÉRIFICATION DES VUES")
    print("=" * 40)
    
    views_files = [
        "agents/views.py",
    ]
    
    for views_file in views_files:
        if Path(views_file).exists():
            print(f"✅ {views_file} trouvé")
            content = Path(views_file).read_text()
            # Vérifier les fonctions de vue pour l'agent
            agent_views = [
                'dashboard_agent', 'creer_bon_soin', 'liste_membres', 
                'verification_cotisation', 'agents_notifications'
            ]
            for view in agent_views:
                if f"def {view}" in content or f"class {view}" in content:
                    print(f"   ✅ Vue '{view}' détectée")
                else:
                    print(f"   ❌ Vue '{view}' NON détectée")
        else:
            print(f"❌ {views_file} non trouvé")

if __name__ == "__main__":
    check_urls_configuration()
    check_views_existence()