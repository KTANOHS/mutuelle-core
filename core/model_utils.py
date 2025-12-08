# core/model_utils.py
import logging
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

def get_nom_agent_securise(agent):
    """Retourne le nom d'un agent de manière sécurisée"""
    try:
        if not agent:
            return "Agent non spécifié"
            
        if hasattr(agent, 'user') and agent.user:
            full_name = agent.user.get_full_name()
            if full_name:
                return full_name
            return agent.user.username
        else:
            return f"Agent {agent.id}"
            
    except Exception as e:
        logger.error(f"Erreur récupération nom agent: {e}")
        return "Agent inconnu"

def get_nom_assureur_securise(assureur):
    """Retourne le nom d'un assureur de manière sécurisée"""
    try:
        if not assureur:
            return "Assureur non spécifié"
            
        if hasattr(assureur, 'user') and assureur.user:
            full_name = assureur.user.get_full_name()
            if full_name:
                return full_name
            return assureur.user.username
        elif hasattr(assureur, 'raison_sociale') and assureur.raison_sociale:
            return assureur.raison_sociale
        else:
            return f"Assureur {assureur.id}"
            
    except Exception as e:
        logger.error(f"Erreur récupération nom assureur: {e}")
        return "Assureur inconnu"

def get_assureur_membre_securise(membre):
    """Retourne l'assureur d'un membre de manière sécurisée"""
    try:
        # Méthode 1: Via agent_createur
        if hasattr(membre, 'agent_createur') and membre.agent_createur:
            agent = membre.agent_createur
            if hasattr(agent, 'assureur') and agent.assureur:
                return agent.assureur
        
        # Méthode 2: Via user (si le user est un assureur)
        if hasattr(membre, 'user') and membre.user:
            try:
                from assureur.models import Assureur
                return Assureur.objects.get(user=membre.user)
            except ObjectDoesNotExist:
                pass
                
        return None
        
    except Exception as e:
        logger.error(f"Erreur récupération assureur membre: {e}")
        return None