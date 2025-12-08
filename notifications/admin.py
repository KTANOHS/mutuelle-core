# notifications/admin.py
from django.contrib import admin
from .models import Notification, PreferenceNotification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'user', 'type_notification', 'lu', 'date_creation']
    list_filter = ['type_notification', 'lu', 'date_creation']
    search_fields = ['titre', 'message', 'user__username']
    readonly_fields = ['date_creation']

@admin.register(PreferenceNotification)
class PreferenceNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_actif', 'push_actif', 'sms_actif']
    list_filter = ['email_actif', 'push_actif', 'sms_actif']
    search_fields = ['user__username']