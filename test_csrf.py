# Créez un script de test

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()

from django.conf import settings
print("DEBUG:", settings.DEBUG)
print("CSRF_TRUSTED_ORIGINS:")
for origin in settings.CSRF_TRUSTED_ORIGINS:
    print(f"  - {origin}")
print(f"\nDomaine actuel: web-production-abe5.up.railway.app")
print(f"Dans la liste: {'https://web-production-abe5.up.railway.app' in settings.CSRF_TRUSTED_ORIGINS}")



