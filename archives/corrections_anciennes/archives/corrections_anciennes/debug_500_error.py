# debug_500_error.py
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
import traceback

def debug_recherche_api():
    """Debug détaillé de l'API de recherche"""
    print("🐛 DEBUG ERREUR 500 - RECHERCHE MEMBRES")
    print("=" * 60)
    
    client = Client()
    
    try:
        # 1. Trouver un utilisateur staff
        user = User.objects.filter(is_staff=True).first()
        if not user:
            print("❌ Aucun utilisateur staff trouvé")
            return
        
        print(f"✅ Utilisateur de test: {user.username}")
        client.force_login(user)
        
        # 2. Tester l'API avec différentes requêtes
        test_queries = ['jean', 'marie', 'MEM', '01']
        
        for query in test_queries:
            print(f"\n🔍 Test recherche: '{query}'")
            try:
                response = client.get(f'/agents/api/recherche-membres/?q={query}')
                print(f"   Statut HTTP: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Succès: {len(data.get('membres', []))} résultats")
                elif response.status_code == 500:
                    print("   ❌ Erreur 500 - Vérifiez les logs Django")
                    # Essayer d'obtenir plus d'infos sur l'erreur
                    try:
                        error_data = response.json()
                        print(f"   Message d'erreur: {error_data}")
                    except:
                        print("   Impossible de récupérer les détails de l'erreur")
            except Exception as e:
                print(f"   ❌ Exception: {e}")
                traceback.print_exc()
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        traceback.print_exc()

def verifier_modeles_et_imports():
    """Vérifie que tous les modèles et imports fonctionnent"""
    print("\n🔍 VÉRIFICATION MODÈLES ET IMPORTS")
    print("=" * 50)
    
    try:
        # Test d'import des modèles
        from membres.models import Membre
        print("✅ Modèle Membre importé")
        
        from paiements.models import Paiement
        print("✅ Modèle Paiement importé")
        
        from agents.models import Agent, VerificationCotisation, ActiviteAgent
        print("✅ Modèles agents importés")
        
        # Test de requête basique
        try:
            membres_count = Membre.objects.count()
            print(f"✅ Membre.objects.count() = {membres_count}")
        except Exception as e:
            print(f"❌ Erreur Membre.objects.count(): {e}")
        
        try:
            paiements_count = Paiement.objects.count()
            print(f"✅ Paiement.objects.count() = {paiements_count}")
        except Exception as e:
            print(f"❌ Erreur Paiement.objects.count(): {e}")
        
        try:
            agents_count = Agent.objects.count()
            print(f"✅ Agent.objects.count() = {agents_count}")
        except Exception as e:
            print(f"❌ Erreur Agent.objects.count(): {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur vérification: {e}")
        return False

def tester_fonction_verification_cotisation():
    """Teste la fonction de vérification de cotisation"""
    print("\n🔍 TEST FONCTION VÉRIFICATION COTISATION")
    print("=" * 50)
    
    try:
        from membres.models import Membre
        from agents.views import verifier_cotisation_membre
        
        # Tester avec un membre existant
        membre = Membre.objects.first()
        if membre:
            print(f"✅ Test avec membre: {membre.prenom} {membre.nom}")
            est_a_jour, details = verifier_cotisation_membre(membre)
            print(f"   Résultat: est_a_jour={est_a_jour}, details={details}")
        else:
            print("❌ Aucun membre trouvé pour le test")
            
    except Exception as e:
        print(f"❌ Erreur test fonction: {e}")
        traceback.print_exc()

def verifier_vue_recherche():
    """Vérifie le code de la vue recherche"""
    print("\n🔍 VÉRIFICATION CODE VUE RECHERCHE")
    print("=" * 50)
    
    views_path = BASE_DIR / 'agents' / 'views.py'
    if views_path.exists():
        with open(views_path, 'r') as f:
            content = f.read()
            # Vérifier les parties critiques
            checks = [
                ('@login_required', 'Décorateur login_required présent'),
                ('def recherche_membres_api', 'Fonction recherche_membres_api présente'),
                ('Agent.objects.get(user=request.user)', 'Récupération agent présente'),
                ('Membre.objects.filter', 'Filtre Membre présent'),
                ('JsonResponse', 'JsonResponse présent'),
            ]
            
            for check, message in checks:
                if check in content:
                    print(f"✅ {message}")
                else:
                    print(f"❌ {message} - MANQUANT")
    else:
        print("❌ Fichier views.py introuvable")

def diagnostic_complet():
    """Exécute un diagnostic complet"""
    print("🚀 DIAGNOSTIC COMPLET ERREUR 500")
    print("=" * 60)
    
    etapes = [
        ("Vérification modèles", verifier_modeles_et_imports),
        ("Vérification code vue", verifier_vue_recherche),
        ("Test fonction vérification", tester_fonction_verification_cotisation),
        ("Debug API recherche", debug_recherche_api),
    ]
    
    for nom, fonction in etapes:
        print(f"\n📝 {nom}...")
        try:
            fonction()
        except Exception as e:
            print(f"   ❌ Erreur lors du diagnostic: {e}")

if __name__ == "__main__":
    diagnostic_complet()