# diagnostic_formulaire_creation.py
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client, RequestFactory
from django.contrib.auth.models import User
from membres.models import Membre
from agents.views import creer_membre
from agents.models import Agent
import logging

# Configuration logging pour voir les erreurs
logging.basicConfig(level=logging.DEBUG)

def diagnostic_formulaire_creation():
    print("🔍 DIAGNOSTIC SPÉCIFIQUE - FORMULAIRE CRÉATION MEMBRE")
    print("=" * 70)
    
    # 1. TEST DIRECT DE LA VUE
    print("1. 🧪 TEST DIRECT DE LA VUE creer_membre:")
    
    factory = RequestFactory()
    
    # Créer une requête POST simulée
    request = factory.post('/agents/creer-membre/', {
        'nom': 'TestDirect',
        'prenom': 'VueDiagnostic', 
        'telephone': '0100000001',
        'email': 'test.direct@example.com'
    })
    
    # Simuler un utilisateur connecté
    try:
        agent_user = User.objects.get(username='koffitanoh')
        request.user = agent_user
        
        # Appeler directement la vue
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        print("   ✅ Configuration requête simulée")
        
    except User.DoesNotExist:
        print("   ❌ Utilisateur koffitanoh non trouvé")
        return
    
    # 2. ANALYSE DU CODE DE LA VUE
    print("\n2. 📝 ANALYSE DU CODE VUE creer_membre:")
    
    # Lire et analyser le code source de la vue
    try:
        import inspect
        source_code = inspect.getsource(creer_membre)
        
        print("   🔍 Points de contrôle dans le code:")
        
        checks = [
            ('request.method == POST', 'POST' in source_code and 'method' in source_code),
            ('Membre.objects.create', 'Membre.objects.create' in source_code),
            ('generer_numero_unique', 'generer_numero_unique' in source_code),
            ('redirect liste_membres', 'redirect' in source_code and 'liste_membres' in source_code),
            ('messages.success', 'messages.success' in source_code),
        ]
        
        for check_name, check_result in checks:
            status = "✅" if check_result else "❌"
            print(f"     {status} {check_name}")
            
    except Exception as e:
        print(f"   ❌ Erreur analyse code: {e}")
    
    # 3. TEST AVEC CLIENT DE TEST DJANGO
    print("\n3. 🌐 TEST AVEC CLIENT DE TEST:")
    
    client = Client()
    
    # Essayer de se connecter avec différents scénarios
    print("   🔐 Test de connexion avec différents scénarios:")
    
    scenarios = [
        {'username': 'koffitanoh', 'password': 'password'},
        {'username': 'koffitanoh', 'password': '123456'},
        {'username': 'koffitanoh', 'password': 'admin'},
    ]
    
    logged_in = False
    for scenario in scenarios:
        logged_in = client.login(**scenario)
        if logged_in:
            print(f"   ✅ Connexion réussie avec: {scenario['password']}")
            break
        else:
            print(f"   ❌ Échec avec: {scenario['password']}")
    
    if not logged_in:
        print("   💡 Aucune connexion réussie - test sans authentification")
    
    # 4. TEST DE CRÉATION AVEC CLIENT
    print("\n4. 📤 TEST ENVOI FORMULAIRE:")
    
    if logged_in:
        # Compter les membres avant
        total_avant = Membre.objects.count()
        print(f"   📊 Membres avant: {total_avant}")
        
        # Envoyer le formulaire
        response = client.post('/agents/creer-membre/', {
            'nom': 'TestClient',
            'prenom': 'FormulaireTest',
            'telephone': '0100000002',
            'email': 'test.client@example.com'
        })
        
        print(f"   📨 Réponse: {response.status_code}")
        print(f"   🔗 Redirection: {getattr(response, 'url', 'Aucune')}")
        
        # Vérifier le résultat
        total_apres = Membre.objects.count()
        print(f"   📊 Membres après: {total_apres}")
        
        if total_apres > total_avant:
            print("   ✅ Membre créé avec succès via client de test!")
        else:
            print("   ❌ Aucun membre créé via client de test")
            
            # Essayer de récupérer les messages d'erreur
            try:
                from django.contrib.messages import get_messages
                messages = list(get_messages(response.wsgi_request))
                if messages:
                    print("   💬 Messages:")
                    for message in messages:
                        print(f"     - {message}")
                else:
                    print("   💬 Aucun message d'erreur")
            except:
                print("   💬 Impossible de récupérer les messages")
    
    # 5. VÉRIFICATION DES PERMISSIONS
    print("\n5. 🔐 VÉRIFICATION DES PERMISSIONS:")
    
    try:
        agent_user = User.objects.get(username='koffitanoh')
        
        # Vérifier les groupes
        groups = agent_user.groups.all()
        if groups.exists():
            print("   👥 Groupes de l'utilisateur:")
            for group in groups:
                print(f"     - {group.name}")
        else:
            print("   ⚠️ Utilisateur n'appartient à aucun groupe")
        
        # Vérifier les permissions
        permissions = agent_user.get_all_permissions()
        if permissions:
            print("   🔑 Permissions de l'utilisateur:")
            for perm in list(permissions)[:5]:  # Afficher les 5 premières
                print(f"     - {perm}")
        else:
            print("   ⚠️ Aucune permission spécifique")
            
    except User.DoesNotExist:
        print("   ❌ Utilisateur koffitanoh non trouvé")
    
    # 6. VÉRIFICATION DES LOGS
    print("\n6. 📋 VÉRIFICATION DES LOGS:")
    
    print("   💡 Vérifiez les logs Django pour voir:")
    print("     - Les tentatives de connexion")
    print("     - Les erreurs de validation du formulaire")
    print("     - Les erreurs de permission")
    print("     - Les messages de debug")
    
    # 7. RECOMMANDATIONS
    print("\n7. 🎯 RECOMMANDATIONS:")
    
    print("   🔧 Solutions possibles:")
    print("     1. Vérifiez le mot de passe exact de l'agent")
    print("     2. Testez avec un superutilisateur")
    print("     3. Vérifiez les logs Django en temps réel")
    print("     4. Testez avec un utilisateur simple")
    print("     5. Vérifiez la configuration des permissions")
    
    print("=" * 70)
    print("🔍 DIAGNOSTIC TERMINÉ")

if __name__ == "__main__":
    diagnostic_formulaire_creation()