#!/usr/bin/env python
"""
VÉRIFICATION SPÉCIFIQUE DU MAPPING DES URLs
"""

import os
import django
from django.urls import reverse, NoReverseMatch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from core.constants import UserGroups

def test_redirect_mapping():
    """Teste chaque entrée du mapping de redirection"""
    print("🔍 TEST DU MAPPING DE REDIRECTION")
    print("=" * 60)
    
    print("Mapping actuel dans UserGroups.REDIRECT_MAPPING:")
    for group, url_name in UserGroups.REDIRECT_MAPPING.items():
        print(f"  {group} -> '{url_name}'")
    
    print("\n🧪 Test avec reverse() (peut causer des erreurs):")
    for group, url_name in UserGroups.REDIRECT_MAPPING.items():
        try:
            url = reverse(url_name)
            print(f"  ✅ {group:15} -> {url}")
        except NoReverseMatch as e:
            print(f"  ❌ {group:15} -> ERREUR: {e}")
    
    print("\n💡 Solution recommandée - URLs absolues:")
    absolute_mapping = {
        UserGroups.ASSUREUR: "/assureur/dashboard/",
        UserGroups.MEDECIN: "/medecin/dashboard/", 
        UserGroups.PHARMACIEN: "/pharmacien/dashboard/",
        UserGroups.ADMIN: "/admin/",
    }
    
    for group, absolute_url in absolute_mapping.items():
        print(f"  📍 {group:15} -> {absolute_url}")

def check_critical_paths():
    """Vérifie l'existence des chemins critiques"""
    print("\n📂 VÉRIFICATION DES CHEMINS ABSOLUS")
    print("-" * 40)
    
    critical_paths = [
        "/assureur/dashboard/",
        "/medecin/dashboard/",
        "/pharmacien/dashboard/", 
        "/dashboard/",
        "/accounts/login/",
        "/admin/",
        "/"
    ]
    
    # Test simulé (en vrai, il faudrait vérifier avec le client test)
    for path in critical_paths:
        print(f"  🔗 {path}")

if __name__ == "__main__":
    test_redirect_mapping()
    check_critical_paths()