#!/usr/bin/env python
"""
Test spécifique du dashboard médecin
"""

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_dashboard():
    print("🎯 TEST SPÉCIFIQUE DU DASHBOARD")
    print("=" * 50)
    
    client = Client()
    
    # 1. Se connecter avec dr.test
    print("1. Connexion...")
    success = client.login(username='dr.test', password='Medecin123!')
    print(f"   Login réussi: {success}")
    
    if not success:
        print("❌ Impossible de se connecter")
        return False
    
    # 2. Tester le dashboard SANS suivre les redirections
    print("2. Test dashboard (sans follow)...")
    response = client.get('/medecin/dashboard/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 302:
        print(f"   🔄 REDIRECTION DÉTECTÉE vers: {response.url}")
        print("   💡 Le problème vient de la vue dashboard_medecin")
        print("   🔧 Vérifiez medecin/views.py - ligne avec return redirect()")
        return False
    elif response.status_code == 200:
        print("   ✅ SUCCÈS: Dashboard affiché!")
        return True
    else:
        print(f"   ❌ Status inattendu: {response.status_code}")
        return False

def test_dashboard_avec_follow():
    print("\n3. Test dashboard (avec follow)...")
    
    client = Client()
    client.login(username='dr.test', password='Medecin123!')
    
    response = client.get('/medecin/dashboard/', follow=True)
    print(f"   Status final: {response.status_code}")
    print(f"   URL finale: {response.request['PATH_INFO']}")
    print(f"   Historique: {response.redirect_chain}")
    
    if '/medecin/dashboard/' in response.request['PATH_INFO']:
        print("   ✅ Finalement sur le dashboard")
        return True
    else:
        print("   ❌ Pas sur le dashboard")
        return False

if __name__ == "__main__":
    print("🔍 DIAGNOSTIC DASHBOARD MÉDECIN")
    print("=" * 60)
    
    # Test 1: Sans follow (pour voir la redirection)
    test1 = test_dashboard()
    
    # Test 2: Avec follow (pour voir où ça mène)
    test2 = test_dashboard_avec_follow()
    
    print("\n" + "=" * 60)
    if test1:
        print("🎉 DASHBOARD FONCTIONNEL!")
    else:
        print("🔧 CORRECTIONS NÉCESSAIRES:")
        print("1. Ouvrez medecin/views.py")
        print("2. Trouvez la fonction dashboard_medecin")
        print("3. Supprimez les lignes avec 'return redirect(...)'")
        print("4. Assurez-vous qu'elle finit par 'return render(...)'")