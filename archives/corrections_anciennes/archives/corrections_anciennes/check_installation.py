import os
import sys
import importlib

def check_installation():
    """Vérifie que tout est installé correctement"""
    print("🔍 VÉRIFICATION DE L'INSTALLATION")
    print("=" * 50)
    
    # Fichiers requis
    required_files = ['utils.py', 'constants.py', 'requirements.txt', 'custom_permissions.py']
    
    print("📁 Fichiers requis:")
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MANQUANT")
    
    # Dépendances Python
    required_packages = [
        'Django', 'Pillow', 'django_crispy_forms', 'crispy_bootstrap5',
        'whitenoise', 'psycopg2', 'reportlab', 'openpyxl'
    ]
    
    print("\n📦 Dépendances Python:")
    for package in required_packages:
        try:
            # Convertir le nom pour l'import
            import_name = package.replace('-', '_').lower()
            importlib.import_module(import_name)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NON INSTALLÉ")
    
    # Vérification Django
    print("\n🐍 Environnement Django:")
    try:
        import django
        from django.conf import settings
        
        print(f"  ✅ Django version: {django.__version__}")
        print(f"  ✅ Settings: {settings.SETTINGS_MODULE}")
        
        # Vérifier la base de données
        from django.db import connection
        connection.ensure_connection()
        print("  ✅ Base de données connectée")
        
    except Exception as e:
        print(f"  ❌ Erreur Django: {e}")
    
    print("\n🎯 RÉSUMÉ:")
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if not missing_files:
        print("  ✅ Tous les fichiers sont présents")
    else:
        print(f"  ❌ Fichiers manquants: {', '.join(missing_files)}")
    
    print("  📋 Exécutez: python test_final_integration.py pour tester")

if __name__ == "__main__":
    check_installation()