#!/usr/bin/env python3
"""
CORRECTION RAPIDE - Applique les correctifs immédiats
"""

import os
import django
from django.urls import reverse, NoReverseMatch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def correction_rapide():
    """Correction rapide des URLs problématiques"""
    print("🔧 CORRECTION RAPIDE DES URLs")
    
    # Vérification des URLs problématiques
    problemes = []
    
    # Test URL création membre
    try:
        url1 = reverse('membres:creer_membre')
        url2 = reverse('creer_membre')
        problemes.append("DOUBLE création membre détectée")
    except NoReverseMatch:
        pass
    
    # Test URLs soins
    try:
        reverse('soins:dashboard')
        reverse('liste_soins')
        problemes.append("Conflit URLs soins détecté")
    except NoReverseMatch:
        pass
    
    if problemes:
        print("❌ PROBLÈMES DÉTECTÉS:")
        for probleme in problemes:
            print(f"   - {probleme}")
        
        print("\n🔄 APPLIQUER LES CORRECTIONS:")
        print("   1. Dans soins/urls.py, remplacer 'wrapper' par des vues spécifiques")
        print("   2. Dans membres/urls.py, garder une seule URL création")
        print("   3. Dans mutuelle_core/urls.py, utiliser include() pour soins/")
    else:
        print("✅ Aucun problème détecté - URLs correctes")

if __name__ == "__main__":
    correction_rapide()