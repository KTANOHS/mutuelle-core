#!/usr/bin/env python
"""
APPLICATION WSGI ULTIME POUR RENDER.COM - VERSION CORRIGÉE
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def apply_migrations():
    """Applique les migrations Django - VERSION FORCÉE"""
    try:
        logger.info("🚨 APPLICATION DES MIGRATIONS EN FORCE...")
        
        # Essayer d'appliquer toutes les migrations
        result = subprocess.run(
            [sys.executable, 'manage.py', 'migrate', '--noinput'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            logger.info("✅ MIGRATIONS APPLIQUÉES AVEC SUCCÈS")
            logger.info(f"Output: {result.stdout[:500]}...")
        else:
            logger.error(f"❌ ERREUR MIGRATIONS: {result.stderr}")
            
            # Essayer de créer les migrations si besoin
            logger.info("🔄 Tentative de création des migrations...")
            subprocess.run(
                [sys.executable, 'manage.py', 'makemigrations', '--noinput'],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            )
            
            # Réessayer les migrations
            subprocess.run(
                [sys.executable, 'manage.py', 'migrate', '--noinput'],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            )
            
    except Exception as e:
        logger.error(f"🚨 EXCEPTION MIGRATIONS: {e}")
        # On continue quand même, peut-être que l'application peut démarrer

def create_superuser():
    """Crée un superutilisateur par défaut si besoin"""
    try:
        logger.info("👤 Vérification/création du superutilisateur...")
        
        subprocess.run([
            sys.executable, '-c', """
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = 'admin'
email = 'admin@mutuelle.com'
password = 'Admin123!'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'✅ Superutilisateur créé: {username} / {password}')
else:
    print(f'✅ Superutilisateur existe déjà: {username}')
"""
        ], cwd=Path(__file__).parent)
        
    except Exception as e:
        logger.warning(f"⚠️ Impossible de créer le superutilisateur: {e}")

def main():
    """Point d'entrée principal"""
    logger.info("=" * 60)
    logger.info("🚀 DÉMARRAGE DE MUTUELLE-CORE SUR RENDER")
    logger.info("=" * 60)
    
    # Vérifier si on est sur Render
    is_render = os.environ.get('RENDER') == 'true'
    logger.info(f"🌐 Environnement: {'RENDER' if is_render else 'LOCAL'}")
    
    # Sur Render, appliquer les migrations FORCÉES
    if is_render:
        apply_migrations()
        create_superuser()
    else:
        logger.info("🔧 Mode local - Pas de migrations automatiques")
    
    # Charger l'application Django
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        
        logger.info("✅ APPLICATION DJANGO CHARGÉE AVEC SUCCÈS!")
        
        # Log de configuration
        from django.conf import settings
        logger.info(f"📊 Configuration:")
        logger.info(f"   DEBUG: {settings.DEBUG}")
        logger.info(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        logger.info(f"   DATABASE: {settings.DATABASES['default']['ENGINE']}")
        
        return application
        
    except Exception as e:
        logger.error(f"🚨 ERREUR CRITIQUE: Impossible de charger Django: {e}")
        logger.error("Détails:", exc_info=True)
        
        # Créer une application minimale en cas d'erreur
        from django.core.wsgi import get_wsgi_application
        return get_wsgi_application()

# Application WSGI
application = main()

# ALIAS POUR GUNICORN - CRITIQUE POUR RENDER
# Gunicorn cherche 'app' dans 'app:app', donc nous créons un alias
app = application

# Pour le développement local
if __name__ == "__main__":
    logger.info("🏃 Exécution en mode développement...")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossible d'importer Django. Êtes-vous sûr qu'il est installé ?"
        ) from exc
    execute_from_command_line(sys.argv)