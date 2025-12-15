#!/usr/bin/env python
import os
import sys
import django

# Configure Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré avec succès")
    
    # Vérifiez la configuration Simple JWT
    from django.conf import settings
    
    print("\n🔧 Configuration Simple JWT:")
    
    if hasattr(settings, 'SIMPLE_JWT'):
        print("✅ SIMPLE_JWT configuré")
        for key, value in settings.SIMPLE_JWT.items():
            print(f"   {key}: {value}")
    else:
        print("❌ SIMPLE_JWT non configuré dans settings.py")
    
    # Vérifiez l'utilisateur admin
    from django.contrib.auth.models import User
    
    print("\n👤 Vérification de l'utilisateur 'admin':")
    try:
        admin_user = User.objects.get(username='admin')
        print(f"✅ Utilisateur 'admin' trouvé (ID: {admin_user.id})")
        print(f"   Email: {admin_user.email}")
        print(f"   Is superuser: {admin_user.is_superuser}")
        print(f"   Is active: {admin_user.is_active}")
        
        # Test du mot de passe
        if admin_user.check_password('Admin123!'):
            print("✅ Mot de passe 'Admin123!' valide")
        else:
            print("❌ Mot de passe 'Admin123!' invalide")
            
    except User.DoesNotExist:
        print("❌ Utilisateur 'admin' non trouvé")
        print("   Pour le créer: python manage.py createsuperuser --username admin --email admin@example.com")
    
    # Vérifiez l'utilisateur matrix
    print("\n👤 Vérification de l'utilisateur 'matrix':")
    try:
        matrix_user = User.objects.get(username='matrix')
        print(f"✅ Utilisateur 'matrix' trouvé (ID: {matrix_user.id})")
        print(f"   Email: {matrix_user.email}")
        print(f"   Is active: {matrix_user.is_active}")
    except User.DoesNotExist:
        print("⚠️  Utilisateur 'matrix' non trouvé")
    
    # Vérifiez les endpoints API
    print("\n🌐 Vérification des URLs API:")
    from django.urls import get_resolver
    
    resolver = get_resolver()
    api_patterns = []
    
    def extract_urls(url_patterns, prefix=''):
        for pattern in url_patterns:
            if hasattr(pattern, 'pattern'):
                full_pattern = prefix + str(pattern.pattern)
                if 'api' in full_pattern:
                    api_patterns.append(full_pattern)
                if hasattr(pattern, 'url_patterns'):
                    extract_urls(pattern.url_patterns, full_pattern)
    
    extract_urls(resolver.url_patterns)
    
    if api_patterns:
        print("✅ URLs API trouvées:")
        for pattern in sorted(set(api_patterns)):
            print(f"   {pattern}")
    else:
        print("❌ Aucune URL API trouvée")
        
except Exception as e:
    print(f"❌ Erreur lors de la configuration Django: {e}")
    import traceback
    traceback.print_exc()
