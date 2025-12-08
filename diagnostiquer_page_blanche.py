# diagnostiquer_page_blanche.py
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

def diagnostiquer_page_envoyer_message():
    print("🔍 DIAGNOSTIC PAGE ENVOYER MESSAGE")
    print("=" * 50)
    
    client = Client()
    User = get_user_model()
    
    try:
        # Se connecter en tant qu'agent
        agent = User.objects.get(username='test_agent')
        client.force_login(agent)
        
        print("✅ Agent connecté:", agent.username)
        
        # Tester la page envoyer-message
        response = client.get('/agents/envoyer-message/')
        
        print(f"📄 Statut de la réponse: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Page accessible (statut 200)")
            
            # Vérifier le contenu
            content_length = len(response.content)
            print(f"📏 Longueur du contenu: {content_length} bytes")
            
            if content_length < 100:
                print("❌ CONTENU TROP COURT - Page probablement blanche")
                print("   Raisons possibles:")
                print("   • Template manquant")
                print("   • Erreur dans la vue")
                print("   • Formulaire non défini")
            else:
                print("✅ Contenu semble normal")
                
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors du diagnostic: {e}")

if __name__ == "__main__":
    diagnostiquer_page_envoyer_message()