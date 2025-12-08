# communication/urls_api.py
from django.urls import path
from . import api_views

app_name = 'communication_api'

urlpatterns = [
    path('api/messages/count/', api_views.api_messages_count, name='api_messages_count'),
    path('api/last-activity/', api_views.api_last_activity, name='api_last_activity'),
    path('api/stats/', api_views.api_communication_stats, name='api_communication_stats'),
]
