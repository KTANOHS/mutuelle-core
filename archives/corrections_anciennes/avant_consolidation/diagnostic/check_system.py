# check_system.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Cotisation, Membre

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
    print(f"   - {m.numero_membre}: {m.nom_complet} ({m.get_type_membre_display()})")

# Compter les cotisations
cotisations = Cotisation.objects.all()
print(f"\n💰 COTISATIONS:")
print(f"   Total: {cotisations.count()}")

# Par période
periodes = cotisations.values_list('periode', flat=True).distinct()
print(f"   Périodes: {list(periodes)}")

# Détail par période
print(f"\n📅 DÉTAIL PAR PÉRIODE:")
for periode in periodes:
    nb = cotisations.filter(periode=periode).count()
    montant_total = sum(c.montant for c in cotisations.filter(periode=periode) if c.montant)
    print(f"   {periode}: {nb} cotisations, {montant_total} FCFA")

print("\n" + "="*60)
print("VÉRIFICATION TERMINÉE")
print("="*60)