#!/usr/bin/env python3
"""
Test de production complet après toutes les corrections
"""

import os
import django
from django.test import Client
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def comprehensive_production_test():
    print("🏭 TEST DE PRODUCTION COMPLET")
    print("=" * 50)
    
    client = Client()
    tests_passed = 0
    total_tests = 0
    
    # Liste des URLs à tester
    test_urls = [
        ('/accounts/login/', 'Page de login'),
        ('/pharmacien/dashboard/', 'Dashboard pharmacien'),
        ('/pharmacien/ordonnances/attente/', 'Liste ordonnances'),
        ('/assureur/dashboard/', 'Dashboard assureur'),
    ]
    
    for url, description in test_urls:
        total_tests += 1
        print(f"{total_tests}. Test de {description} ({url})...")
        
        try:
            response = client.get(url)
            if response.status_code in [200, 302]:  # 302 = redirection vers login
                print(f"   ✅ {description} accessible")
                tests_passed += 1
            else:
                print(f"   ❌ Erreur {response.status_code} sur {description}")
        except Exception as e:
            print(f"   ❌ Exception sur {description}: {e}")
    
    print(f"\n📊 RÉSULTATS: {tests_passed}/{total_tests} tests passés")
    
    if tests_passed == total_tests:
        print("🎉 TOUS LES TESTS DE PRODUCTION SONT RÉUSSIS !")
    else:
        print("⚠️  Certains tests ont échoué")

if __name__ == "__main__":
    comprehensive_production_test()