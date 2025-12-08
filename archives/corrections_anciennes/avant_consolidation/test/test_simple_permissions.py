#!/usr/bin/env python
"""
TEST SIMPLE DES PERMISSIONS
"""
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mutuelle_core.settings")
django.setup()

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Permission, Group

def test_permissions():
    print("🧪 TEST DES PERMISSIONS DE GLORIA1")
    print("=" * 50)
    
    # Authentification
    user = authenticate(username="GLORIA1", password="Pharmacien123!")
    
    if not user:
        print("❌ Échec d'authentification")
        return
    
    print(f"✅ Authentifié: {user.username}")
    print(f"Groupes: {[g.name for g in user.groups.all()]}")
    
    # Test des permissions spécifiques
    print("\n🔍 TEST DES PERMISSIONS:")
    
    permissions_to_test = [
        ("view_ordonnance", "Voir les ordonnances"),
        ("change_ordonnance", "Modifier les ordonnances"),
        ("view_stockpharmacie", "Voir le stock"),
        ("change_stockpharmacie", "Modifier le stock"),
        ("view_pharmacien", "Voir le profil pharmacien"),
    ]
    
    for perm_codename, description in permissions_to_test:
        # Essaie avec différents app_labels
        found = False
        app_labels = ["ordonnances", "pharmacien", "soins", "ordonnance"]
        
        for app_label in app_labels:
            if user.has_perm(f"{app_label}.{perm_codename}"):
                print(f"✅ {description}: OUI ({app_label}.{perm_codename})")
                found = True
                break
        
        if not found and user.has_perm(perm_codename):
            print(f"✅ {description}: OUI ({perm_codename})")
            found = True
        
        if not found:
            print(f"❌ {description}: NON")

if __name__ == "__main__":
    test_permissions()
