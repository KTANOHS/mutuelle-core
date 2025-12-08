#!/usr/bin/env python3
# diagnostic_templates.py

import os
import django
from pathlib import Path

# Configuration Django minimale
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.template.loader import get_template

def check_templates():
    print("🔍 DIAGNOSTIC DES TEMPLATES MEDECIN")
    print("=" * 50)
    
    templates_to_check = [
        'medecin/dashboard.html',
        'medecin/liste_bons.html', 
        'medecin/mes_rendez_vous.html',
        'medecin/creer_ordonnance.html'
    ]
    
    for template_name in templates_to_check:
        try:
            template = get_template(template_name)
            print(f"✅ {template_name} - TROUVÉ")
        except Exception as e:
            print(f"❌ {template_name} - ERREUR: {e}")

if __name__ == "__main__":
    check_templates()