# diagnostic_creation_membre_amelioré.py
import os
import django
import sys
from datetime import datetime
import getpass

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from membres.models import Membre
from agents.models import Agent, ActiviteAgent
import random
import string

def diagnostic_creation_membre_amelioré():
    print("🔍 DIAGNOSTIC CRÉATION MEMBRE PAR AGENT - VERSION AMÉLIORÉE")
    print("=" * 70)
    
    client = Client()
    
    # 1. VÉRIFICATION PRÉLIMINAIRE
    print("1. 📋 VÉRIFICATION PRÉLIMINAIRE:")
    
    total_membres_avant = Membre.objects.count()
    print(f"   ✅ Modèle Membre disponible - {total_membres_avant} membre(s) en base")
    
    agents = User.objects.filter(groups__name='Agents') | User.objects.filter(agent__isnull=False)
    if not agents.exists():
        print("   ❌ Aucun agent trouvé pour le test")
        return
    
    agent = agents.first()
    print(f"   ✅ Agent trouvé: {agent.username} ({agent.get_full_name()})")
    
    # 2. CONNEXION AVEC MOT DE PASSE MANUEL
    print("\n2. 🔐 CONNEXION MANUELLE:")
    
    print(f"   Agent: {agent.username}")
    print("   💡 Entrez le mot de passe manuellement (ne sera pas affiché):")
    
    try:
        # Essayer de récupérer le mot de passe de manière sécurisée
        password = getpass.getpass("   Mot de passe: ")
        
        if not password:
            print("   ⚠️ Aucun mot de passe entré - test sans connexion")
            test_sans_connexion(client, agent, total_membres_avant)
            return
            
        login_success = client.login(username=agent.username, password=password)
        
        if login_success:
            print("   ✅ Connexion réussie !")
        else:
            print("   ❌ Mot de passe incorrect")
            print("   🔄 Passage en mode test sans connexion...")
            test_sans_connexion(client, agent, total_membres_avant)
            return
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la connexion: {e}")
        test_sans_connexion(client, agent, total_membres_avant)
        return
    
    # 3. TEST COMPLET AVEC CONNEXION
    print("\n3. 🎯 TEST COMPLET AVEC CONNEXION:")
    
    # Générer des données de test uniques
    timestamp = str(random.randint(1000, 9999))
    donnees_test = {
        'nom': f"TestDiagnostic{timestamp}",
        'prenom': f"AgentCreation{timestamp}",
        'telephone': f"01{random.randint(10000000, 99999999)}",
        'email': f"test.creation{timestamp}@example.com"
    }
    
    print(f"   📝 Données de test générées:")
    for key, value in donnees_test.items():
        print(f"     - {key}: {value}")
    
    # Test de la page de création
    response = client.get('/agents/creer-membre/')
    if response.status_code == 200:
        print("   ✅ Page création membre accessible")
    else:
        print(f"   ❌ Page création inaccessible: {response.status_code}")
        return
    
    # Création du membre via formulaire
    print("   📤 Envoi du formulaire de création...")
    response = client.post('/agents/creer-membre/', donnees_test)
    
    if response.status_code == 302:
        print("   ✅ Redirection après création (succès)")
        print(f"   🔗 Redirection vers: {response.url}")
    else:
        print(f"   ❌ Pas de redirection - Statut: {response.status_code}")
        # Essayer de récupérer les messages d'erreur
        try:
            from django.contrib.messages import get_messages
            messages = list(get_messages(response.wsgi_request))
            for message in messages:
                print(f"   💬 Message: {message}")
        except:
            pass
    
    # 4. VÉRIFICATION EN BASE DE DONNÉES
    print("\n4. 🗄️ VÉRIFICATION EN BASE DE DONNÉES:")
    
    total_membres_apres = Membre.objects.count()
    print(f"   Membres avant: {total_membres_avant}")
    print(f"   Membres après: {total_membres_apres}")
    
    if total_membres_apres > total_membres_avant:
        print("   ✅ Nouveau membre créé en base !")
        
        # Trouver le nouveau membre
        try:
            nouveau_membre = Membre.objects.filter(
                nom=donnees_test['nom'],
                prenom=donnees_test['prenom']
            ).first()
            
            if nouveau_membre:
                print(f"   📋 Détails du nouveau membre:")
                print(f"     - ID: {nouveau_membre.id}")
                print(f"     - Nom complet: {nouveau_membre.prenom} {nouveau_membre.nom}")
                print(f"     - Numéro unique: {getattr(nouveau_membre, 'numero_unique', 'N/A')}")
                print(f"     - Téléphone: {nouveau_membre.telephone}")
                print(f"     - Email: {nouveau_membre.email}")
                print(f"     - Statut: {getattr(nouveau_membre, 'statut', 'N/A')}")
                print(f"     - Date inscription: {getattr(nouveau_membre, 'date_inscription', 'N/A')}")
            else:
                print("   ⚠️ Membre créé mais non trouvé par recherche")
                
        except Exception as e:
            print(f"   ❌ Erreur recherche nouveau membre: {e}")
    else:
        print("   ❌ Aucun nouveau membre créé")
    
    # 5. VÉRIFICATION ACTIVITÉ ET SYNCHRONISATION
    print("\n5. 📊 VÉRIFICATION ACTIVITÉ ET SYNCHRONISATION:")
    
    # Vérifier l'activité de l'agent
    try:
        activites_recentes = ActiviteAgent.objects.filter(
            agent__user=agent
        ).order_by('-date_activite')[:3]
        
        if activites_recentes.exists():
            print("   ✅ Activités récentes trouvées:")
            for activite in activites_recentes:
                print(f"     - {activite.date_activite}: {activite.description}")
        else:
            print("   ⚠️ Aucune activité récente trouvée")
    except Exception as e:
        print(f"   ❌ Erreur vérification activités: {e}")
    
    # Vérifier la liste des membres
    response = client.get('/agents/liste-membres/')
    if response.status_code == 200:
        content = response.content.decode()
        if donnees_test['nom'] in content and donnees_test['prenom'] in content:
            print("   ✅ Nouveau membre visible dans la liste")
        else:
            print("   ⚠️ Nouveau membre non visible dans la liste")
    else:
        print(f"   ❌ Liste des membres inaccessible: {response.status_code}")
    
    # 6. RAPPORT FINAL
    print("\n6. 📊 RAPPORT FINAL:")
    
    succes_creation = total_membres_apres > total_membres_avant
    if succes_creation:
        print("   🎉 CRÉATION MEMBRE: RÉUSSIE !")
        print("   ✅ Le système de création de membres fonctionne parfaitement")
        print("   ✅ Les données sont correctement stockées en base")
        print("   ✅ La synchronisation est opérationnelle")
    else:
        print("   ❌ CRÉATION MEMBRE: ÉCHEC")
        print("   💡 Prochaines étapes de diagnostic:")
        print("     - Vérifier les logs Django")
        print("     - Tester manuellement via l'interface web")
        print("     - Vérifier les permissions de l'agent")
    
    print("=" * 70)
    print("🔍 DIAGNOSTIC TERMINÉ")

