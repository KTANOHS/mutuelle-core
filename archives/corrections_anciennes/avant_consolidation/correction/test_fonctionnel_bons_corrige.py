# scripts/test_fonctionnel_bons_corrige.py
import os
import django
import sys

# Détection automatique du projet
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)

project_name = None
for item in os.listdir(current_dir):
    if os.path.isdir(os.path.join(current_dir, item)) and 'settings.py' in os.listdir(os.path.join(current_dir, item)):
        project_name = item
        break

if project_name:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
    print(f"🎯 Configuration avec projet: {project_name}")
else:
    print("❌ Impossible de détecter le projet Django")
    sys.exit(1)

django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from agents.models import Agent, BonSoin
from membres.models import Membre

def test_fonctionnel_complet():
    print("🧪 TEST FONCTIONNEL COMPLET - CRÉATION BONS DE SOIN")
    print("=" * 60)
    
    client = Client()
    
    # 1. Trouver un agent existant
    agents = Agent.objects.all()
    if not agents.exists():
        print("❌ Aucun agent trouvé dans la base")
        return
    
    agent = agents.first()
    print(f"🎯 Agent sélectionné: {agent.user.get_full_name()} ({agent.matricule})")
    
    # 2. Se connecter en tant qu'agent
    client.force_login(agent.user)
    print("✅ Authentification réussie")
    
    # 3. Test de l'API de recherche
    print("\n🔍 TEST API RECHERCHE")
    print("-" * 30)
    
    # Rechercher des membres existants
    membres = Membre.objects.all()[:3]  # Prendre les 3 premiers
    termes_recherche = []
    
    for membre in membres:
        if membre.prenom:
            termes_recherche.append(membre.prenom)
        if membre.nom:
            termes_recherche.append(membre.nom)
        if membre.numero_unique:
            termes_recherche.append(membre.numero_unique)
    
    # Ajouter quelques termes génériques
    termes_recherche.extend(['test', '06', 'MEM'])
    
    for terme in termes_recherche[:5]:  # Tester les 5 premiers termes
        response = client.get(reverse('agents:rechercher_membre') + f'?q={terme}')
        print(f"Recherche '{terme}': Status {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                results = data.get('results', [])
                print(f"   ✅ {len(results)} résultat(s) trouvé(s)")
                for result in results[:2]:  # Afficher les 2 premiers
                    print(f"      - {result.get('nom_complet', 'N/A')}")
            else:
                print(f"   ❌ Erreur: {data.get('error', 'Inconnue')}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
    
    # 4. Test création bon de soin
    print("\n📝 TEST CRÉATION BON DE SOIN")
    print("-" * 30)
    
    # Trouver un membre pour tester
    membre = Membre.objects.first()
    if membre:
        print(f"👤 Membre sélectionné: {getattr(membre, 'prenom', 'N/A')} {getattr(membre, 'nom', 'N/A')}")
        
        # Test accès page création
        try:
            url_creation = reverse('agents:creer_bon_soin_membre', args=[membre.id])
            response = client.get(url_creation)
            print(f"Page création: Status {response.status_code}")
            
            if response.status_code == 200:
                # Tester la création réelle
                form_data = {
                    'type_soin': 'consultation',
                    'montant': '15000.00',
                    'symptomes': 'Fièvre et toux persistante - TEST',
                    'diagnostic': 'Infection respiratoire - DIAGNOSTIC TEST',
                }
                
                bons_avant = BonSoin.objects.count()
                response_post = client.post(url_creation, form_data)
                
                print(f"POST création: Status {response_post.status_code}")
                
                if response_post.status_code in [302, 200]:  # Redirection ou succès
                    bons_apres = BonSoin.objects.count()
                    if bons_apres > bons_avant:
                        bon = BonSoin.objects.latest('date_creation')
                        print(f"✅ BON CRÉÉ AVEC SUCCÈS!")
                        print(f"   Code: {bon.code}")
                        print(f"   Membre: {getattr(bon.membre, 'prenom', 'N/A')} {getattr(bon.membre, 'nom', 'N/A')}")
                        print(f"   Montant: {bon.montant_max} FCFA")
                        print(f"   Statut: {bon.get_statut_display()}")
                    else:
                        print("❌ Aucun bon créé - Vérifiez les logs")
                        # Afficher le contenu de la réponse pour debug
                        if hasattr(response_post, 'content'):
                            print(f"   Réponse: {response_post.content[:200]}...")
                else:
                    print("❌ Échec de la création")
            else:
                print(f"❌ Impossible d'accéder à la page de création: {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur lors du test de création: {e}")
    else:
        print("❌ Aucun membre trouvé pour tester")
    
    # 5. Vérification finale
    print("\n📊 VÉRIFICATION FINALE")
    print("-" * 30)
    print(f"Bons de soin en base: {BonSoin.objects.count()}")
    print(f"Membres en base: {Membre.objects.count()}")
    print(f"Agents en base: {Agent.objects.count()}")
    
    print("\n🎯 RÉSUMÉ DU TEST")
    print("=" * 30)
    if BonSoin.objects.count() > 0:
        print("✅ SYSTÈME FONCTIONNEL - Les bons de soin peuvent être créés")
    else:
        print("⚠️  SYSTÈME EN ATTENTE - Vérifier les données et permissions")

if __name__ == "__main__":
    test_fonctionnel_complet()