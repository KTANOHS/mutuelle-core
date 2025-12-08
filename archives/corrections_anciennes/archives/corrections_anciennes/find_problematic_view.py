# find_problematic_view.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps

def find_views_using_date_creation():
    print("🔍 RECHERCHE DES VUES UTILISANT date_creation...")
    print("=" * 50)
    
    # Chercher dans les fichiers de vues
    view_files = [
        './medecin/views.py',
        './soins/views.py', 
        './assureur/views.py',
        './pharmacien/views.py',
        './membres/views.py'
    ]
    
    for view_file in view_files:
        if os.path.exists(view_file):
            print(f"\n📁 {view_file}:")
            with open(view_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines, 1):
                    if 'date_creation' in line and ('filter' in line or 'order_by' in line):
                        print(f"   Ligne {i}: {line.strip()}")

if __name__ == "__main__":
    find_views_using_date_creation()