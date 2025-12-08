# test_urls_final.py
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

from django.urls import reverse, NoReverseMatch

def test_urls_agents():
    """Teste que toutes les URLs agents fonctionnent"""
    print("🔍 TEST DES URLs AGENTS")
    print("=" * 40)
    
    urls_a_tester = [
        ('agents:verification_cotisations', []),
        ('agents:tableau_de_bord', []),
        ('agents:recherche_membres_api', []),
    ]
    
    for url_name, args in urls_a_tester:
        try:
            url = reverse(url_name, args=args)
            print(f"✅ {url_name} -> {url}")
        except NoReverseMatch as e:
            print(f"❌ {url_name} -> ERREUR: {e}")
    
    print("\n🎯 POUR TESTER:")
    print("1. Démarrez le serveur: python manage.py runserver")
    print("2. Visitez: http://localhost:8000/agents/verification-cotisations/")
    print("3. Cliquez sur 'Tableau de bord' dans le menu")

if __name__ == "__main__":
    test_urls_agents()