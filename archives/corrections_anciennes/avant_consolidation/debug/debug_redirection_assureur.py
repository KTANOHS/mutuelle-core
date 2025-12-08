
#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

print("🔍 DÉBOGAGE REDIRECTION /assureur/")
print("=" * 40)

client = Client()

# Tester avec ktanos (qui fonctionne mais redirige mal)
print("\n🔍 Test avec ktanos:")
if client.login(username='ktanos', password='ktanos'):
    print("✅ Connexion réussie")
    
    # Tester directement l'accès à /assureur/
    response = client.get('/assureur/', follow=False)
    print(f"🔗 GET /assureur/ - Status: {response.status_code}")
    
    if response.status_code == 302:
        print(f"🔀 Redirection vers: {response.headers.get('Location')}")
        
        # Suivre la redirection
        response2 = client.get('/assureur/', follow=True)
        print(f"📄 Après suivi - Status: {response2.status_code}")
        print(f"📍 URL finale: {response2.request['PATH_INFO']}")
    
    client.logout()

# Vérifier la vue assureur
print("\n🔍 Vérification de la vue assureur...")
views_path = os.path.join(os.getcwd(), 'assureur', 'views.py')

if os.path.exists(views_path):
    with open(views_path, 'r') as f:
        content = f.read()
    
    print("📄 Analyse de la vue assureur:")
    
    # Chercher des décorateurs problématiques
    import re
    
    # Chercher @staff_member_required ou login_required avec vérification staff
    patterns = [
        (r'@staff_member_required', 'Décorateur staff_member_required (PROBLÈME!)'),
        (r'user_passes_test.*staff', 'Vérification staff (PROBLÈME!)'),
        (r'@login_required', 'Décorateur login_required'),
        (r'@assureur_required', 'Décorateur assureur_required'),
    ]
    
    for pattern, description in patterns:
        if re.search(pattern, content):
            print(f"   🔍 {description} trouvé")
    
    # Chercher la fonction de vue principale
    view_functions = re.findall(r'def (\w+).*\(request.*\):', content)
    print(f"   📋 Fonctions de vue trouvées: {view_functions}")
    
    # Afficher un extrait autour de la première fonction
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('def ') and '(' in line and '):' in line:
            print(f"\n📝 Extrait de la fonction {line.strip()}:")
            start = max(0, i-2)
            end = min(len(lines), i+10)
            for j in range(start, end):
                print(f"{j+1:3}: {lines[j]}")
            break

print("\n🔍 Test de la fonction get_user_redirect_url pour ktanos:")
user = User.objects.get(username='ktanos')
from core.utils import get_user_redirect_url, get_user_primary_group

print(f"   get_user_primary_group: {get_user_primary_group(user)}")
print(f"   get_user_redirect_url: {get_user_redirect_url(user)}")

print("\n🔍 Test d'accès direct à /assureur/ sans login:")
response = client.get('/assureur/', follow=True)
print(f"   Status: {response.status_code}")
print(f"   Redirections: {response.redirect_chain}")
if response.redirect_chain:
    for url, status in response.redirect_chain:
        print(f"     {status} -> {url}")


