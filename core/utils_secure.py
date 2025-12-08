# core/utils_secure.py
import logging
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

def get_assureur_membre_securise(membre):
    """
    Récupère l'assureur d'un membre de manière sécurisée
    """
    try:
        # Méthode 1: Via agent_createur
        if hasattr(membre, 'agent_createur') and membre.agent_createur:
            if hasattr(membre.agent_createur, 'assureur') and membre.agent_createur.assureur:
                return membre.agent_createur.assureur
        
        # Méthode 2: Via user (si le user est un assureur)
        if hasattr(membre, 'user') and membre.user:
            try:
                from assureur.models import Assureur
                return Assureur.objects.get(user=membre.user)
            except ObjectDoesNotExist:
                pass
                
        return None
        
    except Exception as e:
        logger.error(f"Erreur récupération assureur membre {getattr(membre, 'id', 'N/A')}: {e}")
        return None

def get_agent_nom_securise(agent):
    """
    Récupère le nom d'un agent de manière sécurisée
    """
    try:
        if not agent:
            return "Agent non spécifié"
            
        # Essayer différents attributs
        if hasattr(agent, 'nom') and hasattr(agent, 'prenom'):
            return f"{agent.nom} {agent.prenom}"
        elif hasattr(agent, 'user') and agent.user:
            full_name = agent.user.get_full_name()
            if full_name:
                return full_name
            return agent.user.username
        elif hasattr(agent, 'nom'):
            return agent.nom
        else:
            return f"Agent {agent.id}"
            
    except Exception as e:
        logger.error(f"Erreur récupération nom agent {getattr(agent, 'id', 'N/A')}: {e}")
        return "Agent inconnu"