#!/usr/bin/env python3
"""
Vérification de la syntaxe Django dans tous les templates
"""

import re
from pathlib import Path

def check_django_syntax():
    templates_dir = Path("/Users/koffitanohsoualiho/Documents/projet/templates")
    
    print("🔍 VÉRIFICATION DE SYNTAXE DJANGO")
    print("=" * 50)
    
    problematic_templates = []
    
    for template_path in templates_dir.rglob("*.html"):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier les backslashes dans les tags Django
        patterns = [
            r"{%[^%]*\\'[^%]*%}",  # Backslashes dans les tags
            r"{{[^}]*\\'[^}]*}}",  # Backslashes dans les variables
        ]
        
        issues = []
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                issues.append(f"Ligne {line_num}: Backslashes dans tag Django")
        
        if issues:
            problematic_templates.append({
                'template': template_path.relative_to(templates_dir),
                'issues': issues
            })
            print(f"❌ {template_path.relative_to(templates_dir)}")
            for issue in issues:
                print(f"   ⚠️  {issue}")
    
    if problematic_templates:
        print(f"\n🚨 {len(problematic_templates)} templates avec problèmes de syntaxe")
    else:
        print(f"\n✅ Tous les templates ont une syntaxe correcte")

if __name__ == "__main__":
    check_django_syntax()