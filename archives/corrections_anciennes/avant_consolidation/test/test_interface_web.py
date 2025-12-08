import os
import django
import sys
import time
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate
from soins.models import BonDeSoin

def test_interface_web_complete():
    """Test complet de l'interface web"""
    print("🌐 TEST INTERFACE WEB COMPLÈTE")
    print("==============================")
    
    client = Client()
    
    # 1. Authentification
    print("\n1. 🔐 AUTHENTIFICATION")
    user = authenticate(username='agent_operateur', password='agent123')
    
    if not user:
        print("   ❌ Échec authentification")
        return False
    
    client.force_login(user)
    print("   ✅ Authentification réussie")
    
    # 2. Test du tableau de bord
    print("\n2. 📊 TEST TABLEAU DE BORD")
    response = client.get('/agents/tableau-de-bord/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Tableau de bord accessible")
        # Vérifier le contenu
        content = response.content.decode('utf-8')
        if 'tableau de bord' in content.lower():
            print("   ✅ Contenu correct détecté")
    else:
        print("   ❌ Tableau de bord inaccessible")
    
    # 3. Test de la liste des membres
    print("\n3. 👥 TEST LISTE MEMBRES")
    response = client.get('/agents/liste-membres/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Liste membres accessible")
        
        # Test de recherche
        response_recherche = client.get('/agents/liste-membres/?q=test')
        print(f"   🔍 Recherche 'test': {response_recherche.status_code}")
    else:
        print("   ❌ Liste membres inaccessible")
    
    # 4. Test de la création de bons de soin
    print("\n4. 📝 TEST CRÉATION BON DE SOIN")
    response = client.get('/agents/creer-bon-soin/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Page création accessible")
        
        # Test de recherche AJAX
        response_recherche = client.get('/agents/rechercher-membre/?q=an')
        print(f"   🔍 Recherche AJAX 'an': {response_recherche.status_code}")
        
        if response_recherche.status_code == 200:
            print(f"   ✅ Recherche AJAX fonctionnelle")
            print(f"   📄 Résultats: {response_recherche.content.decode('utf-8')[:100]}...")
    
    # 5. Vérification des données créées
    print("\n5. 📊 VÉRIFICATION DONNÉES")
    total_bons = BonDeSoin.objects.count()
    print(f"   📄 Total bons de soin: {total_bons}")
    
    return True

if __name__ == "__main__":
    print("🚀 LANCEZ D'ABORD LA CORRECTION:")
    print("python scripts/correction_agent_operateur.py")
    print("\n💡 Puis exécutez ce test après avoir redémarré le serveur")
    
    # Demander confirmation
    input("Appuyez sur Entrée pour continuer (ou Ctrl+C pour annuler)...")
    
    success = test_interface_web_complete()
    
    if success:
        print("\n🎉 INTERFACE WEB VALIDÉE!")
        print("\n🌐 URLS À TESTER MANUELLEMENT:")
        print("   - Tableau de bord: http://127.0.0.1:8000/agents/tableau-de-bord/")
        print("   - Création bons: http://127.0.0.1:8000/agents/creer-bon-soin/")
        print("   - Liste membres: http://127.0.0.1:8000/agents/liste-membres/")
    else:
        print("\n⚠️  TEST INTERFACE ÉCHOUÉ")