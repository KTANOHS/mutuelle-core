#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from assureur.models import Assureur

print("="*80)
print("🔍 ÉTAT ACTUEL DU SYSTÈME ASSUREUR")
print("="*80)

# 1. Vérifier les groupes
print("\n1. GROUPES ASSUREUR:")
assureur_groups = Group.objects.filter(name__icontains='assureur')
for group in assureur_groups:
    users = group.user_set.all()
    print(f"   • Groupe: {group.name} ({users.count()} utilisateurs)")
    for user in users:
        print(f"     - {user.username}")

# 2. Vérifier les profils Assureur
print("\n2. PROFILS ASSUREUR:")
assureurs = Assureur.objects.select_related('user').all()
print(f"   • Total profils: {assureurs.count()}")
for assureur in assureurs:
    # Vérifier si l'utilisateur est dans un groupe assureur
    user_groups = [g.name for g in assureur.user.groups.all()]
    is_in_assureur = any('assureur' in g.lower() for g in user_groups)
    
    status = "✅" if is_in_assureur else "❌"
    print(f"   {status} {assureur.user.username}: ID={assureur.id}, Département={assureur.departement}")
    if not is_in_assureur:
        print(f"        ⚠️  Groupes actuels: {user_groups}")

# 3. Problèmes à corriger
print("\n3. PROBLÈMES IDENTIFIÉS:")

# a. Utilisateurs sans profil
all_users_in_group = []
for group in assureur_groups:
    all_users_in_group.extend(list(group.user_set.all()))

for user in set(all_users_in_group):
    try:
        Assureur.objects.get(user=user)
    except Assureur.DoesNotExist:
        print(f"   ❌ {user.username}: Dans groupe assureur mais PAS de profil Assureur!")

# b. Profils sans groupe
for assureur in assureurs:
    user_groups = [g.name.lower() for g in assureur.user.groups.all()]
    if not any('assureur' in g for g in user_groups):
        print(f"   ❌ {assureur.user.username}: Profil Assureur mais PAS dans groupe assureur!")

# 4. Recommandations
print("\n4. RECOMMANDATIONS:")
if assureur_groups.count() > 1:
    print("   • Fusionner les groupes multiples en un seul 'Assureur'")

# Compter les incohérences
problems = sum(1 for assureur in assureurs 
               if not any('assureur' in g.name.lower() 
                         for g in assureur.user.groups.all()))

if problems == 0:
    print("   ✅ Tous les assureurs sont correctement configurés!")
else:
    print(f"   • Corriger {problems} incohérence(s) groupe/profil")

print("\n" + "="*80)
print("✅ Diagnostic terminé")