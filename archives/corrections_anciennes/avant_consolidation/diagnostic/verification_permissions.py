import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from agents.models import Agent

def verifier_permissions_utilisateur():
    """Vérifier et corriger les permissions de l'utilisateur"""
    print("🔐 VÉRIFICATION DES PERMISSIONS")
    print("==============================")
    
    username = "koffitanoh"
    
    try:
        user = User.objects.get(username=username)
        print(f"👤 Utilisateur trouvé: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Superutilisateur: {user.is_superuser}")
        print(f"   Staff: {user.is_staff}")
        print(f"   Actif: {user.is_active}")
        
        # Vérifier les groupes
        groups = user.groups.all()
        print(f"   Groupes: {[g.name for g in groups]}")
        
        # Vérifier les permissions
        permissions = user.get_all_permissions()
        print(f"   Permissions: {len(permissions)}")
        
        # Vérifier si c'est un agent
        try:
            agent = Agent.objects.get(user=user)
            print(f"✅ AGENT TROUVÉ: {agent.nom_complet}")
            print(f"   Code agent: {agent.code_agent}")
            print(f"   Poste: {agent.poste}")
        except Agent.DoesNotExist:
            print("❌ L'utilisateur n'est pas associé à un agent")
            print("🔄 Création de l'agent...")
            
            # Créer l'agent
            agent = Agent.objects.create(
                user=user,
                nom_complet=user.get_full_name() or username,
                code_agent=f"AGENT-{user.id:03d}",
                poste="Agent de saisie",
                telephone="+2250102030405",
                email=user.email or f"{username}@mutuelle.ci",
                est_actif=True
            )
            print(f"✅ Agent créé: {agent.nom_complet}")
        
    except User.DoesNotExist:
        print(f"❌ Utilisateur '{username}' non trouvé")
        print("🔄 Création de l'utilisateur...")
        
        user = User.objects.create_user(
            username=username,
            email="koffitanoh@mutuelle.ci",
            password="password123",
            is_staff=True,
            is_active=True
        )
        print(f"✅ Utilisateur créé: {user.username}")

if __name__ == "__main__":
    verifier_permissions_utilisateur()