# debug_middleware.py
# Placez dans core/middleware.py et ajoutez à MIDDLEWARE dans settings.py

import time
from django.utils.deprecation import MiddlewareMixin

class DebugMiddleware(MiddlewareMixin):
    """Middleware pour debugger les connexions et redirections"""
    
    def process_request(self, request):
        request.start_time = time.time()
        
        # Log des informations de connexion
        if request.user.is_authenticated:
            print(f"🔐 [MIDDLEWARE] Utilisateur connecté: {request.user.username}")
            print(f"   📍 URL: {request.path}")
            print(f"   👥 Groupes: {[g.name for g in request.user.groups.all()]}")
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Log des redirections
            if response.status_code in [301, 302]:
                print(f"🔄 [MIDDLEWARE] Redirection détectée:")
                print(f"   📍 De: {request.path}")
                print(f"   🎯 Vers: {response.url}")
                print(f"   ⏱️  Durée: {duration:.2f}s")
                print(f"   👤 Utilisateur: {request.user.username if request.user.is_authenticated else 'Anonyme'}")
        
        return response