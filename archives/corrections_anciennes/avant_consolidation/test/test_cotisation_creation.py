# test_cotisation_creation.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre, Cotisation
from datetime import datetime

print("=== TEST CRÉATION COTISATIONS ===")

# Vérifier les membres
membres_actifs = Membre.objects.filter(statut='actif')
print(f"Membres actifs: {membres_actifs.count()}")

# Créer une cotisation test
if membres_actifs.exists():
    membre = membres_actifs.first()
    try:
        # Vérifier si une cotisation existe déjà pour décembre 2024
        cotisation_existante = Cotisation.objects.filter(
            membre=membre,
            periode='2024-12'
        ).exists()
        
        if not cotisation_existante:
            cotisation = Cotisation.objects.create(
                membre=membre,
                periode='2024-12',
                montant=10000.00,
                statut='en_attente',
                date_emission=datetime.now().date()
            )
            print(f"✓ Cotisation test créée :")
            print(f"  - Membre: {cotisation.membre.nom} {cotisation.membre.prenom}")
            print(f"  - Période: {cotisation.periode}")
            print(f"  - Montant: {cotisation.montant} FCFA")
            print(f"  - Statut: {cotisation.statut}")
        else:
            print("⚠ Cotisation pour décembre 2024 existe déjà")
    except Exception as e:
        print(f"✗ Erreur création cotisation : {e}")
        import traceback
        traceback.print_exc()
else:
    print("✗ Aucun membre actif trouvé")

print(f"\nTotal cotisations : {Cotisation.objects.count()}")