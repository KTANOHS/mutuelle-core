# test_compatibilite.py
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_compatibilite_urls():
    """Teste que toutes les URLs fonctionnent"""
    print("🧪 TEST DE COMPATIBILITÉ DES URLs")
    print("=" * 50)
    
    client = Client()
    
    try:
        user = User.objects.filter(is_staff=True).first()
        if not user:
            print("❌ Aucun utilisateur staff trouvé")
            return
        
        print(f"✅ Utilisateur de test: {user.username}")
        client.force_login(user)
        
        # URLs à tester (anciennes et nouvelles)
        urls_a_tester = [
            # Anciennes URLs (doivent toujours fonctionner)
            ('/agents/dashboard/', 'Ancien dashboard'),
            ('/agents/verification-cotisation/', 'Ancienne vérification'),
            
            # Nouvelles URLs
            ('/agents/tableau-de-bord/', 'Nouveau tableau de bord'),
            ('/agents/verification-cotisations/', 'Nouvelle vérification'),
            
            # APIs anciennes
            ('/agents/api/recherche-membres-old/?q=test', 'API recherche ancienne'),
            
            # APIs nouvelles
            ('/agents/api/recherche-membres/?q=test', 'API recherche nouvelle'),
            ('/agents/api/test-simple/', 'API test simple'),
        ]
        
        for url, description in urls_a_tester:
            response = client.get(url)
            status = "✅" if response.status_code in [200, 302] else "❌"
            print(f"{status} {description}: {url} -> HTTP {response.status_code}")
        
        # Test spécifique de la recherche
        print(f"\n🔍 Test recherche avancé...")
        from membres.models import Membre
        membre = Membre.objects.first()
        if membre:
            response = client.get(f'/agents/api/verifier-cotisation/{membre.id}/')
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Vérification API: {data.get('message', 'Succès')}")
            else:
                print(f"❌ Vérification API: HTTP {response.status_code}")
        
    except Exception as e:
        print(f"❌ Erreur test: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎯 POUR TESTER:")
    print("1. Démarrez le serveur: python manage.py runserver")
    print("2. Testez l'ancienne URL: http://localhost:8000/agents/verification-cotisation/")
    print("3. Testez la nouvelle URL: http://localhost:8000/agents/verification-cotisations/")
    print("4. La recherche devrait maintenant fonctionner!")

if __name__ == "__main__":
    test_compatibilite_urls()