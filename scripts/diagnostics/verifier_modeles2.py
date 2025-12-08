# verifier_modeles.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from soins.models import BonSoin
from paiements.models import Paiement
from agents.models import Agent

def analyser_modele(model, nom):
    """Analyse la structure d'un modèle"""
    print(f"\n🔍 ANALYSE DU MODÈLE: {nom}")
    print("=" * 50)
    
    # Champs du modèle
    print("📋 CHAMPS:")
    for field in model._meta.get_fields():
        print(f"   {field.name} ({field.__class__.__name__})")
    
    # Méthodes spéciales
    print("\n⚙️ MÉTHODES DISPONIBLES:")
    methodes = [meth for meth in dir(model) if not meth.startswith('_') or meth in ['__str__', 'save', 'delete']]
    for meth in sorted(methodes)[:10]:  # Premières 10 méthodes
        print(f"   {meth}")

print("✅ VÉRIFICATION DES MODÈLES")
print("=" * 60)

try:
    analyser_modele(Membre, "Membre")
except Exception as e:
    print(f"❌ Erreur analyse Membre: {e}")

try:
    analyser_modele(BonSoin, "BonSoin") 
except Exception as e:
    print(f"❌ Erreur analyse BonSoin: {e}")

try:
    analyser_modele(Paiement, "Paiement")
except Exception as e:
    print(f"❌ Erreur analyse Paiement: {e}")

try:
    analyser_modele(Agent, "Agent")
except Exception as e:
    print(f"❌ Erreur analyse Agent: {e}")

print("\n🎯 RECOMMANDATIONS:")
print("✅ Les modèles existent - l'import devrait maintenant fonctionner")
print("✅ Utilisez la version corrigée de agents/views.py")