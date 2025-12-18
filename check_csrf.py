import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.conf import settings

print("=== Vérification CSRF ===")
print(f"DEBUG: {settings.DEBUG}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"CSRF_TRUSTED_ORIGINS: {settings.CSRF_TRUSTED_ORIGINS}")
print(f"CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
print(f"CSRF_COOKIE_DOMAIN: {settings.CSRF_COOKIE_DOMAIN}")

# Test avec l'URL de production
test_url = "https://web-production-abe5.up.railway.app"
is_trusted = any(
    origin.replace('*', '') in test_url or test_url.startswith(origin.replace('*', ''))
    for origin in settings.CSRF_TRUSTED_ORIGINS
)
print(f"\nTest URL: {test_url}")
print(f"Est dans CSRF_TRUSTED_ORIGINS: {is_trusted}")