# detect_project.py
import os
import sys

def detecter_projet():
    """Détecte automatiquement le nom du projet Django"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Chercher le fichier settings.py
    for root, dirs, files in os.walk(current_dir):
        if 'settings.py' in files:
            # Le nom du projet est le nom du dossier contenant settings.py
            project_name = os.path.basename(root)
            print(f"🔍 Projet détecté: {project_name}")
            return project_name
    
    # Fallback: chercher manage.py
    if 'manage.py' in os.listdir(current_dir):
        print("ℹ️ Manage.py trouvé, mais settings.py non localisé")
        return "projet"  # Fallback
    
    print("❌ Aucun projet Django détecté")
    return None

if __name__ == "__main__":
    projet = detecter_projet()
    if projet:
        print(f"✅ Utilisez: os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{projet}.settings')")