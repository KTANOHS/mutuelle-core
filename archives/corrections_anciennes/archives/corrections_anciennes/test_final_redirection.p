# test_final_redirection.py
import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur setup Django: {e}")
    sys.exit(1)

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

def test_connexion_utilisateurs():
    """Teste la connexion de différents utilisateurs"""
    print("🧪 TEST DE CONNEXION AVEC RELATIONS")
    print("=" * 60)
    
    User = get_user_model()
    client = Client()
    
    # Utilisateurs de test avec leurs mots de passe
    test_users = [
        ('test_medecin', 'medecin'),
        ('test_membre', 'membre'), 
        ('test_agent', 'agent'),
        ('test_pharmacien', 'pharmacien'),
        ('test_assureur', 'assureur')
    ]
    
    for username, role in test_users:
        try:
            user = User.objects.get(username=username)
            print(f"\n🔍 Test {role}: {username}")
            
            # Vérifier les relations
            relation_name = role
            has_relation = hasattr(user, relation_name)
            
            if has_relation:
                obj = getattr(user, relation_name)
                print(f"   ✅ Relation {role}: {obj}")
                
                # Tenter la connexion (vous devrez ajuster le mot de passe)
                login_success = client.login(username=username, password='password')
                
                if login_success:
                    print("   ✅ Connexion réussie")
                    
                    # Tester la redirection
                    try:
                        response = client.get(reverse('redirect-after-login'))
                        print(f"   📍 Redirection: {response.url}")
                        
                        # Vérifier si c'est la bonne redirection
                        expected_urls = {
                            'medecin': '/medecin/dashboard/',
                            'membre': '/membres/dashboard/', 
                            'agent': '/agents/dashboard/',
                            'pharmacien': '/pharmacien/dashboard/',
                            'assureur': '/assureur/dashboard/'
                        }
                        
                        expected = expected_urls.get(role)
                        if expected and expected in response.url:
                            print("   🎯 SUCCÈS: Bonne redirection!")
                        else:
                            print(f"   ⚠️  Redirection inattendue: {response.url}")
                            
                    except Exception as e:
                        print(f"   ❌ Erreur redirection: {e}")
                else:
                    print("   ❌ Échec connexion - mauvais mot de passe")
            else:
                print(f"   ❌ Aucune relation {role} - problème non résolu")
                
        except User.DoesNotExist:
            print(f"❌ Utilisateur {username} non trouvé")
        except Exception as e:
            print(f"💥 Erreur test {username}: {e}")

def statut_global_relations():
    """Affiche le statut global des relations"""
    print("\n📊 STATUT GLOBAL DES RELATIONS")
    print("=" * 60)
    
    User = get_user_model()
    
    roles = [
        ('Medecin', 'medecin'),
        ('Membre', 'membre'),
        ('Agents', 'agent'),
        ('Pharmacien', 'pharmacien'),
        ('Assureur', 'assureur')
    ]
    
    for group_name, relation in roles:
        users = User.objects.filter(groups__name=group_name)
        with_relation = sum(1 for user in users if hasattr(user, relation))
        
        status = "✅" if with_relation == len(users) else "⚠️"
        print(f"{status} {group_name}: {with_relation}/{len(users)} avec relation")
        
        # Afficher les utilisateurs sans relation
        users_without = [user.username for user in users if not hasattr(user, relation)]
        if users_without:
            print(f"   ❌ Sans relation: {', '.join(users_without)}")

if __name__ == "__main__":
    statut_global_relations()
    test_connexion_utilisateurs()