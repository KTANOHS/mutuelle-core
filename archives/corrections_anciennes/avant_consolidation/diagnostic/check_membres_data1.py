# check_membres_data.py - VERSION CORRIGÉE
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Membre
from django.db.models import Q  # AJOUTER CET IMPORT

print("="*70)
print("🔍 VÉRIFICATION DES DONNÉES MEMBRES")
print("="*70)

# Compter tous les membres
total = Membre.objects.count()
print(f"Total membres dans la base: {total}")

# Afficher les 5 premiers
print("\n📋 5 premiers membres:")
for membre in Membre.objects.all()[:5]:
    print(f"  • {membre.id}: {membre.nom} {membre.prenom} - {membre.statut} - Tél: {membre.telephone}")

# Vérifier les statuts
print("\n📊 Répartition par statut:")
# Éviter les doublons dans l'affichage
statuts_distincts = set(Membre.objects.values_list('statut', flat=True))
for statut in statuts_distincts:
    count = Membre.objects.filter(statut=statut).count()
    print(f"  • {statut}: {count} membres")

# Tester la recherche
print("\n🔍 Test de recherche:")
search_terms = ['a', 'e', 'i', 'o', 'u']  # Lettres communes
for term in search_terms:
    results = Membre.objects.filter(
        Q(nom__icontains=term) | 
        Q(prenom__icontains=term) | 
        Q(telephone__icontains=term) | 
        Q(email__icontains=term)
    ).count()
    print(f"  Recherche '{term}': {results} résultats")

# Tester les filtres de statut
print("\n🔍 Test des filtres de statut:")
print(f"  Statut 'actif': {Membre.objects.filter(statut='actif').count()} membres")
print(f"  Statut 'en_retard': {Membre.objects.filter(statut='en_retard').count()} membres")

print("\n" + "="*70)