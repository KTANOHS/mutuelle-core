import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("✅ VÉRIFICATION INSTALLED_APPS")
print("===============================")

required_apps = ['agents', 'communication', 'channels']
for app in required_apps:
    if app in settings.INSTALLED_APPS:
        print(f"✅ {app} - PRÉSENT")
    else:
        print(f"❌ {app} - MANQUANT")

print(f"\n📊 Total: {len(required_apps)} apps requis")
print(f"📋 Trouvés: {sum(1 for app in required_apps if app in settings.INSTALLED_APPS)}")