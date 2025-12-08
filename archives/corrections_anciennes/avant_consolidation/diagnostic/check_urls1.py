# check_urls.py
import os
import django
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_urls_essentielles():
    urls_essentielles = [
        'communication:liste_notifications',
        'medecin:dashboard_medecin',
        'communication:messagerie',
    ]
    
    print("🔍 VÉRIFICATION DES URLS ESSENTIELLES")
    print("=" * 50)
    
    for url_name in urls_essentielles:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name:40} -> {url}")
        except Exception as e:
            print(f"❌ {url_name:40} -> ERREUR: {e}")

if __name__ == "__main__":
    verifier_urls_essentielles()