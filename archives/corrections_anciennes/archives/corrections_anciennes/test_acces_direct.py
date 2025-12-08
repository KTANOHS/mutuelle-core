#!/usr/bin/env python
"""
TEST D'ACCÈS DIRECT À L'URL
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_acces_direct():
    """Test d'accès direct à l'URL avec différents utilisateurs"""
    print("🎯 TEST D'ACCÈS DIRECT À L'URL")
    print("=" * 60)
    
    client = Client()
    url = '/assureur/bons/creer/5/'
    
    print(f"URL testée: {url}")
    
    # 1. Test sans connexion
    print("\n1. 🔓 SANS CONNEXION:")
    response = client.get(url)
    print(f"   Status: {response.status_code}")
    print(f"   Redirection: {response.url if response.status_code == 302 else 'Non'}")
    
    # 2. Test avec utilisateur normal
    print("\n2. 👤 UTILISATEUR NORMAL:")
    try:
        user_normal = User.objects.get(username='membre_test')
        client.force_login(user_normal)
        response = client.get(url)
        print(f"   Status: {response.status_code}")
        print(f"   Redirection: {response.url if response.status_code == 302 else 'Non'}")
    except User.DoesNotExist:
        print("   ❌ Utilisateur membre_test non trouvé")
    
    # 3. Test avec assureur
    print("\n3. 🏥 UTILISATEUR ASSUREUR:")
    try:
        user_assureur = User.objects.filter(groups__name='Assureur').first()
        if user_assureur:
            client.force_login(user_assureur)
            response = client.get(url)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ ACCÈS AUTORISÉ!")
            else:
                print(f"   ❌ Accès refusé: {response.status_code}")
        else:
            print("   ❌ Aucun utilisateur assureur trouvé")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 4. Test avec staff
    print("\n4. 🔧 UTILISATEUR STAFF:")
    try:
        user_staff = User.objects.filter(is_staff=True).first()
        if user_staff:
            client.force_login(user_staff)
            response = client.get(url)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ ACCÈS AUTORISÉ!")
            else:
                print(f"   ❌ Accès refusé: {response.status_code}")
        else:
            print("   ❌ Aucun utilisateur staff trouvé")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

if __name__ == "__main__":
    test_acces_direct()