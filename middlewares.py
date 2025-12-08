# middlewares.py
from django.shortcuts import redirect
from django.contrib.auth.models import Group

class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Vérifier si l'utilisateur est connecté et sur la page dashboard par défaut
        if (request.user.is_authenticated and 
            request.path == '/dashboard/' and 
            not getattr(request, 'is_ajax', False)):
            
            user = request.user
            
            # Redirection basée sur les groupes
            if user.groups.filter(name='assureur').exists():
                return redirect('/assureur/')
            elif user.groups.filter(name='medecin').exists():
                return redirect('/medecin/dashboard/')
            elif user.groups.filter(name='pharmacien').exists():
                return redirect('/pharmacien/dashboard/')
            elif user.groups.filter(name='membre').exists():
                return redirect('/membres/dashboard/')
        
        return None