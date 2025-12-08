#!/usr/bin/env python3
"""
Test de production final - Simule le serveur en conditions réelles
"""

import os
import django
from django.test import Client
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def production_test():
    print("🏭 TEST DE PRODUCTION FINAL")
    print("=" * 50)
    
    client = Client()
    
    # Test de la page de login
    print("1. Test de la page de login...")
    try:
        response = client.get('/accounts/login/')
        if response.status_code == 200:
            print("   ✅ Page de login accessible")
        else:
            print(f"   ❌ Erreur {response.status_code} sur la page de login")
    except Exception as e:
        print(f"   ❌ Exception sur la page de login: {e}")
    
    # Test du dashboard pharmacien (redirige vers login si non authentifié)
    print("2. Test du dashboard pharmacien...")
    try:
        response = client.get('/pharmacien/dashboard/')
        # Doit rediriger vers login si non authentifié (302)
        if response.status_code in [200, 302]:
            print("   ✅ Dashboard pharmacien accessible")
        else:
            print(f"   ❌ Erreur {response.status_code} sur le dashboard")
    except Exception as e:
        print(f"   ❌ Exception sur le dashboard: {e}")
    
    print("\n🎯 TEST DE PRODUCTION TERMINÉ")

if __name__ == "__main__":
    production_test()