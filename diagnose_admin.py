# diagnose_admin.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors du setup Django: {e}")
    sys.exit(1)

from django.contrib.admin import sites
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin

def diagnose_admin_issues():
    """Diagnostique les problèmes d'administration"""
    print("🔍 Diagnostic approfondi de l'admin Django...")
    
    # Vérifier le site admin principal
    site = sites.site
    print(f"✅ Site admin: {site}")
    
    # Vérifier les modèles enregistrés
    print(f"✅ Nombre de modèles enregistrés: {len(site._registry)}")
    
    # Vérifier les problèmes connus avec Group
    try:
        group_admin = site._registry.get(Group)
        if group_admin:
            print(f"✅ GroupAdmin trouvé: {group_admin}")
            print(f"✅ GroupAdmin.actions: {getattr(group_admin, 'actions', 'Non défini')}")
        else:
            print("❌ GroupAdmin non trouvé dans le registre")
    except Exception as e:
        print(f"❌ Erreur avec GroupAdmin: {e}")
    
    # Vérifier chaque ModelAdmin
    problematic_admins = []
    
    for model, admin in site._registry.items():
        admin_class = admin.__class__
        admin_instance = admin
        
        try:
            # Vérifier l'attribut actions
            actions = getattr(admin_instance, 'actions', None)
            
            if actions is not None:
                if callable(actions):
                    problematic_admins.append(f"{admin_class.__module__}.{admin_class.__name__} - actions est une méthode")
                elif isinstance(actions, str):
                    problematic_admins.append(f"{admin_class.__module__}.{admin_class.__name__} - actions est un string")
                elif not isinstance(actions, (list, tuple)):
                    problematic_admins.append(f"{admin_class.__module__}.{admin_class.__name__} - actions a un type invalide: {type(actions)}")
                else:
                    print(f"✅ {admin_class.__module__}.{admin_class.__name__} - actions: {actions}")
            else:
                print(f"✅ {admin_class.__module__}.{admin_class.__name__} - pas d'actions")
                
        except Exception as e:
            problematic_admins.append(f"{admin_class.__module__}.{admin_class.__name__} - ERREUR: {e}")
    
    # Afficher les problèmes
    if problematic_admins:
        print("\n❌ ADMINISTRATEURS PROBLÉMATIQUES:")
        for problem in problematic_admins:
            print(f"   - {problem}")
    else:
        print("\n🎉 AUCUN PROBLÈME DÉTECTÉ !")
    
    return len(problematic_admins) == 0

if __name__ == "__main__":
    success = diagnose_admin_issues()
    sys.exit(0 if success else 1)