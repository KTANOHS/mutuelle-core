import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from django.db.models import Q

def test_avec_champs_reels():
    print("🎯 TEST AVEC CHAMPS RÉELS")
    print("=" * 35)
    
    # Test avec les VRAIS champs de votre modèle
    query = "DRAMANE"
    resultats = Membre.objects.filter(
        Q(nom__icontains=query) | 
        Q(prenom__icontains=query) |
        Q(numero_membre__icontains=query) |  # ⬅️ CHAMP RÉEL
        Q(email__icontains=query)
    )
    
    print(f"🔍 Recherche '{query}': {resultats.count()} résultat(s)")
    for r in resultats:
        print(f"   ✅ {r.prenom} {r.nom}")
        print(f"      Numéro membre: {r.numero_membre}")
        print(f"      Date adhésion: {r.date_adhesion}")
        print(f"      Email: {r.email}")

def verifier_tri():
    print("\n📋 TEST TRI PAR DATE ADHÉSION")
    print("=" * 35)
    
    # Tester le tri
    membres_tries = Membre.objects.all().order_by('-date_adhesion')[:3]
    print("3 derniers membres (par date adhésion):")
    for m in membres_tries:
        print(f"   👤 {m.prenom} {m.nom} - {m.date_adhesion}")

if __name__ == "__main__":
    test_avec_champs_reels()
    verifier_tri()