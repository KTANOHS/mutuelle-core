#!/usr/bin/env python3
"""
Script pour basculer entre développement et production
"""
import os
import sys

def switch_to_production():
    """Passe en mode production"""
    print("🔧 Passage en mode production...")
    
    # Créer le fichier settings_prod.py s'il n'existe pas
    if not os.path.exists('mutuelle_core/settings_prod.py'):
        print("⚠️  Création de mutuelle_core/settings_prod.py...")
        with open('mutuelle_core/settings_prod.py', 'w') as f:
            f.write('''"""
Configuration Django pour l'environnement de production
"""
import os
from .settings import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '.onrender.com']

# Configuration de base de données pour Render
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600, ssl_require=True)
    }

# Sécurité
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Fichiers statiques
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 
''')
    
    # Mettre à jour .env
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Modifier les valeurs
        content = content.replace('DEBUG=True', 'DEBUG=False')
        content = content.replace('DEBUG=TRUE', 'DEBUG=False')
        
        # Ajouter DJANGO_ENV si absent
        if 'DJANGO_ENV=' not in content:
            content += '\nDJANGO_ENV=production\n'
        else:
            content = content.replace('DJANGO_ENV=development', 'DJANGO_ENV=production')
            content = content.replace('DJANGO_ENV=dev', 'DJANGO_ENV=production')
        
        with open(env_file, 'w') as f:
            f.write(content)
    
    print("✅ Mode production activé")
    print("📋 Variables mises à jour:")
    print("  - DEBUG=False")
    print("  - DJANGO_ENV=production")
    print("📝 Pour tester en production: DJANGO_ENV=production python manage.py runserver")

def switch_to_development():
    """Passe en mode développement"""
    print("🔧 Passage en mode développement...")
    
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
        
        content = content.replace('DEBUG=False', 'DEBUG=True')
        content = content.replace('DEBUG=FALSE', 'DEBUG=True')
        
        if 'DJANGO_ENV=' not in content:
            content += '\nDJANGO_ENV=development\n'
        else:
            content = content.replace('DJANGO_ENV=production', 'DJANGO_ENV=development')
        
        with open(env_file, 'w') as f:
            f.write(content)
    
    print("✅ Mode développement activé")
    print("📝 Pour tester en développement: unset DJANGO_ENV && python manage.py runserver")

def main():
    """Fonction principale"""
    if len(sys.argv) != 2:
        print("Usage: python switch_env.py [prod|dev]")
        print("  prod : Mode production")
        print("  dev  : Mode développement")
        return
    
    mode = sys.argv[1].lower()
    
    if mode == 'prod':
        switch_to_production()
    elif mode == 'dev':
        switch_to_development()
    else:
        print(f"Mode invalide: {mode}")
        print("Utilisez 'prod' ou 'dev'")

if __name__ == '__main__':
    main()
