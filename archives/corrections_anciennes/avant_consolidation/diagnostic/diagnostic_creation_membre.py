# diagnostic_creation_membre.py
import os
import django
import sys
from datetime import datetime

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

def generer_donnees_test():
    """Génère des données de test uniques"""
    timestamp = str(random.randint(1000, 9999))
    return {
        'nom': f"Test{timestamp}",
        'prenom': f"Diagnostic{timestamp}",
        'telephone': f"01{random.randint(10000000, 99999999)}",
        'email': f"test.diagnostic{timestamp}@example.com",
        'numero_unique_attendu': f"MEM{''.join(random.choices(string.ascii_uppercase, k=3))}{timestamp[-4:]}"
    }

def diagnostic_creation_membre():
    print("🔍 DIAGNOSTIC CRÉATION MEMBRE PAR AGENT")
    print("=" * 60)
    
    client = Client()
    
    # 1. VÉRIFICATION PRÉLIMINAIRE
    print("1. 📋 VÉRIFICATION PRÉLIMINAIRE:")
    
    # Vérifier que le modèle Membre est disponible
    try:
        from membres.models import Membre
        total_membres_avant = Membre.objects.count()
        print(f"   ✅ Modèle Membre disponible - {total_membres_avant} membre(s) en base")
    except Exception as e:
        print(f"   ❌ Modèle Membre non disponible: {e}")
        return
    
    # Vérifier qu'il y a des agents
    agents = User.objects.filter(groups__name='Agents') | User.objects.filter(agent__isnull=False)
    if not agents.exists():
        print("   ❌ Aucun agent trouvé pour le test")
        return
    
    agent = agents.first()
    print(f"   ✅ Agent trouvé: {agent.username} ({agent.get_full_name()})")
    
    # 2. TEST DE CONNEXION
    print("\n2. 🔐 TEST DE CONNEXION:")
    
    # Essayer différents mots de passe courants
    mots_de_passe = ['password123', '123456', 'password', 'admin123', 'test123']
    login_success = False
    
    for mdp in mots_de_passe:
        login_success = client.login(username=agent.username, password=mdp)
        if login_success:
            print(f"   ✅ Connexion réussie avec le mot de passe: {mdp}")
            break
    
    if not login_success:
        print("   ❌ Connexion échouée avec tous les mots de passe testés")
        print("   💡 Essayez manuellement avec le bon mot de passe")
        return
    
    # 3. TEST DE LA PAGE DE CRÉATION
    print("\n3. 📄 TEST PAGE CRÉATION MEMBRE:")
    
    response = client.get('/agents/creer-membre/')
    if response.status_code == 200:
        print("   ✅ Page création membre accessible")
        
        # Vérifier que le formulaire est présent
        content = response.content.decode()
        if 'creer-membre' in content or 'Créer un Nouveau Membre' in content:
            print("   ✅ Formulaire de création détecté")
        else:
            print("   ⚠️ Formulaire non détecté dans la page")
    else:
        print(f"   ❌ Page création membre inaccessible: {response.status_code}")
        return
    
    # 4. TEST DE CRÉATION RÉELLE D'UN MEMBRE
    print("\n4. 🎯 TEST CRÉATION RÉELLE DE MEMBRE:")
    
    donnees_test = generer_donnees_test()
    print(f"   Données de test générées:")
    print(f"     - Nom: {donnees_test['nom']}")
    print(f"     - Prénom: {donnees_test['prenom']}")
    print(f"     - Téléphone: {donnees_test['telephone']}")
    print(f"     - Email: {donnees_test['email']}")
    
    # Compter les membres avant création
    total_membres_avant = Membre.objects.count()
    print(f"   Membres avant création: {total_membres_avant}")
    
    # Envoyer la requête POST
    response = client.post('/agents/creer-membre/', {
        'nom': donnees_test['nom'],
        'prenom': donnees_test['prenom'],
        'telephone': donnees_test['telephone'],
        'email': donnees_test['email']
    })
    
    # Vérifier la réponse
    if response.status_code == 302:  # Redirection après succès
        print("   ✅ Redirection après création (statut 302)")
        
        # Vérifier si la redirection va vers la liste des membres
        if response.url == '/agents/liste-membres/':
            print("   ✅ Redirection vers liste des membres")
        else:
            print(f"   ⚠️ Redirection vers: {response.url}")
    else:
        print(f"   ❌ Pas de redirection - Statut: {response.status_code}")
    
    # 5. VÉRIFICATION EN BASE DE DONNÉES
    print("\n5. 🗄️ VÉRIFICATION EN BASE DE DONNÉES:")
    
    # Compter les membres après création
    total_membres_apres = Membre.objects.count()
    print(f"   Membres après création: {total_membres_apres}")
    
    if total_membres_apres > total_membres_avant:
        print("   ✅ Nouveau membre créé en base de données")
        
        # Récupérer le dernier membre créé
        try:
            dernier_membre = Membre.objects.latest('id')
            print(f"   📋 Dernier membre créé:")
            print(f"     - ID: {dernier_membre.id}")
            print(f"     - Nom complet: {dernier_membre.prenom} {dernier_membre.nom}")
            print(f"     - Numéro unique: {getattr(dernier_membre, 'numero_unique', 'N/A')}")
            print(f"     - Téléphone: {dernier_membre.telephone}")
            print(f"     - Email: {dernier_membre.email}")
            print(f"     - Statut: {getattr(dernier_membre, 'statut', 'N/A')}")
            print(f"     - Date inscription: {getattr(dernier_membre, 'date_inscription', 'N/A')}")
            
            # Vérifier si c'est notre membre de test
            if (dernier_membre.nom == donnees_test['nom'] and 
                dernier_membre.prenom == donnees_test['prenom']):
                print("   ✅ Membre de test correctement identifié")
            else:
                print("   ⚠️ Le dernier membre ne correspond pas aux données de test")
                
        except Exception as e:
            print(f"   ❌ Erreur récupération dernier membre: {e}")
    else:
        print("   ❌ Aucun nouveau membre créé en base de données")
    
    # 6. VÉRIFICATION ACTIVITÉ AGENT
    print("\n6. 📊 VÉRIFICATION ACTIVITÉ AGENT:")
    
    try:
        activites = ActiviteAgent.objects.filter(agent__user=agent).order_by('-date_activite')[:5]
        if activites.exists():
            print(f"   ✅ Activités enregistrées: {activites.count()} activité(s) récente(s)")
            derniere_activite = activites.first()
            print(f"   📝 Dernière activité: {derniere_activite.description}")
            print(f"   🕒 Date: {derniere_activite.date_activite}")
        else:
            print("   ⚠️ Aucune activité enregistrée pour l'agent")
    except Exception as e:
        print(f"   ❌ Erreur vérification activités: {e}")
    
    # 7. VÉRIFICATION LISTE DES MEMBRES
    print("\n7. 📋 VÉRIFICATION LISTE DES MEMBRES:")
    
    response = client.get('/agents/liste-membres/')
    if response.status_code == 200:
        content = response.content.decode()
        
        # Vérifier si le nouveau membre apparaît dans la liste
        if donnees_test['nom'] in content and donnees_test['prenom'] in content:
            print("   ✅ Nouveau membre visible dans la liste")
        else:
            print("   ⚠️ Nouveau membre non visible dans la liste")
            
        # Vérifier la pagination
        if 'page=' in content or 'pagination' in content.lower():
            print("   ✅ Pagination détectée")
        else:
            print("   ⚠️ Pagination non détectée")
    else:
        print(f"   ❌ Liste des membres inaccessible: {response.status_code}")
    
    # 8. TEST DE FONCTION GÉNÉRATION NUMÉRO UNIQUE
    print("\n8. 🔧 TEST GÉNÉRATION NUMÉRO UNIQUE:")
    
    try:
        from agents.views import generer_numero_unique
        numero_test = generer_numero_unique()
        print(f"   ✅ Fonction génération numéro: {numero_test}")
        
        # Vérifier que le numéro n'existe pas déjà
        if Membre.objects.filter(numero_unique=numero_test).exists():
            print("   ⚠️ Numéro généré existe déjà (collision)")
        else:
            print("   ✅ Numéro généré est unique")
    except Exception as e:
        print(f"   ❌ Erreur génération numéro: {e}")
    
    # 9. VÉRIFICATION SYNCHRONISATION
    print("\n9. 🔄 VÉRIFICATION SYNCHRONISATION:")
    
    # Vérifier la cohérence des données
    try:
        membres_avec_numero = Membre.objects.exclude(numero_unique='').count()
        membres_sans_numero = Membre.objects.filter(numero_unique='').count()
        print(f"   Membres avec numéro unique: {membres_avec_numero}")
        print(f"   Membres sans numéro unique: {membres_sans_numero}")
        
        if membres_sans_numero == 0:
            print("   ✅ Tous les membres ont un numéro unique")
        else:
            print(f"   ⚠️ {membres_sans_numero} membre(s) sans numéro unique")
            
        # Vérifier les doublons de numéro unique
        from django.db.models import Count
        doublons = Membre.objects.values('numero_unique').annotate(
            count=Count('id')
        ).filter(count__gt=1, numero_unique__isnull=False)
        
        if doublons.exists():
            print(f"   ❌ {doublons.count()} doublon(s) de numéro unique détecté(s)")
        else:
            print("   ✅ Aucun doublon de numéro unique")
            
    except Exception as e:
        print(f"   ❌ Erreur vérification synchronisation: {e}")
    
    # 10. RAPPORT FINAL
    print("\n10. 📊 RAPPORT FINAL:")
    
    succes = total_membres_apres > total_membres_avant
    if succes:
        print("   🎉 CRÉATION MEMBRE: RÉUSSIE")
        print("   ✅ Le membre a été créé et stocké en base de données")
        print("   ✅ La synchronisation semble fonctionner correctement")
    else:
        print("   ❌ CRÉATION MEMBRE: ÉCHEC")
        print("   💡 Vérifiez:")
        print("     - Les logs Django pour les erreurs")
        print("     - La configuration de la base de données")
        print("     - Les permissions de l'agent")
        print("     - Le formulaire de création")
    
    print("=" * 60)
    print("🔍 DIAGNOSTIC TERMINÉ")

if __name__ == "__main__":
    diagnostic_creation_membre()