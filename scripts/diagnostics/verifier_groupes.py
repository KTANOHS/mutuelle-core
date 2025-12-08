#!/usr/bin/env python3
"""
SCRIPT DE VÉRIFICATION DES GROUPES ET PERMISSIONS
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission

def verifier_utilisateurs_et_groupes():
    """Vérifie tous les utilisateurs et leurs groupes"""
    
    print("🔍 VÉRIFICATION COMPLÈTE DES UTILISATEURS ET GROUPES")
    print("=" * 60)
    
    # Tous les utilisateurs
    print("\n👥 TOUS LES UTILISATEURS:")
    for user in User.objects.all().order_by('username'):
        groupes = user.groups.all()
        groupes_str = ", ".join([g.name for g in groupes]) if groupes else "Aucun groupe"
        statut = "🟢 Staff" if user.is_staff else "🔵 Normal"
        print(f"   {statut} {user.username} ({user.get_full_name()}) → Groupes: {groupes_str}")
    
    # Détail par groupe
    print("\n📊 DÉTAIL PAR GROUPE:")
    for groupe in Group.objects.all().order_by('name'):
        membres = groupe.user_set.all()
        if membres:
            print(f"\n👥 {groupe.name} ({len(membres)} membres):")
            for user in membres:
                print(f"   👤 {user.username} - {user.get_full_name()}")
            
            # Permissions du groupe
            permissions = groupe.permissions.all()
            if permissions:
                print(f"   🔐 Permissions ({len(permissions)}):")
                for perm in permissions[:5]:  # Limiter à 5 pour la lisibilité
                    print(f"      • {perm.name}")
                if len(permissions) > 5:
                    print(f"      • ... et {len(permissions) - 5} autres")
    
    # Utilisateurs sans groupe
    utilisateurs_sans_groupe = User.objects.filter(groups__isnull=True)
    if utilisateurs_sans_groupe.exists():
        print(f"\n⚠️  UTILISATEURS SANS GROUPE ({utilisateurs_sans_groupe.count()}):")
        for user in utilisateurs_sans_groupe:
            print(f"   👤 {user.username} - {user.get_full_name()}")

def statistiques():
    """Affiche les statistiques"""
    
    print("\n📈 STATISTIQUES:")
    print(f"   • Utilisateurs totaux: {User.objects.count()}")
    print(f"   • Groupes totaux: {Group.objects.count()}")
    print(f"   • Permissions totales: {Permission.objects.count()}")
    
    for groupe in Group.objects.all():
        print(f"   • {groupe.name}: {groupe.user_set.count()} membres")

if __name__ == "__main__":
    verifier_utilisateurs_et_groupes()
    statistiques()