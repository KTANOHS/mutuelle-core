# scripts/test_fonctionnel_bons.py
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
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
    
    # Test avec différents termes
    termes_recherche = ['Jean', 'Marie', 'MEM', '06']
    
    for terme in termes_recherche:
        response = client.get(reverse('agents:rechercher_membre') + f'?q={terme}')
        print(f"Recherche '{terme}': Status {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ {len(data['results'])} résultat(s) trouvé(s)")
                for result in data['results'][:3]:  # Afficher les 3 premiers
                    print(f"      - {result.get('nom_complet', 'N/A')}")
            else:
                print(f"   ❌ Erreur: {data.get('error', 'Inconnue')}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
    
    # 4. Test création bon de soin
    print("\n📝 TEST CRÉATION BON DE SOIN")
    print("-" * 30)
    
    # Trouver un membre pour tester
    membres = Membre.objects.all()
    if membres.exists():
        membre = membres.first()
        print(f"👤 Membre sélectionné: {membre.prenom} {membre.nom}")
        
        # Test accès page création
        url_creation = reverse('agents:creer_bon_soin_membre', args=[membre.id])
        response = client.get(url_creation)
        print(f"Page création: Status {response.status_code}")
        
        if response.status_code == 200:
            # Tester la création réelle
            form_data = {
                'type_soin': 'consultation',
                'montant': '15000.00',
                'symptomes': 'Fièvre et toux persistante',
                'diagnostic': 'Infection respiratoire à traiter',
                'description': 'Test de création fonctionnelle'
            }
            
            bons_avant = BonSoin.objects.count()
            response_post = client.post(url_creation, form_data)
            
            print(f"POST création: Status {response_post.status_code}")
            
            if response_post.status_code == 302:  # Redirection après succès
                bons_apres = BonSoin.objects.count()
                if bons_apres > bons_avant:
                    bon = BonSoin.objects.latest('date_creation')
                    print(f"✅ BON CRÉÉ AVEC SUCCÈS!")
                    print(f"   Code: {bon.code}")
                    print(f"   Membre: {bon.membre.prenom} {bon.membre.nom}")
                    print(f"   Montant: {bon.montant_max} FCFA")
                    print(f"   Statut: {bon.get_statut_display()}")
                else:
                    print("❌ Aucun bon créé malgré la redirection")
            else:
                print("❌ Échec de la création (pas de redirection)")
        else:
            print("❌ Impossible d'accéder à la page de création")
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
        print("⚠️  SYSTÈME EN ATTENTE - Vérifier les données de test")

if __name__ == "__main__":
    test_fonctionnel_complet()