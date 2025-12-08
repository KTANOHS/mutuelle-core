# test_solution.py
import os
import django
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def tester_solution():
    print("TEST DE LA SOLUTION")
    print("=" * 50)
    
    # URLs qui fonctionnent MAINTENANT
    urls_valides = [
        'agents:liste_messages',
        'communication:envoyer_message', 
        'communication:conversations',
        'communication:message_list'
    ]
    
    for url_name in urls_valides:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name:30} → {url}")
        except Exception as e:
            print(f"❌ {url_name:30} → ERREUR: {e}")
    
    print("\nUTILISEZ CES URLs DANS VOS TEMPLATES !")

if __name__ == "__main__":
    tester_solution()