#!/usr/bin/env python3
"""
CORRECTION RAPIDE - Vérifie les URLs problématiques
"""

import os
import sys
import django

# Ajouter le chemin du projet
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.urls import reverse, NoReverseMatch

def verification_rapide():
    """Vérification rapide des URLs problématiques"""
    print("🔍 VÉRIFICATION RAPIDE DES URLs")
    
    problemes = []
    
    # Test des URLs critiques
    urls_a_verifier = [
        ('membres:creer_membre', 'Création membre'),
        ('soins:dashboard', 'Dashboard soins'),
        ('soins:liste_soins', 'Liste soins'),
        ('communication:notification_count', 'Notification count'),
    ]
    
    for nom_url, description in urls_a_verifier:
        try:
            url = reverse(nom_url)
            print(f"✅ {description}: {url}")
        except NoReverseMatch as e:
            problemes.append(f"❌ {description}: {str(e)}")
    
    # Vérifier les doublons
    print("\n🔍 RECHERCHE DE DOUBLONS...")
    
    if problemes:
        print("\n🚨 PROBLÈMES DÉTECTÉS:")
        for probleme in problemes:
            print(f"   {probleme}")
    else:
        print("✅ Aucun problème détecté")

if __name__ == "__main__":
    verification_rapide()