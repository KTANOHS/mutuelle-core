import os
import django

# Essayer d'importer les settings
try:
    # Ajouter le chemin de votre projet
    import sys
    sys.path.append('.')
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    
    # Configurer Django
    django.setup()
    
    from django.conf import settings
    
    print("🔍 CONFIGURATION ACTUELLE:")
    print(f"DEBUG = {settings.DEBUG}")
    print(f"ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
    print(f"CSRF_TRUSTED_ORIGINS = {getattr(settings, 'CSRF_TRUSTED_ORIGINS', 'Non défini')}")
    print(f"CSRF_COOKIE_DOMAIN = {getattr(settings, 'CSRF_COOKIE_DOMAIN', 'Non défini')}")
    print(f"SECURE_PROXY_SSL_HEADER = {getattr(settings, 'SECURE_PROXY_SSL_HEADER', 'Non défini')}")
    
    # Vérifier spécifiquement notre domaine
    domain = "https://web-production-555c.up.railway.app"
    if hasattr(settings, 'CSRF_TRUSTED_ORIGINS'):
        if domain in settings.CSRF_TRUSTED_ORIGINS:
            print(f"\n✅ {domain} est dans CSRF_TRUSTED_ORIGINS")
        else:
            print(f"\n❌ {domain} N'EST PAS dans CSRF_TRUSTED_ORIGINS")
            print(f"   Origines configurées: {settings.CSRF_TRUSTED_ORIGINS}")
    else:
        print(f"\n⚠️ CSRF_TRUSTED_ORIGINS n'est pas défini")
        
except Exception as e:
    print(f"Erreur: {e}")
    print("\n⚠️ Impossible de charger les settings")
