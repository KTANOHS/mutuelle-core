#!/usr/bin/env python
import os
import sys
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')  # Remplacez par votre projet
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User
from membres.models import Membre

print("🔍 DEBUG CRÉATION MEMBRE SIMPLIFIÉ")
print("=" * 50)

# Création d'un utilisateur de test
test_user, created = User.objects.get_or_create(
    username='debug_test',
    defaults={
        'first_name': 'Debug',
        'last_name': 'Test',
        'email': 'debug@test.com'
    }
)

if created:
    print(f"✅ Utilisateur créé: {test_user.username}")
else:
    print(f"✅ Utilisateur existant: {test_user.username}")

print("\n🔄 Tentative de création Membre...")
try:
    membre = Membre.objects.create(
        user=test_user,
        nom="Test",      # Champ obligatoire
        prenom="Debug"   # Champ obligatoire
    )
    print(f"✅ Membre créé avec succès: {membre.numero_unique}")
    print(f"   Nom: {membre.nom}")
    print(f"   Prénom: {membre.prenom}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print("=" * 50)
print("🔍 DEBUG TERMINÉ")