#!/usr/bin/env python3
import os
import sys

views_path = "pharmacien/views.py"

# Trouver et afficher la fonction historique_validation
with open(views_path, 'r') as f:
    lines = f.readlines()
    
print("=== CONTENU DE historique_validation ===")
in_function = False
function_lines = []

for i, line in enumerate(lines):
    if '@login_required' in line and i+2 < len(lines) and 'historique_validation' in lines[i+2]:
        in_function = True
    if in_function:
        function_lines.append(line)
        if line.strip().startswith('def ') and 'historique_validation' not in line and len(function_lines) > 1:
            break

for line in function_lines:
    print(line.rstrip())

print("\n=== VÉRIFICATION DES IMPORTS ===")
for i, line in enumerate(lines[:50]):
    if 'import' in line:
        print(f"{i+1}: {line.rstrip()}")
