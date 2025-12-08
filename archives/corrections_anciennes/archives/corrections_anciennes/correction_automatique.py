#!/usr/bin/env python3
"""
SCRIPT DE CORRECTION AUTOMATIQUE
"""

import os
import re

def corriger_urls_agents():
    """Corrige le nom de l'URL dans agents/urls.py"""
    file_path = 'agents/urls.py'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer le nom de l'URL
        old_pattern = r"path\('tableau-de-bord/', views\.tableau_de_bord_agent, name='tableau_de_bord'\)"
        new_pattern = "path('tableau-de-bord/', views.tableau_de_bord_agent, name='tableau_de_bord_agent')"
        
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ agents/urls.py corrigé")
        else:
            print("⚠️  Pattern non trouvé dans agents/urls.py")
            
    except Exception as e:
        print(f"❌ Erreur correction agents/urls.py: {e}")

def corriger_recherche_membres():
    """Corrige le champ de recherche dans agents/views.py"""
    file_path = 'agents/views.py'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer numero_membre par numero_unique
        content = content.replace("numero_membre", "numero_unique")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ agents/views.py corrigé (recherche membres)")
            
    except Exception as e:
        print(f"❌ Erreur correction agents/views.py: {e}")

def main():
    print("🔧 APPLICATION DES CORRECTIONS AUTOMATIQUES")
    print("=" * 50)
    
    corriger_urls_agents()
    corriger_recherche_membres()
    
    print("\n🎯 CORRECTIONS APPLIQUÉES - Redémarrez le serveur:")
    print("   python manage.py runserver")

if __name__ == "__main__":
    main()