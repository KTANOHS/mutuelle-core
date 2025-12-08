#!/usr/bin/env python3
"""
Vérification détaillée après correction
"""

import re
from pathlib import Path

def detailed_verification():
    """Vérification détaillée des corrections"""
    print("🔍 VÉRIFICATION DÉTAILLÉE POST-CORRECTION")
    print("=" * 60)
    
    project_root = Path(__file__).parent
    issues = []
    
    # Fichiers spécifiques à vérifier
    critical_files = [
        "templates/assureur/dashboard.html",
        "templates/assureur/partials/_sidebar.html", 
        "assureur/templates/assureur/dashboard.html",
        "templates/assureur/base_assureur.html",
        "assureur/templates/assureur/base_assureur.html"
    ]
    
    print("\n📋 VÉRIFICATION DES URLs PROBLÉMATIQUES")
    print("-" * 40)
    
    for file_path in critical_files:
        full_path = project_root / file_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les URLs problématiques
            problematic_patterns = [
                r'assureur:rapports',
                r"{%\s*url\s+['\"]assureur:rapports['\"]\s*%}"
            ]
            
            file_issues = []
            for pattern in problematic_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    file_issues.extend(matches)
            
            if file_issues:
                print(f"❌ {file_path}")
                for issue in set(file_issues):
                    print(f"   → {issue}")
                issues.append((file_path, file_issues))
            else:
                print(f"✅ {file_path}")
        else:
            print(f"⚠️  NON TROUVÉ: {file_path}")
    
    print("\n📋 VÉRIFICATION DES DOUBLONS")
    print("-" * 40)
    
    duplicates = [
        ("assureur/templates/assureur/base_assureur.html", "templates/assureur/base_assureur.html"),
        ("assureur/templates/assureur/dashboard.html", "templates/assureur/dashboard.html")
    ]
    
    for primary, secondary in duplicates:
        primary_path = project_root / primary
        secondary_path = project_root / secondary
        
        primary_exists = primary_path.exists()
        secondary_exists = secondary_path.exists()
        
        if primary_exists and secondary_exists:
            print(f"❌ DOUBLON: {primary} ET {secondary}")
            issues.append(("duplicate", f"{primary} vs {secondary}"))
        elif primary_exists:
            print(f"✅ OK: {primary} (unique)")
        elif secondary_exists:
            print(f"⚠️  UNIQUE: {secondary} (le principal manque)")
        else:
            print(f"❌ MANQUANT: {primary} et {secondary}")
    
    print("\n" + "=" * 60)
    
    if not issues:
        print("🎉 TOUTES LES CORRECTIONS SONT VALIDÉES!")
        print("✅ Aucun problème détecté")
        return True
    else:
        print(f"❌ {len(issues)} PROBLÈME(S) DÉTECTÉ(S)")
        print("\n🚨 ACTIONS REQUISES:")
        
        for issue_type, issue_data in issues:
            if issue_type == "duplicate":
                print(f"• Supprimer le doublon: {issue_data}")
            else:
                print(f"• Corriger manuellement: {issue_type}")
        
        return False

if __name__ == "__main__":
    success = detailed_verification()
    exit(0 if success else 1)