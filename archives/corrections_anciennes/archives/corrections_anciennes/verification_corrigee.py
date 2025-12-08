# verification_corrigee.py
import os
import sys
import subprocess

def check_package(package_name):
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def check_python_version():
    version = sys.version_info
    return version.major == 3 and version.minor >= 8

def main():
    print("🔧 VÉRIFICATION CORRIGÉE DES PRÉREQUIS")
    print("=" * 50)
    
    # Vérification Python
    if check_python_version():
        print(f"✅ Python {sys.version.split()[0]}")
    else:
        print(f"❌ Version Python incompatible: {sys.version}")
    
    # Vérification des packages
    packages = {
        'django': 'Django',
        'rest_framework': 'Django REST Framework',
        'corsheaders': 'django-cors-headers',
        'channels': 'Channels',
        'celery': 'Celery',
        'redis': 'Redis',
        'psycopg2': 'PostgreSQL',
        'whitenoise': 'WhiteNoise'
    }
    
    print("\n📦 PACKAGES REQUIS:")
    for package, name in packages.items():
        if check_package(package):
            print(f"   ✅ {name}")
        else:
            print(f"   ❌ {name} - À installer")
    
    # Vérification structure projet
    print("\n🏗️ STRUCTURE PROJET:")
    for dir_name in ['api', 'js', 'css', 'templates']:
        if os.path.exists(dir_name):
            print(f"   ✅ {dir_name}")
        else:
            print(f"   ⚠️  {dir_name} - Vérifier la structure")

if __name__ == "__main__":
    main()