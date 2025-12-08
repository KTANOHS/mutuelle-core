import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Agent
from django.contrib.auth.models import User

def verifier_permissions_utilisateur():
    """Vérifier et corriger les permissions de l'utilisateur - VERSION CORRIGÉE"""
    print("🔐 VÉRIFICATION DES PERMISSIONS - CORRIGÉ")
    print("=========================================")
    
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
        
        # Vérifier si c'est un agent - VERSION CORRIGÉE
        try:
            agent = Agent.objects.get(user=user)
            print(f"✅ AGENT TROUVÉ: {agent}")
            print(f"   Matricule: {agent.matricule}")  # CORRIGÉ: matricule au lieu de code_agent
            print(f"   Poste: {agent.poste}")
            print(f"   Est actif: {agent.est_actif}")
            print(f"   Limite quotidienne: {agent.limite_bons_quotidienne}")
            
        except Agent.DoesNotExist:
            print("❌ L'utilisateur n'est pas associé à un agent")
            
    except User.DoesNotExist:
        print(f"❌ Utilisateur '{username}' non trouvé")

if __name__ == "__main__":
    verifier_permissions_utilisateur()