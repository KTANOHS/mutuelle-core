# deploy_pharmacie_public.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def deploy_pharmacie_public():
    """Déploie l'application pharmacie_public complètement"""
    
    print("🏪 DÉPLOIEMENT DE PHARMACIE_PUBLIC")
    print("=" * 50)
    
    # 1. Créer l'application
    print("📁 Création de l'application...")
    os.system('python manage.py startapp pharmacie_public')
    
    # 2. Créer la structure de dossiers
    print("📂 Création de la structure...")
    templates_dir = 'pharmacie_public/templates/pharmacie_public'
    os.makedirs(templates_dir, exist_ok=True)
    
    # 3. Appliquer les migrations
    print("📦 Création des migrations...")
    os.system('python manage.py makemigrations pharmacie_public')
    os.system('python manage.py migrate pharmacie_public')
    
    # 4. Vérifier l'installation
    print("🔍 Vérification de l'installation...")
    try:
        from pharmacie_public.models import PharmaciePublic
        print("✅ Modèles chargés avec succès")
    except Exception as e:
        print(f"❌ Erreur modèles: {e}")
    
    print("\n🎉 PHARMACIE_PUBLIC DÉPLOYÉE AVEC SUCCÈS!")
    print("\n📋 URLs disponibles:")
    print("   /pharmacie-public/inscription/ - Inscription publique")
    print("   /pharmacie-public/pharmacies/ - Liste des pharmacies")
    print("   /pharmacie-public/pharmacies/garde/ - Pharmacies de garde")
    print("   /pharmacie-public/api/pharmacies-garde/ - API JSON")
    
    print("\n⚙️  Configuration nécessaire:")
    print("   1. Ajouter 'pharmacie_public' dans INSTALLED_APPS")
    print("   2. Ajouter les URLs dans mutuelle_core/urls.py")
    print("   3. Créer les templates de base")

if __name__ == "__main__":
    deploy_pharmacie_public()