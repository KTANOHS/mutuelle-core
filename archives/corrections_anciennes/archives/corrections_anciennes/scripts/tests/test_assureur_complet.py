#!/usr/bin/env python
"""
TEST COMPLET DU MODULE ASSUREUR
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.constants import UserGroups

def test_assureur_flow():
    """Test du flux complet assureur"""
    print("🧪 TEST COMPLET DU MODULE ASSUREUR")
    print("=" * 50)
    
    client = Client()
    
    # Créer un utilisateur assureur pour le test
    user, created = User.objects.get_or_create(
        username='test_assureur',
        defaults={'email': 'assureur@test.com', 'password': 'test123'}
    )
    
    if created:
        user.set_password('test123')
        user.save()
        print("✅ Utilisateur de test créé")
    
    # Simuler la connexion
    client.force_login(user)
    print("✅ Utilisateur connecté")
    
    # Tester chaque page
    pages_to_test = [
        '/assureur/dashboard/',
        '/assureur/membres/recherche/',
        '/assureur/bons/',
        '/assureur/rapports/statistiques/',
    ]
    
    for page in pages_to_test:
        response = client.get(page)
        status = "✅" if response.status_code == 200 else "❌"
        print(f"{status} {page:35} -> Status: {response.status_code}")
    
    print("\n🎯 POUR FINALISER:")
    print("   1. Vérifiez les données d'exemple dans la base")
    print("   2. Testez manuellement chaque fonctionnalité")
    print("   3. Validez les exports et rapports")
    print("   4. Vérifiez la responsivité mobile")

if __name__ == "__main__":
    test_assureur_flow()