
#!/usr/bin/env python
import os
import sys

# Vérifier la vue assureur
views_path = os.path.join(os.getcwd(), 'assureur', 'views.py')

if os.path.exists(views_path):
    print(f"🔍 Vérification de: {views_path}")
    with open(views_path, 'r') as f:
        content = f.read()
    
    # Chercher des problèmes
    problems = []
    
    # 1. Vérifier si la vue utilise @staff_member_required
    if '@staff_member_required' in content:
        problems.append("La vue utilise @staff_member_required (problème!)")
    
    # 2. Vérifier si elle utilise @login_required ou @assureur_required
    if '@login_required' not in content and '@assureur_required' not in content:
        problems.append("La vue n'a pas de décorateur de permission")
    
    # 3. Vérifier le nom de la fonction de vue
    if 'def dashboard' in content or 'def tableau_de_bord' in content:
        print("✅ Vue tableau de bord trouvée")
    
    if problems:
        print("❌ Problèmes trouvés:")
        for problem in problems:
            print(f"   - {problem}")
    else:
        print("✅ Aucun problème évident trouvé")
    
    # Afficher les premières lignes de la vue
    print("\n📄 Extrait de la vue assureur:")
    print("-" * 30)
    lines = content.split('\n')[:20]
    for i, line in enumerate(lines):
        print(f"{i+1:3}: {line}")
    
else:
    print(f"❌ Fichier non trouvé: {views_path}")


