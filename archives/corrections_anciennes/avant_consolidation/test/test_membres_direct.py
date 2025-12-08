# test_membres_direct.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Membre
from django.db.models import Q

print("="*70)
print("🔍 TEST DIRECT DE LA RECHERCHE DE MEMBRES")
print("="*70)

# Test 1: Tous les membres
print("\n1. Tous les membres:")
membres = Membre.objects.all()
print(f"   Total: {membres.count()}")
for m in membres[:3]:  # Afficher 3 premiers
    print(f"   - {m.nom} {m.prenom} ({m.statut})")

# Test 2: Recherche par nom
print("\n2. Recherche 'Bernard':")
results = Membre.objects.filter(
    Q(nom__icontains='Bernard') | 
    Q(prenom__icontains='Bernard')
)
print(f"   Résultats: {results.count()}")
for m in results:
    print(f"   - {m.nom} {m.prenom}")

# Test 3: Filtre par statut
print("\n3. Membres avec statut 'actif':")
actifs = Membre.objects.filter(statut='actif')
print(f"   Total actifs: {actifs.count()}")
for m in actifs[:3]:
    print(f"   - {m.nom} {m.prenom}")

# Test 4: Combinaison recherche + filtre
print("\n4. Recherche 'Jean' avec statut 'en_retard':")
results = Membre.objects.filter(
    Q(nom__icontains='Jean') | Q(prenom__icontains='Jean'),
    statut='en_retard'
)
print(f"   Résultats: {results.count()}")
for m in results:
    print(f"   - {m.nom} {m.prenom} ({m.statut})")

print("\n" + "="*70)