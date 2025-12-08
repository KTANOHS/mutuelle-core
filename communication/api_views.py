# communication/api_views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message, Notification

@login_required
def api_messages_count(request):
    """API pour le compteur de messages non lus"""
    try:
        unread_count = request.user.messages_recus.filter(est_lu=False).count()
        return JsonResponse({'unread_count': unread_count})
    except Exception as e:
        return JsonResponse({'unread_count': 0, 'error': str(e)})

@login_required  
def api_last_activity(request):
    """API pour la dernière activité de communication"""
    try:
        last_message = Message.objects.filter(
            Q(expediteur=request.user) | Q(destinataire=request.user)
        ).order_by('-date_envoi').first()
        
        last_activity = last_message.date_envoi if last_message else None
        
        return JsonResponse({
            'last_activity': last_activity.isoformat() if last_activity else None,
            'success': True
        })
    except Exception as e:
        return JsonResponse({
            'last_activity': None,
            'success': False,
            'error': str(e)
        })

@login_required
def api_communication_stats(request):
    """API pour les statistiques de communication"""
    try:
        stats = {
            'messages_non_lus': request.user.messages_recus.filter(est_lu=False).count(),
            'messages_recus_total': request.user.messages_recus.count(),
            'notifications_non_lues': Notification.objects.filter(user=request.user, est_lue=False).count(),
            'conversations_actives': 0,  # À adapter selon votre modèle
        }
        return JsonResponse({'stats': stats, 'success': True})
    except Exception as e:
        return JsonResponse({'stats': {}, 'success': False, 'error': str(e)})
