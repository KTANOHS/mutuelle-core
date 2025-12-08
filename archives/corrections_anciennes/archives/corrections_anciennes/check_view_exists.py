# check_view_exists.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from medecin import views

def check_view():
    print("👁️ VÉRIFICATION DE LA VUE bons_attente")
    print("=" * 40)
    
    if hasattr(views, 'bons_attente'):
        print("✅ La vue 'bons_attente' existe dans medecin/views.py")
        return True
    else:
        print("❌ La vue 'bons_attente' n'existe pas dans medecin/views.py")
        print("Voici les vues disponibles:")
        for attr in dir(views):
            if not attr.startswith('_') and callable(getattr(views, attr)):
                print(f"  - {attr}")
        return False

if __name__ == "__main__":
    check_view()