# test_systeme_rapide.py
import os
import django
import sys
from datetime import date

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from membres.models import Membre
from agents.models import Agent

def test_systeme_rapide():
    print("🚀 TEST RAPIDE DU SYSTÈME")
    print("=" * 50)
    
    client = Client()
    
    # Test 1: Vérification des URLs principales
    print("1. 🔗 TEST DES URLs:")
    
    urls = [
        '/',
        '/agents/tableau-de-bord/',
        '/agents/liste-membres/',
        '/agents/verification-cotisations/',
    ]
    
    for url in urls:
        try:
            response = client.get(url)
            status = "✅ 200" if response.status_code == 200 else f"⚠️ {response.status_code}"
            print(f"   {url} -> {status}")
        except Exception as e:
            print(f"   {url} -> ❌ {e}")
    
    # Test 2: Vérification des modèles
    print("\n2. 📊 TEST DES MODÈLES:")
    
    try:
        user_count = User.objects.count()
        print(f"   👥 Utilisateurs: {user_count}")
    except Exception as e:
        print(f"   👥 Utilisateurs: ❌ {e}")
    
    try:
        membres_count = Membre.objects.count()
        print(f"   👤 Membres: {membres_count}")
    except Exception as e:
        print(f"   👤 Membres: ❌ {e}")
    
    try:
        agents_count = Agent.objects.count()
        print(f"   👨‍💼 Agents: {agents_count}")
    except Exception as e:
        print(f"   👨‍💼 Agents: ❌ {e}")
    
    # Test 3: Vérification module affichage unifié
    print("\n3. 🎨 TEST AFFICHAGE UNIFIÉ:")
    
    try:
        from affichage_unifie import afficher_fiche_cotisation_unifiee
        
        # Créer un membre de test
        membre_test = Membre.objects.first()
        if membre_test:
            fiche = afficher_fiche_cotisation_unifiee(membre_test, None, None)
            if "FICHE COTISATION UNIFIÉE" in fiche:
                print("   ✅ Génération fiche: RÉUSSIE")
            else:
                print("   ⚠️ Génération fiche: Format incorrect")
        else:
            print("   ℹ️  Aucun membre pour tester")
            
    except Exception as e:
        print(f"   ❌ Module affichage: {e}")
    
    # Test 4: Vérification templates
    print("\n4. 📁 TEST TEMPLATES:")
    
    templates = [
        'templates/agents/fiche_cotisation_unifiee.html',
        'templates/agents/liste_membres.html',
        'templates/agents/verification_cotisations.html',
    ]
    
    for template in templates:
        if os.path.exists(template):
            print(f"   ✅ {template}")
        else:
            print(f"   ❌ {template} - MANQUANT")
    
    print("=" * 50)
    print("🎯 TEST TERMINÉ")

if __name__ == "__main__":
    test_systeme_rapide()