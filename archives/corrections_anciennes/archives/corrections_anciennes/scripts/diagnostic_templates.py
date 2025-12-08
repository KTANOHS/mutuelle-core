#!/usr/bin/env python
"""
Diagnostic des problèmes de templates medecin
"""

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostiquer_templates():
    """Diagnostique tous les problèmes de templates medecin"""
    print("🔍 DIAGNOSTIC COMPLET DES TEMPLATES MÉDECIN")
    print("=" * 60)
    
    templates_dir = "templates/medecin"
    
    # 1. Vérifier l'existence des templates
    print("1. VÉRIFICATION DES FICHIERS:")
    print("-" * 30)
    
    templates_existants = []
    for file in os.listdir(templates_dir):
        if file.endswith('.html'):
            templates_existants.append(file)
            print(f"✅ {file}")
    
    # 2. Vérifier les références à base.html
    print("\n2. RECHERCHE DES RÉFÉRENCES À base.html:")
    print("-" * 40)
    
    for template_file in templates_existants:
        filepath = os.path.join(templates_dir, template_file)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        if '{% extends' in content:
            if 'medecin/base.html' in content:
                print(f"⚠️  {template_file} → extends 'medecin/base.html'")
            elif 'base_medecin.html' in content:
                print(f"✅ {template_file} → extends 'base_medecin.html'")
            else:
                # Trouver quelle base est utilisée
                lines = content.split('\n')
                for line in lines:
                    if '{% extends' in line:
                        print(f"ℹ️  {template_file} → {line.strip()}")
    
    # 3. Solution recommandée
    print("\n3. SOLUTION RECOMMANDÉE:")
    print("-" * 25)
    print("Exécutez ces commandes:")
    print("cd templates/medecin")
    print("mv base_medecin.html base.html")
    print("\nOU créez base.html avec ce contenu minimal:")
    
    base_content = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Médecin{% endblock %}</title>
</head>
<body>
    <h1>Espace Médecin</h1>
    {% block content %}{% endblock %}
</body>
</html>"""
    
    print(base_content)

if __name__ == "__main__":
    diagnostiquer_templates()