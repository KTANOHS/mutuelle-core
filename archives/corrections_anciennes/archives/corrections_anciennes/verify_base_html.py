#!/usr/bin/env python3
"""
Vérification que base.html ne contient plus d'URLs problématiques
"""

from pathlib import Path

def verify_base_html():
    base_path = Path("/Users/koffitanohsoualiho/Documents/projet/templates/base.html")
    
    print("🔍 VÉRIFICATION DE base.html")
    print("=" * 40)
    
    with open(base_path, 'r') as f:
        content = f.read()
    
    # Vérifier les URLs problématiques
    problematic_patterns = [
        'valider_ordonnance',
        'ordonnance.id',
        'pharmacien:valider_ordonnance'
    ]
    
    issues = []
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        for pattern in problematic_patterns:
            if pattern in line:
                issues.append((i, line.strip()))
    
    if issues:
        print("❌ PROBLEMES DANS base.html:")
        for line_num, line_content in issues:
            print(f"   Ligne {line_num}: {line_content}")
    else:
        print("✅ base.html est PROPRE - Aucune URL problématique")

if __name__ == "__main__":
    verify_base_html()