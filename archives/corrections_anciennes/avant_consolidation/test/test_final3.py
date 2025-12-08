#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import authenticate

# Test d'authentification
user = authenticate(username='GLORIA1', password='Pharmacien123!')

if user:
    print(f"✅ Authentifié: {user.username}")
    
    # Test des permissions critiques
    tests = [
        ('medecin.view_ordonnance', 'Peut voir les ordonnances'),
        ('medecin.change_ordonnance', 'Peut modifier les ordonnances'),
        ('pharmacien.view_ordonnancepharmacien', 'Peut voir ordonnances pharmacien'),
    ]
    
    for perm, desc in tests:
        result = user.has_perm(perm)
        print(f"{'✅' if result else '❌'} {desc}: {'OUI' if result else 'NON'}")
else:
    print("❌ Échec d'authentification")