"""
ASGI config for mutuelle_core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# 🔥 Import du routage WebSocket depuis l’app communication
import communication.routing

# 🔧 Configuration de l’environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

# 🚀 Configuration du routeur ASGI
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Gestion HTTP classique
    "websocket": AuthMiddlewareStack(  # Gestion WebSocket avec authentification
        URLRouter(
            communication.routing.websocket_urlpatterns
        )
    ),
})
