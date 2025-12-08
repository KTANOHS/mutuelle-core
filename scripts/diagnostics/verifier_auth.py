#!/usr/bin/env python
"""
Script pour vérifier l'authentification de GLORIA1
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import get_backends
from django.conf import settings

def test_backends():
    """Teste tous les backends d'authentification"""
    print("🔍 TEST DES BACKENDS D'AUTHENTIFICATION")
    print("=" * 60)
    
    User = get_user_model()
    
    # Récupère tous les backends
    backends = get_backends()
    print(f"Backends disponibles: {len(backends)}")
    
    for i, backend in enumerate(backends):
        print(f"\n{i+1}. {backend.__class__.__name__}:")
        print(f"   Module: {backend.__module__}")
    
    # Test avec chaque backend
    username = 'GLORIA1'
    password = 'Pharmacien123!'  # Avec point d'exclamation
    
    print(f"\n🔐 Test d'authentification pour {username}")
    print(f"Mot de passe testé: {password}")
    
    # Méthode 1: authenticate() standard
    print("\n1. Méthode authenticate() standard:")
    user = authenticate(username=username, password=password)
    if user:
        print(f"   ✅ Authentification réussie")
        print(f"   User: {user.username}")
        print(f"   Backend: {user.backend}")
    else:
        print(f"   ❌ Authentification échouée")
    
    # Méthode 2: Test avec chaque backend individuellement
    print("\n2. Test avec chaque backend individuellement:")
    for backend in backends:
        try:
            user = backend.authenticate(None, username=username, password=password)
            if user:
                print(f"   ✅ {backend.__class__.__name__}: Authentification réussie")
            else:
                print(f"   ❌ {backend.__class__.__name__}: Échec")
        except Exception as e:
            print(f"   ⚠ {backend.__class__.__name__}: Erreur - {str(e)}")
    
    # Méthode 3: Vérification directe
    print("\n3. Vérification directe avec l'utilisateur:")
    try:
        user = User.objects.get(username=username)
        print(f"   ✅ Utilisateur trouvé dans DB: {user.username}")
        print(f"   Mot de passe hash: {user.password[:30]}...")
        print(f"   is_active: {user.is_active}")
        print(f"   last_login: {user.last_login}")
        
        # Test de vérification de mot de passe
        if user.check_password(password):
            print(f"   ✅ check_password() réussie")
        else:
            print(f"   ❌ check_password() échouée")
            
            # Test avec d'autres mots de passe possibles
            test_passwords = [
                'Pharmacien123',  # Sans point d'exclamation
                'Pharmacien123!', # Avec point d'exclamation
                'GLORIA1',        # Le username
                '',               # Vide
            ]
            
            print(f"   🔍 Test autres mots de passe:")
            for test_pwd in test_passwords:
                if user.check_password(test_pwd):
                    print(f"      ✅ Mot de passe correct: '{test_pwd}'")
                    break
            else:
                print(f"      ❌ Aucun mot de passe testé ne correspond")
                
    except User.DoesNotExist:
        print(f"   ❌ Utilisateur {username} non trouvé")

def reinitialiser_complet():
    """Réinitialisation complète de GLORIA1"""
    print("\n" + "=" * 60)
    print("🔄 RÉINITIALISATION COMPLÈTE")
    print("=" * 60)
    
    User = get_user_model()
    
    try:
        # 1. Récupère l'utilisateur
        user = User.objects.get(username='GLORIA1')
        
        # 2. Définit un nouveau mot de passe SANS point d'exclamation
        new_password = 'Pharmacien123'  # Sans point d'exclamation
        user.set_password(new_password)
        user.save()
        
        print(f"✅ Mot de passe mis à jour: {new_password}")
        print(f"   Username: GLORIA1")
        print(f"   Password: {new_password}")
        
        # 3. Test immédiat
        print("\n🧪 Test immédiat après réinitialisation:")
        
        # Test avec check_password
        if user.check_password(new_password):
            print("   ✅ check_password() réussie")
        else:
            print("   ❌ check_password() échouée")
        
        # Test avec authenticate
        auth_user = authenticate(username='GLORIA1', password=new_password)
        if auth_user:
            print(f"   ✅ authenticate() réussie")
            print(f"   User: {auth_user.username}")
        else:
            print(f"   ❌ authenticate() échouée")
        
        return user
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def tester_connexion_differentes_methodes():
    """Teste différentes méthodes de connexion"""
    print("\n" + "=" * 60)
    print("🔧 TEST DE DIFFÉRENTES MÉTHODES")
    print("=" * 60)
    
    # Méthode 1: Utiliser le client de test Django
    print("\n1. Méthode: Client Django (simule une requête web)")
    from django.test import Client
    client = Client()
    
    # Tente la connexion
    response = client.post('/accounts/login/', {
        'username': 'GLORIA1',
        'password': 'Pharmacien123',
    })
    
    print(f"   Status: {response.status_code}")
    print(f"   Redirect: {response.get('Location', 'Pas de redirection')}")
    if response.status_code == 302:
        print("   ✅ Redirection détectée (connexion réussie)")
    else:
        print("   ❌ Pas de redirection")
    
    # Méthode 2: Vérifier la session
    print("\n2. Méthode: Vérification de session")
    if client.session.get('_auth_user_id'):
        user_id = client.session['_auth_user_id']
        print(f"   ✅ Session active - User ID: {user_id}")
    else:
        print("   ❌ Aucune session active")
    
    # Méthode 3: Tester l'API directement
    print("\n3. Méthode: Test API direct")
    import requests
    
    session = requests.Session()
    
    # Récupère CSRF
    response = session.get('http://127.0.0.1:8000/accounts/login/')
    import re
    csrf_match = re.search(r'csrfmiddlewaretoken[\'"] value=[\'"]([^\'"]+)', response.text)
    
    if csrf_match:
        csrf_token = csrf_match.group(1)
        
        # Tente la connexion
        response = session.post('http://127.0.0.1:8000/accounts/login/', {
            'username': 'GLORIA1',
            'password': 'Pharmacien123',
            'csrfmiddlewaretoken': csrf_token,
        })
        
        print(f"   Status API: {response.status_code}")
        print(f"   Location: {response.headers.get('Location', 'Non spécifié')}")
        
        if response.status_code == 302:
            print("   ✅ Connexion API réussie")
        else:
            print("   ❌ Connexion API échouée")

def main():
    """Fonction principale"""
    print("🔧 SCRIPT DE DÉPANNAGE - GLORIA1")
    print("=" * 60)
    
    # Vérifie les backends
    test_backends()
    
    # Réinitialisation
    print("\n" + "=" * 60)
    reponse = input("Voulez-vous réinitialiser GLORIA1 avec 'Pharmacien123' (sans !) ? (o/N): ").lower()
    if reponse == 'o':
        reinitialiser_complet()
    
    # Test différentes méthodes
    print("\n" + "=" * 60)
    reponse = input("Voulez-vous tester différentes méthodes de connexion ? (o/N): ").lower()
    if reponse == 'o':
        tester_connexion_differentes_methodes()
    
    print("\n" + "=" * 60)
    print("📋 RÉCAPITULATIF DES IDENTIFIANTS À ESSAYER:")
    print("=" * 60)
    print("Option 1 - Avec point d'exclamation:")
    print("   Username: GLORIA1")
    print("   Password: Pharmacien123!")
    print()
    print("Option 2 - Sans point d'exclamation:")
    print("   Username: GLORIA1")
    print("   Password: Pharmacien123")
    print()
    print("🔗 URL de test: http://127.0.0.1:8000/accounts/login/")

if __name__ == "__main__":
    main()