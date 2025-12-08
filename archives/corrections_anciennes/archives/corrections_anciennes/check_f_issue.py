#!/usr/bin/env python
"""
Script rapide pour vérifier le problème forms.F
"""

import os
import sys
from pathlib import Path

# Trouver le fichier forms.py
project_root = Path(__file__).parent
forms_file = project_root / 'assureur' / 'forms.py'

if not forms_file.exists():
    print(f"❌ Fichier non trouvé: {forms_file}")
    sys.exit(1)

print(f"🔍 Analyse de: {forms_file}")

with open(forms_file, 'r') as f:
    lines = f.readlines()

# Chercher forms.F
issues = []
for i, line in enumerate(lines, 1):
    if 'forms.F' in line:
        issues.append((i, line.strip()))

if issues:
    print("❌ PROBLEMES TROUVÉS:")
    for line_num, line_content in issues:
        print(f"   Ligne {line_num}: {line_content}")
        print(f"   → Corriger par: {line_content.replace('forms.F', 'models.F')}")
else:
    print("✅ Aucun problème forms.F détecté")

# Vérifier les imports
print("\n📥 IMPORTS:")
for i, line in enumerate(lines, 1):
    if 'import' in line and ('forms' in line or 'models' in line or 'F' in line):
        print(f"   Ligne {i}: {line.strip()}")