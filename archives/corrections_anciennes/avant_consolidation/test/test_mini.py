#!/usr/bin/env python
"""
MINI-SCRIPT DE TEST DES CONNEXIONS
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.utils import get_user_primary_group, get_user_redirect_url

print("🧪 TEST RAPIDE DES CONNEXIONS")
print("=" * 40)

client = Client()

# Test spécial DOUA1
print("\n🔍 TEST SPÉCIAL DOUA1:")
doua1 = User.objects.get(username='DOUA1')
print(f"   Groupes Django: {[g.name for g in doua1.groups.all()]}")
print(f"   get_user_primary_group: {get_user_primary_group(doua1)}")
print(f"   get_user_redirect_url: {get_user_redirect_url(doua1)}")

if client.login(username='DOUA1', password='DOUA1'):
    print("   ✅ Connexion réussie")
    response = client.get('/redirect-after-login/', follow=True)
    final_url = response.request['PATH_INFO']
    print(f"   🎯 URL finale: {final_url}")
    
    if '/assureur/' in final_url or 'assureur' in final_url:
        print("   ✅ DOUA1 correctement redirigé vers l'espace assureur")
    else:
        print(f"   ❌ PROBLÈME: DOUA1 redirigé vers {final_url}")
else:
    print("   ❌ Échec de connexion")

# Test rapide de tous les utilisateurs
print("\n🔍 TEST DE TOUS LES UTILISATEURS:")
tests = [
    ("DOUA", "DOUA", "/assureur/"),
    ("ktanos", "ktanos", "/assureur/"),
    ("ORNELLA", "ORNELLA", "/agents/tableau-de-bord/"),
    ("Yacouba", "Yacouba", "/medecin/dashboard/"),
    ("GLORIA", "GLORIA", "/pharmacien/dashboard/"),
    ("ASIA", "ASIA", "/membres/dashboard/"),
]

for username, password, expected in tests:
    print(f"\n👤 {username}:")
    
    # Réinitialiser le client
    client = Client()
    
    if client.login(username=username, password=password):
        print("   ✅ Connexion réussie")
        
        user = User.objects.get(username=username)
        print(f"   📊 Groupe détecté: {get_user_primary_group(user)}")
        
        response = client.get('/redirect-after-login/', follow=True)
        final_url = response.request['PATH_INFO']
        print(f"   🎯 URL finale: {final_url}")
        
        if expected in final_url:
            print(f"   ✅ Redirection correcte")
        else:
            print(f"   ⚠️  Redirection inattendue")
    else:
        print("   ❌ Échec de connexion")

print("\n✅ TEST TERMINÉ")