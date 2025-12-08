#!/usr/bin/env python3
"""
Analyse détaillée des templates pour trouver les URLs exactes problématiques
"""

import re
from pathlib import Path

def deep_analysis():
    templates_dir = Path("/Users/koffitanohsoualiho/Documents/projet/templates")
    
    print("🔍 ANALYSE PROFONDE DES TEMPLATES PHARMACIEN")
    print("=" * 60)
    
    problematic_templates = [
        'pharmacien/dashboard.html',
        'pharmacien/liste_ordonnances.html',
        'pharmacien/detail_ordonnance.html'
    ]
    
    for template_name in problematic_templates:
        template_path = templates_dir / template_name
        
        if not template_path.exists():
            continue
            
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n📄 {template_name}:")
        print("-" * 40)
        
        # Trouver toutes les lignes avec valider_ordonnance
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'valider_ordonnance' in line and 'ordonnance.id' in line:
                print(f"   Ligne {i}: {line.strip()}")
            
            # Aussi chercher les URLs pharmacien:valider_ordonnance
            if 'pharmacien:valider_ordonnance' in line and 'ordonnance.id' in line:
                print(f"   Ligne {i}: {line.strip()}")

if __name__ == "__main__":
    deep_analysis()