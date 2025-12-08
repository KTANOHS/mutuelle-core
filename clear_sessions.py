#!/usr/bin/env python
"""
Script pour nettoyer les sessions expirées
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.sessions.models import Session
from django.utils import timezone

def clear_expired_sessions():
    """Supprime toutes les sessions expirées"""
    expired_count = Session.objects.filter(expire_date__lt=timezone.now()).count()
    Session.objects.filter(expire_date__lt=timezone.now()).delete()
    return expired_count

if __name__ == '__main__':
    cleared = clear_expired_sessions()
    print(f"Sessions expirées nettoyées: {cleared}")
    print("✅ Sessions nettoyées avec succès")
