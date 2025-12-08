import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate

def tester_redirections_corrigees():
    """Tester les redirections après corrections"""
    print("🔄 TEST REDIRECTIONS CORRIGÉES")
    print("==============================")
    
    client = Client()
    user = authenticate(username='koffitanoh', password='nouveau_mot_de_passe')
    
    if not user:
        print("❌ Authentification échouée")
        return
    
    client.force_login(user)
    print("✅ Authentification réussie")
    
    # Tester les pages avec suivi des redirections
    pages = [
        '/agents/creer-bon-soin/',
        '/agents/tableau-de-bord/',
        '/agents/liste-membres/',
        '/admin/'
    ]
    
    for page in pages:
        print(f"\n🔗 Test: {page}")
        response = client.get(page, follow=True)  # follow=True pour suivre les redirections
        
        # Afficher la chaîne de redirections
        if len(response.redirect_chain) > 0:
            print(f"   🔄 Redirections: {response.redirect_chain}")
        
        print(f"   🎯 Page finale: {response.status_code}")
        
        # Vérifier le contenu de la page finale
        if response.status_code == 200:
            if 'creer-bon-soin' in str(response.content):
                print("   ✅ Page création bon de soin chargée")
            elif 'tableau-de-bord' in str(response.content):
                print("   ✅ Tableau de bord chargé")
            elif 'liste-membres' in str(response.content):
                print("   ✅ Liste membres chargée")
            elif 'admin' in str(response.content):
                print("   ⚠️  Page admin chargée")

if __name__ == "__main__":
    tester_redirections_corrigees()