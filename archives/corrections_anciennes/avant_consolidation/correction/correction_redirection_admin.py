import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group

def corriger_redirection_admin():
    """Corriger la redirection automatique vers l'admin pour les superusers"""
    print("🔄 CORRECTION REDIRECTION ADMIN")
    print("===============================")
    
    username = "koffitanoh"
    
    try:
        user = User.objects.get(username=username)
        print(f"👤 Utilisateur: {user.username}")
        print(f"   Superuser: {user.is_superuser}")
        print(f"   Staff: {user.is_staff}")
        
        # Option 1: Créer un utilisateur non-superuser pour les agents
        print("\n1. 🔧 CRÉATION UTILISATEUR AGENT DÉDIÉ")
        agent_username = "agent_operateur"
        
        if not User.objects.filter(username=agent_username).exists():
            agent_user = User.objects.create_user(
                username=agent_username,
                email="agent@mutuelle.ci",
                password="agent123",
                is_staff=True,
                is_superuser=False
            )
            
            # Ajouter au groupe Agent
            groupe_agent, created = Group.objects.get_or_create(name='Agent')
            agent_user.groups.add(groupe_agent)
            
            print(f"   ✅ Utilisateur agent créé: {agent_username}")
            print(f"   🔑 Mot de passe: agent123")
        else:
            print(f"   ✅ Utilisateur agent existe déjà: {agent_username}")
        
        # Option 2: Vérifier les groupes
        print(f"\n2. 📋 GROUPES DE {username}:")
        for group in user.groups.all():
            print(f"   - {group.name}")
        
        # Option 3: Solution temporaire - URLs directs
        print(f"\n3. 🌐 URLS DIRECTS POUR TEST:")
        print(f"   http://localhost:8000/agents/liste-membres/")
        print(f"   http://localhost:8000/agents/creer-bon-soin/")
        print(f"   http://localhost:8000/agents/tableau-de-bord/")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = corriger_redirection_admin()
    
    if success:
        print("\n🎉 CORRECTIONS APPLIQUÉES!")
        print("💡 Utilisez l'utilisateur 'agent_operateur' pour l'interface agent")