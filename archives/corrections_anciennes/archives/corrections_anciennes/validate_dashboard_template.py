#!/usr/bin/env python3
"""
Test de validation du template dashboard.html
"""

import os
import django
from django.template import Template, Context
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def validate_dashboard_template():
    print("🧪 VALIDATION DU TEMPLATE DASHBOARD")
    print("=" * 50)
    
    template_path = "/Users/koffitanohsoualiho/Documents/projet/templates/pharmacien/dashboard.html"
    
    try:
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # Test de compilation du template
        template = Template(template_content)
        
        # Test de rendu avec un contexte simulé
        context = Context({
            'ordonnances_attente': 5,
            'ordonnances_aujourdhui': 2,
            'total_ordonnances': 10,
            'date_aujourdhui': '13/10/2025',
            'dernieres_ordonnances': [],
            'user_group': 'Pharmacien'
        })
        
        rendered = template.render(context)
        print("✅ SUCCÈS: dashboard.html se compile et se rend correctement")
        print("   Le template est maintenant syntaxiquement valide")
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        print("   Le template a encore des problèmes de syntaxe")

if __name__ == "__main__":
    validate_dashboard_template()