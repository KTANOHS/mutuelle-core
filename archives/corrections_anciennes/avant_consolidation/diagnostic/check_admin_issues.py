# check_admin_issues.py
import os
import sys
import django
from django.conf import settings

# Configuration Django minimale
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.admin.sites import site

def check_admin_issues():
    """Vérifie tous les ModelAdmin pour des problèmes d'actions"""
    print("🔍 Diagnostic des problèmes Admin...")
    
    for model, admin_class in site._registry.items():
        admin_instance = admin_class(model, site)
        
        # Vérifier l'attribut actions
        actions = getattr(admin_instance, 'actions', None)
        
        if actions is not None:
            if callable(actions):
                print(f"❌ PROBLÈME: {admin_class.__module__}.{admin_class.__name__} - actions est une méthode")
            elif isinstance(actions, str):
                print(f"❌ PROBLÈME: {admin_class.__module__}.{admin_class.__name__} - actions est un string")
            elif not isinstance(actions, (list, tuple)):
                print(f"❌ PROBLÈME: {admin_class.__module__}.{admin_class.__name__} - actions a un type invalide: {type(actions)}")
            else:
                print(f"✅ OK: {admin_class.__module__}.{admin_class.__name__}")

if __name__ == "__main__":
    check_admin_issues()