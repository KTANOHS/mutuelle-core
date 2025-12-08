# verifier_base_corrige.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

from django.contrib.auth.models import User
from agents.models import Agent

def verifier_base_complete():
    print("🗃️ ÉTAT COMPLET DE LA BASE (CORRIGÉ)")
    print("=" * 60)
    
    # Utilisateurs
    print("\n👥 UTILISATEURS:")
    users = User.objects.all()
    for user in users:
        print(f"   {user.username:20} | Superuser: {user.is_superuser:5} | Staff: {user.is_staff:5} | Actif: {user.is_active:5}")
    
    # Agents - VERSION CORRIGÉE
    print("\n👤 AGENTS:")
    agents = Agent.objects.all().select_related('user')
    for agent in agents:
        # Afficher les champs disponibles
        available_fields = [f.name for f in Agent._meta.get_fields() if hasattr(agent, f.name)]
        print(f"   User: {agent.user.username}")
        print(f"   - Champs disponibles: {', '.join(available_fields)}")
        print(f"   - Statut: {getattr(agent, 'statut', 'N/A')}")
        print()
    
    # Vérification des permissions
    print("\n🔐 VÉRIFICATION DES PERMISSIONS:")
    from core.utils import est_agent
    for user in users:
        if user.username in ['koffitanoh', 'test_agent']:  # Seulement les utilisateurs importants
            peut_creer_bons = est_agent(user)
            status = "✅ PEUT créer bons" if peut_creer_bons else "❌ NE peut PAS créer bons"
            print(f"   {user.username:20} | {status}")

def analyser_modele_agent():
    print("\n🔍 ANALYSE DU MODÈLE AGENT")
    print("-" * 30)
    
    try:
        from agents.models import Agent
        print("Champs du modèle Agent:")
        for field in Agent._meta.get_fields():
            field_type = field.get_internal_type()
            required = "REQUIS" if not field.null and not field.blank else "OPTIONNEL"
            print(f"   - {field.name}: {field_type} ({required})")
    except Exception as e:
        print(f"Erreur analyse modèle: {e}")

if __name__ == "__main__":
    verifier_base_complete()
    analyser_modele_agent()