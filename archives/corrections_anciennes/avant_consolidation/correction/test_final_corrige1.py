import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from django.db.models import Q

def test_recherche_finale():
    print("🎯 TEST FINAL AVEC CHAMPS CORRECTS")
    print("=" * 40)
    
    # Test avec les VRAIS champs de votre modèle
    query = "DRAMANE"
    resultats = Membre.objects.filter(
        Q(nom__icontains=query) | 
        Q(prenom__icontains=query) |
        Q(numero_unique__icontains=query) |  # ⬅️ CHAMP CORRECT
        Q(email__icontains=query)
    )
    
    print(f"🔍 Recherche '{query}': {resultats.count()} résultat(s)")
    for r in resultats:
        print(f"   ✅ {r.prenom} {r.nom}")
        print(f"      Numéro unique: {r.numero_unique}")
        print(f"      Email: {r.email}")
        print(f"      Date inscription: {r.date_inscription}")

def verifier_champs_reels():
    print("\n📋 CHAMPS RÉELS POUR LA RECHERCHE")
    print("=" * 40)
    
    # Prendre un membre existant
    membre = Membre.objects.filter(prenom="ASIA", nom="DRAMANE").first()
    if not membre:
        membre = Membre.objects.first()
    
    if membre:
        print("Champs disponibles:")
        print(f"   ✅ nom: {membre.nom}")
        print(f"   ✅ prenom: {membre.prenom}")
        print(f"   ✅ numero_unique: {membre.numero_unique}")
        print(f"   ✅ email: {membre.email}")
        print(f"   ✅ date_inscription: {membre.date_inscription}")

if __name__ == "__main__":
    test_recherche_finale()
    verifier_champs_reels()