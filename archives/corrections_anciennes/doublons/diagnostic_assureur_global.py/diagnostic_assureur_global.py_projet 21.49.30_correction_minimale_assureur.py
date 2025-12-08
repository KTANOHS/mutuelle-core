#!/usr/bin/env python
"""
CORRECTION MINIMALE - SYSTÈME ASSUREUR
Nettoie les groupes et corrige les incohérences sans toucher au superutilisateur.
"""

import os
import sys
import django
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from assureur.models import Assureur

print("🔧 CORRECTION MINIMALE - SYSTÈME ASSUREUR")
print("="*60)
print("⚠️  Le superutilisateur 'matrix' sera préservé")
print("="*60)

corrections = []

# 1. Supprimer le groupe vide "ASSUREUR" (majuscules)
try:
    groupe_vide = Group.objects.get(name='ASSUREUR')
    if groupe_vide.user_set.count() == 0:
        groupe_vide.delete()
        corrections.append("✅ Groupe vide 'ASSUREUR' supprimé")
    else:
        corrections.append("⚠️  Groupe 'ASSUREUR' non vide, conservé")
except Group.DoesNotExist:
    corrections.append("✅ Pas de groupe 'ASSUREUR' à supprimer")

# 2. S'assurer qu'on a le groupe "Assureur" (avec A majuscule)
try:
    groupe_assureur = Group.objects.get(name='Assureur')
    corrections.append(f"✅ Groupe 'Assureur' existe déjà")
except Group.DoesNotExist:
    groupe_assureur = Group.objects.create(name='Assureur')
    corrections.append("✅ Groupe 'Assureur' créé")

# 3. Pour TOUS les profils Assureur (sauf superusers), vérifier qu'ils sont dans le groupe
assureurs = Assureur.objects.select_related('user').all()
for assureur in assureurs:
    user = assureur.user
    
    if user.is_superuser:
        # Ne PAS modifier les superutilisateurs
        continue
    
    if not user.groups.filter(name='Assureur').exists():
        user.groups.add(groupe_assureur)
        corrections.append(f"✅ {user.username}: Ajouté au groupe Assureur")

# 4. Pour TOUS les utilisateurs normaux dans le groupe, vérifier qu'ils ont un profil
for user in groupe_assureur.user_set.filter(is_superuser=False):
    try:
        Assureur.objects.get(user=user)
    except Assureur.DoesNotExist:
        # Créer le profil pour les utilisateurs normaux
        assureur = Assureur.objects.create(
            user=user,
            numero_employe=user.username,
            departement="Service Client",
            date_embauche=date.today(),
            est_actif=True
        )
        corrections.append(f"✅ Profil créé pour {user.username}")

# 5. Afficher le récapitulatif
print("\n📋 RÉCAPITULATIF DES CORRECTIONS:")
print("="*60)

for correction in corrections:
    print(correction)

# 6. État final
print("\n📊 ÉTAT FINAL:")
print("="*60)

# Compter
normal_users = groupe_assureur.user_set.filter(is_superuser=False)
superusers = groupe_assureur.user_set.filter(is_superuser=True)

print(f"👥 Groupe 'Assureur': {normal_users.count()} utilisateur(s) normal(aux)")
for user in normal_users:
    print(f"  • {user.username}")

if superusers.exists():
    print(f"\n👑 Groupe 'Assureur': {superusers.count()} superutilisateur(s)")
    for user in superusers:
        print(f"  👑 {user.username} (SUPERUTILISATEUR - non modifié)")

# Profils
total_profiles = Assureur.objects.count()
normal_profiles = Assureur.objects.filter(user__is_superuser=False).count()
super_profiles = Assureur.objects.filter(user__is_superuser=True).count()

print(f"\n📋 Profils Assureur:")
print(f"  • Total: {total_profiles}")
print(f"  • Utilisateurs normaux: {normal_profiles}")
print(f"  • Superutilisateurs: {super_profiles}")

print("\n✅ Correction terminée!")
print("⚠️  Le superutilisateur 'matrix' est resté intact")