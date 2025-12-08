# check_system_corrige.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Cotisation, Membre
from django.db.models import Count, Sum

print("="*60)
print("ÉTAT DU SYSTÈME DE COTISATIONS")
print("="*60)

# Compter les membres
membres = Membre.objects.all()
membres_actifs = Membre.objects.filter(statut='actif')
print(f"📊 MEMBRES:")
print(f"   Total: {membres.count()}")
print(f"   Actifs: {membres_actifs.count()}")
print(f"   Inactifs: {membres.filter(statut='inactif').count()}")

# Afficher les membres actifs
print(f"\n👥 LISTE DES MEMBRES ACTIFS:")
for m in membres_actifs:
    # Utiliser le champ 'nom_complet' s'il existe, sinon combiner nom et prénom
    if hasattr(m, 'nom_complet'):
        nom_affichage = m.nom_complet
    else:
        nom_affichage = f"{getattr(m, 'nom', '')} {getattr(m, 'prenom', '')}".strip()
    
    # Utiliser le bon attribut pour le type (type_membre ou type_contrat)
    if hasattr(m, 'get_type_membre_display'):
        type_membre = m.get_type_membre_display()
    elif hasattr(m, 'get_type_contrat_display'):
        type_membre = m.get_type_contrat_display()
    else:
        type_membre = "Non spécifié"
    
    print(f"   - {m.numero_membre}: {nom_affichage} ({type_membre})")

# Compter les cotisations
cotisations = Cotisation.objects.all()
print(f"\n💰 COTISATIONS:")
print(f"   Total: {cotisations.count()}")

# Obtenir les périodes distinctes avec aggregate
periodes_distinctes = cotisations.values('periode').annotate(
    total_count=Count('id'),
    total_amount=Sum('montant')
).order_by('periode')

print(f"   Périodes distinctes: {len(periodes_distinctes)}")

# Détail par période
print(f"\n📅 DÉTAIL PAR PÉRIODE:")
for periode in periodes_distinctes:
    periode_val = periode['periode']
    nb = periode['total_count']
    montant_total = periode['total_amount'] or 0
    print(f"   {periode_val}: {nb} cotisations, {montant_total:,.0f} FCFA")

# Statistiques par statut
print(f"\n📊 STATUT DES COTISATIONS:")
if hasattr(Cotisation, 'STATUT_CHOICES'):
    for statut_code, statut_label in Cotisation.STATUT_CHOICES:
        nb = cotisations.filter(statut=statut_code).count()
        print(f"   {statut_label}: {nb}")
else:
    print("   Aucun statut défini")

print("\n" + "="*60)
print("VÉRIFICATION TERMINÉE")
print("="*60)