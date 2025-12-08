# verifier_base.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

from django.contrib.auth.models import User
from agents.models import Agent

def verifier_base_complete():
    print("🗃️ ÉTAT COMPLET DE LA BASE")
    print("=" * 60)
    
    # Utilisateurs
    print("\n👥 UTILISATEURS:")
    users = User.objects.all()
    for user in users:
        print(f"   {user.username:15} | Superuser: {user.is_superuser:5} | Staff: {user.is_staff:5} | Actif: {user.is_active:5}")
    
    # Agents
    print("\n👤 AGENTS:")
    agents = Agent.objects.all().select_related('user')
    for agent in agents:
        print(f"   {agent.prenom} {agent.nom:15} | User: {agent.user.username:15} | Statut: {agent.statut:10}")
    
    # Vérification des permissions
    print("\n🔐 VÉRIFICATION DES PERMISSIONS:")
    from core.utils import est_agent
    for user in users:
        peut_creer_bons = est_agent(user)
        status = "✅ PEUT créer bons" if peut_creer_bons else "❌ NE peut PAS créer bons"
        print(f"   {user.username:15} | {status}")

if __name__ == "__main__":
    verifier_base_complete()