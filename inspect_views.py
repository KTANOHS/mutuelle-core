# inspect_views.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

# Importer les vues de assureur
try:
    import assureur.views
    print("="*70)
    print("🔍 INSPECTION DES VUES DANS assureur.views")
    print("="*70)
    
    # Lister toutes les classes dans le module
    for name in dir(assureur.views):
        obj = getattr(assureur.views, name)
        if isinstance(obj, type):  # C'est une classe
            print(f"\n📋 Classe: {name}")
            # Vérifier si c'est une vue (hérite de View ou a des méthodes HTTP)
            if hasattr(obj, 'as_view'):
                print(f"   ✅ C'est une vue Django")
                # Essayer d'inspecter la méthode get_queryset si elle existe
                if hasattr(obj, 'get_queryset'):
                    print(f"   ⚙️  A une méthode get_queryset")
except Exception as e:
    print(f"Erreur: {e}")