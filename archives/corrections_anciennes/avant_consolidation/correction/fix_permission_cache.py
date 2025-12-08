#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def test_with_auth():
    """Tester avec authentification réelle"""
    print("🧪 TEST AVEC AUTHENTIFICATION RÉELLE")
    print("=" * 40)
    
    # Remplacez par le vrai mot de passe de GLORIA1
    password = "votremotdepasse"  # À modifier !
    
    # Authentifier
    user = authenticate(username='GLORIA1', password=password)
    
    if not user:
        print("❌ Échec de l'authentification")
        print("💡 Vérifiez le mot de passe dans le script")
        return
    
    print(f"✅ Authentifié: {user.username}")
    print(f"📋 Groupes: {[g.name for g in user.groups.all()]}")
    
    # Tester les permissions
    test_permissions = [
        ('medecin.view_ordonnance', 'Voir ordonnances médecin'),
        ('medecin.change_ordonnance', 'Modifier ordonnances médecin'),
        ('medecin.add_ordonnance', 'Ajouter ordonnances médecin'),
        ('medecin.delete_ordonnance', 'Supprimer ordonnances médecin'),
        ('pharmacien.view_ordonnancepharmacien', 'Voir ordonnances pharmacien'),
        ('pharmacien.change_ordonnancepharmacien', 'Modifier ordonnances pharmacien'),
        ('pharmacien.add_ordonnancepharmacien', 'Ajouter ordonnances pharmacien'),
        ('pharmacien.delete_ordonnancepharmacien', 'Supprimer ordonnances pharmacien'),
    ]
    
    print("\n🔍 TEST DES PERMISSIONS:")
    print("-" * 30)
    
    for perm_code, perm_name in test_permissions:
        if user.has_perm(perm_code):
            print(f"✅ {perm_name}")
        else:
            print(f"❌ {perm_name}")
    
    # Vérifier si c'est un problème de superutilisateur
    print(f"\n👑 Superutilisateur: {user.is_superuser}")
    print(f"👔 Staff: {user.is_staff}")
    
    # Afficher le nombre total de permissions
    all_perms = user.get_all_permissions()
    print(f"\n📊 Total permissions: {len(all_perms)}")
    
    # Compter par application
    from collections import defaultdict
    app_counts = defaultdict(int)
    for perm in all_perms:
        app = perm.split('.')[0]
        app_counts[app] += 1
    
    print("📦 Permissions par application:")
    for app, count in sorted(app_counts.items()):
        print(f"   {app}: {count}")

if __name__ == "__main__":
    test_with_auth()