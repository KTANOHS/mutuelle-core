# debug_temps_reel.py
import os
import django
import sys
import time

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User
from membres.models import Membre

def creer_utilisateur_test():
    """Crée un utilisateur de test avec un mot de passe connu"""
    print("🔧 CRÉATION D'UN UTILISATEUR DE TEST")
    print("=" * 50)
    
    username = "agent_test"
    password = "test123"
    
    try:
        # Vérifier si l'utilisateur existe déjà
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': 'Agent',
                'last_name': 'Test',
                'email': 'agent.test@example.com',
                'is_staff': True,
                'is_active': True
            }
        )
        
        if created:
            user.set_password(password)
            user.save()
            print(f"✅ Utilisateur créé: {username}")
            print(f"🔑 Mot de passe: {password}")
        else:
            # Réinitialiser le mot de passe
            user.set_password(password)
            user.save()
            print(f"✅ Utilisateur existant - mot de passe réinitialisé: {username}")
            print(f"🔑 Nouveau mot de passe: {password}")
        
        # Vérifier la connexion
        from django.contrib.auth import authenticate
        user_auth = authenticate(username=username, password=password)
        if user_auth:
            print("🔐 Connexion test réussie")
        else:
            print("❌ Connexion test échouée")
            
        return username, password
        
    except Exception as e:
        print(f"❌ Erreur création utilisateur: {e}")
        return None, None

def test_creation_membre_avec_utilisateur_test():
    """Test avec un utilisateur dont on connaît le mot de passe"""
    print("\n🎯 TEST AVEC UTILISATEUR DE TEST")
    print("=" * 50)
    
    from django.test import Client
    
    # Créer l'utilisateur de test
    username, password = creer_utilisateur_test()
    
    if not username:
        return
    
    client = Client()
    
    # Connexion
    logged_in = client.login(username=username, password=password)
    if not logged_in:
        print("❌ Impossible de se connecter avec l'utilisateur de test")
        return
    
    print("✅ Connexion réussie avec l'utilisateur de test")
    
    # Test création membre
    total_avant = Membre.objects.count()
    print(f"📊 Membres avant: {total_avant}")
    
    response = client.post('/agents/creer-membre/', {
        'nom': 'TestDebug',
        'prenom': 'UtilisateurTest', 
        'telephone': '0100000003',
        'email': 'test.debug@example.com'
    })
    
    print(f"📨 Statut réponse: {response.status_code}")
    print(f"🔗 Redirection: {getattr(response, 'url', 'Aucune')}")
    
    total_apres = Membre.objects.count()
    print(f"📊 Membres après: {total_apres}")
    
    if total_apres > total_avant:
        print("🎉 SUCCÈS ! Membre créé via l'interface web")
        nouveau_membre = Membre.objects.latest('id')
        print(f"📋 Détails: {nouveau_membre.prenom} {nouveau_membre.nom}")
        print(f"🔢 Numéro: {getattr(nouveau_membre, 'numero_unique', 'N/A')}")
    else:
        print("❌ ÉCHEC - Aucun membre créé")
        
        # Essayer de comprendre pourquoi
        if response.status_code == 200:
            print("💡 Le formulaire est réaffiché (erreur de validation)")
        elif response.status_code == 403:
            print("💡 Erreur de permission (403)")
        elif response.status_code == 302:
            print("💡 Redirection mais pas de création")
        else:
            print(f"💡 Statut inhabituel: {response.status_code}")

if __name__ == "__main__":
    test_creation_membre_avec_utilisateur_test()