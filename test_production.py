
#!/usr/bin/env python3
"""
Test de configuration production
"""
import os
import sys
import django

# Forcer le mode production
os.environ['DJANGO_ENV'] = 'production'

print("🔍 Test configuration production...")

# Essayer d'importer les settings
try:
    from mutuelle_core import settings_prod
    print("✅ settings_prod.py trouvé")
    
    # Vérifier les paramètres
    print(f"📊 Configuration:")
    print(f"  - DEBUG: {settings_prod.DEBUG}")
    print(f"  - ALLOWED_HOSTS: {settings_prod.ALLOWED_HOSTS}")
    print(f"  - STATIC_ROOT: {settings_prod.STATIC_ROOT}")
    
except ImportError as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

print("🎉 Test réussi!")


