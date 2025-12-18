# mutuelle_core/wsgi.py - Assurez-vous qu'il ressemble à ceci
"""
WSGI config for mutuelle_core project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

application = get_wsgi_application()

# Pour WhiteNoise (servir les fichiers statiques)
from whitenoise import WhiteNoise
if not os.path.exists('staticfiles'):
    os.makedirs('staticfiles', exist_ok=True)
application = WhiteNoise(application, root='staticfiles')