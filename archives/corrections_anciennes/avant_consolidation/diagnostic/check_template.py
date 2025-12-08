#!/usr/bin/env python3
import os

template_path = "templates/pharmacien/historique_validation.html"

if not os.path.exists(template_path):
    print(f"❌ Template non trouvé: {template_path}")
    exit(1)

with open(template_path, 'r') as f:
    content = f.read()

print(f"✓ Template trouvé: {template_path}")
print(f"Taille: {len(content)} caractères, {len(content.split('\\n'))} lignes")

# Vérifications de base
checks = [
    ('{% extends', 'Extends présent'),
    ('{% block content', 'Block content présent'),
    ('{% for', 'Boucle for présente'),
    ('{{', 'Variables Django présentes'),
]

print("\n=== VÉRIFICATIONS DU TEMPLATE ===")
for pattern, description in checks:
    if pattern in content:
        print(f"  ✓ {description}")
    else:
        print(f"  ⚠ {description} - Non trouvé")

# Vérifier les erreurs courantes
print("\n=== RECHERCHE D'ERREURS COURANTES ===")
error_patterns = [
    ('{% endblock %}', 'endblock correct'),
    ('{% endfor %}', 'endfor correct'),
    ('{% endif %}', 'endif correct'),
]

for pattern, description in error_patterns:
    if content.count('{% for') != content.count('{% endfor %}'):
        print("  ⚠ Nombre de 'for' et 'endfor' ne correspond pas")
    if content.count('{% if') != content.count('{% endif %}'):
        print("  ⚠ Nombre de 'if' et 'endif' ne correspond pas")

print("\n=== EXTRACTION DE 10 LIGNES AUTOUR D'UNE ÉVENTUELLE ERREUR ===")
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'erreur' in line.lower() or 'error' in line.lower():
        start = max(0, i-5)
        end = min(len(lines), i+6)
        print(f"Ligne {i+1}:")
        for j in range(start, end):
            prefix = '>>>' if j == i else '   '
            print(f"{prefix} {j+1}: {lines[j]}")
        break
else:
    print("Aucune ligne avec 'erreur' ou 'error' trouvée")
