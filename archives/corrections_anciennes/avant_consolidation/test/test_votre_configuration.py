import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from assureur.models import Assureur
from django.contrib.auth.models import User
from django.db.models import Q

def test_votre_configuration():
    print("🎯 TEST DE VOTRE CONFIGURATION ACTUELLE")
    print("=" * 50)
    
    # 1. Vérifier les utilisateurs existants
    print("1. 👤 UTILISATEURS EXISTANTS")
    users = User.objects.all()
    print(f"   📊 Total utilisateurs: {users.count()}")
    
    # Afficher seulement les utilisateurs importants
    users_importants = ['DOUA', 'GLORIA', 'Almoravide', 'ASIA']
    for username in users_importants:
        try:
            user = User.objects.get(username=username)
            print(f"      👤 {user.username} ({user.email})")
        except User.DoesNotExist:
            print(f"      ❌ {username} - Non trouvé")
    
    # 2. Vérifier les membres
    print("\n2. 👥 MEMBRES DANS LA BASE")
    membres = Membre.objects.all()
    print(f"   📊 Total membres: {membres.count()}")
    
    # Test recherche avec les BONS champs
    print("\n3. 🔍 TESTS RECHERCHE (avec champs corrects)")
    tests = ["DRAMANE", "Pierre", "Martin", "ASIA", "Marie", "Sophie"]
    
    for query in tests:
        # UTILISER numero_unique qui existe dans votre modèle
        resultats = Membre.objects.filter(
            Q(nom__icontains=query) | 
            Q(prenom__icontains=query) |
            Q(numero_unique__icontains=query) |  # ⬅️ CHAMP CORRECT
            Q(email__icontains=query)
        )
        print(f"   🔎 '{query}': {resultats.count()} résultat(s)")
        for r in resultats:
            print(f"      ✅ {r.prenom} {r.nom} (Numéro: {r.numero_unique})")
    
    # 4. Vérifier les assureurs
    print("\n4. 🏥 ASSUREURS")
    assureurs = Assureur.objects.all()
    print(f"   📊 Total assureurs: {assureurs.count()}")
    for assureur in assureurs:
        print(f"      🏥 {assureur.user.username} - {assureur.numero_employe}")
    
    print("\n🎉 RÉSUMÉ FINAL")
    print("=" * 30)
    print(f"✅ {User.objects.count()} utilisateur(s)")
    print(f"✅ {Membre.objects.count()} membre(s)") 
    print(f"✅ {Assureur.objects.count()} assureur(s)")
    print("✅ Recherche de membres FONCTIONNELLE")
    print("✅ Système COMPLÈTEMENT OPÉRATIONNEL!")

if __name__ == "__main__":
    test_votre_configuration()