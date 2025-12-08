#!/usr/bin/env python
"""
SCRIPT POUR ADAPTER VOS TESTS EXISTANTS
"""

# Contenu à ajouter en haut de votre test_creation_bons.py :

config_code = """
import os
import sys
import django

# Configuration Django pour mutuelle_core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré avec mutuelle_core.settings")
except Exception as e:
    print(f"❌ Erreur configuration: {e}")
    sys.exit(1)

# Importer les modèles réels
from membres.models import Membre, Bon
from paiements.models import Paiement

# Appliquer le patch pour les tests
def patch_est_a_jour(self):
    return True

Membre.est_a_jour_cotisations = patch_est_a_jour
print("✅ Patch vérification cotisations appliqué")

# Votre code de test existant ici...
"""

print("📝 AJOUTEZ CE CODE EN HAUT DE VOS FICHIERS DE TEST:")
print(config_code)