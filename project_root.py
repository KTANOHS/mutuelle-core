#!/usr/bin/env python
"""
Vérification finale du fichier forms.py corrigé
"""

from pathlib import Path

forms_file = Path('/Users/koffitanohsoualiho/Documents/projet/assureur/forms.py')

print("🔍 VÉRIFICATION FINALE DU FICHIER FORMS.PY")
print("=" * 50)

with open(forms_file, 'r') as f:
    lines = f.readlines()

# Vérification 1: Import de F
print("1. Vérification des imports:")
f_imported = False
for i, line in enumerate(lines, 1):
    if 'from django.db.models import F' in line:
        print(f"   ✅ Ligne {i}: {line.strip()}")
        f_imported = True
    elif 'import F' in line and 'django' in line:
        print(f"   ✅ Ligne {i}: {line.strip()}")
        f_imported = True

if not f_imported:
    print("   ❌ Import de F manquant")

# Vérification 2: Ligne 245 corrigée
print("\n2. Vérification de la ligne 245:")
if len(lines) >= 245:
    line_245 = lines[244].strip()
    print(f"   Ligne 245: {line_245}")
    if "F('montant_facture')" in line_245 and "forms.F" not in line_245:
        print("   ✅ Ligne 245 correctement corrigée")
    else:
        print("   ❌ Ligne 245 toujours problématique")
else:
    print("   ❌ Fichier trop court")

# Vérification 3: Absence de forms.F
print("\n3. Recherche de forms.F résiduels:")
forms_f_found = False
for i, line in enumerate(lines, 1):
    if 'forms.F' in line:
        print(f"   ❌ Ligne {i}: {line.strip()}")
        forms_f_found = True

if not forms_f_found:
    print("   ✅ Aucun forms.F résiduel trouvé")

print("\n🎉 VÉRIFICATION TERMINÉE")