#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.test import Client

print("🔍 VÉRIFICATION APRÈS CORRECTIONS")
print("=" * 40)

client = Client()

# Vérifier les assureurs
assureurs = User.objects.filter(groups__name='Assureur')
print("\n👥 ASSUREURS CORRIGÉS:")
for assureur in assureurs:
    print(f"\n• {assureur.username}:")
    print(f"  is_staff: {assureur.is_staff}")
    print(f"  is_superuser: {assureur.is_superuser}")
    print(f"  Groupes: {[g.name for g in assureur.groups.all()]}")
    
    # Tester la connexion
    if client.login(username=assureur.username, password=assureur.username):
        print(f"  ✅ Connexion réussie")
        
        # Tester la redirection
        response = client.get('/redirect-after-login/', follow=True)
        if response.redirect_chain:
            print(f"  🔗 Redirections:")
            for i, (url, status) in enumerate(response.redirect_chain):
                print(f"    {i+1}. {status} -> {url}")
        
        client.logout()
    else:
        print(f"  ❌ Échec connexion")

# Vérifier ORNELLA
print("\n👤 ORNELLA (Agent):")
ornella = User.objects.get(username='ORNELLA')
try:
    from agents.models import Agent
    agent = Agent.objects.filter(user=ornella).first()
    if agent:
        print(f"  ✅ Profil Agent trouvé: {agent}")
    else:
        print(f"  ❌ Profil Agent non trouvé")
except Exception as e:
    print(f"  ⚠️  Erreur: {e}")

if client.login(username='ORNELLA', password='ORNELLA'):
    print(f"  ✅ Connexion réussie")
    response = client.get('/redirect-after-login/', follow=True)
    if response.redirect_chain:
        print(f"  🔗 Redirections:")
        for url, status in response.redirect_chain:
            print(f"    {status} -> {url}")
    client.logout()

print("\n✅ VÉRIFICATION TERMINÉE")
