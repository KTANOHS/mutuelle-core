#!/usr/bin/env python
import os
import sys
import django
from django.utils import timezone

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')  # Remplacez par votre vrai projet
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User
from membres.models import Membre
import logging

logger = logging.getLogger(__name__)

print("🔍 DEBUG CRÉATION MEMBRE FINAL")
print("=" * 50)

# Nettoyage des données de test existantes
print("🧹 Nettoyage des données de test existantes...")
Membre.objects.filter(user__username='debug_test').delete()
User.objects.filter(username='debug_test').delete()

# 1. Création d'un utilisateur de test
test_user = User.objects.create_user(
    username='debug_test',
    first_name='Debug',
    last_name='Test', 
    email='debug@test.com',
    password='testpass123'
)

print(f"✅ Utilisateur créé: {test_user.username}")
print(f"   First name: '{test_user.first_name}'")
print(f"   Last name: '{test_user.last_name}'")

# 2. Génération manuelle d'un numéro unique pour éviter les conflits
annee = timezone.now().year
dernier_membre = Membre.objects.filter(
    numero_unique__startswith=f"MEM{annee}"
).order_by('-numero_unique').first()

if dernier_membre:
    try:
        dernier_numero = int(dernier_membre.numero_unique[-4:])
        nouveau_numero = dernier_numero + 1
    except (ValueError, IndexError):
        nouveau_numero = 1
else:
    nouveau_numero = 1

numero_unique_manuel = f"MEM{annee}{str(nouveau_numero).zfill(4)}"
print(f"🔢 Numéro unique généré: {numero_unique_manuel}")

# 3. Création du membre avec numéro unique manuel
print("\n🔄 Tentative de création Membre...")
try:
    membre = Membre(
        user=test_user,
        nom="Test",        
        prenom="Debug",    
        telephone="+2250102030405",
        email="debug@test.com",
        numero_unique=numero_unique_manuel  # On fournit le numéro unique manuellement
    )
    
    # On appelle save() manuellement pour éviter la génération automatique du numéro
    membre.save(force_insert=True)
    
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