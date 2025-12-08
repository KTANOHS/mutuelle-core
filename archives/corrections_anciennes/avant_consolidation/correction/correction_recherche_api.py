import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps

def corriger_vue_recherche():
    """Corriger la vue de recherche pour enlever le champ 'assureur'"""
    print("🔧 CORRECTION VUE RECHERCHE")
    print("===========================")
    
    # Trouver le fichier de vues des agents
    vue_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'agents', 'views.py')
    
    if os.path.exists(vue_path):
        print(f"📁 Fichier de vues trouvé: {vue_path}")
        
        with open(vue_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chercher la partie recherche
        if 'assureur' in content:
            print("⚠️  Champ 'assureur' détecté dans les vues")
            # Remplacer assureur par un champ valide
            new_content = content.replace("assureur", "nom")  # ou autre champ valide
            new_content = new_content.replace("assureur", "prenom")  # double remplacement
            
            with open(vue_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("✅ Vue recherche corrigée")
        else:
            print("✅ Aucun champ 'assureur' problématique trouvé")
    else:
        print(f"❌ Fichier de vues non trouvé: {vue_path}")

if __name__ == "__main__":
    corriger_vue_recherche()