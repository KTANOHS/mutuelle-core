# test_acces_temps_reel.py

import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def tester_acces_utilisateur(username, password, urls_a_tester):
    """Teste l'accès d'un utilisateur à différentes URLs"""
    client = Client()
    
    print(f"\n🔐 TEST ACCÈS: {username}")
    print("-" * 30)
    
    # Connexion
    login_success = client.login(username=username, password=password)
    if not login_success:
        print(f"❌ Échec connexion pour {username}")
        return
    
    print(f"✅ Connexion réussie")
    
    # Test des URLs
    for url_name, description in urls_a_tester:
        try:
            url = reverse(url_name)
            response = client.get(url)
            
            if response.status_code == 200:
                print(f"   ✅ {description}: ACCÈS AUTORISÉ")
            elif response.status_code == 403:
                print(f"   ❌ {description}: ACCÈS REFUSÉ")
            elif response.status_code == 302:
                print(f"   🔄 {description}: REDIRECTION")
            else:
                print(f"   ⚠️  {description}: CODE {response.status_code}")
                
        except Exception as e:
            print(f"   💥 {description}: ERREUR - {e}")

def test_complet_acces():
    """Test complet des accès pour tous les rôles"""
    
    print("🧪 TEST COMPLET DES ACCÈS EN TEMPS RÉEL")
    print("=" * 50)
    
    # URLs à tester pour chaque rôle
    urls_agents = [
        ('agents:dashboard', 'Tableau de bord agents'),
        ('agents:liste_membres', 'Liste des membres'),
        ('agents:creer_bon_soin', 'Créer bon de soin'),
        ('medecin:dashboard', 'Dashboard médecin (devrait être refusé)'),
    ]
    
    urls_medecin = [
        ('medecin:dashboard', 'Tableau de bord médecin'),
        ('medecin:creer_ordonnance', 'Créer ordonnance'),
        ('agents:dashboard', 'Dashboard agents (devrait être refusé)'),
    ]
    
    urls_pharmacien = [
        ('pharmacien:dashboard', 'Tableau de bord pharmacien'),
        ('pharmacien:liste_ordonnances_attente', 'Ordonnances en attente'),
        ('medecin:dashboard', 'Dashboard médecin (devrait être refusé)'),
    ]
    
    urls_membre = [
        ('membres:dashboard', 'Tableau de bord membre'),
        ('membres:mes_bons', 'Mes bons de soin'),
        ('agents:dashboard', 'Dashboard agents (devrait être refusé)'),
    ]
    
    # Test pour chaque utilisateur
    utilisateurs_test = [
        ('agent_test', 'password123', urls_agents, 'AGENT'),
        ('medecin_test', 'password123', urls_medecin, 'MÉDECIN'),
        ('pharmacien_test', 'password123', urls_pharmacien, 'PHARMACIEN'),
        ('membre_test', 'password123', urls_membre, 'MEMBRE'),
    ]
    
    for username, password, urls, role in utilisateurs_test:
        # Vérifier que l'utilisateur existe
        if User.objects.filter(username=username).exists():
            tester_acces_utilisateur(username, password, urls)
        else:
            print(f"\n❌ Utilisateur {username} ({role}) n'existe pas")
            print("   Exécutez d'abord diagnostic_permissions_acces.py")

if __name__ == "__main__":
    test_complet_acces()