# test_urls.py
import os
import django
from django.urls import reverse, NoReverseMatch
from django.test import TestCase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def tester_urls_communication():
    """Tester toutes les URLs potentielles pour liste_messages"""
    
    print("TEST DES URLs COMMUNICATION")
    print("=" * 50)
    
    # Noms d'URL à tester
    test_cases = [
        # Sans namespace
        'liste_messages',
        'envoyer_message',
        'detail_message',
        'conversations',
        
        # Avec namespace communication
        'communication:liste_messages',
        'communication:envoyer_message', 
        'communication:detail_message',
        'communication:conversations',
        
        # Avec namespace agents
        'agents:liste_messages',
        'agents:envoyer_message',
        'agents:detail_message',
        
        # Autres variations
        'communication_liste_messages',
        'message_list',
        'communication_message_list'
    ]
    
    results = []
    
    for name in test_cases:
        try:
            url = reverse(name)
            status = "✓ SUCCÈS"
            results.append((name, url, status))
        except NoReverseMatch as e:
            status = "✗ ÉCHEC"
            results.append((name, str(e), status))
    
    # Afficher les résultats
    for name, url, status in results:
        print(f"{status:10} {name:30} → {url}")
    
    return results

if __name__ == "__main__":
    tester_urls_communication()