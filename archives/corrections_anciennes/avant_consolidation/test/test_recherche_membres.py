# test_recherche_membres.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre
from django.db.models import Q

print("="*70)
print("🔍 TEST DE LA RECHERCHE SUR LE MODÈLE ASSUREUR")
print("="*70)

# Vérifier combien de membres existent
total = Membre.objects.count()
print(f"Total membres dans assureur.models.Membre: {total}")

# Tester la recherche "ASIA" comme dans l'URL
search_term = "ASIA"
print(f"\n🔍 Recherche pour le terme: '{search_term}'")

results = Membre.objects.filter(
    Q(nom__icontains=search_term) |
    Q(prenom__icontains=search_term) |
    Q(numero_membre__icontains=search_term) |
    Q(email__icontains=search_term) |
    Q(telephone__icontains=search_term)
)

print(f"Nombre de résultats: {results.count()}")

if results.count() > 0:
    print("\n📋 Résultats trouvés:")
    for membre in results:
        print(f"  • {membre.id}: {membre.nom} {membre.prenom}")
        print(f"    - Email: {membre.email}")
        print(f"    - Téléphone: {membre.telephone}")
        print(f"    - Numéro membre: {membre.numero_membre}")
        print(f"    - Statut: {membre.statut}")
else:
    print("\n❌ Aucun résultat trouvé")
    print("\n📋 Tous les membres (pour debug):")
    for membre in Membre.objects.all()[:5]:
        print(f"  • {membre.id}: {membre.nom} {membre.prenom}")

print("\n" + "="*70)