# test_final_render.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

from django.template.loader import get_template

try:
    template = get_template('registration/logout.html')
    print("✅ Template chargé avec succès par Django")
    
    # Test de rendu
    html = template.render()
    print(f"✅ Rendu réussi ({len(html)} caractères)")
    print("📱 Extrait:", html[:100] + "...")
    
except Exception as e:
    print(f"❌ Erreur: {e}")