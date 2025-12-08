# test_simple.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
try:
    django.setup()
    print("✅ Django configuré avec succès")
    
    from django.conf import settings
    print(f"✅ INSTALLED_APPS: {settings.INSTALLED_APPS[:3]}...")
    
except Exception as e:
    print(f"❌ Erreur: {e}")