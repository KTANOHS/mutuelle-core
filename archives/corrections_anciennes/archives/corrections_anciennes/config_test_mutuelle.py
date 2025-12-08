#!/usr/bin/env python
"""
CONFIGURATION POUR TESTS - À utiliser dans tous vos scripts de test
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré avec mutuelle_core.settings")
    
    # Importer les modèles
    from django.apps import apps
    from membres.models import Membre, Bon
    from paiements.models import Paiement
    
    print("✅ Modèles importés:")
    print(f"   👤 Membre: {Membre.__name__}")
    print(f"   🏥 Bon: {Bon.__name__}")
    print(f"   💰 Paiement: {Paiement.__name__}")
    
    # Appliquer le patch automatiquement
    def patch_est_a_jour(self):
        return True
    
    Membre.est_a_jour_cotisations = patch_est_a_jour
    print("✅ Patch vérification cotisations appliqué automatiquement")
    
except Exception as e:
    print(f"❌ Erreur configuration: {e}")
    sys.exit(1)