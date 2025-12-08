#!/usr/bin/env python
"""
Test immédiat après corrections
"""

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

def immediate_test():
    print("🎯 TEST IMMÉDIAT - ESPACE AGENT")
    print("=" * 40)
    
    from django.test import Client
    from django.contrib.auth.models import User
    
    client = Client()
    
    try:
        # 1. Connexion
        print("1. 🔐 Connexion...")
        login_ok = client.login(username='test_agent', password='testpass123')
        if not login_ok:
            print("   ❌ Échec connexion")
            return False
        print("   ✅ Connecté")
        
        # 2. Test URLs principales
        print("\n2. 🌐 Test des URLs...")
        
        urls = [
            ('/agents/dashboard/', 'Dashboard'),
            ('/agents/bons/creer/', 'Création bons'),
            ('/agents/membres/', 'Liste membres'),
            ('/agents/notifications/', 'Notifications'),
        ]
        
        for url, name in urls:
            response = client.get(url)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {name}: {response.status_code}")
        
        # 3. Vérification profil
        print("\n3. 👤 Vérification profil...")
        user = User.objects.get(username='test_agent')
        if hasattr(user, 'agent'):
            agent = user.agent
            print(f"   ✅ Profil agent trouvé")
            print(f"   📋 Matricule: {agent.matricule}")
            print(f"   💼 Poste: {agent.poste}")
            print(f"   📞 Téléphone: {agent.telephone}")
        else:
            print("   ❌ Pas de profil agent")
            return False
        
        print("\n🎉 ESPACE AGENT OPÉRATIONNEL !")
        print("\n📍 Accédez à:")
        print("   http://127.0.0.1:8000/agents/dashboard/")
        print("   http://127.0.0.1:8000/agents/bons/creer/")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = immediate_test()
    if success:
        print("\n🚀 Vous pouvez maintenant utiliser l'espace agent!")
    else:
        print("\n❌ Des problèmes persistent.")