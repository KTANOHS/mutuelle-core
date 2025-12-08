#!/usr/bin/env python
"""
Solution COMPLÈTE pour les templates medecin
"""

import os
import sys

def solution_complete():
    print("🔄 SOLUTION COMPLÈTE POUR LES TEMPLATES MÉDECIN")
    print("=" * 60)
    
    templates_dir = "templates/medecin"
    
    # 1. Vérifier que base.html existe
    base_path = os.path.join(templates_dir, "base.html")
    if not os.path.exists(base_path):
        print("❌ base.html n'existe pas - création d'urgence...")
        base_content = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Espace Médecin - Mutuelle{% endblock %}</title>
</head>
<body>
    <h1>🏥 Espace Médecin</h1>
    {% block content %}{% endblock %}
</body>
</html>"""
        with open(base_path, 'w', encoding='utf-8') as f:
            f.write(base_content)
        print("✅ base.html créé")
    
    # 2. Créer le lien symbolique base_medecin.html → base.html
    base_medecin_path = os.path.join(templates_dir, "base_medecin.html")
    if not os.path.exists(base_medecin_path):
        print("🔗 Création lien symbolique base_medecin.html → base.html")
        try:
            os.symlink('base.html', base_medecin_path)
            print("✅ Lien symbolique créé")
        except:
            print("❌ Impossible de créer le lien symbolique")
    
    # 3. Lister tous les templates problématiques
    print("\n📋 TEMPLATES À CORRIGER:")
    templates_problematiques = []
    
    for filename in os.listdir(templates_dir):
        if filename.endswith('.html') and filename != 'base.html':
            filepath = os.path.join(templates_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'base_medecin.html' in content:
                templates_problematiques.append(filename)
                print(f"   ⚠️  {filename} utilise base_medecin.html")
    
    # 4. Corriger les templates
    print(f"\n🔧 CORRECTION DE {len(templates_problematiques)} TEMPLATES:")
    for filename in templates_problematiques:
        filepath = os.path.join(templates_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        nouveau_content = content.replace('base_medecin.html', 'base.html')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(nouveau_content)
        print(f"   ✅ {filename} corrigé")
    
    print(f"\n🎉 {len(templates_problematiques)} templates corrigés!")
    print("\n📝 VÉRIFICATION FINALE:")
    
    # Vérifier l'état final
    for filename in ['dashboard.html', 'liste_ordonnances.html', 'creer_ordonnance.html']:
        filepath = os.path.join(templates_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
            print(f"   {filename}: {first_line}")

if __name__ == "__main__":
    solution_complete()
    
    print("\n🚀 MAINTENANT TESTEZ:")
    print("python scripts/test_final_medecin.py")