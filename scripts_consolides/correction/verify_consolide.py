"""
FICHIER CONSOLIDÉ: verify
Catégorie: correction
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
# ORIGINE 1: verify_fix.py (2025-12-01)
# ============================================================

#!/usr/bin/env python3
import os
import sys
import django

project_path = "/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30"
sys.path.insert(0, project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("=== VÉRIFICATION COMPLÈTE DE LA CORRECTION ===")

# 1. Vérifier la vue corrigée
print("\n1. VÉRIFICATION DE LA VUE historique_validation:")
try:
    from pharmacien.views import historique_validation
    print("   ✓ Vue importée avec succès")

    # Vérifier les décorateurs
    import inspect
    source = inspect.getsource(historique_validation)
    if '@login_required' in source and '@pharmacien_required' in source and '@gerer_erreurs' in source:
        print("   ✓ Tous les décorateurs présents")
    else:
        print("   ✗ Décorateurs manquants")

except Exception as e:
    print(f"   ✗ Erreur: {e}")

# 2. Vérifier le modèle OrdonnancePharmacien
print("\n2. VÉRIFICATION DU MODÈLE OrdonnancePharmacien:")
try:
    from pharmacien.models import OrdonnancePharmacien
    print(f"   ✓ Modèle importé")
    print(f"   - Nombre d'objets: {OrdonnancePharmacien.objects.count()}")

    # Afficher les champs importants
    date_fields = [f.name for f in OrdonnancePharmacien._meta.fields if 'date' in f.name]
    print(f"   - Champs de date: {date_fields}")

    # Vérifier la relation avec l'utilisateur
    for field in OrdonnancePharmacien._meta.get_fields():
        if field.name == 'pharmacien':
            print(f"   - Relation pharmacien: {field.related_model}")
            break

except Exception as e:
    print(f"   ✗ Erreur: {e}")

... (tronqué)

# ============================================================
# ORIGINE 2: verify_fix_communication_urls.sh (2025-12-01)
# ============================================================

#!/bin/bash

echo "🔍 VÉRIFICATION DES URLS COMMUNICATION"
echo "======================================"

# 1. Vérifier la vue communication_home dans views.py
echo ""
echo "1. Vérification de la vue communication_home:"
if grep -n "def communication_home" communication/views.py; then
    echo "✅ Vue trouvée dans views.py"
else
    echo "❌ Vue NON TROUVÉE dans views.py"
    echo "   Exécutez d'abord le script de correction des vues !"
    exit 1
fi

# 2. Vérifier l'URL racine
echo ""
echo "2. Vérification de l'URL racine (/communication/):"
ROOT_URL=$(grep -n "path(''," communication/urls.py | head -1)
if echo "$ROOT_URL" | grep -q "communication_home"; then
    echo "✅ URL racine correctement configurée (pointe vers communication_home)"
    echo "   Ligne: $ROOT_URL"
else
    echo "❌ URL racine INCORRECTE !"
    echo "   Actuel: $ROOT_URL"
    echo "   Doit pointer vers: views.communication_home"
fi

# 3. Lister toutes les URLs
echo ""
echo "3. Liste de toutes les URLs configurées:"
python -c "
import sys
sys.path.insert(0, '.')
try:
    from communication import urls
    print('📋 URLs du module communication:')
    print('=' * 50)

    for pattern in urls.urlpatterns:
        if hasattr(pattern, 'name') and pattern.name:
            name = pattern.name
        else:
            name = 'SANS_NOM'

        print(f'• {pattern.pattern:<40} → {name}')

    print('=' * 50)
    print(f'Total: {len(urls.urlpatterns)} URLs configurées')
... (tronqué)

# ============================================================
# ORIGINE 3: verify_fixes1.py (2025-11-19)
# ============================================================

#!/usr/bin/env python
"""
Script de vérification après correction des timezones
"""

import re
from pathlib import Path

def check_file_after_fix(file_path):
    """Vérifie un fichier après correction"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        issues = []

        # Vérifier la présence de l'import timezone
        if 'from django.utils import timezone' not in content:
            issues.append("❌ Import timezone manquant")

        # Vérifier les patterns problématiques restants
        problematic_patterns = [
            r'datetime\.datetime\.now\(\)',
            r'(?<!\.)datetime\.now\(\)',
        ]

        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern in problematic_patterns:
                if re.search(pattern, line) and not line.strip().startswith('#'):
                    issues.append(f"❌ Ligne {i}: {pattern} trouvé")

        # Vérifier l'utilisation correcte de timezone
        timezone_uses = len(re.findall(r'timezone\.now\(\)', content))

        return {
            'file': file_path.name,
            'path': str(file_path),
            'issues': issues,
            'timezone_uses': timezone_uses,
            'status': '✅ OK' if not issues else '❌ PROBLEMES'
        }

    except Exception as e:
        return {
            'file': file_path.name,
            'path': str(file_path),
            'issues': [f"❌ Erreur de lecture: {e}"],
            'timezone_uses': 0,
            'status': '❌ ERREUR'
... (tronqué)

