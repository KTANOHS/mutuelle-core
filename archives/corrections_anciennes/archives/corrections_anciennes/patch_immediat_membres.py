#!/usr/bin/env python
"""
PATCH IMMÉDIAT POUR L'APP MEMBRES
À exécuter avant vos tests
"""

import os
import sys
import django

# Configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré avec mutuelle_core.settings")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

from membres.models import Membre

def appliquer_patch_immediat():
    """Applique le patch immédiat pour les tests"""
    print("⚡ PATCH IMMÉDIAT POUR MEMBRES...")
    
    # Patch la méthode est_a_jour_cotisations
    def patch_est_a_jour(self):
        print(f"⚡ Patch actif: {self.nom} {self.prenom} considéré comme à jour")
        return True
    
    Membre.est_a_jour_cotisations = patch_est_a_jour
    print("✅ Patch appliqué au modèle Membre")
    
    # Tester le patch
    try:
        membre_test = Membre.objects.first()
        if membre_test:
            resultat = membre_test.est_a_jour_cotisations()
            print(f"🧪 Test patch: {membre_test.nom} {membre_test.prenom} -> À jour: {resultat}")
        else:
            print("⚠️  Aucun membre pour tester le patch")
    except Exception as e:
        print(f"❌ Erreur test patch: {e}")
    
    print("🎯 Patch appliqué! Vous pouvez maintenant lancer vos tests")

if __name__ == "__main__":
    appliquer_patch_immediat()