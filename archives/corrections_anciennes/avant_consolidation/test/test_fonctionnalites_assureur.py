#!/usr/bin/env python
"""
SCRIPT DE TEST AUTOMATISÉ - FONCTIONNALITÉS ASSUREUR
Teste les principales fonctionnalités de l'application.
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from assureur.models import Assureur

def test_fonctionnalites_assureur():
    """Teste les fonctionnalités principales"""
    print("🧪 TESTS FONCTIONNALITÉS ASSUREUR")
    print("="*60)
    
    client = Client()
    
    # 1. Test de connexion avec différents utilisateurs
    print("\n1. TESTS DE CONNEXION:")
    
    test_users = ['DOUA', 'ktanos', 'DOUA1']
    
    for username in test_users:
        try:
            user = User.objects.get(username=username)
            # Simuler une connexion
            client.force_login(user)
            
            # Tester l'accès au dashboard
            response = client.get('/assureur/')
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {username}: Dashboard -> {response.status_code}")
            
            client.logout()
        
        except User.DoesNotExist:
            print(f"   ❌ {username}: Utilisateur non trouvé")
    
    # 2. Test des URLs principales (sans authentification)
    print("\n2. TESTS URLs (sans auth - doit rediriger):")
    
    urls_to_test = [
        '/assureur/',
        '/assureur/membres/',
        '/assureur/bons/',
        '/assureur/paiements/'
    ]
    
    for url in urls_to_test:
        response = client.get(url)
        if response.status_code in [302, 301]:  # Redirection vers login
            print(f"   ✅ {url}: Redirige vers login (attendu)")
        else:
            print(f"   ❌ {url}: Code {response.status_code} (inattendu)")
    
    # 3. Test des données
    print("\n3. TESTS DES DONNÉES:")
    
    # Vérifier les profils Assureur
    total_profiles = Assureur.objects.count()
    print(f"   ✅ Profils Assureur: {total_profiles}")
    
    # Vérifier la cohérence groupe/profil
    inconsistencies = []
    for assureur in Assureur.objects.select_related('user'):
        if not assureur.user.groups.filter(name='Assureur').exists() and not assureur.user.is_superuser:
            inconsistencies.append(assureur.user.username)
    
    if inconsistencies:
        print(f"   ❌ Incohérences: {len(inconsistencies)} profils sans groupe")
        for user in inconsistencies:
            print(f"      • {user}")
    else:
        print(f"   ✅ Tous les profils sont cohérents")
    
    # 4. Test des permissions de superutilisateur
    print("\n4. TEST SUPERUTILISATEUR:")
    
    try:
        matrix = User.objects.get(username='matrix')
        client.force_login(matrix)
        
        # Le superutilisateur devrait pouvoir accéder à tout
        response = client.get('/assureur/')
        status = "✅" if response.status_code == 200 else "❌"
        print(f"   {status} matrix (superuser): Dashboard -> {response.status_code}")
        
        # Test admin
        response = client.get('/admin/')
        status = "✅" if response.status_code == 200 else "❌"
        print(f"   {status} matrix (superuser): Admin -> {response.status_code}")
        
        client.logout()
    
    except User.DoesNotExist:
        print(f"   ❌ matrix: Superutilisateur non trouvé")
    
    print("\n" + "="*60)
    print("🧪 TESTS TERMINÉS")

if __name__ == "__main__":
    test_fonctionnalites_assureur()