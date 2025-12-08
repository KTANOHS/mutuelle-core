#!/usr/bin/env python
"""
VÉRIFICATION RAPIDE ASSUREUR
Vérifications essentielles en 30 secondes
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

def verification_rapide():
    """Vérification rapide des éléments critiques"""
    print("🔍 VÉRIFICATION RAPIDE ASSUREUR")
    print("="*50)
    
    checks = []
    
    # 1. Vérifier l'application dans INSTALLED_APPS
    from django.conf import settings
    if 'assureur' in settings.INSTALLED_APPS:
        checks.append(("✅ Application dans INSTALLED_APPS", True))
    else:
        checks.append(("❌ Application absente de INSTALLED_APPS", False))
    
    # 2. Vérifier les modèles
    try:
        from assureur.models import Membre, Bon, Cotisation
        checks.append(("✅ Modèles principaux importables", True))
    except ImportError as e:
        checks.append((f"❌ Erreur import modèles: {e}", False))
    
    # 3. Vérifier les vues
    try:
        from assureur.views import dashboard_assureur, liste_cotisations
        checks.append(("✅ Vues principales importables", True))
    except ImportError as e:
        checks.append((f"❌ Erreur import vues: {e}", False))
    
    # 4. Vérifier les URLs
    try:
        from assureur.urls import urlpatterns
        checks.append((f"✅ {len(urlpatterns)} patterns d'URL configurés", True))
    except Exception as e:
        checks.append((f"❌ Erreur URLs: {e}", False))
    
    # 5. Vérifier les templates
    templates_dir = BASE_DIR / 'templates' / 'assureur'
    if templates_dir.exists():
        nb_templates = len(list(templates_dir.rglob('*.html')))
        checks.append((f"✅ {nb_templates} templates trouvés", True))
    else:
        checks.append(("❌ Dossier templates/assureur manquant", False))
    
    # Afficher les résultats
    for check, success in checks:
        print(check)
    
    # Résumé
    succes = sum(1 for _, s in checks if s)
    total = len(checks)
    
    print(f"\n📊 Score: {succes}/{total}")
    
    if succes == total:
        print("🎉 Tous les checks passent! L'application est opérationnelle.")
    else:
        print("⚠️  Des problèmes ont été détectés. Utilisez analyse_assureur.py pour plus de détails.")

if __name__ == "__main__":
    verification_rapide()