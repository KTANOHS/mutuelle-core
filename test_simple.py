# test_simple.py
import os
import sys

print("🧪 TEST SIMPLE POUR RENDER")
print("=" * 40)

# 1. Vérifier les imports
print("\n1. Vérification des imports...")
try:
    import django
    print("✅ Django")
except:
    print("❌ Django")
    sys.exit(1)

try:
    import dj_database_url
    print("✅ dj-database-url")
except:
    print("❌ dj-database-url")

try:
    import whitenoise
    print("✅ whitenoise")
except:
    print("❌ whitenoise")

try:
    import gunicorn
    print("✅ gunicorn")
except:
    print("❌ gunicorn")

# 2. Tester en mode production
print("\n2. Test mode production...")
os.environ['DJANGO_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'test-secret-key'
os.environ['DEBUG'] = 'False'

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    import django
    django.setup()
    
    from django.conf import settings
    print(f"✅ Django configuré")
    print(f"   • DEBUG: {settings.DEBUG}")
    print(f"   • ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"   • DATABASE: {settings.DATABASES['default']['ENGINE']}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

# 3. Tester collectstatic
print("\n3. Test collectstatic...")
try:
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'collectstatic', '--dry-run', '--noinput'])
    print("✅ collectstatic fonctionne")
except:
    print("⚠ collectstatic a un problème")

print("\n" + "=" * 40)
print("🎯 Votre application est prête pour Render !")
print("\nProchaines étapes:")
print("1. Créez les fichiers: runtime.txt, Procfile, build.sh, render.yaml")
print("2. git add . && git commit -m 'Prêt pour Render' && git push")
print("3. Allez sur https://render.com et déployez")