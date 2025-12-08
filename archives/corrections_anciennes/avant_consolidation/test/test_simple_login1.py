#!/usr/bin/env python
"""
TEST SIMPLE DE CONNEXION GLORIA1
"""

import os
import sys
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import authenticate, get_user_model

print("🧪 TEST SIMPLE DE CONNEXION GLORIA1")
print("==================================")

# Test 1: Avec point d'exclamation
print("\nTest 1: Avec 'Pharmacien123!'")
user = authenticate(username='GLORIA1', password='Pharmacien123!')
if user:
    print('✅ SUCCÈS avec Pharmacien123!')
    print(f'   User: {user.username}')
else:
    print('❌ ÉCHEC avec Pharmacien123!')

# Test 2: Sans point d'exclamation
print("\nTest 2: Sans point d'exclamation")
user = authenticate(username='GLORIA1', password='Pharmacien123')
if user:
    print('✅ SUCCÈS avec Pharmacien123')
    print(f'   User: {user.username}')
else:
    print('❌ ÉCHEC avec Pharmacien123')

# Test 3: Vérification directe
print("\nTest 3: Vérification directe")
User = get_user_model()
try:
    user = User.objects.get(username='GLORIA1')
    print(f'User: {user.username}')
    print(f'Password hash: {user.password[:50]}...')
    print(f'is_active: {user.is_active}')

    # Test tous les mots de passe possibles
    passwords = ['Pharmacien123!', 'Pharmacien123', 'GLORIA1', '', 'Gloria123']
    for pwd in passwords:
        if user.check_password(pwd):
            print(f'✅ Mot de passe trouvé: "{pwd}"')
            break
    else:
        print('❌ Aucun mot de passe ne correspond')
except User.DoesNotExist:
    print('❌ Utilisateur GLORIA1 non trouvé')

print("\n" + "=" * 40)