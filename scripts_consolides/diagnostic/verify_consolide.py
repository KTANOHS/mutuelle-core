"""
FICHIER CONSOLIDÉ: verify
Catégorie: diagnostic
Fusion de 3 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: verify_existing_data.py (2025-12-03)
# ============================================================

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

# ============================================================
# ORIGINE 2: verify_cotisations.py (2025-12-03)
# ============================================================

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

# ============================================================
# ORIGINE 3: verify_function.py (2025-11-27)
# ============================================================

# verify_function.py
import os
import sys

# Lire le fichier views.py pour vérifier si la fonction existe
views_path = "agents/views.py"

try:
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "def verifier_statut_cotisation_simple" in content:
        print("✅ SUCCÈS : La fonction verifier_statut_cotisation_simple EST dans le fichier")

        # Vérifier l'ordre des fonctions
        pos_simple = content.find("def verifier_statut_cotisation_simple")
        pos_simplifiee = content.find("def verifier_cotisation_membre_simplifiee")

        if pos_simple < pos_simplifiee:
            print("✅ ORDRE CORRECT : simple AVANT simplifiee")
        else:
            print("❌ ORDRE INCORRECT : simple APRÈS simplifiee")

    else:
        print("❌ ÉCHEC : La fonction verifier_statut_cotisation_simple N'EST PAS dans le fichier")
        print("💡 Vous devez l'ajouter manuellement")

except FileNotFoundError:
    print(f"❌ Fichier {views_path} non trouvé")
except Exception as e:
    print(f"❌ Erreur: {e}")

