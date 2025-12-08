#!/usr/bin/env python3
"""
Script de vérification après correction des templates assureur
"""

import os
import re
from pathlib import Path

def verify_corrections():
    """Vérifie que toutes les corrections ont été appliquées"""
    print("🔍 VÉRIFICATION POST-CORRECTION")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    issues_found = 0
    
    # URLs qui ne devraient plus exister
    forbidden_urls = ['assureur:rapports']
    
    # Templates problématiques identifiés
    problematic_templates = [
        project_root / "templates/assureur/dashboard.html",
        project_root / "templates/assureur/partials/_sidebar.html"
    ]
    
    for template_path in problematic_templates:
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for url in forbidden_urls:
                if url in content:
                    print(f"❌ URL problématique trouvée: {url} dans {template_path}")
                    issues_found += 1
                else:
                    print(f"✅ URL corrigée: {url} dans {template_path}")
    
    # Vérifier les doublons
    duplicates = {
        'base_assureur.html': [
            project_root / "assureur/templates/assureur/base_assureur.html",
            project_root / "templates/assureur/base_assureur.html"
        ],
        'dashboard.html': [
            project_root / "assureur/templates/assureur/dashboard.html",
            project_root / "templates/assureur/dashboard.html" 
        ]
    }
    
    for template_name, paths in duplicates.items():
        existing = [p for p in paths if p.exists()]
        if len(existing) > 1:
            print(f"⚠️  Doublon toujours présent: {template_name}")
            for path in existing:
                print(f"   - {path}")
            issues_found += 1
    
    # Rapport final
    print("\n" + "=" * 50)python verification_corrections.py
    if issues_found == 0:
        print("🎉 TOUTES LES CORRECTIONS SONT VALIDÉES!")
        print("✅ Aucun problème détecté")
        return True
    else:
        print(f"❌ {issues_found} problème(s) nécessite(nt) encore attention")
        return False

if __name__ == "__main__":
    success = verify_corrections()
    exit(0 if success else 1)