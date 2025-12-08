# setup_user_groups.py
import os
import sys
import django

sys.path.append('/Users/koffitanohsoualiho/Documents/projet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def setup_complete_groups():
    print("👥 CONFIGURATION COMPLÈTE DES GROUPES")
    print("=" * 60)
    
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group
    
    User = get_user_model()
    
    # 1. Créer tous les groupes nécessaires
    groups_to_create = ['assureur', 'medecin', 'pharmacien', 'membre', 'admin']
    
    for group_name in groups_to_create:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"✅ Groupe créé: {group_name}")
        else:
            print(f"ℹ️  Groupe existe: {group_name}")
    
    # 2. Assigner les groupes aux utilisateurs existants
    user_group_mapping = {
        'testuser': 'membre',
        'assureur_test': 'assureur',
        'ktanos': 'admin',
        'asia': 'membre',
        'alia': 'membre',
        'gloria': 'membre', 
        'leti': 'membre'
    }
    
    print("\n🔗 ASSIGNATION DES GROUPES:")
    for username, group_name in user_group_mapping.items():
        try:
            user = User.objects.get(username=username)
            group = Group.objects.get(name=group_name)
            
            # Vider les groupes existants et assigner le nouveau
            user.groups.clear()
            user.groups.add(group)
            
            print(f"✅ {username} → Groupe {group_name}")
            
        except User.DoesNotExist:
            print(f"⚠️  Utilisateur non trouvé: {username}")
        except Group.DoesNotExist:
            print(f"❌ Groupe non trouvé: {group_name}")
    
    # 3. Vérifier la configuration
    print("\n🔍 VÉRIFICATION FINALE:")
    users = User.objects.all()
    for user in users:
        groups = [g.name for g in user.groups.all()]
        print(f"   👤 {user.username}: {groups or 'AUCUN GROUPE'}")

def test_redirect_function():
    print("\n\n🧪 TEST DE LA FONCTION DE REDIRECTION")
    print("=" * 60)
    
    try:
        from mutuelle_core.utils import get_user_redirect_url
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        
        test_users = ['testuser', 'assureur_test', 'ktanos']
        
        for username in test_users:
            try:
                user = User.objects.get(username=username)
                redirect_url = get_user_redirect_url(user)
                groups = [g.name for g in user.groups.all()]
                
                print(f"🔗 {username}:")
                print(f"   Groupes: {groups}")
                print(f"   Redirection: {redirect_url}")
                
            except User.DoesNotExist:
                print(f"⚠️  Utilisateur non trouvé: {username}")
    except ImportError:
        print("❌ Impossible d'importer get_user_redirect_url - vérifiez utils.py")

if __name__ == "__main__":
    setup_complete_groups()
    test_redirect_function()