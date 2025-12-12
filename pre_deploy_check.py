#!/usr/bin/env python
# pre_deploy_check.py
import os
import sys

def check_critical_files():
    """Vérifie les fichiers critiques pour Render"""
    print("🔍 VÉRIFICATION PRÉ-DÉPLOIEMENT RENDER")
    print("="*50)
    
    critical_files = [
        ('requirements.txt', True),
        ('manage.py', True),
        ('app.py', True),
        ('templates/base.html', True),
        ('templates/home.html', True),
        ('static/images/logo.jpg', True),
        ('static/js/messagerie-integration.js', False),  # Optionnel
        ('static/img/patient-avatar.png', False),  # Optionnel
    ]
    
    all_ok = True
    
    for filepath, required in critical_files:
        if os.path.exists(filepath):
            print(f"✅ {filepath}")
        else:
            if required:
                print(f"❌ REQUIS MANQUANT: {filepath}")
                all_ok = False
            else:
                print(f"⚠️  Optionnel manquant: {filepath}")
    
    print("\n" + "="*50)
    
    # Vérifier app.py
    if os.path.exists('app.py'):
        with open('app.py', 'r') as f:
            content = f.read()
        
        checks = [
            ('RENDER' in content, "Configuration Render"),
            ('whitenoise' in content, "WhiteNoise configuré"),
            ('collectstatic' in content, "Collectstatic automatique"),
            ('migrate' in content, "Migrations automatiques"),
        ]
        
        for condition, description in checks:
            if condition:
                print(f"✅ {description}")
            else:
                print(f"⚠️  {description} manquante dans app.py")
    
    return all_ok

def check_django():
    """Teste Django rapidement"""
    print("\n🚀 TEST DJANGO RAPIDE")
    print("="*50)
    
    try:
        # Vérifier que Django peut démarrer
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        
        import django
        django.setup()
        
        from django.conf import settings
        
        print(f"✅ Django version: {django.__version__}")
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS[:3]}...")
        print(f"✅ STATIC_ROOT: {settings.STATIC_ROOT}")
        
        # Tester un modèle basique
        from django.contrib.auth.models import User
        user_count = User.objects.count()
        print(f"✅ Users in DB: {user_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur Django: {e}")
        return False

if __name__ == "__main__":
    print("🎯 VÉRIFICATION FINALE AVANT DÉPLOIEMENT RENDER\n")
    
    files_ok = check_critical_files()
    django_ok = check_django()
    
    print("\n" + "="*50)
    print("📊 RÉSUMÉ FINAL")
    print("="*50)
    
    if files_ok and django_ok:
        print("🎉 TOUT EST PRÊT POUR LE DÉPLOIEMENT !")
        print("\n🚀 COMMANDES FINALES:")
        print("1. git add . && git commit -m 'Ready for Render'")
        print("2. git push origin main")
        print("3. Render déploiera automatiquement")
        print("\n🌐 URL: https://mutuelle-core-19.onrender.com")
        sys.exit(0)
    else:
        print("❌ Des problèmes doivent être résolus avant le déploiement.")
        sys.exit(1)