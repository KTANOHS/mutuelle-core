#!/usr/bin/env python
"""
Point d'entrée pour Railway
"""
import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Fonction principale pour Railway"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossible d'importer Django. Êtes-vous sûr qu'il est installé ?"
        ) from exc
    
    # Vérifier si c'est pour collecter les statiques ou démarrer le serveur
    if len(sys.argv) > 1 and sys.argv[1] in ['collectstatic', 'migrate']:
        execute_from_command_line(sys.argv)
    else:
        # Par défaut, démarrer le serveur
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])

if __name__ == '__main__':
    main()