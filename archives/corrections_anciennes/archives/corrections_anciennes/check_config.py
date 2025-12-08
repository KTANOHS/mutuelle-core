# check_config.py
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.conf import settings

print("⚙️ CONFIGURATION DJANGO VÉRIFIÉE")
print("=" * 40)
print(f"MIDDLEWARE: {'AuthRedirectMiddleware' in settings.MIDDLEWARE}")
print(f"LOGIN_REDIRECT_URL: {getattr(settings, 'LOGIN_REDIRECT_URL', 'Non défini')}")
print(f"INSTALLED_APPS: {len(settings.INSTALLED_APPS)} applications")