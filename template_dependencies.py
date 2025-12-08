#!/usr/bin/env python3
"""
Vérifier les liens entre templates (extends, include)
"""

import re
from pathlib import Path

class TemplateDependencyChecker:
    def __init__(self, templates_dir="templates"):
        self.templates_dir = Path(templates_dir)
        self.dependencies = {}
        
    def check_extends_and_includes(self):
        """Vérifier tous les extends et includes"""
        missing_references = []
        
        for template_file in self.templates_dir.rglob("*.html"):
            content = template_file.read_text(encoding='utf-8', errors='ignore')
            
            # Trouver les extends
            extends = re.findall(r'\{%\s*extends\s+[\'"]([^\'"]+)[\'"]\s*%\}', content)
            
            # Trouver les includes  
            includes = re.findall(r'\{%\s*include\s+[\'"]([^\'"]+)[\'"]\s*%\}', content)
            
            # Vérifier chaque référence
            for ref in extends + includes:
                ref_path = self.templates_dir / ref
                if not ref_path.exists():
                    missing_references.append({
                        'source': template_file.relative_to(self.templates_dir),
                        'missing': ref,
                        'type': 'extends' if ref in extends else 'include'
                    })
        
        return missing_references

# Utilisation
checker = TemplateDependencyChecker()
missing = checker.check_extends_and_includes()

if missing:
    print("❌ Références manquantes:")
    for item in missing:
        print(f"   {item['source']} → {item['missing']} ({item['type']})")
else:
    print("✅ Toutes les références sont valides!")