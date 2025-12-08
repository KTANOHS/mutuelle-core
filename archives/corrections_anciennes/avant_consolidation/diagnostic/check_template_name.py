#!/usr/bin/env python3
import os
import sys

views_path = "pharmacien/views.py"

with open(views_path, 'r') as f:
    content = f.read()

# Chercher le template utilisé dans la vue historique_validation
import re

# Chercher le render avec le template
pattern = r'def historique_validation\(request\).*?render\(request,\s*[\'"](.*?)[\'"]'
match = re.search(pattern, content, re.DOTALL)

if match:
    template_name = match.group(1)
    print(f"Template utilisé dans la vue: '{template_name}'")
else:
    print("Template non trouvé dans la vue")

# Vérifier aussi le template minimal
pattern2 = r'render\(request,\s*[\'"]pharmacien/historique'
if re.search(pattern2, content):
    print("La vue utilise 'pharmacien/historique'")
