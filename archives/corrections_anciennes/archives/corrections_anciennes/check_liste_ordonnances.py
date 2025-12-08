#!/usr/bin/env python3
"""
Vérification finale de liste_ordonnances.html
"""

from pathlib import Path

def check_liste_ordonnances():
    template_path = Path("/Users/koffitanohsoualiho/Documents/projet/templates/pharmacien/liste_ordonnances.html")
    
    with open(template_path, 'r') as f:
        content = f.read()
    
    print("🔍 VÉRIFICATION FINALE liste_ordonnances.html")
    print("=" * 50)
    
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
        print("❌ PROBLEMES DANS liste_ordonnances.html:")
        for line_num, line_content in issues:
            print(f"   Ligne {line_num}: {line_content}")
    else:
        print("✅ liste_ordonnances.html est PROPRE")
        
    # Vérifier spécifiquement la ligne 62 mentionnée précédemment
    print(f"\n📋 Ligne 62 actuelle:")
    if len(lines) >= 62:
        print(f"   {lines[61]}")
    else:
        print("   La ligne 62 n'existe pas (le template a peut-être changé)")

if __name__ == "__main__":
    check_liste_ordonnances()