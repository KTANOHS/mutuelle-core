# Script de diagnostic
import os
import django
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    print("🔍 DIAGNOSTIC DES ADMIN CLASSES")
    print("=" * 50)
    
    # Vérifier toutes les classes admin enregistrées
    from django.contrib import admin
    site = admin.site
    
    for model, admin_class in site._registry.items():
        print(f"📊 {model._meta.app_label}.{model._meta.model_name}")
        print(f"   Admin: {admin_class.__class__.__name__}")
        
        # Vérifier si cette admin class a un attribut 'actions' problématique
        if hasattr(admin_class, 'actions'):
            actions_value = getattr(admin_class, 'actions')
            print(f"   ⚠️  ACTIONS: {type(actions_value)} - {actions_value}")
            
            if callable(actions_value):
                print(f"   ❌ PROBLÈME: 'actions' est une méthode!")
            elif isinstance(actions_value, (list, tuple)):
                print(f"   ✅ OK: 'actions' est une liste/tuple")
            else:
                print(f"   ⚠️  TYPE INATTENDU: {type(actions_value)}")
        
        print()
    
    print("🎯 RECHERCHE DES FICHIERS ADMIN PROBLEMATIQUES")
    print("=" * 50)
    
    # Chercher dans tous les fichiers admin.py
    import glob
    admin_files = glob.glob("*/admin.py") + glob.glob("*/*/admin.py")
    
    for admin_file in admin_files:
        print(f"📁 Vérification de {admin_file}")
        with open(admin_file, 'r') as f:
            content = f.read()
            if 'def actions(' in content:
                print(f"   ❌ TROUVÉ: Méthode 'actions' dans {admin_file}")
            if 'actions = ' in content and 'list_display' not in content:
                print(f"   ❌ TROUVÉ: Attribut 'actions' dans {admin_file}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")


