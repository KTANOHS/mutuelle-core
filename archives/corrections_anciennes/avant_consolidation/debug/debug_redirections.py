
#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User, Group

print("🔍 DÉBOGAGE COMPLET DES REDIRECTIONS")
print("=" * 50)

# 1. Examiner la fonction get_user_redirect_url
print("\n1. ANALYSE DE LA FONCTION get_user_redirect_url")
print("-" * 30)

# Essayer d'importer et d'examiner la fonction
try:
    import inspect
    from core.utils import get_user_redirect_url
    
    print("✅ Fonction importée depuis core/utils")
    
    # Afficher le code source
    source = inspect.getsource(get_user_redirect_url)
    print("\n📝 Code source de get_user_redirect_url:")
    print("-" * 20)
    
    # Afficher seulement les premières lignes
    lines = source.split('\n')
    for i, line in enumerate(lines[:30]):
        print(f"{i+1:3}: {line}")
    
    if len(lines) > 30:
        print("   ... (tronqué)")
    
except Exception as e:
    print(f"❌ Erreur: {e}")

# 2. Tester avec chaque utilisateur
print("\n2. TEST MANUEL DE LA DÉTECTION")
print("-" * 30)

def test_user_detection(user):
    """Test manuel de la détection du type d'utilisateur"""
    print(f"\n👤 {user.username}:")
    
    # Méthode 1: Vérifier les groupes
    groups = user.groups.all()
    group_names = [g.name for g in groups]
    print(f"   Groupes: {group_names}")
    
    # Méthode 2: Vérifier les permissions
    print(f"   is_staff: {user.is_staff}")
    print(f"   is_superuser: {user.is_superuser}")
    
    # Déterminer manuellement le type
    if user.is_superuser:
        return "ADMIN"
    elif 'Assureur' in group_names:
        return "ASSUREUR"
    elif 'Agent' in group_names:
        return "AGENT"
    elif 'Medecin' in group_names:
        return "MEDECIN"
    elif 'Pharmacien' in group_names:
        return "PHARMACIEN"
    elif 'Membre' in group_names:
        return "MEMBRE"
    else:
        return "INCONNU"

# Tester tous les utilisateurs
users_to_test = User.objects.filter(is_active=True)
for user in users_to_test:
    user_type = test_user_detection(user)
    print(f"   → Type détecté manuellement: {user_type}")
    
    # Tester la fonction réelle
    try:
        from core.utils import get_user_redirect_url, get_user_type
        actual_type = get_user_type(user)
        redirect_url = get_user_redirect_url(user)
        print(f"   → get_user_type(): {actual_type}")
        print(f"   → get_user_redirect_url(): {redirect_url}")
        
        if user_type != actual_type:
            print(f"   ⚠️  CONFLIT: Manuel={user_type} vs Fonction={actual_type}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

# 3. Vérifier spécifiquement DOUA1
print("\n3. ANALYSE SPÉCIFIQUE DE DOUA1")
print("-" * 30)

doua1 = User.objects.get(username='DOUA1')
print(f"ID: {doua1.id}")
print(f"Date joined: {doua1.date_joined}")
print(f"Last login: {doua1.last_login}")
print(f"Email: {doua1.email}")

# Vérifier tous les attributs
print("\n🔍 Attributs de DOUA1:")
for attr in dir(doua1):
    if not attr.startswith('_') and not attr.startswith('password'):
        try:
            value = getattr(doua1, attr)
            if not callable(value) and attr in ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active']:
                print(f"  {attr}: {value}")
        except:
            pass

# 4. Solution de contournement
print("\n4. SOLUTION ALTERNATIVE")
print("-" * 30)

print("""
Si DOUA1 est toujours mal détecté, créez une fonction de contournement:

Dans core/utils.py, ajoutez cette fonction:

def get_user_redirect_url_fixed(user):
    '''Version corrigée de la redirection'''
    if not user.is_authenticated:
        return '/accounts/login/'
    
    # Cas spécial pour DOUA1
    if user.username == 'DOUA1':
        return '/assureur/'
    
    # Logique normale
    user_type = get_user_type(user)
    redirect_map = {
        'ADMIN': '/admin/',
        'ASSUREUR': '/assureur/',
        'AGENT': '/agents/tableau-de-bord/',
        'MEDECIN': '/medecin/dashboard/',
        'PHARMACIEN': '/pharmacien/dashboard/',
        'MEMBRE': '/membres/dashboard/',
    }
    return redirect_map.get(user_type, '/')
""")

print("\n" + "=" * 50)
print("✅ DÉBOGAGE TERMINÉ")

