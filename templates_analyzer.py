#!/usr/bin/env python
"""
ANALYSE DES TEMPLATES AGENTS
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

def analyze_templates():
    print("📄 ANALYSE DES TEMPLATES AGENTS")
    print("=" * 40)
    
    templates_dir = BASE_DIR / 'templates' / 'agents'
    
    if not templates_dir.exists():
        print("❌ Dossier templates/agents non trouvé")
        return
        
    templates = list(templates_dir.glob('*.html'))
    
    print(f"📂 Templates trouvés: {len(templates)}")
    print("-" * 30)
    
    # Analyser chaque template
    for template in templates:
        print(f"\n🔸 {template.name}:")
        
        with open(template, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Statistiques de base
        lines = content.split('\n')
        size_kb = len(content) / 1024
        
        print(f"   📏 Taille: {size_kb:.1f} KB, Lignes: {len(lines)}")
        
        # Vérifier les balises importantes
        checks = [
            ('{% extends', 'Héritage'),
            ('{% block', 'Blocs'),
            ('{{', 'Variables'),
            ('{% url', 'URLs'),
            ('{% static', 'Fichiers statiques'),
        ]
        
        for pattern, desc in checks:
            count = content.count(pattern)
            if count > 0:
                print(f"   ✅ {desc}: {count} occurrences")

def check_template_variables():
    """Vérifie les variables utilisées dans les templates"""
    print("\n🔍 VARIABLES DANS LES TEMPLATES")
    print("=" * 30)
    
    # Variables attendues dans les templates principaux
    expected_variables = {
        'dashboard.html': ['stats', 'agent', 'actions_recentes'],
        'verification_cotisations.html': ['verifications_du_jour', 'dernieres_verifications'],
        'creer_bon_soin.html': ['bons_du_jour', 'membre'],
    }
    
    templates_dir = BASE_DIR / 'templates' / 'agents'
    
    for template_name, expected_vars in expected_variables.items():
        template_path = templates_dir / template_name
        if template_path.exists():
            with open(template_path, 'r') as f:
                content = f.read()
                
            print(f"\n📋 {template_name}:")
            for var in expected_vars:
                if f'{{{{ {var}' in content:
                    print(f"   ✅ Variable '{var}' utilisée")
                else:
                    print(f"   ⚠️  Variable '{var}' NON TROUVÉE")

if __name__ == '__main__':
    analyze_templates()
    check_template_variables()