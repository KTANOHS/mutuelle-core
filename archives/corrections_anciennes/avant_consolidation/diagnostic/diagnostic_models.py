# diagnostic_models.py
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')  # Remplacez par votre vrai nom de projet
django.setup()

def diagnostic_models():
    print("🔍 DIAGNOSTIC DES MODÈLES")
    print("=" * 50)
    
    # Vérifier Assureur
    try:
        from assureur.models import Assureur
        print("✅ Modèle Assureur importé")
        print(f"   Champs disponibles: {[f.name for f in Assureur._meta.get_fields()]}")
    except Exception as e:
        print(f"❌ Erreur Assureur: {e}")
    
    # Vérifier Agent
    try:
        from agents.models import Agent
        print("✅ Modèle Agent importé")
        print(f"   Champs disponibles: {[f.name for f in Agent._meta.get_fields()]}")
    except Exception as e:
        print(f"❌ Erreur Agent: {e}")
        
    # Vérifier Membre
    try:
        from membres.models import Membre
        print("✅ Modèle Membre importé")
        print(f"   Champs disponibles: {[f.name for f in Membre._meta.get_fields()]}")
    except Exception as e:
        print(f"❌ Erreur Membre: {e}")
        
    # Vérifier BonSoin
    try:
        from agents.models import BonSoin
        print("✅ Modèle BonSoin importé")
        print(f"   Champs disponibles: {[f.name for f in BonSoin._meta.get_fields()]}")
    except Exception as e:
        print(f"❌ Erreur BonSoin: {e}")

if __name__ == "__main__":
    diagnostic_models()