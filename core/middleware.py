from .models import Notification

class NotificationsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.notifications = Notification.objects.filter(
                utilisateur=request.user, 
                lu=False
            )[:10]
        else:
            request.notifications = []
        
        response = self.get_response(request)
        return response