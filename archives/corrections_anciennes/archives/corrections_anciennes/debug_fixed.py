#!/usr/bin/env python
import os
import sys
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')  # Remplacez par votre vrai nom de projet
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User
from membres.models import Membre

print("🔍 DEBUG CRÉATION MEMBRE CORRIGÉ")
print("=" * 50)

# 1. Création d'un utilisateur de test
test_user, created = User.objects.get_or_create(
    username='debug_test',
    defaults={
        'first_name': 'Debug',
        'last_name': 'Test', 
        'email': 'debug@test.com',
        'password': 'testpass123'
    }
)

if created:
    print(f"✅ Utilisateur créé: {test_user.username}")
    print(f"   First name: '{test_user.first_name}'")
    print(f"   Last name: '{test_user.last_name}'")
else:
    print(f"✅ Utilisateur existant: {test_user.username}")

# 2. Création du membre AVEC les champs obligatoires
print("\n🔄 Tentative de création Membre...")
try:
    membre = Membre.objects.create(
        user=test_user,
        nom="Test",        # ⚠️ CHAMP OBLIGATOIRE
        prenom="Debug",    # ⚠️ CHAMP OBLIGATOIRE
        telephone="+2250102030405",  # Optionnel mais recommandé
        email="debug@test.com"       # Optionnel
    )
    
    print(f"✅ Membre créé avec succès!")
    print(f"   Numéro unique: {membre.numero_unique}")
    print(f"   Nom: {membre.nom}")
    print(f"   Prénom: {membre.prenom}") 
    print(f"   Statut: {membre.get_statut_display()}")
    print(f"   Catégorie: {membre.get_categorie_display()}")
    print(f"   Date inscription: {membre.date_inscription}")
    
except Exception as e:
    print(f"❌ Erreur création Membre: {e}")
    print(f"   Type d'erreur: {type(e).__name__}")
    print("\n📋 Stack trace complète:")
    import traceback
    traceback.print_exc()

print("=" * 50)
print("🔍 DEBUG TERMINÉ")