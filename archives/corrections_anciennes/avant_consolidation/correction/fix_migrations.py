import os
import glob

def fix_migrations():
    """Corrige les problèmes de migrations"""
    
    # Supprimer les fichiers de migration sauf __init__.py
    migration_files = glob.glob("*/migrations/0*.py")
    for file in migration_files:
        os.remove(file)
        print(f"Supprimé: {file}")
    
    # Supprimer la base de données
    if os.path.exists("db.sqlite3"):
        os.remove("db.sqlite3")
        print("Base de données supprimée")
    
    print("✅ Nettoyage terminé")
    print("🎯 Exécutez maintenant:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    print("   python manage.py createsuperuser")
    print("   python manage.py runserver")

if __name__ == "__main__":
    fix_migrations()