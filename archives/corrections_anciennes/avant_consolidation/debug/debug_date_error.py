# debug_date_error.py
import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("=== DIAGNOSTIC ERREUR DATE ===")

# 1. Vérifier le format attendu par le modèle Cotisation
from assureur.models import Cotisation
from datetime import datetime

# Test de création d'une cotisation avec différentes dates
test_data = [
    ('2025-12', 'Format YYYY-MM'),
    ('01/12/2025', 'Format dd/mm/yyyy'),
    ('12/2025', 'Format mm/yyyy'),
]

for periode, description in test_data:
    print(f"\nTest avec: {periode} ({description})")
    try:
        # Essayer de créer une cotisation test
        from assureur.models import Membre
        membre = Membre.objects.first()
        
        if membre:
            cotisation = Cotisation(
                membre=membre,
                periode=periode,
                montant=10000.00,
                statut='en_attente',
                date_emission=datetime.now().date(),
                date_echeance=datetime.now().date(),
                type_cotisation='mensuelle',
                reference='TEST-REF'
            )
            # Essayer de valider le modèle
            cotisation.full_clean()
            print(f"  ✅ Validation réussie")
        else:
            print("  ⚠ Aucun membre trouvé pour le test")
    except Exception as e:
        print(f"  ❌ Erreur: {e}")

# 2. Vérifier s'il y a des signaux ou des méthodes save() qui causent des problèmes
print("\n=== VÉRIFICATION DU MODÈLE COTISATION ===")
try:
    # Vérifier la méthode save() du modèle
    import inspect
    if hasattr(Cotisation, 'save'):
        source = inspect.getsource(Cotisation.save)
        print("Méthode save() trouvée:")
        print(source[:500])
    else:
        print("Pas de méthode save() personnalisée")
except Exception as e:
    print(f"Erreur lors de l'inspection: {e}")