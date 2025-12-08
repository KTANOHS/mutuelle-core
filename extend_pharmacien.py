# extend_pharmacien.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def extend_pharmacien():
    """Étend le modèle Pharmacien existant avec les nouvelles fonctionnalités"""
    
    print("🏪 EXTENSION DU MODULE PHARMACIEN")
    print("=" * 50)
    
    print("📦 Création des migrations...")
    os.system('python manage.py makemigrations pharmacien')
    
    print("🚀 Application des migrations...")
    os.system('python manage.py migrate')
    
    print("✅ Module pharmacien étendu avec succès!")
    print("\n🎯 Nouvelles fonctionnalités ajoutées:")
    print("   • Inscription publique des pharmacies")
    print("   • Recherche de pharmacies par localisation") 
    print("   • Pharmacies de garde")
    print("   • Catalogue de médicaments")
    print("   • Commandes en ligne")
    print("   • API publique")
    
    print("\n📋 URLs disponibles:")
    print("   /pharmacien/inscription/ - Inscription publique")
    print("   /pharmacien/pharmacies/ - Liste des pharmacies")
    print("   /pharmacien/pharmacies/garde/ - Pharmacies de garde")
    print("   /pharmacien/api/pharmacies-garde/ - API JSON")

if __name__ == "__main__":
    extend_pharmacien()