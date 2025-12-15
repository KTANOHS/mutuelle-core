import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

from django.conf import settings

print("🔧 Configuration pour Render:")
print(f"DEBUG = {settings.DEBUG}")
print(f"ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
print(f"SECRET_KEY défini = {'SECRET_KEY' in dir(settings)}")
print(f"DATABASE ENGINE = {settings.DATABASES['default']['ENGINE']}")

# Vérifiez les apps installées
print(f"\nApps installées ({len(settings.INSTALLED_APPS)}):")
for app in settings.INSTALLED_APPS:
    if 'api' in app or 'rest' in app:
        print(f"  → {app}")
