import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from django.db.models import Q

def test_recherche_avec_champs_corrects():
    print("🎯 TEST RECHERCHE AVEC CHAMPS CORRECTS")
    print("=" * 45)
    
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

def test_multiple_recherches():
    print("\n🔍 TESTS MULTIPLES")
    print("=" * 30)
    
    tests = ["DRAMANE", "Pierre", "Martin", "ASIA", "Marie"]
    
    for query in tests:
        resultats = Membre.objects.filter(
            Q(nom__icontains=query) | 
            Q(prenom__icontains=query) |
            Q(numero_unique__icontains=query) |
            Q(email__icontains=query)
        )
        print(f"🔎 '{query}': {resultats.count()} résultat(s)")
        for r in resultats:
            print(f"   👤 {r.prenom} {r.nom}")

def verifier_membre_dramane():
    print("\n📋 VÉRIFICATION ASIA DRAMANE")
    print("=" * 35)
    
    # Vérifier spécifiquement ASIA DRAMANE
    dramane = Membre.objects.filter(nom="DRAMANE", prenom="ASIA").first()
    if dramane:
        print("✅ ASIA DRAMANE trouvée dans la base!")
        print(f"   ID: {dramane.id}")
        print(f"   Nom: {dramane.nom}")
        print(f"   Prénom: {dramane.prenom}")
        print(f"   Numéro unique: {dramane.numero_unique}")
        print(f"   Email: {dramane.email}")
        print(f"   Statut: {dramane.statut}")
    else:
        print("❌ ASIA DRAMANE non trouvée")
        # Lister tous les membres pour debug
        print("\n👥 Tous les membres:")
        for m in Membre.objects.all():
            print(f"   - {m.prenom} {m.nom}")

if __name__ == "__main__":
    test_recherche_avec_champs_corrects()
    test_multiple_recherches()
    verifier_membre_dramane()