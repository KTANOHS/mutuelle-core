# temp_ordonnance_fix.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def temp_ordonnance_fix():
    """Solution temporaire pour la validation des ordonnances"""
    print("🔄 SOLUTION TEMPORAIRE ORDONNANCES...")
    
    # Vérifier le fichier soins/models.py
    soins_models_path = 'soins/models.py'
    
    try:
        with open(soins_models_path, 'r') as f:
            content = f.read()
        
        # Vérifier si la propriété est_valide existe
        if 'def est_valide' in content:
            print("✅ Propriété est_valide trouvée dans soins/models.py")
            
            # Trouver et afficher la propriété
            start = content.find('def est_valide')
            if start != -1:
                end = content.find('def ', start + 1)
                if end == -1:
                    end = len(content)
                prop_content = content[start:end]
                print("📋 Contenu de est_valide:")
                print(prop_content[:500] + "..." if len(prop_content) > 500 else prop_content)
        else:
            print("❌ Propriété est_valide non trouvée")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    temp_ordonnance_fix()