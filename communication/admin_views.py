from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Notification

@user_passes_test(lambda u: u.is_staff)
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.est_lue = True
    notification.save()
    
    messages.success(request, f"Notification marquée comme lue.")
    return redirect('admin:communication_notification_changelist')

@user_passes_test(lambda u: u.is_staff)
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.delete()
    
    messages.success(request, f"Notification supprimée avec succès.")
    return redirect('admin:communication_notification_changelist')