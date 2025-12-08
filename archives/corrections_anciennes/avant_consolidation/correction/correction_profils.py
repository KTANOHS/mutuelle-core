# correction_profils.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from agents.models import Agent

def corriger_profils_agents():
    """Crée les profils Agent manquants"""
    groupe_agents = Group.objects.get(name='Agents')
    users_agents = groupe_agents.user_set.all()
    
    for user in users_agents:
        if not hasattr(user, 'agent'):
            # Générer un numéro d'agent unique
            dernier_agent = Agent.objects.order_by('-id').first()
            nouveau_numero = f"AGT{dernier_agent.id + 1 if dernier_agent else 1:04d}"
            
            # Créer le profil Agent
            Agent.objects.create(
                user=user,
                numero_agent=nouveau_numero,
                actif=True
            )
            print(f"✅ Profil Agent créé pour {user.username}")

if __name__ == "__main__":
    corriger_profils_agents()