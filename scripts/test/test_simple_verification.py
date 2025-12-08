# test_simple_verification.py
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from membres.models import Membre

def test_simple_verification():
    print("🎯 TEST SIMPLE DE VÉRIFICATION")
    print("=" * 50)
    
    client = Client()
    
    # Test 1: Vérifier qu'un agent existant peut se connecter
    print("1. 🔐 TEST DE CONNEXION:")
    
    # Utiliser un agent existant de votre base
    login_success = client.login(username='agent_test', password='password123')
    print(f"   Connexion agent_test: {'✅ RÉUSSIE' if login_success else '❌ ÉCHEC'}")
    
    # Test 2: Vérifier l'accès aux pages après connexion
    print("\n2. 📄 TEST PAGES APRÈS CONNEXION:")
    
    if login_success:
        urls = [
            '/agents/tableau-de-bord/',
            '/agents/liste-membres/',
            '/agents/verification-cotisations/',
        ]
        
        for url in urls:
            response = client.get(url)
            status = "✅ 200" if response.status_code == 200 else f"⚠️ {response.status_code}"
            print(f"   {url} -> {status}")
    else:
        print("   ⏩ Test des pages ignoré (connexion requise)")
    
    # Test 3: Vérifier la fiche unifiée avec un membre existant
    print("\n3. 🎨 TEST FICHE UNIFIÉE:")
    
    membre = Membre.objects.first()
    if membre:
        print(f"   Membre test: {membre.prenom} {membre.nom} (ID: {membre.id})")
        
        if login_success:
            response = client.get(f'/agents/fiche-cotisation-unifiee/{membre.id}/')
            if response.status_code == 200:
                print("   ✅ Fiche unifiée: ACCESSIBLE")
                if 'FICHE COTISATION UNIFIÉE' in response.content.decode():
                    print("   ✅ Contenu fiche: CORRECT")
                else:
                    print("   ⚠️ Contenu fiche: FORMAT INATTENDU")
            else:
                print(f"   ❌ Fiche unifiée: ERREUR {response.status_code}")
        else:
            print("   ⏩ Test fiche ignoré (connexion requise)")
    else:
        print("   ℹ️  Aucun membre disponible pour le test")
    
    # Test 4: Vérification module affichage unifié
    print("\n4. 🔧 TEST MODULE AFFICHAGE:")
    
    try:
        from affichage_unifie import afficher_fiche_cotisation_unifiee
        
        if membre:
            fiche_html = afficher_fiche_cotisation_unifiee(membre, None, None)
            if "FICHE COTISATION UNIFIÉE" in fiche_html:
                print("   ✅ Génération fiche: RÉUSSIE")
            else:
                print("   ⚠️ Génération fiche: Format incorrect")
        else:
            print("   ℹ️  Aucun membre pour tester la génération")
            
    except Exception as e:
        print(f"   ❌ Module affichage: {e}")
    
    print("=" * 50)
    print("🎯 TEST SIMPLE TERMINÉ")

if __name__ == "__main__":
    test_simple_verification()