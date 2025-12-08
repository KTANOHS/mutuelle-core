from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session
import os

class Command(BaseCommand):
    help = 'Analyse les problèmes d\'authentification et de redirection'
    
    def handle(self, *args, **options):
        # Importer et exécuter les fonctions d'analyse
        from mutuelle_core.debug_connection import (
            analyze_connection_issues, 
            test_user_redirections,
            check_session_data
        )
        
        analyze_connection_issues()
        test_user_redirections()
        check_session_data()