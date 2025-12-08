import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from django.db.models import Q

def tester_recherche_dramane():
    print("🔍 TEST RECHERCHE 'DRAMANE'")
    print("=" * 35)
    
    # Test exactement comme dans votre vue
    query = "DRAMANE"
    resultats = Membre.objects.filter(
        Q(nom__icontains=query) | 
        Q(prenom__icontains=query) |
        Q(numero_membre__icontains=query) |
        Q(email__icontains=query)
    )
    
    print(f"🔎 Recherche '{query}': {resultats.count()} résultat(s)")
    for r in resultats:
        print(f"   ✅ {r.prenom} {r.nom} (ID: {r.id})")
        print(f"      Email: {r.email}")
        print(f"      Numéro membre: {getattr(r, 'numero_membre', 'Non défini')}")

def tester_champs_membre():
    print("\n📋 CHAMPS DU MODÈLE MEMBRE")
    print("=" * 35)
    
    # Vérifier les champs disponibles
    membre = Membre.objects.first()
    if membre:
        print("Champs disponibles:")
        for field in membre._meta.fields:
            print(f"  - {field.name}")
        
        # Vérifier les valeurs spécifiques
        print(f"\nValeurs pour ASIA DRAMANE:")
        dramane = Membre.objects.get(prenom="ASIA", nom="DRAMANE")
        print(f"  Prénom: {dramane.prenom}")
        print(f"  Nom: {dramane.nom}")
        print(f"  Email: {dramane.email}")
        print(f"  Numéro membre: {getattr(dramane, 'numero_membre', 'NON DÉFINI')}")
        print(f"  Statut: {dramane.statut}")

if __name__ == "__main__":
    tester_recherche_dramane()
    tester_champs_membre()