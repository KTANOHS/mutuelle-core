# test_final.py
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def test_urls():
    """Teste que les URLs sont correctement configurées"""
    print("🔍 TEST FINAL DES URLs")
    
    # Vérifier urls.py principal
    main_urls = BASE_DIR / 'mutuelle_core' / 'urls.py'
    if main_urls.exists():
        with open(main_urls, 'r') as f:
            content = f.read()
            if 'agents' in content and 'include' in content:
                print("✅ URLs agents incluses dans urls principal")
            else:
                print("❌ URLs agents MANQUANTES dans urls principal")
    
    # Vérifier urls.py agents
    agents_urls = BASE_DIR / 'agents' / 'urls.py'
    if agents_urls.exists():
        with open(agents_urls, 'r') as f:
            content = f.read()
            if 'recherche-membres' in content:
                print("✅ URL recherche-membres configurée")
            else:
                print("❌ URL recherche-membres MANQUANTE")
    
    print("\n🎯 POUR TESTER:")
    print("1. Démarrez le serveur: python manage.py runserver")
    print("2. Visitez: http://localhost:8000/agents/verification-cotisations/")
    print("3. Essayez de rechercher 'Jean'")

if __name__ == "__main__":
    test_urls()