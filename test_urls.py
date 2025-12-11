#!/usr/bin/env python
"""
Tester les URLs de l'application
"""

import sys
import os
import django
from django.test import Client
from django.core.management import execute_from_command_line

def test_urls():
    """Tester les URLs principales"""
    print("🔗 TEST DES URLS DE L'APPLICATION")
    print("=" * 50)
    
    # Configurer Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()
    
    client = Client()
    
    urls_to_test = [
        ("/", "Page d'accueil", 200),
        ("/admin/login/", "Admin login", 302),  # Redirige vers login
        ("/accounts/login/", "Connexion", 200),
        ("/inscription/", "Inscription", 200),
        ("/api/", "API REST", 200),
    ]
    
    all_ok = True
    
    for url, description, expected_code in urls_to_test:
        try:
            response = client.get(url)
            status = response.status_code
            
            if status == expected_code or (expected_code == 302 and status in [301, 302]):
                print(f"✅ {description}: HTTP {status}")
            else:
                print(f"❌ {description}: HTTP {status} (attendu {expected_code})")
                all_ok = False
                
        except Exception as e:
            print(f"❌ {description}: ERREUR - {e}")
            all_ok = False
    
    print("\n" + "=" * 50)
    if all_ok:
        print("🎉 Toutes les URLs répondent correctement!")
    else:
        print("🚨 Certaines URLs ont des problèmes")
    
    return all_ok

if __name__ == "__main__":
    # Démarrer le serveur de test si nécessaire
    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        print("🚀 Démarrage du serveur de test...")
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
    else:
        success = test_urls()
        sys.exit(0 if success else 1)