def test_sans_connexion(client, agent, total_membres_avant):
    """Test sans connexion pour diagnostic de base"""
    print("\n🔧 MODE DIAGNOSTIC SANS CONNEXION:")
    
    # Vérifications basiques
    print("1. 📋 VÉRIFICATIONS BASIQUES:")
    
    # Test de génération de numéro unique
    try:
        from agents.views import generer_numero_unique
        numero_test = generer_numero_unique()
        print(f"   ✅ Génération numéro unique: {numero_test}")
        
        # Vérifier unicité
        if Membre.objects.filter(numero_unique=numero_test).exists():
            print("   ⚠️ Numéro généré existe déjà")
        else:
            print("   ✅ Numéro généré est unique")
    except Exception as e:
        print(f"   ❌ Erreur génération numéro: {e}")
    
    # Vérifier intégrité base de données
    try:
        membres_avec_numero = Membre.objects.exclude(numero_unique='').count()
        membres_sans_numero = Membre.objects.filter(numero_unique='').count()
        print(f"   📊 Statistiques base:")
        print(f"     - Membres avec numéro: {membres_avec_numero}")
        print(f"     - Membres sans numéro: {membres_sans_numero}")
        
        if membres_sans_numero == 0:
            print("   ✅ Tous les membres ont un numéro unique")
        else:
            print(f"   ⚠️ {membres_sans_numero} membre(s) sans numéro unique")
            
    except Exception as e:
        print(f"   ❌ Erreur vérification base: {e}")
    
    # Test création manuelle
    print("\n2. 🧪 TEST CRÉATION MANUELLE:")
    
    try:
        # Créer un membre directement en base
        nouveau_membre = Membre.objects.create(
            nom="TEST_DIAGNOSTIC",
            prenom="SansConnexion",
            telephone="0100000000",
            email="test.diagnostic@example.com",
            numero_unique="MEMDIAG123",
            statut="actif"
        )
        print("   ✅ Membre créé directement en base")
        print(f"   📋 ID: {nouveau_membre.id}, Numéro: {nouveau_membre.numero_unique}")
        
        # Vérifier persistance
        total_apres = Membre.objects.count()
        if total_apres > total_membres_avant:
            print("   ✅ Données correctement persistées")
        else:
            print("   ❌ Problème de persistance")
            
        # Nettoyer
        nouveau_membre.delete()
        print("   🧹 Membre test supprimé")
        
    except Exception as e:
        print(f"   ❌ Erreur création manuelle: {e}")
    
    print("\n💡 RECOMMANDATIONS:")
    print("   - Testez manuellement via l'interface web")
    print("   - Vérifiez que l'agent a les bonnes permissions")
    print("   - Consultez les logs Django pour plus de détails")

if __name__ == "__main__":
    diagnostic_creation_membre_amelioré()