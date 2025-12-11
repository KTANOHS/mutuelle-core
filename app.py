import os
import sys
import subprocess

# Appliquer les migrations automatiquement sur Render
if os.environ.get('RENDER') == 'true':
    print("🔄 Application des migrations sur Render...")
    try:
        # Appliquer les migrations
        subprocess.run(['python', 'manage.py', 'migrate', '--noinput'], check=False)
        print("✅ Migrations appliquées")
    except Exception as e:
        print(f"⚠️ Erreur lors des migrations: {e}")

# Charger l'application Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()