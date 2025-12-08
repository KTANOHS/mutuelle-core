# votre_app/middlewares.py
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

class AuthRedirectMiddleware:
    """
    Middleware pour rediriger les utilisateurs vers leurs dashboards spécifiques
    après la connexion lorsqu'ils accèdent à la page dashboard par défaut.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Traitement avant la réponse
        response = self.get_response(request)
        
        # Éviter les boucles de redirection - NE PAS rediriger si c'est déjà une redirection
        if (request.user.is_authenticated and 
            request.path == '/dashboard/' and 
            not getattr(request, 'is_ajax', False) and
            not isinstance(response, HttpResponseRedirect)):
            
            # Vérifier le type d'utilisateur et rediriger vers le dashboard approprié
            if hasattr(request.user, 'assureur'):
                return redirect('assureur_dashboard_direct')
            elif hasattr(request.user, 'medecin'):
                return redirect('medecin_dashboard_direct') 
            elif hasattr(request.user, 'pharmacien'):
                return redirect('pharmacien_dashboard_direct')
            elif hasattr(request.user, 'membre'):
                return redirect('membre_dashboard_direct')
        
        return response
