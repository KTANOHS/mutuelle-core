# verify_cotisations.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre, Cotisation

print("=== VÉRIFICATION DES DONNÉES ===")

# Membres
membres = Membre.objects.filter(statut='actif')
print(f"Membres actifs: {membres.count()}")
for m in membres:
    print(f"  - {m.nom} {m.prenom} ({m.numero_membre})")

# Cotisations
cotisations = Cotisation.objects.all()
print(f"\nTotal cotisations: {cotisations.count()}")

if cotisations.exists():
    print("\nDétail des cotisations:")
    for c in cotisations.order_by('-periode'):
        membre_nom = f"{c.membre.nom} {c.membre.prenom}" if c.membre else "N/A"
        print(f"  - {c.periode}: {membre_nom} - {c.montant} FCFA - {c.statut}")
else:
    print("\nAucune cotisation trouvée.")

# Vérifier pour décembre 2024
cotis_decembre = Cotisation.objects.filter(periode='2024-12')
print(f"\nCotisations pour décembre 2024: {cotis_decembre.count()}")