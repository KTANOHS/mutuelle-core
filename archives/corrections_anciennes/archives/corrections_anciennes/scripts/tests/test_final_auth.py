#!/usr/bin/env python
"""
TEST FINAL DE L'AUTHENTIFICATION - VÉRIFICATION DE LA BOUCLE
"""

import os
import django

# Configuration Django doit être la première chose
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    exit(1)

from django.test import Client
from django.contrib.auth.models import User
from core.utils import get_user_redirect_url, get_user_primary_group

def test_redirect_function():
    """Teste la fonction de redirection"""
    print("🧪 TEST DE LA FONCTION get_user_redirect_url")
    print("=" * 50)
    
    try:
        # Test avec un superuser
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            redirect_url = get_user_redirect_url(superuser)
            print(f"✅ Superuser -> {redirect_url}")
        else:
            print("ℹ️  Aucun superuser trouvé")
        
        # Test avec un utilisateur normal
        normal_user = User.objects.filter(is_superuser=False).first()
        if normal_user:
            redirect_url = get_user_redirect_url(normal_user)
            primary_group = get_user_primary_group(normal_user)
            groups = [g.name for g in normal_user.groups.all()]
            print(f"✅ Utilisateur normal -> {redirect_url}")
            print(f"   Groupe principal: {primary_group}")
            print(f"   Tous les groupes: {groups}")
        else:
            print("ℹ️  Aucun utilisateur normal trouvé")
        
        # Test avec utilisateur non authentifié
        print(f"✅ Non authentifié -> {get_user_redirect_url(None)}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

def test_auth_flow():
    """Teste le flux d'authentification complet"""
    print("\n🔐 TEST DU FLUX D'AUTHENTIFICATION")
    print("=" * 50)
    
    try:
        client = Client()
        
        # 1. Test page login
        print("\n1. 📝 Page de login...")
        response = client.get('/accounts/login/')
        print(f"   Status: {response.status_code} (attendu: 200)")
        
        # 2. Test redirection si déjà connecté
        print("\n2. 🔄 Redirection si connecté...")
        user = User.objects.filter(is_superuser=False).first()
        if user:
            client.force_login(user)
            response = client.get('/accounts/login/', follow=False)
            print(f"   Status: {response.status_code}")
            if response.status_code == 302:
                print(f"   Redirection vers: {response.url}")
        
        # 3. Test accès dashboard
        print("\n3. 🏠 Accès dashboard...")
        response = client.get('/dashboard/')
        print(f"   Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test d'authentification: {e}")

def check_actual_urls():
    """Vérifie que les URLs existent réellement"""
    print("\n🌐 VÉRIFICATION DES URLs RÉELLES")
    print("=" * 50)
    
    try:
        client = Client()
        
        urls_to_check = [
            '/',
            '/accounts/login/',
            '/dashboard/',
            '/admin/',
            '/assureur/dashboard/',
            '/medecin/dashboard/',
            '/pharmacien/dashboard/'
        ]
        
        for url in urls_to_check:
            try:
                response = client.get(url, follow=False)
                print(f"🔗 {url:25} -> Status: {response.status_code}")
            except Exception as e:
                print(f"🔗 {url:25} -> Erreur: {e}")
                
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des URLs: {e}")

def check_configuration():
    """Vérifie la configuration Django"""
    print("🔧 CONFIGURATION DJANGO")
    print("=" * 50)
    
    from django.conf import settings
    
    configs = [
        ('DEBUG', settings.DEBUG),
        ('LOGIN_REDIRECT_URL', getattr(settings, 'LOGIN_REDIRECT_URL', 'Non défini')),
        ('LOGIN_URL', getattr(settings, 'LOGIN_URL', 'Non défini')),
        ('LOGOUT_REDIRECT_URL', getattr(settings, 'LOGOUT_REDIRECT_URL', 'Non défini')),
    ]
    
    for key, value in configs:
        print(f"   {key}: {value}")

if __name__ == "__main__":
    check_configuration()
    test_redirect_function()
    test_auth_flow()
    check_actual_urls()
    
    print("\n" + "=" * 60)
    print("🎯 TEST TERMINÉ")
    print("=" * 60)