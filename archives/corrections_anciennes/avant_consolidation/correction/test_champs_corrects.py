import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from django.db.models import Q

def test_avec_champs_corrects():
    print("🎯 TEST AVEC CHAMPS CORRECTS")
    print("=" * 35)
    
    # Test avec le VRAI champ numero_membre
    query = "DRAMANE"
    resultats = Membre.objects.filter(
        Q(nom__icontains=query) | 
        Q(prenom__icontains=query) |
        Q(numero_membre__icontains=query) |  # ⬅️ CHAMP CORRECT
        Q(email__icontains=query)
    )
    
    print(f"🔍 Recherche '{query}': {resultats.count()} résultat(s)")
    for r in resultats:
        print(f"   ✅ {r.prenom} {r.nom}")
        print(f"      Numéro membre: {r.numero_membre}")
        print(f"      Email: {r.email}")

def lister_champs_membre():
    print("\n📋 CHAMPS RÉELS DU MODÈLE MEMBRE")
    print("=" * 35)
    
    membre = Membre.objects.first()
    if membre:
        print("Champs disponibles pour la recherche:")
        champs_recherche = ['nom', 'prenom', 'numero_membre', 'email']
        for champ in champs_recherche:
            if hasattr(membre, champ):
                valeur = getattr(membre, champ)
                print(f"   ✅ {champ}: {valeur}")
            else:
                print(f"   ❌ {champ}: N'existe pas")

if __name__ == "__main__":
    test_avec_champs_corrects()
    lister_champs_membre()