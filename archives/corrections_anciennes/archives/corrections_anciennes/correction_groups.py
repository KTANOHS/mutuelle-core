# corriger_groupes.py
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votre_projet.settings')
django.setup()

from django.contrib.auth.models import Group, User

def nettoyer_et_corriger_groupes():
    print("🔧 NETTOYAGE ET CORRECTION DES GROUPES")
    print("=" * 50)
    
    # 1. Supprimer les groupes en double (majuscules)
    groupes_a_supprimer = ['Assureur', 'Medecin', 'Pharmacien', 'Membre']
    for groupe_nom in groupes_a_supprimer:
        try:
            groupe = Group.objects.get(name=groupe_nom)
            # Transférer les utilisateurs vers les groupes en minuscules
            groupe_minuscule = groupe_nom.lower()
            try:
                nouveau_groupe = Group.objects.get(name=groupe_minuscule)
                for user in groupe.user_set.all():
                    user.groups.remove(groupe)
                    user.groups.add(nouveau_groupe)
                    print(f"   ➤ Transféré {user.username} de {groupe_nom} vers {groupe_minuscule}")
            except Group.DoesNotExist:
                print(f"   ⚠️ Groupe {groupe_minuscule} n'existe pas")
            
            # Supprimer le groupe en majuscules
            groupe.delete()
            print(f"   ✅ Groupe {groupe_nom} supprimé")
        except Group.DoesNotExist:
            print(f"   ℹ️ Groupe {groupe_nom} déjà supprimé")
    
    # 2. Vérifier et corriger les assignations des utilisateurs
    print("\n👥 CORRECTION DES ASSIGNATIONS UTILISATEURS")
    print("-" * 40)
    
    mappings_utilisateurs = {
        'asia': 'assureur',
        'alia': 'medecin', 
        'gloria': 'pharmacien',
        'leti': 'membre',
        'assureur': 'assureur',
        'medecin': 'medecin',
        'pharmacien': 'pharmacien',
        'membre': 'membre'
    }
    
    for username, groupe_nom in mappings_utilisateurs.items():
        try:
            user = User.objects.get(username=username)
            groupe = Group.objects.get(name=groupe_nom)
            
            # Nettoyer tous les groupes existants
            user.groups.clear()
            # Ajouter le bon groupe
            user.groups.add(groupe)
            
            print(f"   ✅ {username} assigné à {groupe_nom}")
            
        except User.DoesNotExist:
            print(f"   ⚠️ Utilisateur {username} non trouvé")
        except Group.DoesNotExist:
            print(f"   ❌ Groupe {groupe_nom} non trouvé")
    
    # 3. Donner un groupe à ktanos
    try:
        ktanos = User.objects.get(username='ktanos')
        groupe_membre = Group.objects.get(name='membre')
        ktanos.groups.add(groupe_membre)
        print(f"   ✅ ktanos assigné au groupe membre")
    except Exception as e:
        print(f"   ⚠️ Impossible d'assigner ktanos: {e}")
    
    # 4. Afficher le résultat final
    print("\n📊 SITUATION FINALE")
    print("-" * 30)
    for groupe in Group.objects.all().order_by('name'):
        count = groupe.user_set.count()
        print(f"   • {groupe.name}: {count} utilisateur(s)")
    
    print("\n🎯 UTILISATEURS ET LEURS GROUPES")
    print("-" * 35)
    for user in User.objects.all().order_by('username'):
        groupes = list(user.groups.values_list('name', flat=True))
        print(f"   • {user.username}: {groupes}")

if __name__ == "__main__":
    nettoyer_et_corriger_groupes()