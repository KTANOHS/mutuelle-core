# verifier_middlewares.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

from django.conf import settings

def verifier_configuration():
    print("⚙️ VÉRIFICATION DE LA CONFIGURATION DJANGO")
    print("=" * 50)
    
    # Middlewares critiques
    middlewares_critiques = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware', 
        'django.contrib.messages.middleware.MessageMiddleware'
    ]
    
    print("🔍 Middlewares installés:")
    for middleware in getattr(settings, 'MIDDLEWARE', []):
        statut = "✅" if middleware in middlewares_critiques else "  "
        print(f"   {statut} {middleware}")
    
    # Vérifier les apps installées
    apps_critiques = [
        'django.contrib.sessions',
        'django.contrib.auth',
        'django.contrib.messages'
    ]
    
    print("\n📦 Applications installées:")
    for app in settings.INSTALLED_APPS:
        statut = "✅" if app in apps_critiques else "  "
        print(f"   {statut} {app}")
    
    # Vérifier le contexte processeur
    context_processors = getattr(settings, 'TEMPLATES', [{}])[0].get('OPTIONS', {}).get('context_processors', [])
    print("\n🎨 Context processors:")
    for processor in context_processors:
        print(f"   - {processor}")

if __name__ == "__main__":
    verifier_configuration()