# verify_existing_data.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Cotisation

print("=== VÉRIFICATION DES DONNÉES EXISTANTES ===")

# Vérifier une cotisation existante (si elle existe)
cotisation_existante = Cotisation.objects.first()
if cotisation_existante:
    print(f"Cotisation existante trouvée:")
    print(f"  Référence: {cotisation_existante.reference}")
    print(f"  Type: {cotisation_existante.type_cotisation}")
    print(f"  Statut: {cotisation_existante.statut}")
    print(f"  Période: {cotisation_existante.periode}")
    print(f"  Montant: {cotisation_existante.montant}")
else:
    print("Aucune cotisation existante")