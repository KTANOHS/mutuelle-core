#!/usr/bin/env python
"""
Vérifie les URLs de dashboard disponibles
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def check_available_dashboards():
    """Vérifie quels dashboards sont accessibles"""
    print("🌐 VÉRIFICATION DES DASHBOARDS ACCESSIBLES")
    print("=" * 50)
    
    test_users = [
        ('test_assureur', 'pass123'),
        ('test_medecin', 'pass123'),
        ('test_pharmacien', 'pass123'),
        ('test_membre', 'pass123')
    ]
    
    # URLs à tester
    dashboard_urls = [
        '/',
        '/dashboard/',
        '/assureur-dashboard/',
        '/assureur/dashboard/',
        '/assureur/',
        '/medecin-dashboard/',
        '/medecin/dashboard/',
        '/medecin/',
        '/pharmacien-dashboard/',
        '/pharmacien/dashboard/', 
        '/pharmacien/',
        '/membre-dashboard/',
        '/membres/dashboard/',
        '/membres/',
        '/generic-dashboard/'
    ]
    
    for username, password in test_users:
        print(f"\n👤 Test pour {username}:")
        
        client = Client()
        if not client.login(username=username, password=password):
            print("  ❌ Connexion échouée")
            continue
        
        accessible_urls = []
        
        for url in dashboard_urls:
            response = client.get(url, follow=True)
            final_url = response.redirect_chain[-1][0] if response.redirect_chain else url
            final_status = response.redirect_chain[-1][1] if response.redirect_chain else response.status_code
            
            if final_status == 200:
                accessible_urls.append((url, final_url))
                print(f"  ✅ {url} -> {final_url}")
            else:
                print(f"  ❌ {url} -> Status: {final_status}")
        
        print(f"  📊 URLs accessibles: {len(accessible_urls)}")

if __name__ == "__main__":
    check_available_dashboards()