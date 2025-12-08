#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Définir l'environnement par défaut
    if 'DJANGO_ENV' not in os.environ:
        os.environ.setdefault('DJANGO_ENV', 'development')
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Ajouter un message de démarrage
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        env = os.environ.get('DJANGO_ENV', 'development')
        print(f"🚀 Démarrage du serveur Django en mode {env}")
        print(f"🔧 DEBUG: {os.environ.get('DEBUG', 'True' if env == 'development' else 'False')}")
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()