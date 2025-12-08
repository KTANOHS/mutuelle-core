"""
WSGI config for mutuelle_core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Définir l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

# Initialiser Django
application = get_wsgi_application()

# Middleware WhiteNoise pour servir les fichiers statiques
try:
    from whitenoise import WhiteNoise
    application = WhiteNoise(application, root='staticfiles')
    print("✅ WhiteNoise activé pour les fichiers statiques")
except ImportError:
    print("⚠ WhiteNoise non disponible, fichiers statiques non optimisés")