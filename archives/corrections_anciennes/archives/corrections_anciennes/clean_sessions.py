"""
Nettoyage des sessions pour résoudre les problèmes de connexion - VERSION CORRIGÉE
"""
import os
import django

# Configuration Django AVANT tout import
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    exit(1)

from django.contrib.sessions.models import Session
from django.core.management import call_command

def clean_sessions():
    try:
        # Compter les sessions avant nettoyage
        before_count = Session.objects.count()
        print(f"Sessions avant nettoyage: {before_count}")
        
        # Nettoyer les sessions expirées
        call_command('clearsessions')
        
        # Compter après nettoyage
        after_count = Session.objects.count()
        print(f"Sessions après nettoyage: {after_count}")
        print(f"Sessions supprimées: {before_count - after_count}")
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {e}")

if __name__ == "__main__":
    clean_sessions()