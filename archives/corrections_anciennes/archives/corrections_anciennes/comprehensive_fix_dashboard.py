#!/usr/bin/env python3
"""
Correction complète de dashboard.html - Version corrigée
"""

import re
from pathlib import Path

def comprehensive_fix_dashboard():
    template_path = Path("/Users/koffitanohsoualiho/Documents/projet/templates/pharmacien/dashboard.html")
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 CORRECTION COMPLÈTE DE DASHBOARD.HTML")
    print("=" * 50)
    
    # Vérifier si le template a déjà été corrigé
    if "\\'" not in content and '\\"' not in content:
        print("✅ dashboard.html est déjà corrigé")
        return True
    
    # CORRECTION : Supprimer tous les backslashes des URLs Django
    corrections = [
        # Backslashes simples dans les guillemets simples
        (r"\\'", "'"),
        # Backslashes dans les guillemets doubles  
        (r'\\"', '"'),
    ]
    
    changes_made = False
    for pattern, replacement in corrections:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            changes_made = True
            print(f"✅ Backslashes supprimés (pattern: {pattern})")
    
    if changes_made:
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("💾 dashboard.html corrigé avec succès")
    else:
        print("ℹ️  Aucune correction nécessaire")
    
    return changes_made

if __name__ == "__main__":
    comprehensive_fix_dashboard()