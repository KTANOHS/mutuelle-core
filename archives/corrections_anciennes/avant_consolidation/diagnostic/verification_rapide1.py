# verification_rapide.py

import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_rapide():
    """Vérification rapide de l'état de l'application agents"""
    
    print("🔍 VÉRIFICATION RAPIDE AGENTS")
    print("=" * 50)
    
    # Vérifier l'accès aux URLs principales
    from django.urls import reverse
    from django.test import Client
    
    urls_test = [
        'agents:tableau_de_bord',
        'agents:creer_membre', 
        'agents:liste_membres',
        'agents:creer_bon_soin',
    ]
    
    client = Client()
    
    print("\n🌐 Test des URLs:")
    for url_name in urls_test:
        try:
            url = reverse(url_name)
            print(f"   ✅ {url_name} -> {url}")
        except Exception as e:
            print(f"   ❌ {url_name} -> ERREUR: {e}")
    
    # Vérifier les modèles
    print("\n📊 Données existantes:")
    try:
        from agents.models import Agent
        from membres.models import Membre
        from soins.models import BonDeSoin
        
        print(f"   • Agents: {Agent.objects.count()}")
        print(f"   • Membres: {Membre.objects.count()}")
        print(f"   • Bons de soin: {BonDeSoin.objects.count()}")
        
    except Exception as e:
        print(f"   ❌ Erreur données: {e}")
    
    print("\n✅ Vérification terminée")

if __name__ == "__main__":
    verification_rapide()