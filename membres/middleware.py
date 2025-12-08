# membres/middleware.py
from django.utils import timezone
from .models import UserLoginSession

class TrackingConnexionsMiddleware:
    """Middleware pour tracker les connexions des utilisateurs - VERSION CORRIGÉE"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # ✅ CORRECTION : Vérifier d'abord si l'utilisateur est authentifié
        response = self.get_response(request)
        
        # Tracker la connexion APRÈS que le middleware d'authentification ait fait son travail
        if hasattr(request, 'user') and request.user.is_authenticated:
            self.track_login(request)
        
        return response
    
    def track_login(self, request):
        """Tracker la connexion d'un utilisateur"""
        try:
            if not hasattr(request, 'login_tracked'):
                session_key = request.session.session_key
                
                # Vérifier si une session active existe déjà
                existing_session = UserLoginSession.objects.filter(
                    user=request.user,
                    session_key=session_key,
                    logout_time__isnull=True
                ).first()
                
                if not existing_session:
                    # Récupérer l'adresse IP
                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                    if x_forwarded_for:
                        ip = x_forwarded_for.split(',')[0]
                    else:
                        ip = request.META.get('REMOTE_ADDR')
                    
                    # Créer une nouvelle session
                    UserLoginSession.objects.create(
                        user=request.user,
                        session_key=session_key,
                        ip_address=ip,
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
                
                request.login_tracked = True
        except Exception as e:
            # Éviter de casser l'application en cas d'erreur
            print(f"Erreur dans le tracking de connexion: {e}")
    
    def process_exception(self, request, exception):
        """Gérer les exceptions dans le middleware"""
        return None