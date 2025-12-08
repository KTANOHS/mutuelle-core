#!/usr/bin/env python
import os
import sys
import django

# Trouver le bon settings module
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

# Essayer plusieurs noms de settings
settings_modules = [
    'settings',
    'projet.settings',
    'app.settings',
    'config.settings',
    'mutuelle_core.settings'
]

for settings_module in settings_modules:
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
        django.setup()
        print(f"✅ Settings module trouvé: {settings_module}")
        break
    except:
        continue

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

print("\n🔍 TEST SIMPLIFIÉ DES PERMISSIONS")
print("=" * 40)

# Option 1: Tester directement sans authentification
try:
    user = User.objects.get(username='GLORIA1')
    print(f"✅ Utilisateur trouvé: {user.username}")
    print(f"   Actif: {user.is_active}")
    print(f"   Superutilisateur: {user.is_superuser}")
    
    # Tester les permissions directement
    print("\n🔐 PERMISSIONS DIRECTES:")
    print("-" * 30)
    
    # Recharger l'utilisateur pour éviter le cache
    user = User.objects.get(pk=user.pk)
    
    permissions = [
        'medecin.view_ordonnance',
        'medecin.change_ordonnance',
        'pharmacien.view_stockpharmacie',
        'pharmacien.change_stockpharmacie',
    ]
    
    for perm in permissions:
        if user.has_perm(perm):
            print(f"✅ {perm}")
        else:
            print(f"❌ {perm}")
    
except User.DoesNotExist:
    print("❌ Utilisateur GLORIA1 non trouvé")

# Option 2: Essayer l'authentification
print("\n🔑 TEST D'AUTHENTIFICATION:")
print("-" * 30)

# Essayer plusieurs mots de passe possibles
passwords_to_try = [
    'Pharmacien123!',
    'NouveauMotDePasse123',
    'password123',
    'admin123',
    'gloria1',
    'pharmacien'
]

authenticated = False
for password in passwords_to_try:
    user = authenticate(username='GLORIA1', password=password)
    if user:
        print(f"✅ Authentification réussie avec le mot de passe: {password}")
        authenticated = True
        
        # Afficher quelques permissions
        print(f"\n📋 Groupes: {[g.name for g in user.groups.all()]}")
        
        # Vérifier une permission spécifique
        if user.has_perm('medecin.view_ordonnance'):
            print("✅ L'utilisateur peut voir les ordonnances")
        else:
            print("❌ L'utilisateur NE peut PAS voir les ordonnances")
            
        break

if not authenticated:
    print("❌ Aucun mot de passe n'a fonctionné")
    print("\n💡 Pour réinitialiser le mot de passe:")
    print("   python manage.py shell")
    print("   from django.contrib.auth.models import User")
    print("   user = User.objects.get(username='GLORIA1')")
    print("   user.set_password('VotreMotDePasse')")
    print("   user.save()")