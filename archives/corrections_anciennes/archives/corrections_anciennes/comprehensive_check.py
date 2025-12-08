#!/usr/bin/env python3
"""
Correction définitive de la faute de frappe dans les extends
"""

from pathlib import Path

def fix_final_typo():
    templates_dir = Path("/Users/koffitanohsoualiho/Documents/projet/templates/pharmacien")
    
    templates_to_fix = [
        "liste_ordonnance.html",
        "historique_validation.html"
    ]
    
    for template_name in templates_to_fix:
        template_path = templates_dir / template_name
        if template_path.exists():
            with open(template_path, 'r') as f:
                content = f.read()
            
            # Corriger la faute de frappe DEFINITIVE
            new_content = content.replace(
                "{% extends 'pharmacien/base_phoncien.html' %}",
                "{% extends 'pharmacien/base_pharmacien.html' %}"
            )
            
            with open(template_path, 'w') as f:
                f.write(new_content)
            
            print(f"✅ Faute de frappe corrigée dans: {template_name}")

if __name__ == "__main__":
    fix_final_typo()